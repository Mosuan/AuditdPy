# AuditdPy

![][Python 2.7]

> Linux服务器命令监控辅助脚本，ElasticSearch + Logstash + Kibana + Redis + Auditd（简称elkra吧,hhh），该程序在elkra做就是把Auditd的日志读取出来，然后发送到Redis。

> 之所以写这个是因为部署方便 / 减少消耗不必要的资源，每台Server都部署Logstash的话很消耗资源。我个人的代码水平、正则水平比较菜，代码水平强的人可以优化下代码和正则。

elkraa部署文档
----
[elkraa部署文档][2]

目录结构
----
```
├── README.md
├── docs
│   └── rule.txt      auditd规则
├── lib
│   ├── RedisAdd.py   redis操作
│   ├── __init__.py
│   ├── config.py     配置文件
│   ├── daemon.py     守护进程
│   ├── log.py        debug log
│   ├── mail.py       send mail
│   └── redis         python redis package
└── main.py           入口文件
```

配置
----
#### Redis or Mail 配置：./lib/config.py 文件，redis的配置是必填的，邮箱那里可以选填，因为代码里面写的是默认不发送邮件的。
```
#-*- coding:utf-8 -*-

# redis config
# redis地址
redis_host = 'localhost'
# redis密码
redis_pass = 'Mosuan'
# redis db(可选，默认就ok)
redis_db = 0
# redis端口
redis_port = 6379
# redis key, 可以说是频道名吧
redis_key = 'logstash:redis'

# mail config
# 邮箱服务器地址
mail_host = 'smtp.126.com'
# 邮箱服务器端口
mail_port = 25
# 邮箱
mail_user = 'mosuan_6c6c6c@126.com'
# 邮箱密码
mail_pass = 'xxxxxxxxx'
# 发送给谁
mail_receivers = 'mosuansb@gmail.com'
# 邮件标题
mail_title = 'Auditd Error Message'
```

#### 命令白名单配置： ./main.py 文件 self.command_white 变量
```
# 支持正则，添加规则的时候必须指定以什么开头和什么结尾，不然误报漏报估计会很严重
# 例子：
self.command_white = [
            "^(sudo ausearch) -",
            "^grep [a-zA-Z1-9]{1,20}",
            "^ifconfig -a",
        ]
```

#### 发送邮件的开关：./main.py 文件 mail_status 变量
```
# False 为不发送邮件， True为发送邮件
mail_status = False
```

运行程序
----
#### 运行程序
```
sudo python main.py start
```

#### 停止程序
```
sudo python main.py stop
```


[Python 2.7]: https://img.shields.io/badge/python-2.7-brightgreen.svg
[2]: https://github.com/Mosuan/AuditdPy/blob/master/docs/elkraa.md
