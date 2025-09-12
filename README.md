本地运行：python3 loginkey.py

本期：
■查看
https://127.0.0.1:8080/loginkey?keyname=test

■日志
https://127.0.0.1:8080/loginkey?action=log&keyname=test

■支持的命令
https://127.0.0.1:8080/loginkey?action=commands

■查看login URL
https://127.0.0.1:8080/loginurl

■添加login URL
https://127.0.0.1:8080/loginurl?action=create

■删除login URL
https://127.0.0.1:8080/loginurl?action=delete&id=login URL's id

上期：
■查看
https://127.0.0.1:8080/loginkey

■添加
https://127.0.0.1:8080/loginkey?action=create&keyname=test&keyvalue=key

■修改
https://127.0.0.1:8080/loginkey?action=save&keyname=test&keyvalue=newkey

■删除
https://127.0.0.1:8080/loginkey?action=delete&keyname=test
