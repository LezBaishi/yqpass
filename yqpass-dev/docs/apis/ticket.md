# 工单相关接口

## 获取工单列表

### URL

/api/tickets/

### method

GET

### 请求参数

| 参数名       | 类型    | 必填 | 说明                                                         |
| ------------ | ------- | ---- | ------------------------------------------------------------ |
| sn           | varchar | 否   | 过滤参数：工单编号                                           |
| title        | varchar | 否   | 过滤参数：工单标题                                           |
| create_start | varchar | 否   | 过滤参数：创建时间起                                         |
| create_end   | varchar | 否   | 过滤参数：创建时间至                                         |
| reverse      | varchar | 否   | 按创建时间排序，0倒序、1正序                                 |
| per_page     | int     | 否   | 每页显示个数、默认10                                         |
| page         | int     | 否   | 页码、默认1                                                  |
| workflow_id  | int     | 否   | 过滤参数：工作流ID                                           |
| category     | varchar | 否   | 显示工单类型，默认为duty：{ 'all':所有工单, 'owner':我创建的工单, 'duty':我的待处理工单, 'relation':我的关联工单 } |

### 返回数据

```
{
    "code": 1,
    "data": {
        "value": [
            {
                "id": 13,
                "title": "VPN申请2",
                "workflow": {
                    "workflow_id": 1,
                    "workflow_name": "VPN申请"
                },
                "sn": "YQ-0120180809-008",
                "state": {
                    "state_id": 3,
                    "state_name": "结束"
                },
                "parent_ticket_id": 0,
                "parent_ticket_state_id": 0,
                "participant_info": {
                    "participant": "",
                    "participant_name": "",
                    "participant_type_id": 0,
                    "participant_type_name": "",
                    "participant_alias": ""
                },
                "creator": "admin",
                "gmt_created": "2018-08-09 15:20:12",
                "gmt_modified": "2018-08-15 15:51:14"
            }
        ],
        "per_page": 10,
        "page": 1,
        "total": 1
    },
    "msg": ""
}
```

## 新建工单

### URL

/api/tickets/

### method

POST

### 请求参数

| 参数名                 | 类型    | 必填 | 说明                                                         |
| ---------------------- | ------- | ---- | ------------------------------------------------------------ |
| workflow_id            | int     | 是   | 工作流ID                                                     |
| transition_id          | int     | 是   | 工单流转ID、可根据/workflow/<int: pk>/init_state/获取        |
| parent_ticket_id       | int     | 否   | 父工单的ID（用于子工单的逻辑，如果新建的工单是某个工单的子工单需要填写父工单的ID） |
| parent_ticket_state_id | varchar | 否   | 父工单的状态（子工单是和父工单的某个状态关联的）             |
| suggestion             | varchar | 否   | 处理意见                                                     |
| 其他                   | varchar | 否   | 其他必填字段或可选字段（取决于工作流指定的自定义字段)        |

### 返回数据

```
{
    "code": 1,
    "data": {
        "ticket_id": 14
    },
    "msg": ""
}
```

##获取工单详情

### URL

/api/tickets/<int: pk>

### method

POST

### 请求参数

| 参数名 | 类型 | 必填 | 说明 |
| ------ | ---- | ---- | ---- |
|        |      |      |      |

### 返回数据

```
{
    "code": 1,
    "data": {
        "id": 13,
        "sn": "YQ-0120180809-008",
        "title": "VPN申请2",
        "state_id": 2,
        "parent_ticket_id": 0,
        "participant": "admin",
        "participant_type_id": 1,
        "workflow_id": 1,
        "creator": "admin",
        "gmt_created": "2018-08-09 15:20:12",
        "gmt_modified": "2018-08-15 16:47:59",
        "field_list": [
            {
                "field_key": "sn",
                "name": "工单编号",
                "value": "YQ-0120180809-008",
                "order_id": 0,
                "field_type_id": 5,
                "field_attribute": "1"
            },
            {
                "field_key": "title",
                "name": "标题",
                "value": "VPN申请2",
                "order_id": 20,
                "field_type_id": 5,
                "field_attribute": "2"
            },
            {
                "field_key": "use_type",
                "field_name": "用途",
                "field_value": "拿来使用",
                "order_id": 40,
                "field_type_id": 5,
                "field_attribute": "1",
                "field_choice": {}
            },
            {
                "field_key": "use_days",
                "field_name": "使用时长",
                "field_value": 5,
                "order_id": 40,
                "field_type_id": 10,
                "field_attribute": "2",
                "field_choice": {}
            }
        ]
    },
    "msg": ""
}
```

## 处理工单

### URL

/api/tickets/<int: pk>

### method

POST

### 请求参数

| 参数名        | 类型    | 必填 | 说明                                              |
| ------------- | ------- | ---- | ------------------------------------------------- |
| transition_id | int     | 是   | 流转ID                                            |
| suggestion    | varchar | 否   | 处理意见                                          |
| 其他          | varchar | 否   | 必填字段或可选字段（取决于工作流指定的自定义字段) |

### 返回数据

```
{
    "code": 1,
    "data": {
        "value": true
    },
    "msg": ""
}
```

## 获取工单可做操作

### URL

/api/tickets/<int: pk>/transitions/

### method

GET

### 请求参数

| 参数名        | 类型    | 必填 | 说明                                              |
| ------------- | ------- | ---- | ------------------------------------------------- |
| transition_id | int     | 是   | 流转ID                                            |
| suggestion    | varchar | 否   | 处理意见                                          |
| 其他          | varchar | 否   | 必填字段或可选字段（取决于工作流指定的自定义字段) |

### 返回数据

```
{
    "code": 1,
    "data": {
        "value": [
			{
                "transition_id": 0,
                "transition_name": "接单",
                "field_require_check": false,
                "is_accept": true,
                "in_add_node": false
            }
        ]
    },
    "msg": ""
}
```

## 获取工单流转记录

### URL

/api/tickets/<int: pk>/flowlogs/

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
        "value": [
            {
                "id": 42,
                "ticket_id": "14",
                "state": {
                    "state_id": 4,
                    "state_name": "审批中"
                },
                "transition": {
                    "transition_id": 2,
                    "transition_name": "同意"
                },
                "intervene_type_id": 0,
                "participant": "admin",
                "participant_type_id": 1,
                "suggestion": "测试处理工单",
                "gmt_created": "2018-08-16 09:12:36",
                "gmt_modified": "2018-08-16 09:12:36"
            },
            {
                "id": 39,
                "ticket_id": "14",
                "state": {
                    "state_id": 1,
                    "state_name": "新建中"
                },
                "transition": {
                    "transition_id": 1,
                    "transition_name": "提交"
                },
                "intervene_type_id": 0,
                "participant": "admin",
                "participant_type_id": 1,
                "suggestion": "",
                "gmt_created": "2018-08-15 16:53:18",
                "gmt_modified": "2018-08-15 16:53:18"
            }
        ],
        "per_page": 10,
        "page": 1,
        "total": 2
    },
    "msg": ""
}
```

## 获取工单处理步骤信息

### URL

/api/tickets/<int: pk>/flowsteps/

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
        "value": [
            {
                "state_id": 1,
                "state_name": "新建中",
                "order_id": 0,
                "state_flow_log_list": [
                    {
                        "id": 39,
                        "transition": {
                            "transition_name": "提交",
                            "transition_id": 1
                        },
                        "participant_type_id": 1,
                        "participant": "admin",
                        "intervene_type_id": 0,
                        "suggestion": "",
                        "state_id": 1,
                        "gmt_created": "2018-08-15 16:53:18"
                    }
                ]
            },
            {
                "state_id": 4,
                "state_name": "审批中",
                "order_id": 0,
                "state_flow_log_list": [
                    {
                        "id": 42,
                        "transition": {
                            "transition_name": "同意",
                            "transition_id": 2
                        },
                        "participant_type_id": 1,
                        "participant": "admin",
                        "intervene_type_id": 0,
                        "suggestion": "测试处理工单",
                        "state_id": 4,
                        "gmt_created": "2018-08-16 09:12:36"
                    }
                ]
            },
            {
                "state_id": 2,
                "state_name": "处理中",
                "order_id": 1,
                "state_flow_log_list": []
            },
            {
                "state_id": 3,
                "state_name": "结束",
                "order_id": 3,
                "state_flow_log_list": []
            },
            {
                "state_id": 5,
                "state_name": "脚本处理",
                "order_id": 5,
                "state_flow_log_list": []
            }
        ]
    },
    "msg": ""
}
```

## 修改工单状态信息

### URL

/api/tickets/<int: pk>/change_state/

### method

POST

### 请求参数

| 参数名   | 类型 | 必填 | 说明         |
| -------- | ---- | ---- | ------------ |
| state_id | int  | 是   | 目标状态信息 |

### 返回数据

```
{
    "code": 1,
    "data": "",
    "msg": "修改工单状态成功"
}
```

## 接单操作（当处理人大于1人的时候需要先接单）

### URL

/api/tickets/<int: pk>/accept/

### method

POST

### 请求参数

| 参数名   | 类型 | 必填 | 说明         |
| -------- | ---- | ---- | ------------ |
| state_id | int  | 是   | 目标状态信息 |

### 返回数据

```
{
    "code": 1,
    "data": true,
    "msg": "接单成功"
}
```

## 转单操作（不改变工单状态）

### URL

/api/tickets/<int: pk>/deliver/

### method

POST

### 请求参数

| 参数名          | 类型    | 必填 | 说明           |
| --------------- | ------- | ---- | -------------- |
| target_username | varchar | 是   | 转交用户名信息 |
| suggestion      | varchar | 否   | 转单意见       |

### 返回数据

```
{
    "code": 1,
    "data": true,
    "msg": ""
}
```

## 加签

### URL

/api/tickets/<int: pk>/add_node/

### method

POST

### 场景

当在处理工单时需要额外的一人提供一些必要的信息再回单来处理，这时候可以选择加签给一个人，他处理完点击“完成”后回到原来工单处理人。再按照工作流正常流转下去。

### 请求参数

| 参数名          | 类型    | 必填 | 说明     |
| --------------- | ------- | ---- | -------- |
| target_username | varchar | 是   | 加签对象 |
| suggestion      | varchar | 否   | 加签意见 |

### 返回数据

```
{
    "code": 1,
    "data": true,
    "msg": ""
}
```

## 加签完成

### URL

/api/tickets/<int: pk>/add_node_end/

### method

POST

### 场景

当在处理工单时需要额外的一人提供一些必要的信息再回单来处理，这时候可以选择加签给一个人，他处理完点击“完成”后回到原来工单处理人。再按照工作流正常流转下去。

### 请求参数

| 参数名     | 类型    | 必填 | 说明         |
| ---------- | ------- | ---- | ------------ |
| suggestion | varchar | 否   | 加签完成意见 |

### 返回数据

```
{
    "code": 1,
    "data": true,
    "msg": ""
}
```

##  删除工单

### URL

/api/tickets/delete/

### method

POST

### 请求参数

| 参数名     | 类型    | 必填 | 说明                                                  |
| ---------- | ------- | ---- | ----------------------------------------------------- |
| delete_str | varchar | 是   | 删除工单ID，删除多个工单使用逗号,隔开，比如：13,14,15 |

### 返回数据

```
{
    "code": 1,
    "data": "13,14,15",
    "msg": ""
}
```

##  