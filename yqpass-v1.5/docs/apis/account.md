# 用户管理相关接口

## 获取 CSRF TOKEN

### URL

/api/accounts/get_token/

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
    "data": token,
    "msg": ""
}
```

## 登陆

### URL
/api/accounts/login/

### method
POST

### Headers

Content-Type: application/json 

### 请求参数

| 参数名              | 类型    | 必填 | 说明                                        |
| ------------------- | ------- | ---- | ------------------------------------------- |
| csrfmiddlewaretoken | varchar | 是   | CSRF 参数、通过 /accounts/get_token/ 获取。 |
| username            | varchar | 是   | 用户名                                      |
| password            | varchar | 是   | 密码                                        |

### 返回数据

```json
{
    "code": 1,
    "data": "admin",
    "msg": "用户已经登陆"
}
```

```json
{
    "code": 0,
    "data": "",
    "msg": "用户名与密码不匹配, 请修改后再尝试连接"
}
```

***

## 注销

### URL

/api/accounts/logout/

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
    "data": "用户已注销",
    "msg": ''
}
```

## 注册

### URL

/api/accounts/register/

### method

POST

### Headers

Content-Type: application/json 

### 请求参数

| 参数名              | 类型    | 必填 | 说明                                        |
| ------------------- | ------- | ---- | ------------------------------------------- |
| csrfmiddlewaretoken | varchar | 是   | CSRF 参数、通过 /accounts/get_token/ 获取。 |
| username            | varchar | 是   | 用户名，登陆使用                            |
| password1           | varchar | 是   | 密码                                        |
| password2           | varchar | 是   | 确认密码                                    |
| alias               | varchar | 否   | 别名                                        |
| email               | varchar | 是   | 电子邮箱                                    |
| phone               | varchar | 是   | 电话号码                                    |
| job_number          | varchar | 否   | 工号                                        |
| dept_id             | varchar | 是   | 部门id                                      |

### 返回数据

```json
{
    "code": 1,
    "data": "用户注册成功",
    "msg": '{'username': username}'
}
```

## 用户信息修改

### URL

/api/accounts/account_change/

### method

POST

### Headers

Content-Type: application/json 

### 请求参数

| 参数名              | 类型    | 必填 | 说明                                        |
| ------------------- | ------- | ---- | ------------------------------------------- |
| csrfmiddlewaretoken | varchar | 是   | CSRF 参数、通过 /accounts/get_token/ 获取。 |
| alias               | varchar | 是   | 别名                                        |
| email               | varchar | 是   | 电子游戏                                    |
| phone               | varchar | 是   | 电话号码                                    |
| job_number          | varchar | 是   | 工号                                        |
| dept_id             | varchar | 是   | 部门id                                      |

### 返回数据

```json
{
    "code": 1,
    "data": "用户信息修改成功",
    "msg": '{'alias': user.alias,
             'email': user.email,
             'phone': user.phone,
             'job_number': user.job_number,
             'dept_id': user.dept_id}'
}
```

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
        "id": 3,
        "last_login": "2018-10-10 23:07:31",
        "username": "jiekouren",
        "alias": "",
        "email": "jiekouren@x-zj.cn",
        "phone": "",
        "dept_id": "0",
        "job_number": "",
        "is_active": true,
        "is_admin": false,
        "is_viewer": false,
        "creator": "admin",
        "gmt_created": "2018-09-18 15:49:45",
        "modifier": "admin",
        "gmt_modified": "2018-09-18 15:49:45",
        "is_deleted": false,
        "role_info": [
            {
                "role_id": 2,
                "role_name": "审核方"
            }
        ]
    },
    "msg": ""
}
```

## 修改密码

### URL

/api/accounts/password_change/

### method

POST

### 请求参数

| 参数名              | 类型    | 必填 | 说明                                        |
| ------------------- | ------- | ---- | ------------------------------------------- |
| csrfmiddlewaretoken | varchar | 是   | CSRF 参数、通过 /accounts/get_token/ 获取。 |
| old_password        | varchar | 是   | 旧密码                                      |
| new_password1       | varchar | 是   | 密码                                        |
| new_password2       | varchar | 是   | 确认密码                                    |

### 返回数据

```json
{
    "code": 1,
    "data": "密码修改成功, 请重新登陆",
    "msg": ''
}
```

## 获取用户列表

### URL

/api/accounts/user_list/

### method

GET

### 请求参数

| 参数名   | 类型    | 必填 | 说明                                                         |
| -------- | ------- | ---- | ------------------------------------------------------------ |
| username | varchar | 否   | 过滤参数：用户名                                             |
| email    | varchar | 否   | 过滤参数：电子邮箱                                           |
| alias    | varchar | 否   | 过滤参数：用户别名                                           |
| per_page | varchar | 否   | 每页显示条数，默认为10                                       |
| page     | varchar | 否   | 页码，默认为1                                                |
| category | varchar | 否   | 显示用户类型，默认为all：{ 'all':所有用户, 'general':一般用户, 'admin':管理用户 , “viewer”: 参观者} |

### 返回数据

```json
{
    "code": 1,
    "data": {
        "value": [
            {
                "id": 7,
                "username": "shenpiren1",
                "email": "13802887711@139.com",
                "alias": "审批人1",
                "active": true,
                "admin": false,
                "viewer": false,
            },
            {
                "id": 2,
                "username": "admin",
                "email": "790169239@qq.com",
                "alias": "鹳狸猿",
                "active": true,
                "admin": true,
                "viewer": false,
            }
        ],
        "per_page": 10,
        "page": 1,
        "total": 2
    },
    "msg": ""
}
```

## 获取用户详情

### URL

/api/accounts/<int: pk>/user_detail/

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
        "id": 3,
        "last_login": "2018-10-10 23:07:31",
        "username": "jiekouren",
        "alias": "",
        "email": "jiekouren@x-zj.cn",
        "phone": "",
        "dept_id": "0",
        "job_number": "",
        "is_active": true,
        "is_admin": false,
        "is_viewer": false,
        "creator": "admin",
        "gmt_created": "2018-09-18 15:49:45",
        "modifier": "admin",
        "gmt_modified": "2018-09-18 15:49:45",
        "is_deleted": false,
        "role_info": [
            {
                "role_id": 2,
                "role_name": "审核方"
            }
        ]
    },
    "msg": ""
}
```

## 操作角色成员（新增、删除）

### URL

/api/accounts/<int: pk>/role_members/

### method

POST

### 请求参数

| 参数名  | 类型 | 必填 | 说明                                                         |
| ------- | ---- | ---- | ------------------------------------------------------------ |
| user    | str  | 是   | 操作用户字符串。<br />eg: “1,2,3,4,5”, 多个用户id的话用逗号隔开。 |
| command | str  | 是   | 操作命令: append(新增), delete(删除)                         |

### 返回数据

```json
{
    "code": 1,
    "data": "4已添加",
    "msg": ""
}
```

## 删除用户

### URL

/api/accounts/user_delete/

### method

POST

### Headers

Content-Type: application/json 

### 请求参数

| 参数名  | 类型 | 必填 | 说明   |
| ------- | ---- | ---- | ------ |
| user_id | int  | 是   | 用户id |

### 返回数据

```json
{
    "code": 1,
    "data": "test",		# username
    "msg": ""
}
```

## 获取角色列表

### URL

/api/accounts/role_list/

### method

GET

### 请求参数

| 参数名    | 类型    | 必填 | 说明                   |
| --------- | ------- | ---- | ---------------------- |
| role_name | varchar | 否   | 过滤参数：角色名       |
| per_page  | varchar | 否   | 每页显示条数，默认为10 |
| page      | varchar | 否   | 页码，默认为1          |

### 返回数据

```json
{
    "code": 1,
    "data": {
        "value": [
            {
                "id": 2,
                "name": "approval",
                "description": "审批人",
                "label": "",
                "creator": "admin",
                "gmt_created": "2018-08-01 15:20:15",
                "gmt_modified": "2018-08-01 15:20:15"
            },
            {
                "id": 1,
                "name": "applicant",
                "description": "申请人",
                "label": "",
                "creator": "admin",
                "gmt_created": "2018-08-01 15:19:13",
                "gmt_modified": "2018-08-01 15:21:12"
            }
        ],
        "per_page": 10,
        "page": 1,
        "total": 4
    },
    "msg": ""
}
```

## 获取角色详情

### URL

/api/accounts/<int: pk>/role_detail/

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
        "id": 1,
        "name": "applicant",
        "description": "申请人",
        "label": "",
        "creator": "admin",
        "gmt_created": "2018-08-01 15:19:13",
        "gmt_modified": "2018-08-01 15:21:12",
        "user_list": {								# 角色包含用户简略情况
            "value": [
                {
                    "id": 2,
                    "username": "admin",
                    "email": "790169239@qq.com",
                    "alias": "鹳狸猿",
                    "active": true,
                    "admin": true，
                    "viewer": false
                }
            ],
            "per_page": 10,
            "page": 1,
            "total": 1
        }
    },
    "msg": ""
}
```

## 删除角色

### URL

/api/accounts/role_delete/

### method

POST

### Headers

Content-Type: application/json 

### 请求参数

| 参数名  | 类型 | 必填 | 说明   |
| ------- | ---- | ---- | ------ |
| role_id | int  | 是   | 角色id |

### 返回数据

```json
{
    "code": 1,
    "data": "测试组",		@ role_name
    "msg": ""
}
```

## 获取部门列表

### URL

/api/accounts/dept_list/

### method

GET

### 请求参数

| 参数名    | 类型    | 必填 | 说明                   |
| --------- | ------- | ---- | ---------------------- |
| dept_name | varchar | 否   | 过滤参数：部门名       |
| per_page  | varchar | 否   | 每页显示条数，默认为10 |
| page      | varchar | 否   | 页码，默认为1          |

### 返回数据

```json
{
    "code": 1,
    "data": {
        "value": [
            {
                "id": 1,
                "name": "监控分析室",
                "parent_dept_id": 0,
                "leader": "",
                "approver": "shenpiren",
                "label": "",
                "creator": "admin",
                "gmt_created": "2018-08-01 15:22:19",
                "gmt_modified": "2018-08-01 15:22:19"
            }
        ],
        "per_page": 10,
        "page": 1,
        "total": 1
    },
    "msg": ""
}
```

## 获取部门详情

### URL

/api/accounts/<int: pk>/dept_detail/

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
        "id": 1,
        "name": "监控分析室",
        "parent_dept_id": 0,
        "leader": "",
        "approver": [
            {
                "id": 2,
                "username": "admin",
                "email": "790169239@qq.com",
                "alias": "鹳狸猿",
                "active": true,
                "admin": true
            }
        ],
        "label": "",
        "creator": "admin",
        "gmt_created": "2018-08-01 15:22:19",
        "gmt_modified": "2018-08-27 15:00:43",
        "is_deleted": false
    },
    "msg": ""
}
```

## 删除部门

### URL

/api/accounts/dept_delete/

### method

POST

### Headers

Content-Type: application/json 

### 请求参数

| 参数名  | 类型 | 必填 | 说明   |
| ------- | ---- | ---- | ------ |
| dept_id | int  | 是   | 角色id |

### 返回数据

```json
{
    "code": 1,
    "data": "测试部门",		# dept_name
    "msg": ""
}
```

