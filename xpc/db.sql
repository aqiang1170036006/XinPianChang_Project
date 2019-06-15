CREATE DATABASE `xpc_1901`;
USE `xpc_1901`;

CREATE TABLE `posts` (
  `pid` bigint(20) unsigned NOT NULL DEFAULT '0' COMMENT '作品表主键',
  `title` varchar(256) NOT NULL COMMENT '作品标题',
  `banner` varchar(512) DEFAULT NULL COMMENT '视频预览图',
  `video` varchar(512) DEFAULT NULL COMMENT '视频链接',
  `category` varchar(512) NOT NULL DEFAULT '' COMMENT '作品分类',
  `created_at` varchar(128) NOT NULL DEFAULT '' COMMENT '发表时间',
  `description` text COMMENT '作品描述',
  `play_counts` int(8) NOT NULL DEFAULT '0' COMMENT '播放次数',
  `like_counts` int(8) NOT NULL DEFAULT '0' COMMENT '被点赞次数',
  `thumbnail` varchar(512) DEFAULT NULL COMMENT '视频缩略图',
  `duration` int(8) NOT NULL DEFAULT '0' COMMENT '播放时长',
  `vid` varchar(16) DEFAULT NULL,
  PRIMARY KEY (`pid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='作品表';


CREATE TABLE `comments` (
  `id` int(11) NOT NULL COMMENT '评论表主键',
  `pid` bigint(20) unsigned NOT NULL DEFAULT '0' COMMENT '评论的作品ID',
  `cid` bigint(20) unsigned NOT NULL DEFAULT '0' COMMENT '评论人ID',
  `avatar` varchar(512) DEFAULT NULL COMMENT '评论人头像',
  `uname` varchar(512) DEFAULT NULL COMMENT '评论人名称',
  `created_at` varchar(128) NOT NULL DEFAULT '' COMMENT '发表时间',
  `content` text COMMENT '评论内容',
  `like_counts` int(8) NOT NULL DEFAULT '0' COMMENT '被点赞次数',
  `referid` int(8) NOT NULL DEFAULT '0' COMMENT '回复其他评论的ID，如果不是则为0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='评论表';

CREATE TABLE `composers` (
  `cid` bigint(20) unsigned NOT NULL DEFAULT '0' COMMENT '创作者表主键',
  `banner` varchar(512) NOT NULL COMMENT '用户主页banner图片',
  `avatar` varchar(512) NOT NULL DEFAULT '' COMMENT '用户头像',
  `verified` varchar(128) DEFAULT '' COMMENT '是否加V',
  `name` varchar(128) NOT NULL COMMENT '名字',
  `intro` text COMMENT '自我介绍',
  `like_counts` int(8) NOT NULL DEFAULT '0' COMMENT '被点赞次数',
  `fans_counts` int(8) NOT NULL DEFAULT '0' COMMENT '被关注数量',
  `follow_counts` int(8) NOT NULL DEFAULT '0' COMMENT '关注数量',
  `location` varchar(32) DEFAULT NULL COMMENT '所在地点',
  `career` varchar(32) DEFAULT NULL COMMENT '职业',
  PRIMARY KEY (`cid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='用户表';

CREATE TABLE `copyrights` (
  `pcid` varchar(32) NOT NULL COMMENT '主键，由pid_cid组成',
  `pid` bigint(20) unsigned NOT NULL DEFAULT '0' COMMENT '对应作品表主键',
  `cid` bigint(20) unsigned NOT NULL DEFAULT '0' COMMENT '对应作者表主键',
  `roles` varchar(32) NOT NULL DEFAULT '' COMMENT '担任角色',
  PRIMARY KEY (`pcid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='著作权关系表';


insert into `comments`
(`id`,`content`,`created_at`,`pid`,`cid`,`avatar`,`uname`,`like_counts`,`referid`)
values
('313474','\');drop database xpc_1901;\'','1559731661','10445920','10790847',
'https://cs.xinpianchang.com/user_center_xpc_line/user_avatar_10790847.jpg',
'Alex','1','0');


Good
');drop database xpc_1901;'


insert into `comments`
(`id`,`content`,`created_at`,`pid`,`cid`,`avatar`,`uname`,`like_counts`,`referid`)
values
(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);