create database my_apis;

use my_apis;

create table users
(
    id          int unsigned primary key auto_increment,
    phone       varchar(32)                                 not null comment '手机号码',
    country     smallint unsigned default 86                not null comment '国家号（中国86）',
    username    varchar(32)                                 not null comment '用户姓名',
    password    varchar(64)                                 not null comment '密码',
    is_root     tinyint unsigned  default 0                 not null comment '是否是超管',
    status      tinyint unsigned  default 1                 not null comment '状态',
    json_extent json                                        null comment 'json拓展',
    create_at   datetime          default CURRENT_TIMESTAMP not null comment '创建时间',
    modified_at datetime          default CURRENT_TIMESTAMP not null on update CURRENT_TIMESTAMP comment '更新时间',
    index `username` (username),
    unique index phone (phone),
    index create_at (create_at)
) comment '用户表';

create table inter_users
(
    id          int unsigned primary key auto_increment,
    user_id     int unsigned                               not null comment '用户ID',
    status      tinyint unsigned default 1                 not null comment '状态',
    json_extent json                                       null comment 'json拓展',
    create_at   datetime         default CURRENT_TIMESTAMP not null comment '创建时间',
    modified_at datetime         default CURRENT_TIMESTAMP not null on update CURRENT_TIMESTAMP comment '更新时间',
    index user_id (user_id),
    index create_at (create_at)
) comment '内部用户表';

create table secret_keys
(
    id          int unsigned primary key auto_increment,
    user_id     int unsigned                       not null comment '用户ID',
    secret_key  varchar(32)                        not null comment '密钥',
    create_at   datetime default CURRENT_TIMESTAMP not null comment '创建时间',
    modified_at datetime default CURRENT_TIMESTAMP not null on update CURRENT_TIMESTAMP comment '更新时间',
    index user_id (user_id),
    unique index secret_key (secret_key),
    index create_at (create_at)
) comment '密钥表';

create table configs
(
    id          int unsigned primary key auto_increment,
    `key`       varchar(64),
    version     smallint unsigned                          not null comment '版本',
    config      json                                       not null comment '配置',
    status      tinyint unsigned default 1                 not null comment '状态',
    create_at   datetime         default CURRENT_TIMESTAMP not null comment '创建时间',
    modified_at datetime         default CURRENT_TIMESTAMP not null on update CURRENT_TIMESTAMP comment '更新时间',
    unique index key_version (`key`, version),
    index create_at (create_at)
) comment '配置表';

create table sensitive_logs
(
    id        int unsigned primary key auto_increment,
    user_id   int unsigned                       not null comment '用户ID',
    ip        varchar(15)                        not null comment '用户IP',
    ua        varchar(512)                       not null comment '客户端user-agent',
    url       varchar(256)                       not null comment '访问的url',
    method    varchar(16)                        not null comment '请求的方法',
    behavior  json                               not null comment '行为',
    create_at datetime default CURRENT_TIMESTAMP not null comment '创建时间',
    index user_id (user_id),
    index ip (ip),
    index create_at (create_at)
) comment '敏感日志';
