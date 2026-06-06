import requests
import json
import time
import random
import hashlib
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor

thread_mum = 10  # 线程数

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
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36 Edg/145.0.0.0",
    "appCode": "miguvideo_default_h5",
    "appId": "miguvideo",
    "channel": "H5",
    "sec-ch-ua": "\"Chromium\";v=\"145\", \"Microsoft Edge\";v=\"145\", \"Not.A/Brand\";v=\"99\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "terminalId": "h5"
}

lives = ['央视', '卫视', '地方', '体育', '影视', '少儿', '新闻', '教育', '纪实']

LIVE = {
    '热门': 'e7716fea6aa1483c80cfc10b7795fcb8',
    '体育': '7538163cdac044398cb292ecf75db4e0',
    '央视': '1ff892f2b5ab4a79be6e25b69d2f5d05',
    '卫视': '0847b3f6c08a4ca28f85ba5701268424',
    '地方': '855e9adc91b04ea18ef3f2dbd43f495b',
    '影视': '10b0d04cb23d4ac5945c4bc77c7ac44e',
    '新闻': 'c584f67ad63f4bc983c31de3a9be977c',
    '教育': 'af72267483d94275995a4498b2799ecd',
    '熊猫': 'e76e56e88fff4c11b0168f55e826445d',
    '综艺': '192a12edfef04b5eb616b878f031f32f',
    '少儿': 'fc2f5b8fd7db43ff88c4243e731ecede',
    '纪实': 'e1165138bdaa44b9a3138d74af6c6673'
}

path = 'mig.m3u'
appVersion = "2600034600"
All_Live = []
FLAG = 0


def format_date_ymd():
    current_date = datetime.now()
    return f"{current_date.year}{current_date.month:02d}{current_date.day:02d}"


def writefile(path, content):
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)


def appendfile(path, content):
    with open(path, 'a+', encoding='utf-8') as f:
        f.write(content)


def md5(text):
    md5_obj = hashlib.md5()
    md5_obj.update(text.encode('utf-8'))
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
        "accept": "application/json, text/plain, */*",
        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
        "apipost-client-id": "81960567-1977-492a-8828-7cc9a5848b60",
        "apipost-language": "zh-cn",
        "apipost-machine": "13d46013f5c002",
        "apipost-platform": "Win",
        "apipost-terminal": "web",
        "apipost-token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJwYXlsb2FkIjp7InVzZXJfaWQiOjQwMjE2NjM4Mzk1NTcwNTg1NiwidGltZSI6MTc3OTM2MDU3NiwidXVpZCI6ImMyNWM5ZDM5LTU1MDItMTFmMS1hNWFlLWY2NjY5MWQxOGFiYSJ9fQ.I1SxTAW6A_Tdfk2OjnTv4qqZF3mTreFh8nAqhKExvNo",
        "apipost-version": "8.2.7",
        "cache-control": "no-cache",
        "content-type": "application/json",
        "pragma": "no-cache",
        "priority": "u=1, i",
        "sec-ch-ua": '"Google Chrome";v="149", "Chromium";v="149", "Not A(Brand";v="24"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "cookie": "apipost-token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJwYXlsb2FkIjp7InVzZXJfaWQiOjQwMjE2NjM4Mzk1NTcwNTg1NiwidGltZSI6MTc3OTM2MDU3NiwidXVpZCI6ImMyNWM5ZDM5LTU1MDItMTFmMS1hNWFlLWY2NjY5MWQxOGFiYSJ9fQ.I1SxTAW6A_Tdfk2OjnTv4qqZF3mTreFh8nAqhKExvNo; SERVERID=8c24774bebe341378d5513f514bfb8dc|1780710973|1780710973; SERVERCORSID=8c24774bebe341378d5513f514bfb8dc|1780710973|1780710973",
        "Referer": "https://workspace.apipost.net/594c83209c88000/apis",
        "Referrer-Policy": "strict-origin-when-cross-origin"
    }

    # ==================== 广东卫视特殊处理 ====================
    if pid == "608831231":
        rateType = "2"   # 广东卫视使用 rateType=2 更稳定
        print(f"[特殊处理] 广东卫视 使用 rateType=2")
    else:
        rateType = "3"   # 其他频道强制 720P（非会员最高清晰度）
    # =========================================================

    client_id = md5(str(int(time.time() * 1000)))

    result = getSaltAndSign(pid)

    # 额外参数
    extra_params_str = "&flvEnable=true&super4k=true"

    URL = (f"https://play.miguvideo.com/playurl/v1/play/playurl?"
           f"sign={result['sign']}&rateType={rateType}&contId={pid}&"
           f"timestamp={result['timestamp']}&salt={result['salt']}{extra_params_str}")

    params_list = URL.split("?")[1].split("&")

    # 构建 Apipost Header
    header_parameter = [
        {"description": "", "field_type": "string", "is_checked": 1, "key": "AppVersion",
         "value": "2600034600", "not_None": 1, "schema": {"type": "string"}, "param_id": "3c60653273e0b3"},
        {"description": "", "field_type": "string", "is_checked": 1, "key": "TerminalId",
         "value": "android", "not_None": 1, "schema": {"type": "string"}, "param_id": "3c6075c1f3e0e1"},
        {"description": "", "field_type": "string", "is_checked": 1, "key": "X-UP-CLIENT-CHANNEL-ID",
         "value": "2600034600-99000-201600010010028", "not_None": 1, "schema": {"type": "string"}, "param_id": "3c60858bb3e10c"},
        {"description": "", "field_type": "string", "is_checked": 1, "key": "ClientId",
         "value": client_id, "not_None": 1, "schema": {"type": "string"}, "param_id": "clientid_new"}
    ]

    # CCTV5 / CCTV5+ 不加 appCode
    if pid not in ["641886683", "641886773"]:
        header_parameter.append({
            "description": "", "field_type": "string", "is_checked": 1, "key": "appCode",
            "value": "miguvideo_default_android", "not_None": 1, "schema": {"type": "string"}, "param_id": "appcode_new"
        })

    # 动态生成 query parameter
    query_parameter = []
    for idx, p in enumerate(params_list):
        if '=' in p:
            k, v = p.split('=', 1)
            query_parameter.append({
                "param_id": f"qp_{idx}",
                "field_type": "string",
                "is_checked": 1,
                "key": k,
                "not_None": 1,
                "value": v,
                "description": ""
            })

    body = {
        "option": {
            "scene": "http_request",
            "lang": "zh-cn",
            "globals": {},
            "project": {
                "request": {
                    "header": {"parameter": header_parameter},
                    "query": {"parameter": query_parameter},
                    "body": {"parameter": []},
                    "cookie": {"parameter": []},
                    "auth": {"type": "noauth"},
                    "pre_tasks": [],
                    "post_tasks": []
                }
            },
            "env": {
                "env_id": "1",
                "env_name": "默认环境",
                "env_pre_url": "",
                "env_pre_urls": {
                    "1": {"server_id": "1", "name": "默认服务", "sort": 1000, "uri": ""},
                    "default": {"server_id": "1", "name": "默认服务", "sort": 1000, "uri": ""}
                },
                "environment": {}
            },
            "cookies": {"switch": 1, "data": []},
            "system_configs": {
                "send_timeout": 0,
                "auto_redirect": -1,
                "max_redirect_time": 5,
                "auto_gen_mock_url": -1,
                "request_param_auto_json": -1,
                "proxy": {
                    "type": 2,
                    "envfirst": 1,
                    "bypass": [],
                    "protocols": ["http"],
                    "auth": {"authenticate": -1, "host": "", "username": "", "password": ""}
                },
                "ca_cert": {"open": -1, "path": "", "base64": ""},
                "client_cert": {}
            },
            "custom_functions": {},
            "collection": [
                {
                    "target_id": "3c5fd6a9786002",
                    "target_type": "api",
                    "parent_id": "0",
                    "name": "MIGU",
                    "request": {
                        "auth": {"type": "inherit"},
                        "body": {
                            "mode": "None",
                            "parameter": [],
                            "raw": "",
                            "raw_parameter": [],
                            "raw_schema": {"type": "object"},
                            "binary": None
                        },
                        "pre_tasks": [],
                        "post_tasks": [],
                        "header": {"parameter": header_parameter},
                        "query": {"parameter": query_parameter, "query_add_equal": 1},
                        "cookie": {"parameter": [], "cookie_encode": 1},
                        "restful": {"parameter": []},
                        "tabs_default_active_key": "query"
                    },
                    "parents": [],
                    "method": "GET",
                    "protocol": "http/1.1",
                    "url": URL,
                    "pre_url": ""
                }
            ],
            "database_configs": {}
        },
        "test_events": [
            {
                "type": "api",
                "data": {
                    "target_id": "3c5fd6a9786002",
                    "project_id": "57a21612a051000",
                    "parent_id": "0",
                    "target_type": "api"
                }
            }
        ]
    }

    body_str = json.dumps(body, separators=(",", ":"))
    proxy_url = "https://workspace.apipost.net/proxy/v2/http"

    resp = requests.post(proxy_url, headers=_headers, data=body_str, timeout=15)
    
    try:
        result = resp.json()
        response_body = result["data"]["data"]["response"]["body"]
        return json.loads(response_body)
    except Exception as e:
        print(f"Apipost 返回解析失败: {e}")
        print("原始响应:", resp.text[:500])
        raise


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
        raw_url = respData["body"]["urlInfo"]["url"]
        real_pid = respData.get("body", {}).get("content", {}).get("contId", data["pID"])
        
        playurl = getddCalcu720p(raw_url, real_pid)
        rate = respData["body"]["urlInfo"].get("rateType", "未知")

        content = f'#EXTINF:-1 tvg-id="{data["name"]}" tvg-name="{data["name"]}" tvg-logo="{data["pics"]["highResolutionH"]}" group-title="{live}",{data["name"]}\n{playurl}\n'
        All_Live[flag] = content
        print(f'频道 [{data["name"]}] rateType={rate} → 更新成功')
    except Exception as e:
        print(f'频道 [{data["name"]}] 更新失败！ ERROR: {e}')


def update(live, url):
    global FLAG, All_Live
    pool = ThreadPoolExecutor(thread_mum)
    response = requests.get(url, headers=headers).json()
    dataList = response["body"]["dataList"]
    for flag, data in enumerate(dataList):
        All_Live.append("")
        pool.submit(append_All_Live, live, FLAG + flag, data)
    pool.shutdown()
    FLAG += len(dataList)


def main():
    writefile(path,
              '#EXTM3U x-tvg-url="https://cdn.jsdelivr.net/gh/develop202/migu_video/playback.xml,https://ghfast.top/raw.githubusercontent.com/develop202/migu_video/refs/heads/main/playback.xml,https://hk.gh-proxy.org/raw.githubusercontent.com/develop202/migu_video/refs/heads/main/playback.xml,https://develop202.github.io/migu_video/playback.xml,https://raw.githubusercontents.com/develop202/migu_video/refs/heads/main/playback.xml" catchup="append" catchup-source="&playbackbegin=\${(b)yyyyMMddHHmmss}&playbackend=\${(e)yyyyMMddHHmmss}"\n')
    
    for live in lives:
        print(f"\n分类 ----- [{live}] ----- 开始更新...")
        url = f'https://program-sc.miguvideo.com/live/v2/tv-data/{LIVE[live]}'
        update(live, url)
    
    for content in All_Live:
        if content:
            appendfile(path, content)
    
    print("\n全部更新完成！m3u 文件已生成：", path)


if __name__ == "__main__":
    main()
