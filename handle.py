# -*- coding: utf-8 -*-
# filename: handle.py

import hashlib
import logging
import pymysql
from src.utils.conf_section import get_conf_section

config = {'host': get_conf_section("MYSQL", "HOST"),
          'port': int(get_conf_section("MYSQL", "PORT")),
          'user': get_conf_section("MYSQL", "USER"),
          'passwd': get_conf_section("MYSQL", "PASSWORD"),
          'db': get_conf_section("MYSQL", "DB")
          }
conn = pymysql.connect(**config)

import web

import receive
import reply


class Handle(object):
    def GET(self):
        try:
            data = web.input()
            if len(data) == 0:
                return "hello, this is handle view"
            signature = data.signature
            timestamp = data.timestamp
            nonce = data.nonce
            echostr = data.echostr
            token = get_conf_section("APP", "TOKEN")  # 请按照公众平台官网\基本配置中信息填写
            print("token:", token)

            list = [token, timestamp, nonce]
            list.sort()
            sha1 = hashlib.sha1()
            map(sha1.update, list)
            # hashcode = sha1.hexdigest()  # python2的写法
            sha1.update("".join(list).encode('utf-8'))  # python3 写法
            hashcode = sha1.hexdigest()
            print("handle/GET func: hashcode, signature: ", hashcode, signature)
            if hashcode == signature:
                return echostr
            else:
                return ""
        except Exception as Argument:
            return Argument

    def POST(self):
        try:
            webData = web.data()
            print("Handle Post webdata is ", webData)  # 后台打日志
            recMsg = receive.parse_xml(webData)
            if isinstance(recMsg, receive.Msg):
                toUser = recMsg.FromUserName
                fromUser = recMsg.ToUserName
                create_time = recMsg.CreateTime
                msg_type = recMsg.MsgType
                msg_id = recMsg.MsgId
                print(toUser, fromUser, create_time, msg_type, msg_id)

                cursor = conn.cursor()
                sql = f"insert tb_wechat_text(from_user_name,to_user_name,create_time,msg_type, msg_id) " \
                      f"values({toUser},{fromUser},{create_time},{msg_type},{msg_id})"
                # ret = cursor.execute(sql, (toUser, fromUser, create_time, msg_type, msg_id))
                ret = cursor.execute(sql)
                conn.commit()

                row = cursor.fetchone()
                print("sql:", sql)
                print("result:", ret)
                print("sql_row:", row)

                if recMsg.MsgType == 'text':
                    content = "test"
                    replyMsg = reply.TextMsg(toUser, fromUser, content)
                    return replyMsg.send()
                if recMsg.MsgType == 'image':
                    mediaId = recMsg.MediaId
                    replyMsg = reply.ImageMsg(toUser, fromUser, mediaId)
                    return replyMsg.send()
                else:
                    return reply.Msg().send()
            else:
                print("暂且不处理")
                return reply.Msg().send()
        except Exception as Argment:
            print(Argment)
            return Argment
