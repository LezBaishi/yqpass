# 园区传输资源管理及调度系统
## 安装

### 安装依赖项

相关依赖项如 requirements.txt 文件所示，可通过指令快速安装：

```
(venv) $ pip install -r requirements.txt
```

### 数据库配置

- 安装 Mysql 数据库并创建项目所需数据库。

```
$ mysql -uroot -p
输入密码后命令如下
mysql> create database yuanqu default charset=utf8;
mysql> flush privileges;
```

- 安装 Redis

可参考：http://www.cnblogs.com/guanfuchang/p/6561126.html

- 修改 /yuanqu2/settings.py 数据库配置，根据本机配置按需修改。

```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'yuanqu',  # 部署到服务器数据库名称要改
        'USER': 'root',  # 部署到服务器用户名要改
        'PASSWORD': '123456',  # 部署到服务器密码要改
        'HOST': 'localhost',  # 部署到服务器要改为127.0.0.1
        'PORT': '3306',
    }
}
```

- 迁移数据库

```
$ python manage.py makemigrations
$ python manage.py migrate
```

### 创建管理员账号、收集静态文件

```
$ python manage.py createsuperuser
$ python manage.py collectstatic
```

### 启动开发环境

```
$ python manage.py runserver
```

### 启动 Celery 任务

```
$ celery -A yuanqu2 worker -l info -P eventlet -Q celery,yqpass
```



## 文档

该项目相关文档见目录 /docs 所示。

