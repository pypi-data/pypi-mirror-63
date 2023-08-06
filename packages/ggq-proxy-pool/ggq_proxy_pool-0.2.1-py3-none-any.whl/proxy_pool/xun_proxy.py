import json
import logging
import random
from time import sleep

import requests
from proxy_pool.ip_pool import ReachMaxException

from proxy_pool import IpPool

REQUEST_SUCCESS = 0
REQUEST_TOO_QUICK = 1
REQUEST_REACH_MAX = 2


class XunProxy(IpPool):
    def __init__(self, api_url, max_count=5):
        super().__init__(api_url, max_count)

    def start(self):
        self._update_ip()

    def _request_ip(self):
        res = self.sess.get(self.api_url).content.decode()  # 请求ip
        res = json.loads(res)  # 解析成字典
        if res['ERRORCODE'] == "0":
            with self.cond:
                logging.debug("请求新的代理IP")
                ip_port_list = res['RESULT']
                self.ip_pool = set([f"{ll['ip']}:{ll['port']}" for ll in ip_port_list])
                self.cond.notify_all()
                logging.debug("完成请求")
                return REQUEST_SUCCESS
        elif res['ERRORCODE'] in ["10036", "10038", "10055"]:
            logging.info("提取频率过高")
            return REQUEST_TOO_QUICK
        elif res["ERRORCODE"] == "10032":
            logging.info("已达上限!!")
            return REQUEST_REACH_MAX
