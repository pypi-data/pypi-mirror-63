import requests
import json
import logging
from time import sleep
import random
import threading
from collections import Counter

REQUEST_SUCCESS = 0
REQUEST_TOO_QUICK = 1
REQUEST_REACH_MAX = 2


class IpPool(object):
    def __init__(self, api_url, max_count=5):
        self.api_url = api_url
        self.ip_pool = set()
        self.ip_pool_back_up = set()
        self.bad_net_ip_count = list()
        logging.basicConfig()
        self.cond = threading.Condition()
        self.lock = threading.Lock()
        self.max_count = max_count
        self.sess = requests.Session()  # 构建 connections pool
        adapter = requests.adapters.HTTPAdapter(pool_connections=20, pool_maxsize=20)
        self.sess.mount("https://", adapter)
        self.sess.mount("http://", adapter)

    def start(self):
        self._update_ip()

    def _request_ip(self):
        res = self.sess.get(self.api_url).content.decode()  # 请求ip
        res = json.loads(res)  # 解析成字典
        if res['ERRORCODE'] == "0":
            with self.cond:
                logging.info("请求新的代理IP")
                ip_port_list = res['RESULT']
                self.ip_pool = set([f"{ll['ip']}:{ll['port']}" for ll in ip_port_list])
                self.cond.notify_all()
                logging.info("完成请求")
                return REQUEST_SUCCESS
        elif res['ERRORCODE'] in ["10036", "10038", "10055"]:
            logging.info("提取频率过高")
            return REQUEST_TOO_QUICK
        elif res["ERRORCODE"] == "10032":
            logging.info("已达上限!!")
            return REQUEST_REACH_MAX

    def _has_ip(self):
        return len(self.ip_pool) != 0

    def get_ip(self):
        """
        从池中拿去一个IP,如果当前没有IP就wait，直到新的IP已经产生
        :return:
        """
        with self.cond:
            self.cond.wait_for(self._has_ip)
            return random.choice(list(self.ip_pool))

    def report_baned_ip(self, ip):
        """
        报告已经被ban掉的IP，针对被ban掉的IP采取措施，
        1.直接将ip从池中删除，
        2.判断当前Ip池是否为空，如果为空，就加锁并开始请求新的IP，
        :param ip:
        :return:
        """
        logging.debug(f"remove {ip} from pool!")
        self.ip_pool_back_up.add(ip)
        self.ip_pool.discard(ip)
        logging.debug(f"now the pool is {self.ip_pool}")
        if len(self.ip_pool) == 0 and self.lock.acquire(blocking=False) and ip in self.ip_pool_back_up:
            self._update_ip()
            self.ip_pool_back_up.clear()
            self.bad_net_ip_count.clear()
            self.lock.release()

    def _update_ip(self):
        res = self._request_ip()
        while res != REQUEST_SUCCESS:
            if res == REQUEST_TOO_QUICK:
                sleep(10)
                res = self._request_ip()
                continue
            if res == REQUEST_REACH_MAX:
                raise ReachMaxException()

    def report_bad_net_ip(self, ip):
        """
        报告网络不好的ip，并对这些ip采取措施
        1.将报告的IP加入到队列中
        2.对队列中的IP进行统计，当某一个ip的被报告次数达到10次时，就将其从当前池中删除，
        3.如果当前池中没有IP了，就执行更新IP的操作
        :param ip:
        :return:
        """
        if ip not in self.ip_pool:
            return
        logging.debug(f"bad net ip {ip}")
        self.bad_net_ip_count.append(ip)  # 将其加入到集合中
        count_list = Counter(self.bad_net_ip_count)
        most_common_item = count_list.most_common(1)[0]
        logging.debug(f"the baddest net ip is {most_common_item}")
        if most_common_item[1] == self.max_count:
            self.bad_net_ip_count = [ip for ip in self.bad_net_ip_count if ip != most_common_item[0]]
            self.report_baned_ip(most_common_item[0])


class ReachMaxException(Exception):
    def __init__(self):
        pass
