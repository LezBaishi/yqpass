# 资源管理相关接口

## 获取楼栋机房信息列表

### URL

/api/resmanage/building_room/

### method

GET

### 请求参数

| 参数名       | 类型    | 必填 | 说明                                                         |
| ------------ | ------- | ---- | ------------------------------------------------------------ |
| building    | varchar | 否   | 过滤参数：楼栋号              |
| room        | varchar | 否   | 过滤参数：机房号              |
| description  | varchar | 否   | 过滤参数：详细说明          |
| room_id | int | 否 | 过滤参数：楼栋机房id |
| reverse      | varchar | 否   | 按照ID倒序（False:0和True:1）, 默认1|
| per_page     | int     | 否   | 每页显示个数，默认10         |
| page         | int     | 否   | 页码，默认1                 |

### 返回数据

~~~
{
    "code": 1,
    "data": {
        "value": [
            {
                "id": 1,
                "building": "3.1",
                "room": "101",
                "description": ""
            },
            {
                "id": 2,
                "building": "3.1",
                "room": "102",
                "description": ""
            },
            {
                "id": 3,
                "building": "3.1",
                "room": "103",
                "description": ""
            },
            {
                "id": 4,
                "building": "3.1",
                "room": "104",
                "description": ""
            },
            {
                "id": 5,
                "building": "3.1",
                "room": "201",
                "description": ""
            },
            {
                "id": 6,
                "building": "3.1",
                "room": "202",
                "description": ""
            },
            {
                "id": 7,
                "building": "3.1",
                "room": "203",
                "description": ""
            },
            {
                "id": 8,
                "building": "3.1",
                "room": "204",
                "description": ""
            },
            {
                "id": 9,
                "building": "3.1",
                "room": "205",
                "description": ""
            },
            {
                "id": 10,
                "building": "3.1",
                "room": "206",
                "description": ""
            }
        ],
        "per_page": 10,
        "page": 1,
        "total": 109
    },
    "msg": ""
}
~~~

## 获取光缆段（视图）列表

### URL

/api/resmanage/ocable_section/

### method

GET

### 请求参数

| 参数名       | 类型    | 必填 | 说明                                                         |
| ------------ | ------- | ---- | ------------------------------------------------------------ |
| building    | varchar | 否   | 过滤参数：光缆端点楼栋名称                                    |
| room        | varchar | 否   | 过滤参数：光缆端点机房号                                |
| ocable_name   | varchar | 否   | 光缆名称                                   |
| reverse       | varchar | 否   | 按照光缆段ID倒序（False:0和True:1）                         |
|per_page       | int     | 否   | 每页显示个数，默认10                                         |
| page          | int     | 否   | 页码，默认1                                                |

### 返回数据

~~~
{
    "code": 1,
    "data": {
        "value": [
            {
                "id": 1,
                "building_A": "3.1",
                "room_A": "103",
                "name_A": "3.1栋103传输机房",
                "building_Z": "1.1",
                "room_Z": "-1F",
                "name_Z": "1.1栋负1楼北塔无线基站",
                "ocable_name": "3.1栋103传输机房-1.1栋负1楼北塔无线基站",
                "core_num": 48,
                "used_core_num": "0",
                "core_occ": "0.00%",
                "unused_core_num": "48",
                "ocable_length": "0.60",
                "core_kilo": "28.80",
                "used_core_kilo": "0.00",
                "core_usage": "0.00%",
                "ocable_type": "单模",
                "ocable_level": "广州本地网",
                "ofiber_type": "G652",
                "notes": "test"
            },
            {
                "id": 5,
                "building_A": "3.1",
                "room_A": "204",
                "name_A": "3.1栋204传输机房路由1",
                "building_Z": "出局",
                "room_Z": "西德胜",
                "name_Z": "西德胜",
                "ocable_name": "3.1栋204传输机房路由1-西德胜",
                "core_num": 72,
                "used_core_num": "0",
                "core_occ": "0.00%",
                "unused_core_num": "72",
                "ocable_length": "0.08",
                "core_kilo": "5.76",
                "used_core_kilo": "0.00",
                "core_usage": "0.00%",
                "ocable_type": "单模",
                "ocable_level": "广州本地网",
                "ofiber_type": "G655",
                "notes": "test"
            },
            {
                "id": 6,
                "building_A": "2.3",
                "room_A": "202",
                "name_A": "2.3栋202传输机房",
                "building_Z": "6.1",
                "room_Z": "3FNR",
                "name_Z": "6.1栋3楼北弱电间",
                "ocable_name": "2.3栋202传输机房-6.1栋3楼北弱电间",
                "core_num": 12,
                "used_core_num": "2",
                "core_occ": "16.67%",
                "unused_core_num": "10",
                "ocable_length": "0.25",
                "core_kilo": "3.00",
                "used_core_kilo": "0.50",
                "core_usage": "16.67%",
                "ocable_type": "单模",
                "ocable_level": "南方基地园区",
                "ofiber_type": "G652",
                "notes": ""
            }
        ],
        "per_page": 10,
        "page": 1,
        "total": 3
    },
    "msg": ""
}
~~~

## 新建光缆段

### URL

/api/resmanage/ocable_section/

### method

POST

### Headers

Content-Type: application/json 

### 请求参数

| 参数名       | 类型    | 必填 | 说明                                                         |
| ------------ | ------- | ---- | ------------------------------------------------------------ |
| building_A | varchar | 是  | A端楼栋名称                              |
| room_A | varhcar | 是 | A端机房名称 |
| name_A      | varchar | 是   | A端名称                                       |
| building_Z | varchar | 是   | Z端楼栋名称                         |
| room_Z | varchar | 是 | Z端机房名称 |
| name_Z      | varchar | 是   | Z端名称                                       |
| core_num    | int     | 是   | 纤芯数                                        |
|ocable_length| decimal(5,2)|是|光缆长度，单位：皮长公里                         |
| ocable_type | varchar | 是   | 光缆类型 (“单模”, “多模”)                     |
| ocable_level| varchar | 是   | 光缆等级 ("干线", "广州本地网", "南方基地园区", "南方基地园区（CMNET网络成端）") |
| ofiber_type | varchar | 是   | 光纤型号 ('G652', 'G655')                 |
| notes       | varchar | 否   | 备注                                          |

### 返回数据

~~~
{
    "code": 1, 
    "data": {
        "ocable_section_id": 128
    }, 
    "msg": ""
}
~~~

## 光缆段详情

### URL

/api/resmanage/<int: pk>/ocable_section/

### method

GET

### 请求参数

| 参数名 | 类型 | 必填 | 说明 |
| ------ | ---- | ---- | ---- |
|        |      |      |      |

### 返回数据

```
{
    "code": 1,
    "data": {
        "id": 1,
        "building_A": "3.1",
        "room_A": "103",
        "name_A": "3.1栋103传输机房",
        "building_Z": "1.1",
        "room_Z": "-1F",
        "name_Z": "1.1栋负1楼北塔无线基站",
        "ocable_name": "3.1栋103传输机房-1.1栋负1楼北塔无线基站",
        "core_num": 48,
        "used_core_num": "3",
        "core_occ": "6.25%",
        "unused_core_num": "45",
        "ocable_length": "0.60",
        "core_kilo": "28.80",
        "used_core_kilo": "1.80",
        "core_usage": "6.25%",
        "ocable_type": "单模",
        "ocable_level": "广州本地网",
        "ofiber_type": "G652",
        "notes": "test"
    },
    "msg": ""
}
```

## 编辑光缆段

### URL

/api/resmanage/<int: pk>/ocable_section/

### method

POST

### Headers

Content-Type: application/json 

### 请求参数

| 参数名       | 类型    | 必填 | 说明                                                         |
| ------------ | ------- | ---- | ------------------------------------------------------------ |
| bri_A_id    | int     | 是   | A端楼栋机房号id                                |
| name_A      | varchar | 是   | A端名称                                       |
| bri_Z_id    | int     | 是   | Z端楼栋机房号id                                |
| name_Z      | varchar | 是   | Z端名称                                       |
| core_num    | int     | 是   | 纤芯数                                        |
|ocable_length| decimal(5,2) |是|光缆长度，单位：皮长公里                         |
| ocable_type | varchar | 是   | 光缆类型 (“单模”, “多模”)                     |
| ocable_level| varchar | 是   | 光缆等级 ("干线", "广州本地网", "南方基地园区", "南方基地园区（CMNET网络成端）") |
| ofiber_type | varchar | 是   | 光纤型号 ('G652', 'G655')                 |
| notes       | varchar | 否   | 备注                                          |

### 返回数据

~~~
{
    "code": 1, 
    "data": {
        "value": true 
    }, 
    "msg": "编辑光缆段成功"
}
~~~

## 删除光缆段

### URL

/api/resmanage/ocable_section/delete/

### method

POST

### Headers

Content-Type: application/json

### 请求参数

| 参数名       | 类型    | 必填 | 说明                                                         |
| ------------ | ------- | ---- | ------------------------------------------------------------ |
| delete_str   | varchar | 是   | 删除光缆段ID，删除多个光缆段使用逗号隔开，比如：13,14,15|


### 返回数据

~~~
{
    "code": 1, 
    "data": "13,14,15", 
    "msg": "删除光缆段成功"
}
~~~

## 获取纤芯（视图）列表

### URL

/api/resmanage/ofiber_core/

### method

GET

### 请求参数

| 参数名       | 类型    | 必填 | 说明                                                         |
| ------------ | ------- | ---- | ------------------------------------------------------------ |
| ocable_section_id   | varchar | 否   | 过滤参数：光缆段ID                                      |
| ocable_odf        | varchar | 否   | 过滤参数：光缆ODF                                    |
| switch_dport | varchar | 否   | 过滤参数：转接设备端口                                     |
| ocable_cor      | varchar | 否   | 过滤参数：光缆对应                                           |
| core_quality      | varchar | 否   | 过滤参数：纤芯质量                                         |
| circuit_num      | varchar | 否   | 过滤参数：电路编号                                          |
| occ_business      | varchar | 否   | 过滤参数：占用业务                                         |
| sn      | varchar | 否   | 过滤参数：施工单号                                                   |
| building | varchar | 否 | 过滤参数：楼栋名称 |
| room | varchar | 否 | 过滤参数：机房名称 |
| reverse      | varchar | 否   | 按照光缆段ID倒序（False:0和True:1）                             |
| per_page     | int     | 否   | 每页显示个数，默认10                                            |
| page         | int     | 否   | 页码，默认1                                                    |

### 返回数据

~~~
{
    "code": 1,
    "data": {
        "value": [
            {
                "id": 1,
                "ocable_section_id": 1,
                "core_no": 1,
                "ocable_odf_A": "3.1栋103机房G101-1-A1",
                "switch_dport_A": null,
                "ocable_cor": "3.1栋103传输机房-1.1栋负1楼北塔无线基站-48芯之1",
                "ocable_odf_Z": "1.1栋负1楼ODF01-1-A1",
                "switch_dport_Z": null,
                "core_quality": "良好",
                "circuit_num": null,
                "occ_business": null,
                "sn": null,
                "notes": "3"
            },
            {
                "id": 11,
                "ocable_section_id": 6,
                "core_no": 1,
                "ocable_odf_A": "2.3栋202传输机房A101-5-B1",
                "switch_dport_A": null,
                "ocable_cor": "2.3栋202传输机房-6.1栋3楼北弱电间-12芯之1",
                "ocable_odf_Z": "6.1栋3楼北弱电间ODF01-1-A1",
                "switch_dport_Z": null,
                "core_quality": "",
                "circuit_num": null,
                "occ_business": null,
                "sn": null,
                "notes": ""
            },
            {
                "id": 23,
                "ocable_section_id": 5,
                "core_no": 1,
                "ocable_odf_A": "3.1栋204机房G101-1-A1",
                "switch_dport_A": null,
                "ocable_cor": "3.1栋204传输机房路由1-西德胜-72芯之1",
                "ocable_odf_Z": "K05-1-A1",
                "switch_dport_Z": null,
                "core_quality": "",
                "circuit_num": null,
                "occ_business": null,
                "sn": null,
                "notes": ""
            },
            {
                "id": 2,
                "ocable_section_id": 1,
                "core_no": 2,
                "ocable_odf_A": "3.1栋103机房G101-1-A2",
                "switch_dport_A": null,
                "ocable_cor": "3.1栋103传输机房-1.1栋负1楼北塔无线基站-48芯之2",
                "ocable_odf_Z": "1.1栋负1楼ODF01-1-A2",
                "switch_dport_Z": null,
                "core_quality": "良好",
                "circuit_num": null,
                "occ_business": null,
                "sn": null,
                "notes": "3"
            },
            {
                "id": 12,
                "ocable_section_id": 6,
                "core_no": 2,
                "ocable_odf_A": "2.3栋202传输机房A101-5-B2",
                "switch_dport_A": null,
                "ocable_cor": "2.3栋202传输机房-6.1栋3楼北弱电间-12芯之2",
                "ocable_odf_Z": "6.1栋3楼北弱电间ODF01-1-A2",
                "switch_dport_Z": null,
                "core_quality": "",
                "circuit_num": null,
                "occ_business": null,
                "sn": null,
                "notes": ""
            },
            {
                "id": 7,
                "ocable_section_id": 1,
                "core_no": 3,
                "ocable_odf_A": "3.1栋103机房G101-1-A3",
                "switch_dport_A": null,
                "ocable_cor": "3.1栋103传输机房-1.1栋负1楼北塔无线基站-48芯之3",
                "ocable_odf_Z": "1.1栋负1楼ODF01-1-A3",
                "switch_dport_Z": null,
                "core_quality": "",
                "circuit_num": null,
                "occ_business": null,
                "sn": null,
                "notes": ""
            },
            {
                "id": 13,
                "ocable_section_id": 6,
                "core_no": 3,
                "ocable_odf_A": "2.3栋202传输机房A101-5-B3",
                "switch_dport_A": "A02架S9303交换机",
                "ocable_cor": "2.3栋202传输机房-6.1栋3楼北弱电间-12芯之3",
                "ocable_odf_Z": "6.1栋3楼北弱电间ODF01-1-A3",
                "switch_dport_Z": "A02架S9303交换机",
                "core_quality": "",
                "circuit_num": "F0331",
                "occ_business": "6.1栋计算机内网上网（备用）",
                "sn": "20120321-01",
                "notes": ""
            },
            {
                "id": 8,
                "ocable_section_id": 1,
                "core_no": 4,
                "ocable_odf_A": "3.1栋103机房G101-1-A4",
                "switch_dport_A": null,
                "ocable_cor": "3.1栋103传输机房-1.1栋负1楼北塔无线基站-48芯之4",
                "ocable_odf_Z": "1.1栋负1楼ODF01-1-A4",
                "switch_dport_Z": null,
                "core_quality": "良好",
                "circuit_num": null,
                "occ_business": null,
                "sn": null,
                "notes": ""
            },
            {
                "id": 14,
                "ocable_section_id": 6,
                "core_no": 4,
                "ocable_odf_A": "2.3栋202传输机房A101-5-B4",
                "switch_dport_A": "A02架S9303交换机",
                "ocable_cor": "2.3栋202传输机房-6.1栋3楼北弱电间-12芯之4",
                "ocable_odf_Z": "6.1栋3楼北弱电间ODF01-1-A4",
                "switch_dport_Z": "A02架S9303交换机",
                "core_quality": "",
                "circuit_num": "F0331",
                "occ_business": "6.1栋计算机内网上网（备用）",
                "sn": "20120321-01",
                "notes": ""
            },
            {
                "id": 15,
                "ocable_section_id": 6,
                "core_no": 5,
                "ocable_odf_A": "2.3栋202传输机房A101-5-B5",
                "switch_dport_A": null,
                "ocable_cor": "2.3栋202传输机房-6.1栋3楼北弱电间-12芯之5",
                "ocable_odf_Z": "6.1栋3楼北弱电间ODF01-1-A5",
                "switch_dport_Z": null,
                "core_quality": "",
                "circuit_num": null,
                "occ_business": null,
                "sn": null,
                "notes": ""
            }
        ],
        "per_page": 10,
        "page": 1,
        "total": 17
    },
    "msg": ""
}
~~~

## 新建纤芯

### URL

/api/resmanage/ofiber_core/

### method

POST

### Headers

Content-Type: application/json 

### 请求参数

| 参数名       | 类型    | 必填 | 说明                                                         |
| ------------ | ------- | ---- | ---------------------------------------------------------  |
| ocable_section_id| int | 是   | 光缆段ID                                                    |
| ocable_odf_A| varchar  | 是   | A端光缆ODF                                                  |
| ocable_odf_Z| varchar  | 是   | Z端光缆ODF                                                  |
| core_quality| varchar  | 否   | 纤芯质量                                                    |
| notes       | varchar  | 否   | 备注                                                       |

### 返回数据

~~~
{
    "code": 1, 
    "data": {
        "ofiber_core_id": 12
    }, 
    "msg": "新建纤芯成功"
}
~~~

## 编辑纤芯

### URL

/api/resmanage/<int: pk>/ofiber_core/

### method

POST

### Headers

Content-Type: application/json 

### 请求参数

| 参数名       | 类型    | 必填 | 说明                                                         |
| ------------ | ------- | ---- | ------------------------------------------------------------ |
| core_no     | int     | 是   | 纤芯序号                                |
| ocable_section_id| int | 是   | 光缆段ID                                     |
| ocable_odf_A| varchar  | 是   | A端光缆ODF                            |
| ocable_odf_Z| varchar  | 是   | Z端光缆ODF                                     |
| core_quality| varchar  | 否   | 纤芯质量                                        |
| notes       | varchar  | 否   | 备注                                          |

### 返回数据

~~~
{
    "code": 1, 
    "data": {
        "value": true 
    }, 
    "msg": "编辑纤芯成功"
}
~~~

## 删除纤芯

### URL

/api/resmanage/ofiber_core/delete/

### method

POST

### Headers

Content-Type: application/json

### 请求参数

| 参数名       | 类型    | 必填 | 说明                                                         |
| ------------ | ------- | ---- | ------------------------------------------------------------ |
| delete_str   | varchar | 是   | 删除纤芯ID，删除多个纤芯使用逗号隔开，比如：13,14,15|

### 返回数据

~~~
{
    "code": 1, 
    "data": "13,14,15", 
    "msg": "删除纤芯成功"
}
~~~

## 获取在用电路列表

### URL

/api/resmanage/using_circuit/

### method

GET

### 请求参数

| 参数名       | 类型    | 必填 | 说明                                                         |
| ------------ | ------- | ---- | ---------------------------------------------------------- |
| project_name| varchar | 否   | 过滤参数：项目名称                                             |
| name_az | varchar | 否   | 过滤参数：A、Z端名称                                        |
| circuit_num | varchar | 否   | 过滤参数：电路编号                                             |
| state      | varchar | 否   | 过滤参数：状态(在用/停闭)                                       |
| sn         | varchar | 否   | 过滤参数：施工单号                                              |
| reverse    | varchar | 否   | 按照电路编号倒序（False:0和True:1），默认1                       |
| per_page   | int     | 否   | 每页显示个数，默认10                                            |
| page       | int     | 否   | 页码，默认1                                                    |

### 返回数据

~~~
{
    "code": 1,
    "data": {
        "value": [
            {
                "project_name": "6.1栋计算机内网上网（备用）",
                "name_A": "6.2栋2楼弱电间",
                "name_Z": "6.1栋3楼北弱电间",
                "circuit_num": "F0331",
                "state": "在用",
                "sn": "20120321-01",
                "route": {
                    "first": [
                        [
                            "2.3栋202传输机房A101-5-B3",
                            "2.3栋202传输机房-6.1栋3楼北弱电间-12芯之3",
                            "6.1栋3楼北弱电间ODF01-1-A3"
                        ]
                    ],
                    "second": [
                        [
                            "2.3栋202传输机房A101-5-B4",
                            "2.3栋202传输机房-6.1栋3楼北弱电间-12芯之4",
                            "6.1栋3楼北弱电间ODF01-1-A4"
                        ]
                    ]
                }
            },
            {
                "project_name": "维速信息（高唐路）",
                "name_A": "3.1栋308机房",
                "name_Z": "3.1栋103机房",
                "circuit_num": "F4865",
                "state": "在用",
                "sn": "20180105-01",
                "route": {
                    "first": [
                        [
                            "3.1栋303机房 ODF G09-5-A7",
                            "3.1栋303机房-3.1栋308机房-144芯之7",
                            "3.1栋303机房 ODF G09-5-A7"
                        ],
                        [
                            "3.1栋103机房 ODF A113-3-F1",
                            "3.1栋103机房（路由3）-3.1栋303机房（路由3）-144芯之61",
                            "3.1栋303机房 ODF H11-1-F1"
                        ]
                    ],
                    "second": [
                        [
                            "3.1栋303机房 ODF G09-5-A8",
                            "3.1栋303机房-3.1栋308机房-144芯之8",
                            "3.1栋308机房 ODF A10-1-A8"
                        ],
                        [
                            "3.1栋103机房 ODF A113-3-F2",
                            "3.1栋103机房（路由3）-3.1栋303机房（路由3）-144芯之62",
                            "3.1栋303机房 ODF H11-1-F2"
                        ]
                    ]
                }
            }
        ],
        "per_page": 10,
        "page": 1,
        "total": 2
    },
    "msg": ""
}
~~~

## 分配电路路由（废弃）

### URL

/api/resmanage/circuit_route/

### method

POST

### Headers

Content-Type: application/json 

### 请求参数

| 参数名       | 类型    | 必填 | 说明                                                         |
| ------------ | ------- | ---- | ---------------------------------------------------------  |
| application_detail_id| int    | 是   | 申请单明细表ID                                        |
| circuit_num   | varchar  | 是     | 电路编号                                                |
| route         | varchar  | 是     | 路由信息，包括路由编号（route_no）+路由位置（route_where）+纤芯ID（ofiber_core_id）|
| state         | varchar  | 是     | 状态                                                   |

### 返回数据

~~~
{
    "code": 1, 
    "data": "13,14,15", 
    "msg": "分配电路路由成功"
}
~~~

PS.data内容为路由信息表新增记录的ID，ID之间使用逗号隔开。

## 停闭电路

### URL

/api/resmanage/circuit_route/delete/

### method

POST

### Headers

Content-Type: application/json

### 请求参数

| 参数名       | 类型    | 必填 | 说明                                                         |
| ------------ | ------- | ---- | ------------------------------------------------------------ |
| delete_str   | varchar | 是   | 停闭多条电路，停闭多条电路使用逗号隔开，比如：F0013, F0014, F0015|

### 返回数据

~~~
{
    "code": 1, 
    "data": "F0013, F0014, F0015", 
    "msg": "停闭电路成功"
}
~~~

PS.停闭电路需将路由信息表相关电路的状态改为停闭，并释放路由资源（将is_delete标为true）