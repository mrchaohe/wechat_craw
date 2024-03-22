import os
import json
import logging
from time import sleep, localtime, time, strftime

from bs4 import BeautifulSoup
import requests


from .log import log 

class Wechat(object):
    def __init__(self):
        self.headers = {
            'Host': 'mp.weixin.qq.com',
            'User-Agent': r'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
        }
        self.initpath = os.getcwd()

    def login(self, username, passwd):
        with open(self.initpath+"\cookie.json", 'r+') as fp:
                cookieToken_dict = json.load(fp)
                # cookies = cookieToken_dict['COOKIES']
                # token = cookieToken_dict['TOKEN']
                cookies = cookieToken_dict[0]['COOKIES']
                token = cookieToken_dict[0]['TOKEN']
        log.debug("token: {}, cookie: {}".format(token, cookies))

        try:
            html = self.sess.get(r'https://mp.weixin.qq.com/cgi-bin/home?t=home/index&lang=zh_CN&token=%s' % token, timeout=(30, 60), headers={"Cookie":cookies})
        except Exception as e:
            log.debug("无cookie.json或失效 - %s" %e)
            
    
        if "登陆" not in html.text:
            log.debug("cookie有效,无需浏览器登陆")
            return token, cookies
        
        # todo selenium 登录获取
        return "", ""
    
    def Process(self):
        try:
            query_name = "男孩派"                                     # 公众号的英文名称
            self.time_gap = 10                                       # 每页爬取等待时间
            self.start = "20240101"                                  # 起始时间
            self.end = "20240301"                                    # 结束时间
            self.key_word = ""                                       # 关键词
 
            token, cookies = self.login("", "")
            # self.Add_Cookies(cookies)
            if self.keyword_search_mode == 1:
                self.keyWord_2 = self.lineEdit_keyword_2.text()  # 关键词
                self.KeyWord_Search(token, self.keyWord_2)
            else:
                [fakeid, nickname] = self.Get_WeChat_Subscription(token, query_name)
                if self.isresume == 0:
                    Index_Cnt = 0
                    while True:
                        try:
                            self.rootpath = os.path.join(os.getcwd(), "spider-%d" % Index_Cnt, nickname) #+ r"/spider-%d/" % Index_Cnt + nickname  # !!!!!!!!!!!!!!
                            os.makedirs(self.rootpath)
                            self.conf.set("resume", "rootpath", self.rootpath)
                            self.conf.write(open(self.cfgpath, "r+", encoding="utf-8"))
                            break
                        except:
                            Index_Cnt = Index_Cnt + 1
                self.Get_Articles(token, fakeid)
        except Exception as e:
            self.Label_Debug("!!![%s]" % str(e))
            log.debug("!!![%s]" % str(e))
            if "list" in str(e):
                self.Label_Debug("请删除cookie.json")
                log.debug("请删除cookie.json")
    

def main():
    pass