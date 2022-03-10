# demo-django-supermarket
毕业设计 (2019)


## 环境配置 (Ubuntu 18.04)

### 数据库 (mysqlclient)
1. 系统需要装好 default-libmysqlclient-dev
2. pip 升级  

> 参考  
https://stackoverflow.com/a/64095095  
https://stackoverflow.com/a/64095095
```bash
> pip3 install -U pip
> pip3 install -U setuptools
```
3. pip3 install mysqlclient
4. 本机安装好 mysql 服务并启动 sudo /etc/init.d/mysql start
5. 使用/创建用户 admin, 使用创建数据库 demo_django_supermarket (root权限下)
```mysql
mysql> CREATE USER 'admin'@'localhost' IDENTIFIED BY '123456';
mysql> GRANT ALL PRIVILEGES ON demo_django_supermarket.* TO 'admin'@'localhost';
```

### 初始化数据
1. migrate 迁移/初始化数据库
```bash
> python3 manage.py makemigrations
> python3 manage.py migrate
```
2. 设置一个超级管理员 admin (root@123456)
> 参考
https://docs.djangoproject.com/en/4.0/howto/initial-data/
```bash
> python3 manage.py loaddata fixtures/*
```

## 开始

1. 启动服务
```bash
> python3 manage.py runserver localhost:8001
```

## TODO
- [ ] 使用 docker 来启动 mysql 和本服务 
- [ ] 增加初始化商品数据的 fixture 
- [ ] 接口文档 wiki
- [ ] 测试开发环境配置(换一个机器重新开发) 
- [ ] 测试用例