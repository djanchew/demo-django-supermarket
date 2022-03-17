# demo-django-supermarket
毕业设计 (2019)


## 环境配置 (Ubuntu 18.04)
- Ubuntu 18.04
- python3.7 [升级3.7](https://jcutrer.com/linux/upgrade-python37-ubuntu1810)

### 数据库 (mysqlclient)
1. 系统需要装好 default-libmysqlclient-dev

```bash
> sudo apt-get install default-libmysqlclient-dev python3.7 python3.7-dev
```

2. pip 升级  

> 参考  
https://stackoverflow.com/a/64095095  
```bash
> pip3 install -U pip
> pip3 install -U setuptools
```
3. pip3 install mysqlclient
4. 本机安装好 mysql 服务并启动 sudo /etc/init.d/mysql start
5. 使用/创建用户 admin, 使用创建数据库 demo_django_supermarket (root权限下)
    - 创建数据库 
    ```mysql
    mysql> CREATE DATABASE demo_django_supermarket DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
    ```
    - 检查数据库默认编码
    ```mysql
    mysql> USE demo_django_supermarket;
    mysql> SELECT @@character_set_database, @@collation_database;
    +--------------------------+----------------------+
    | @@character_set_database | @@collation_database |
    +--------------------------+----------------------+
    | utf8mb4                  | utf8mb4_unicode_ci   |
    +--------------------------+----------------------+
    1 row in set (0.00 sec)

    mysql> SHOW TABLE STATUS FROM demo_django_supermarket;
   (略)
    ```
    - 创建数据库连接用户并授权
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
2. 设置一个超级管理员 admin (admin@123456)
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
> 若启动以 0.0.0.0:8001 还能在局域网内的其他设备访问

## TODO
- [ ] 使用 docker 来启动 mysql 和本服务 
- [x] ~~fixture~~/migrate 增加初始化商品数据的  
- [x] migrate 增加模拟销售数据 
- [ ] 接口文档 wiki
- [ ] 测试开发环境配置(换一个机器重新开发) 
- [ ] 测试用例