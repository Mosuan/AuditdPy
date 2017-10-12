# elkraa 部署文档
![][Python 2.7] ![][redis]
elkraa是什么
----
* elasticsearch
* logstash
* kibana
* redis
* auditd
* auditdPy

以上这些程序的首字母、简称，每次都打出全部的感觉好累，就这样简称吧。

### 均以 Ubuntu 为例

服务器要求
----
```
server    n台     简称为Auditd机器
elk+redis 一台    简称为elk机器
```

流程
----
![elkraa][1]

* 多台服务器部署Auditd + AuditdPy。
* elk机器部署ElasticSearch + Logstash + Kibana + Redis。

##### 流程：
1. Auditd 监控服务器的命令文件执行，并写入Log。
2. AuditdPy 从 Log 中提取数据 rpush 到Redis。
3. Redis 在框架中就是个队列的角色。
4. Logstash 监控 Redis 的 key，有数据则发送到 ElasticSearch。
5. 最后Kibana 读取 ElasticSearch 的数据展示到前端。


elk机器配置
----

##### redis设置密码

##### 修改 ElasticSearch 配置 `sudo vim /etc/elasticsearch/elasticsearch.yml`，搜索`network.host`，修改如下配置
```
network.host: localhost
```

##### 添加 Logstash 配置 `sudo vim /etc/logstash/conf.d/config.conf`
```
input {    
    redis {
        host => '127.0.0.1'
        password => 'Mosuan'
        data_type => 'list'
        key => 'logstash:redis'
    }
}
output {
    elasticsearch { hosts => localhost }
    stdout { codec => rubydebug }
}
```

##### 运行Logstash
```
sudo nohup /opt/logstash/bin/logstash -f /etc/logstash/conf.d/ &
```

##### 修改 Kibana 配置 `sudo vim /opt/kibana/config/kibana.yml`，搜索`server.host`，修改如下配置：
```
server.host: "0.0.0.0"
```

##### 以上修改配置之后均要重启一次服务。


Auditd机器配置
----

##### 安装auditd (centos 6.x自带)
```
sudo apt-get install auditd
```

##### auditPy
```
git clone https://github.com/Mosuan/AuditdPy
```

##### 查看并复制auditd 的规则
```
cat ./AuditdLogPy/docs/rule.txt
```

##### 将auditd规则粘贴覆盖到rules
```
sudo vim /etc/audit/audit.rules
```

##### 重启auditd
```
sudo /etc/init.d/auditd restart
```

##### 查看auditd 规则是否加载上
```
sudo auditctl -l
```
下面就是加载成功的样子：
![auditctl][2]

#### auditdPy 配置

##### Redis or Mail 配置：./lib/config.py 文件，redis的配置是必填的，邮箱那里可以选填，因为代码里面写的是默认不发送邮件的。
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

##### 命令白名单配置： ./main.py 文件 self.command_white 变量
```
# 支持正则，添加规则的时候必须指定以什么开头和什么结尾，不然误报漏报估计会很严重
# 例子：
self.command_white = [
            "^(sudo ausearch) -",
            "^grep [a-zA-Z1-9]{1,20}",
            "^ifconfig -a",
        ]
```

##### 发送邮件的开关：./main.py 文件 mail_status 变量
```
# False 为不发送邮件， True为发送邮件
mail_status = False
```

##### 运行程序
```
sudo python main.py start
```

##### 停止程序
```
sudo python main.py stop
```

##### 错误日志
```
cat /tmp/auditd_py_error.log
```

效果
----
![kibana][6]

参考
----
[Python Redis库文档][3]
[Logstash Redis 文档][4]
[Auditd 文档][5]



  [1]: http://static.secbox.cn/2017-10-12-elkeaa.jpg
  [2]: http://static.secbox.cn/2017-10-12-auditctl.jpg
  [Python 2.7]: https://img.shields.io/badge/python-2.7-brightgreen.svg
  [redis]: https://img.shields.io/badge/redis-4.0.1-red.svg
  [3]: http://redis-py.readthedocs.io/en/latest/
  [4]: https://kibana.logstash.es/content/logstash/scale/redis.html
  [5]: https://access.redhat.com/documentation/zh-cn/red_hat_enterprise_linux/7/html/security_guide/sec-understanding_audit_log_files
  [6]: http://static.secbox.cn/2017-10-12-46C02DDF193BBDD707ADFA88AC0805AC.jpg
