# 工作流相关接口

## 获取工作流列表

### URL

/api/workflow/

### method

GET

### 请求参数

| 参数名   | 类型    | 必填 | 说明                 |
| -------- | ------- | ---- | -------------------- |
| name     | varchar | 否   | 工作流搜索参数       |
| page     | int     | 否   | 页码、默认1          |
| per_page | int     | 否   | 每页显示个数，默认10 |

### 返回数据

```json
{
    "code": 1,
    "data": {
        "value": [
            {
                "id": 1,
                "name": "VPN申请",
                "description": "VPN申请流程",
                "creator": "admin",
                "gmt_created": "2018-08-06 16:00:38"
            },
            {
                "id": 2,
                "name": "电缆申请",
                "description": "电缆申请流程",
                "creator": "admin",
                "gmt_created": "2018-08-06 16:01:28"
            }
        ],
        "per_page": 10,
        "page": 1,
        "total": 2
    },
    "msg": ""
}
```

## 获取工作流初始状态

### URL

/api/workflow/<int: pk>/init_state 

### method

GET

### 请求参数

| 参数名   | 类型    | 必填 | 说明                 |
| -------- | ------- | ---- | -------------------- |
| name     | varchar | 否   | 工作流搜索参数       |
| page     | int     | 否   | 页码、默认1          |
| per_page | int     | 否   | 每页显示个数，默认10 |

### 返回数据

```json
{
    "code": 1,
    "data": {
        "id": 1,
        "name": "新建中",
        "workflow_id": 1,
        "sub_workflow_id": 0,
        "distribute_type_id": 1,
        "is_hidden": false,
        "order_id": 0,
        "type_id": 1,
        "participant_type_id": 1,
        "participant": "admin",
        "field_list": [
            {
                "field_key": "title",
                "name": "标题",
                "value": null,
                "order_id": 20,
                "field_type_id": 5,
                "field_attribute": "2"
            },
            {
                "field_key": "use_type",
                "field_name": "用途",
                "field_value": null,
                "order_id": 40,
                "field_type_id": 5,
                "field_attribute": "2",
                "field_choice": {}
            },
            {
                "field_key": "use_days",
                "field_name": "使用时长",
                "field_value": null,
                "order_id": 40,
                "field_type_id": 10,
                "field_attribute": "2",
                "field_choice": {}
            }
        ],
        "label": {},
        "creator": "admin",
        "gmt_created": "2018-08-07 11:39:52",
        "transition": [
            {
                "transtion_id": 1,
                "transtion_name": "提交"
            }
        ]
    },
    "msg": ""
}
```

# 获取工作流状态列表

### URL

/api/workflow/<int: pk>/states_list/

### method

GET

### 请求参数

| 参数名   | 类型 | 必填 | 说明             |
| -------- | ---- | ---- | ---------------- |
| per_page | int  | 否   | 每页个数，默认10 |
| page     | int  | 否   | 页码，默认1      |

### 返回数据

```json
{
    "code": 1,
    "data": {
        "value": [
            {
                "id": 1,
                "name": "新建工单",
                "workflow_id": 1,
                "sub_workflow_id": 0,
                "distribute_type_id": 1,
                "is_hidden": false,
                "order_id": 0,
                "type_id": 1,
                "participant_type_id": 4,
                "participant": "1",
                "state_field": {
                    "sn": 2,
                    "title": 2,
                    "application_date": 2,
                    "open_date": 2,
                    "person1": 2,
                    "phone1": 2,
                    "email1": 2,
                    "person2": 2,
                    "phone2": 2,
                    "email2": 2,
                    "application_detail": 2
                },
                "label": {},
                "creator": "admin",
                "gmt_created": "2018-08-29 11:16:09"
            },
            ...... # 省略
        ],
        "per_page": 10,
        "page": 1,
        "total": 7
    },
    "msg": ""
}
```

## 获取工作流状态详情

### URL

/api/workflow/<int: pk>/state/

### method

GET

### 请求参数

| 参数名 | 类型 | 必填 | 说明 |
| ------ | ---- | ---- | ---- |
|        |      |      |      |

### 返回数据

```json
{
    "code": 1,
    "data": {
        "id": 2,
        "name": "处理中",
        "workflow_id": 1,
        "sub_workflow_id": 0,
        "distribute_type_id": 1,
        "is_hidden": false,
        "order_id": 1,
        "type_id": 0,
        "participant_type_id": 1,
        "participant": "admin",
        "state_field": {
            "title": "2",
            "sn": "1",
            "use_type": "1",
            "use_days": "2"
        },
        "label": {},
        "creator": "admin",
        "gmt_created": "2018-08-07 11:42:48"
    },
    "msg": ""
}
```

##  