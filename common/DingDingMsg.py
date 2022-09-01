import json
import hashlib
import base64
import hmac
import os
import time
import requests
from common.LoggerTools import log
from urllib.parse import quote_plus
import common.ParamUtil as ParamUtil


class Messenger:
    def __init__(self, token=os.getenv("DD_ACCESS_TOKEN"), secret=os.getenv("DD_SECRET")):
        self.timestamp = str(round(time.time() * 1000))
        self.URL = "https://oapi.dingtalk.com/robot/send"
        self.headers = {'Content-Type': 'application/json'}
        secret = secret
        secret_enc = secret.encode('utf-8')
        string_to_sign = '{}\n{}'.format(self.timestamp, secret)
        string_to_sign_enc = string_to_sign.encode('utf-8')
        hmac_code = hmac.new(secret_enc, string_to_sign_enc, digestmod=hashlib.sha256).digest()
        self.sign = quote_plus(base64.b64encode(hmac_code))
        self.params = {'access_token': token, "sign": self.sign}

    def send_text(self, content):
        """
        发送文本
        @param content: str, 文本内容
        """
        data = {"msgtype": "text", "text": {"content": content}}
        self.params["timestamp"] = self.timestamp
        return requests.post(
            url=self.URL,
            data=json.dumps(data),
            params=self.params,
            headers=self.headers
        )

    def send_md(self, title, content):
        """
        发送Markdown文本
        @param title: str, 标题
        @param content: str, 文本内容
        """
        data = {"msgtype": "markdown", "markdown": {"title": title, "text": content}}
        self.params["timestamp"] = self.timestamp
        return requests.post(
            url=self.URL,
            data=json.dumps(data),
            params=self.params,
            headers=self.headers
        )

def DD2MSG(context):
    """
    发送DingDing消息
    @param context: str, 消息内容
    """

    # 下注释为发送markdown文件实例
    # markdown_text = "\n".join(open("md_test.md", encoding="utf-8").readlines())
    token = str(ParamUtil.ETL_DD_TOKEN.split("=")[1])
    secret = ParamUtil.ETL_DD_SECRET
    m = Messenger(
        token=token,
        secret=secret
    )
    try:
        m.send_text(context)
        log.info("信息发送钉钉成功！")
    except Exception as e:
        log.info("信息发送钉钉失败！")
        print(e)
    # m.send_md("测试Markdown", markdown_text)