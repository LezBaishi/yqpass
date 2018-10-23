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

```
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
### 请求参数

| 参数名              | 类型    | 必填 | 说明                                        |
| ------------------- | ------- | ---- | ------------------------------------------- |
| csrfmiddlewaretoken | varchar | 是   | CSRF 参数、通过 /accounts/get_token/ 获取。 |
| username            | varchar | 是   | 用户名                                      |
| password            | varchar | 是   | 密码                                        |

### 返回数据

```
{
    "code": 1,
    "data": "admin",
    "msg": "用户已经登陆"
}
```

```
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

```
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

```
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

```
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

```
{
    "code": 1,
    "data": user_form_dict,
    "msg": "用户信息"
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

```
{
    "code": 1,
    "data": "密码修改成功, 请重新登陆",
    "msg": ''
}
```

