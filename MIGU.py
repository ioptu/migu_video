import requests
import json
import time
import random
import hashlib
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor

thread_mum = 10  # 线程
headers = {
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
    "Cache-Control": "no-cache",
    "Connection": "keep-alive",
    "Origin": "https://m.miguvideo.com",
    "Pragma": "no-cache",
    "Referer": "https://m.miguvideo.com/",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-site",
    "Support-Pendant": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36 Edg/136.0.0.0",
    "appCode": "miguvideo_default_h5",
    "appId": "miguvideo",
    "channel": "H5",
    "sec-ch-ua": "\"Chromium\";v=\"136\", \"Microsoft Edge\";v=\"136\", \"Not.A/Brand\";v=\"99\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "terminalId": "h5"
}
lives = ['热门', '央视', '卫视', '地方', '体育', '影视', '综艺', '少儿', '新闻', '教育', '熊猫', '纪实']
LIVE = {'热门': 'e7716fea6aa1483c80cfc10b7795fcb8', '体育': '7538163cdac044398cb292ecf75db4e0',
        '央视': '1ff892f2b5ab4a79be6e25b69d2f5d05', '卫视': '0847b3f6c08a4ca28f85ba5701268424',
        '地方': '855e9adc91b04ea18ef3f2dbd43f495b', '影视': '10b0d04cb23d4ac5945c4bc77c7ac44e',
        '新闻': 'c584f67ad63f4bc983c31de3a9be977c', '教育': 'af72267483d94275995a4498b2799ecd',
        '熊猫': 'e76e56e88fff4c11b0168f55e826445d', '综艺': '192a12edfef04b5eb616b878f031f32f',
        '少儿': 'fc2f5b8fd7db43ff88c4243e731ecede', '纪实': 'e1165138bdaa44b9a3138d74af6c6673'}
path = 'migu.txt'
appVersion = "2600034600"
appVersionID = appVersion + "-99000-201600010010028"
All_Live = []
FLAG = 0


def format_date_ymd():
    """
    格式化日期为「年+补0月+补0日」字符串（对应JS逻辑）
    :return: 如"20251216"
    """
    current_date = datetime.now()
    return f"{current_date.year}{current_date.month:02d}{current_date.day:02d}"


def writefile(path, content):
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)


def appendfile(path, content):
    with open(path, 'a+', encoding='utf-8') as f:
        f.write(content)


def md5(text):
    """MD5加密：返回32位小写结果"""
    # 创建MD5对象
    md5_obj = hashlib.md5()
    # 更新加密内容（需转字节流）
    md5_obj.update(text.encode('utf-8'))
    # 获取16进制加密结果
    return md5_obj.hexdigest()


def getSaltAndSign(pid):
    timestamp = str(int(time.time() * 1000))
    random_num = random.randint(0, 999999)
    salt = f"{random_num:06d}25"
    suffix = "2cac4f2c6c3346a5b34e085725ef7e33migu" + salt[:4]
    app_t = timestamp + pid + appVersion[:8]
    sign = md5(md5(app_t) + suffix)
    return {
        "salt": salt,
        "sign": sign,
        "timestamp": timestamp
    }


def get_content(pid):
    _headers = {
        "AppVersion": appVersion,
        "TerminalId": "android",
        "X-UP-CLIENT-CHANNEL-ID": appVersionID
    }
    result = getSaltAndSign(pid)
    rateType = "2" if pid == "608831231" else "3"  # 广东卫视有些特殊
    URL = f"https://play.miguvideo.com/playurl/v1/play/playurl?sign={result['sign']}&rateType={rateType}&contId={pid}&timestamp={result['timestamp']}&salt={result['salt']}"
    respData = requests.get(URL, headers=_headers).json()
    return respData


def getddCalcu720p(url, pID):
    puData = url.split("&puData=")[1]
    keys = "cdabyzwxkl"
    ddCalcu = []
    for i in range(0, int(len(puData) / 2)):
        ddCalcu.append(puData[int(len(puData)) - i - 1])
        ddCalcu.append(puData[i])
        if i == 1:
            ddCalcu.append("v")
        if i == 2:
            ddCalcu.append(keys[int(format_date_ymd()[2])])
        if i == 3:
            ddCalcu.append(keys[int(pID[6])])
        if i == 4:
            ddCalcu.append("a")
    return f'{url}&ddCalcu={"".join(ddCalcu)}&sv=10004&ct=android'


def append_All_Live(live, flag, data):
    try:
        respData = get_content(data["pID"])
        playurl = getddCalcu720p(respData["body"]["urlInfo"]["url"], data["pID"])
        print(playurl)

        if playurl != "":
            z = 1
            while z <= 1:
                obj = requests.get(playurl, allow_redirects=False)
                location = obj.headers["Location"]
                if location == "" or location is None:
                    continue
                if location.startswith("http://hlsz"):
                    playurl = location
                    break
                if z <= 6:
                    time.sleep(0.15)
                z += 1
        content = f'#EXTINF:-1 tvg-id="{data["name"]}" tvg-name="{data["name"]}" tvg-logo="{data["pics"]["highResolutionH"]}" group-title="{live}",{data["name"]}\n{playurl}\n'
        All_Live[flag] = content
        print(f'频道 [{data["name"]}] 更新成功！')
    except Exception as e:
        print(f'频道 [{data["name"]}] 更新失败！')
        print(f"ERROR:{e}")

def update(live, url):
    global FLAG
    global All_Live
    global headers
    pool = ThreadPoolExecutor(thread_mum)  # 多线程申请
    response = requests.get(url, headers=headers).json()
    dataList = response["body"]["dataList"]
    for flag, data in enumerate(dataList):
        All_Live.append("")
        pool.submit(append_All_Live, live, FLAG + flag, data)
        break
    pool.shutdown()  # 结束线程
    FLAG += len(dataList)



def main():
    writefile(path,
              '#EXTM3U x-tvg-url="https://cdn.jsdelivr.net/gh/develop202/migu_video/playback.xml,https://ghfast.top/raw.githubusercontent.com/develop202/migu_video/refs/heads/main/playback.xml,https://hk.gh-proxy.org/raw.githubusercontent.com/develop202/migu_video/refs/heads/main/playback.xml,https://develop202.github.io/migu_video/playback.xml,https://raw.githubusercontents.com/develop202/migu_video/refs/heads/main/playback.xml" catchup="append" catchup-source="&playbackbegin=\${(b)yyyyMMddHHmmss}&playbackend=\${(e)yyyyMMddHHmmss}"\n')

    for live in lives:
        print(f"分类 ----- [{live}] ----- 开始更新. . .")
        url = f'https://program-sc.miguvideo.com/live/v2/tv-data/{LIVE[live]}'
        update(live, url)
        break
    for content in All_Live:
        appendfile(path, content)


if __name__ == "__main__":
    main()
