## 创建user数据库

1.新建数据库：hmsc_db

```
create database 'hmsc_db' default character set = 'utf8'
```

2.新建user表

```mysql
create table 'user'(
	'uid' bigint(20) not null auto_increment comment '用户id',
	'nickname' varchar(100) not null default '' comment '用户昵称',
	'mobile' varchar(20) not null default '' comment '手机号码',
	'email' varchar(20) not null default '' comment '邮箱地址',
	'sex' tinyint(1) not null default '0' comment '1:男 2:女 0:空白',
	'avatar' varchar(64) not null default '' comment '头像',
	'login_name' varchar(20) not null default '' comment '登录用户名',
	'login_pwd' varchar(32) not null default '' comment '登录密码',
	'login_salt' varchar(32) not null default '' comment '登录密码的随机秘钥',
	'status' tinyint(1) not null default '1' comment '1:有效 0:无效',
	'updated_time' timestamp not null default current_timestamp comment '最后后一次更新时间',
	'created_time' timestamp not null default current_timestamp comment '创建时间',
	primary key ('uid'),
	unique key 'login_name' ('login_name')
)ENGINE=InnoDB default charset=utf8 comment='用户表(管理员)';


insert into 'user' ('uid','nickname','mobile','email','sex','avatar','login_name','login_pwd','login_salt','status','updated_time','created_time') values(1,'Dws','18295956300','695036039@qq.com',1,'','dws888','816440c40b7a9d55ff9eb7b20760862c','cF3JfH5FJfQ8B2Ba',1,'2020-04-23 11:30:59','2020-4-23 11:11:11');
```



3.使用flask-sqlacodegen 反向生成ORM

安装  pip install flask-sqlacodegen

安装mysqlclient(pymysql): pip install mysqlclient

安装flask-sqlalchemy

```python
flask-sqlacodegen 'mysql://root:123456@127.0.0.1/hmsc_db' --tables user --outfile 'common/models/user.py' --flask

flask-sqlacodegen 'mysql://root:123456@127.0.0.1/hmsc_db' --outfile 'common/models/model.py' --flask
```

## 六、配置文件统一管理

1.从配置文件中加载配置

```python
Application类中
self.config.from_pyfile('config/base_setting.py')
```

## 七、结合MD5算法生成密码

common/libs/user/UserService.py

```python
class UserService():

    # 结合salt和md5生成新的密码 
    @staticmethod
    def generatePwd(pwd,salt):
        m = hashlib.md5()
        str = '%s-%s'%(base64.encodebytes(pwd.encode('utf-8')),salt)
        m.update(str.encode('utf-8'))
        return m.hexdigest()

    # 对Cookie中存储的信息进行加密
    @staticmethod
    def generateAuthCode(user_info = None):
        m = hashlib.md5()
        str = "%s-%s-%s-%s"%(user_info.uid,user_info.login_name,user_info.login_pwd,user_info.login_salt)
        m.update(str.encode("utf-8"))
        return m.hexdigest()

    # 生成16位的字符串，包含字母和数字
    # string.ascii_letters 大小写字母
    # string.digits 0-9 数字
    @staticmethod
    def  generateSalt(length=16):
        keyList = [random.choice(( string.ascii_letters + string.digits )) for i in range(length)]

        return (''.join(keyList))
```

## 八，状态管理，将登陆状态记录到cookie中

自行补充session的状态管理

引入make_response库：from flask import make_response

对Cookie中存储的信息进行加密

```python
    # 对Cookie中存储的信息进行加密
    @staticmethod
    def generateAuthCode(user_info = None):
        m = hashlib.md5()
        str = '%s-%s-%s-%s'%(user_info.uid,user_info.login_name,user_info.pwd,user_info.login_salt)
        m.update(str.encode('utf-8'))

        return m.hexdigest()
```

## 九、flask的g对象

专门用来存储用户信息的g对象，全称叫做global，g对象在一次请求中的所有的代码地方，都可以使用。

g和session的区别？（面试题）

## 十一，网站首页数据库结构

全站日统计

```mysql
use hmsc_db;

drop table if exists `stat_daily_site`;

create table `stat_daily_site`(
	`id` int(11) unsigned not null auto_increment,
	`data` data not null comment '日期',
	`total_pay_money` decimal(10,2) not null default '0.00' comment '当日收入总额',
	`total_member_count` int(11) not null comment '当日会员总数',
	`total_new_member_count` int(11) not null comment '当日新增会员总数',
	`total_order_count` int(11) not null comment '当日订单数',
	`total_shared_count` int(11) not null comment '分享总数',
	`updated_time` timestamp not null default current_timestamp comment '最近更新时间',
	`created_time` timestamp not null default current_timestamp comment '插入时间',
	primary key (`id`),
	key `idx_data` (`date`)
)engine=InnoDB default charset=utf8 comment='全站日统计';
```

```mysql
flask-sqlacodegen 'mysql://root:123456@127.0.0.1/hmsc_db' --tables stat_daily_site --outfile 'common/models/stat/StatDailySite.py' --flask
```

## 十二、account模块

1.路由网址中：request.args.get('id')

2.搜索要引入：from sqlalchemy import or_

3.分页：

​	关键字：当前页（page），每页显示多少（page_size），一共多少页（pages）

## 十三，member会员管理

1.数据库

```mysql
use hmsc_db;

drop table if exists `member`;


create table `member` (
	`id` int(11) unsigned not null auto_increment,
	`nickname` varchar(100) not null default '' comment '会员昵称',
	`mobile` varchar(20) not null default '' comment '会员手机号码',
	`sex` tinyint(1) not null default '0' comment '1:男 2:女 0:没有填写',
	`avatar` varchar(200) not null default '' comment '会员头像',
	`salt` varchar(32) not null default '' comment '登录密码的随机密钥',
	`reg_ip` varchar(100) not null default '' comment '注册ip',
	`status` tinyint(1) not null default '1' comment '1:有效 0:无效',
	`updated_time` timestamp not null default current_timestamp comment '最后一次更新时间',
	`created_time` timestamp not null default current_timestamp comment '创建时间',
	primary key (`id`)
)ENGINE=InnoDB default charset=utf8 comment='会员表';
```

```mysql
flask-sqlacodegen 'mysql://root:123456@127.0.0.1/hmsc_db' --tables member --outfile 'common/models/member/Member.py' --flask
```

```mysql
insert into `member` (`id`,`nickname`,`mobile`,`sex`,`avatar`,`salt`,`reg_ip`,`status`,`updated_time`,`created_time`) values(1,'二郎神','18295956300',1,'','cF3JfH5FJfQ8B2Ba','111.111.111',1,'2020-04-23 11:30:59','2020-4-23 11:11:11');
```







## 十四，商品管理 goods

1.数据库

```mysql
use hmsc_db;

drop table if exists `goods`;


create table `goods` (
    `id` int(11) unsigned not null auto_increment,
    `cat_id` int(11) not null default '0' comment '分类id',
    `name` varchar(100) not null default '' comment '商品名称',
    `price` decimal(10,2) not null default '0.00' comment '商品价格',
    `main_image` varchar(100) not null default '' comment '商品主图',
    `summary` varchar(10000) not null default '' comment '商品描述',
    `stock` int(11) not null default '0' comment '库存数',
    `tags` varchar(200) not null default '' comment 'tag 标签，用“,”连接',
    `status` tinyint(1) not null default '1' comment '1:有效，0：无效',
    `month_count` int(11) not null default '0' comment '月销量',
    `total_count` int(11) not null default '0' comment '总销量',
    `view_count` int(11) not null default '0' comment '总浏览次数',
    `comment_count` int(11) not null default '0' comment '总评论数',
    `updated_time` timestamp not null default current_timestamp comment '最后一次更新时间',
	`created_time` timestamp not null default current_timestamp comment '创建时间',
	primary key (`id`)
)ENGINE=InnoDB default charset=utf8 comment='商品表';
```

```mysql
flask-sqlacodegen 'mysql://root:123456@127.0.0.1/hmsc_db' --tables goods --outfile 'common/models/goods/Goods.py' --flask
```



## 十五：会员评论数据库

```mysql
use hmsc_db;

drop table if exists `member_comments`;
create table `member_comments`(
	`id` int(11) unsigned not null auto_increment,
	`member_id` int(11) not null default '0' comment '会员id',
	`goods_id` varchar(200) not null default '' comment '商品id',
	`pay_order_id` int(11) not null default '0' comment '订单id',
	`score` tinyint(4) not null default '0' comment '评分',
	`content` varchar(200) not null default '' comment '评论内容',
	`created_time` timestamp not null default current_timestamp on update current_timestamp comment '创建时间',
	primary key (`id`),
	key `idx_member_id` (`member_id`)
)ENGINE=InnoDB default charset=utf8 comment='会员评论表';
```

```mysql
flask-sqlacodegen 'mysql://root:123456@127.0.0.1/hmsc_db' --tables member_comments --outfile "common/models/member/MemberComment.py" --flask
```

```mysql
insert into `member_comments` (`id`,`member_id`,`goods_id`,`pay_order_id`,`score`,`content`,`created_time`) values (1,1,'1',1,'10','好，good','2020-04-29 11:10:30');
```

## 集成UEditor和HighCharts

**一、UEditor**

1.官网：`http://ueditor.baidu.com//website`文档

2.在flask项目中集成UEditor:`https://segmentfault.com/a/1190000002429055/`

3.上传图片：

上传图片后，图片在服务器上的地址：/web/static/upload/20200430/avatar.jpg

图片在前端img标签中的src中的地址

4.服务器图片加密存储UUID16进制32位的一串字符串，基于随机数

```python
import uuid
```



















