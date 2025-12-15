async function fetchMiguVideo(url){
    const headers = {
        "accept": "application/json, text/plain, */*",
        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
        "apipost-client-id": "465aea51-4548-495a-8709-7e532dbe3703",
        "apipost-language": "zh-cn",
        "apipost-machine": "3a214a07786002",
        "apipost-platform": "Win",
        "apipost-terminal": "web",
        "apipost-token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJwYXlsb2FkIjp7InVzZXJfaWQiOjM5NDY2NDM3MTIyMzAwMzEzNywidGltZSI6MTc2NTYzMjU2NSwidXVpZCI6ImJlNDJjOTMxLWQ4MjctMTFmMC1hNThiLTUyZTY1ODM4NDNhOSJ9fQ.QU0RXa0e-yB-fwJNjYt_OnyM6RteY3L1BaUWqCrdAB4",
        "apipost-version": "8.2.6",
        "cache-control": "no-cache",
        "content-type": "application/json",
        "pragma": "no-cache",
        "priority": "u=1, i",
        "sec-ch-ua": '"Chromium";v="136", "Microsoft Edge";v="136", "Not.A/Brand";v="99"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "cookie": "apipost-token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJwYXlsb2FkIjp7InVzZXJfaWQiOjM5NDY2NDM3MTIyMzAwMzEzNywidGltZSI6MTc2NTYzMjU2NSwidXVpZCI6ImJlNDJjOTMxLWQ4MjctMTFmMC1hNThiLTUyZTY1ODM4NDNhOSJ9fQ.QU0RXa0e-yB-fwJNjYt_OnyM6RteY3L1BaUWqCrdAB4; SERVERID=236fe4f21bf23223c449a2ac2dc20aa4|1765632725|1765632691; SERVERCORSID=236fe4f21bf23223c449a2ac2dc20aa4|1765632725|1765632691",
        "Referer": "https://workspace.apipost.net/57a21612a051000/apis",
        "Referrer-Policy": "strict-origin-when-cross-origin"
    }
    const params = url.split("?")[1].split("&")
    const body = {
    "option": {
        "scene": "http_request",
        "lang": "zh-cn",
        "globals": {},
        "project": {
            "request": {
                "header": {
                    "parameter": [
                        {
                            "key": "Accept",
                            "value": "*/*",
                            "is_checked": 1,
                            "field_type": "String",
                            "is_system": 1
                        },
                        {
                            "key": "Accept-Encoding",
                            "value": "gzip, deflate, br",
                            "is_checked": 1,
                            "field_type": "String",
                            "is_system": 1
                        },
                        {
                            "key": "User-Agent",
                            "value": "PostmanRuntime-ApipostRuntime/1.1.0",
                            "is_checked": 1,
                            "field_type": "String",
                            "is_system": 1
                        },
                        {
                            "key": "Connection",
                            "value": "keep-alive",
                            "is_checked": 1,
                            "field_type": "String",
                            "is_system": 1
                        }
                    ]
                },
                "query": {
                    "parameter": []
                },
                "body": {
                    "parameter": []
                },
                "cookie": {
                    "parameter": []
                },
                "auth": {
                    "type": "noauth"
                },
                "pre_tasks": [],
                "post_tasks": []
            }
        },
        "env": {
            "env_id": "1",
            "env_name": "默认环境",
            "env_pre_url": "",
            "env_pre_urls": {
                "1": {
                    "server_id": "1",
                    "name": "默认服务",
                    "sort": 1000,
                    "uri": ""
                },
                "default": {
                    "server_id": "1",
                    "name": "默认服务",
                    "sort": 1000,
                    "uri": ""
                }
            },
            "environment": {}
        },
        "cookies": {
            "switch": 1,
            "data": []
        },
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
                "protocols": [
                    "http"
                ],
                "auth": {
                    "authenticate": -1,
                    "host": "",
                    "username": "",
                    "password": ""
                }
            },
            "ca_cert": {
                "open": -1,
                "path": "",
                "base64": ""
            },
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
                    "auth": {
                        "type": "inherit"
                    },
                    "body": {
                        "mode": "null",
                        "parameter": [],
                        "raw": "",
                        "raw_parameter": [],
                        "raw_schema": {
                            "type": "object"
                        },
                        "binary": null
                    },
                    "pre_tasks": [],
                    "post_tasks": [],
                    "header": {
                        "parameter": [
                            {
                                "description": "",
                                "field_type": "string",
                                "is_checked": 1,
                                "key": " AppVersion",
                                "value": "2600034600",
                                "not_null": 1,
                                "schema": {
                                    "type": "string"
                                },
                                "param_id": "3c60653273e0b3"
                            },
                            {
                                "description": "",
                                "field_type": "string",
                                "is_checked": 1,
                                "key": "TerminalId",
                                "value": "android",
                                "not_null": 1,
                                "schema": {
                                    "type": "string"
                                },
                                "param_id": "3c6075c1f3e0e1"
                            },
                            {
                                "description": "",
                                "field_type": "string",
                                "is_checked": 1,
                                "key": "X-UP-CLIENT-CHANNEL-ID",
                                "value": "2600034600-99000-201600010010028",
                                "not_null": 1,
                                "schema": {
                                    "type": "string"
                                },
                                "param_id": "3c60858bb3e10c"
                            }
                        ]
                    },
                    "query": {
                        "parameter": [
                            {
                                "param_id": "3c5fd74233e004",
                                "field_type": "string",
                                "is_checked": 1,
                                "key": "sign",
                                "not_null": 1,
                                "value": params[0].split("=")[1],
                                "description": ""
                            },
                            {
                                "param_id": "3c6022f433e030",
                                "field_type": "string",
                                "is_checked": 1,
                                "key": "rateType",
                                "not_null": 1,
                                "value": params[1].split("=")[1],
                                "description": ""
                            },
                            {
                                "param_id": "3c60354133e05b",
                                "field_type": "string",
                                "is_checked": 1,
                                "key": "contId",
                                "not_null": 1,
                                "value": params[2].split("=")[1],
                                "description": ""
                            },
                            {
                                "param_id": "3c605e4bf860b1",
                                "field_type": "String",
                                "is_checked": 1,
                                "key": "timestamp",
                                "not_null": 1,
                                "value": params[3].split("=")[1],
                                "description": ""
                            },
                            {
                                "param_id": "3c605e4c3860b2",
                                "field_type": "String",
                                "is_checked": 1,
                                "key": "salt",
                                "not_null": 1,
                                "value": params[4].split("=")[1],
                                "description": ""
                            }
                        ],
                        "query_add_equal": 1
                    },
                    "cookie": {
                        "parameter": [],
                        "cookie_encode": 1
                    },
                    "restful": {
                        "parameter": []
                    },
                    "tabs_default_active_key": "query"
                },
                "parents": [],
                "method": "POST",
                "protocol": "http/1.1",
                "url": url,
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
    try {
    // 第一步：await 等待 fetch 响应（结束 pending 状态）
    const response = await fetch("https://workspace.apipost.net/proxy/v2/http", {
      "headers": headers,
      "body": JSON.stringify(body),
      "method": "POST"
    });

    // 第二步：await 解析响应数据（json/text 等）
    const data = await response.json(); // 若返回 JSON 用这个
    // const data = await response.text(); // 若返回纯文本用这个
    const res = data.data.data.response.body
    // console.log("请求结果：", res); // 最终拿到数据
    return JSON.parse(res);
  } catch (error) {
    console.error("请求失败：", error); // 捕获网络/解析错误
  }
}


// async function sss(){
//     const url = 'https://play.miguvideo.com/playurl/v1/play/playurl?sign=f5d56bd3d6a3d7947a825fdecca2fed8&rateType=3&contId=608807420&timestamp=1765785119617&salt=40570425'

//     const respData = await fetchMiguVideo(url);
// //    console.log(respData)
// }
export {    fetchMiguVideo    }


