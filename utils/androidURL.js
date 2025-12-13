import { getStringMD5 } from "./EncryUtils.js";
import { getddCalcuURL, getddCalcuURL720p } from "./ddCalcuURL.js";
import { printYellow } from "./colorOut.js";

/**
 * @typedef {object} SaltSign
 * @property {string} salt 盐值
 * @property {string} sign 签名
 */

/**
 * @param {string} md5 - md5字符串
 * @returns {SaltSign} - 
 */
function getSaltAndSign(md5) {

  const salt = 1230024
  const suffix = "3ce941cc3cbc40528bfd1c64f9fdf6c0migu0123"
  const sign = getStringMD5(md5 + suffix)
  return {
    salt: salt,
    sign: sign
  }
}

/**
 * @param {string} userId - 用户ID
 * @param {string} token - 用户token
 * @param {string} pid - 节目ID
 * @param {number} rateType - 清晰度
 * @returns {object} - 
 */
async function getAndroidURL(userId, token, pid, rateType) {

  if (rateType <= 1) {
    return {
      url: "",
      rateType: 0,
      content: null
    }
  }
  // 获取url
  const timestramp = Date.now()
  const appVersion = "26000370"
  let headers = {
    AppVersion: 2600037000,
    TerminalId: "android",
    "X-UP-CLIENT-CHANNEL-ID": "2600037000-99000-200300220100002"
  }

  // 广东卫视有些特殊
  if (pid == "608831231") {
    rateType = 2
  }

  if (rateType != 2 && userId != "" && token != "") {
    headers.UserId = userId
    headers.UserToken = token
  }
  console.log(headers)
  const str = timestramp + pid + appVersion
  const md5 = getStringMD5(str)
  const result = getSaltAndSign(md5)

  // 请求
  const baseURL = "https://play.miguvideo.com/playurl/v1/play/playurl"
  let params = "?sign=" + result.sign + "&rateType=" + rateType
    + "&contId=" + pid + "&timestamp=" + timestramp + "&salt=" + result.salt
  let respData = await fetch(baseURL + params, {
    headers: headers
  }).then(r => r.json())

  if (respData.rid == 'TIPS_NEED_MEMBER') {
    printYellow("该账号没有会员 正在降低画质")

    params = "?sign=" + result.sign + "&rateType=" + (rateType - 1)
      + "&contId=" + pid + "&timestamp=" + timestramp + "&salt=" + result.salt
    respData = await fetch(baseURL + params, {
      headers: headers
    }).then(r => r.json())
  }

  // console.dir(respData, { depth: null })
  // console.log(respData)
  const url = respData.body.urlInfo?.url
  // console.log(rateType)
  // console.log(url)
  if (!url) {
    return {
      url: "",
      rateType: 0,
      content: respData
    }
  }

  // 将URL加密
  const resURL = getddCalcuURL(url, pid, "android", rateType)

  rateType = respData.body.urlInfo?.rateType
  // console.log("清晰度" + rateType)

  return {
    url: resURL,
    rateType: parseInt(rateType),
    content: respData
  }

}


/**
 * 旧版高清画质
 * @param {string} pid - 节目ID
 * @returns {object} - 
 */
async function getAndroidURL720p(pid) {
  // 获取url
  const timestramp = Math.round(Date.now()).toString()
  const appVersion = "2600034600"
  const appVersionID = appVersion + "-99000-201600010010028"
  let headers = {
    AppVersion: `${appVersion}`,
    TerminalId: "android",
    "X-UP-CLIENT-CHANNEL-ID": `${appVersionID}`
  }
   console.log(pid)
  console.log(headers)
  const str = timestramp + pid + appVersion.substring(0, 8)
  const md5 = getStringMD5(str)

  const salt = String(Math.floor(Math.random() * 1000000)).padStart(6, '0') + '25'
  const suffix = "2cac4f2c6c3346a5b34e085725ef7e33migu" + salt.substring(0, 4)
  const sign = getStringMD5(md5 + suffix)

  let rateType = 3
  // 广东卫视有些特殊
  if (pid == "608831231") {
    rateType = 2
  }
  // 请求
  const baseURL = "https://play.miguvideo.com/playurl/v1/play/playurl"
  const params = "?sign=" + sign + "&rateType=" + rateType
    + "&contId=" + pid + "&timestamp=" + timestramp + "&salt=" + salt
  console.log(baseURL + params)
  const respData = await fetch(baseURL + params, {
    headers: headers
  }).then(r => r.json())
  const ssss = await fetch("https://play.miguvideo.com/playurl/v1/play/playurl?sign=ba3fed4cd92710cc51cc58f3b89d4689&rateType=3&contId=608807420&timestamp=1765629576272&salt=75482825", {
    headers: {
    // 核心：模拟国内 Chrome 浏览器
  "User-Agent": "Mozilla/5.0 (Linux; Android 13; MI 13 Pro Build/TKQ1.221005.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/120.0.6099.230 Mobile Safari/537.36",
  // 国内运营商/地域标识（可选，建议保留）
  "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
  // 接受的内容类型
  "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
  // 缓存策略
  "Cache-Control": "max-age=0",
  // 避免被识别为爬虫（关键）
  "Sec-Fetch-Dest": "document",
  "Sec-Fetch-Mode": "navigate",
  "Sec-Fetch-Site": "same-origin",
  "Sec-Fetch-User": "?1",
  // 国内常见的编码
  "Accept-Encoding": "gzip, deflate, br",
  // 咪咕视频必要的 Referer（根据请求的页面调整）
  "Referer": "https://www.miguvideo.com/",
  // 保持连接
  "Connection": "keep-alive",
  "AppVersion": '2600034600',
  "TerminalId": 'android',
  'X-UP-CLIENT-CHANNEL-ID': '2600034600-99000-201600010010028'
}
  }).then(r => r.json())
  console.dir(ssss, { depth: null })
  const url = respData.body.urlInfo?.url
  // console.log(rateType)
  // console.log(url)
  if (!url) {
    return {
      url: "",
      rateType: 0,
      content: respData
    }
  }

  rateType = respData.body.urlInfo?.rateType

  // 将URL加密
  const resURL = getddCalcuURL720p(url, pid)

  return {
    url: resURL,
    rateType: parseInt(rateType),
    content: respData
  }

}

export { getAndroidURL, getAndroidURL720p }
