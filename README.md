# Class-Note-Manager-Python
Class Note Manager Server, built with Python.

## 部署方法

项目前端代码已经预先打包，不需要再进行配置。以下是部署后端的步骤。
1.	安装Python 3最新版本；
2.	将代码解压并放在合适位置；
3.	使用如下命令，利用pip3安装Flask；
```
pip3 install –-user flask
```
4.	在电脑上安装PostgreSQL，并建立一个数据库；
5.	在数据库控制台执行项目根目录下database.sql文件内容，完成建表；
6.	修改项目根目录下的serverConfig.conf文件内容，各项解释如下
    -	[Server]部分
        -	ListenPort：服务器监听哪一个端口，默认是2333；
    -	[Database]部分
        -	Name：数据库的名字；
        -	Address：连接数据库使用的IP地址；
        -	Port：连接数据库使用的端口号；
        -	Username：连接数据库使用的用户名；
        -	Password：连接数据库使用的密码；
    -	[File]部分
        -	NoteFilePosition：设定提交的笔记文件存放的文件夹，默认是项目文件夹下的Note文件夹下。
7.	以上都配置完成后，使用Python 3解释器运行main.py；
8.	如main.py顺利运行，打开浏览器输入http://localhost:2333即可访问系统，如果后端没有部署在本机，根据服务器的具体情况输入对应的URL；
9.	如果运行失败，请根据错误信息检查配置文件是否正确填写。
