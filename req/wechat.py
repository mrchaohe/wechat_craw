import requests

class Wechat(object):
    def __init__(self):
        self.sess = requests.Session()
        self.headers = {
            "Cookie": "",
            'Host': 'mp.weixin.qq.com',
            'User-Agent': r'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
        }
        self.keyword_search_mode = 0

    def get_fakeid(self, token, cookie, query):
        # 获取公众号对应的信息。查询会匹配多个，返回第一个
        try:
            url = r'https://mp.weixin.qq.com/cgi-bin/searchbiz?action=search_biz&token={0}&lang=zh_CN&f=json&ajax=1&random=0.5182749224035845&query={1}&begin=0&count=5'.format(
                token, query)
            self.headers["Cookie"] = cookie
            html_json = self.sess.get(url, headers=self.headers, timeout=(30, 60)).json()
            fakeid = html_json['list'][0]['fakeid']
            nickname = html_json['list'][0]['nickname']
        except Exception as e:
            fakeid = ""
        return fakeid


    # def login(self, username, passwd):
    #     with open(self.initpath+"\cookie.json", 'r+') as fp:
    #             cookieToken_dict = json.load(fp)
    #             # cookies = cookieToken_dict['COOKIES']
    #             # token = cookieToken_dict['TOKEN']
    #             cookies = cookieToken_dict[0]['COOKIES']
    #             token = cookieToken_dict[0]['TOKEN']
    #     log.debug("token: {}, cookie: {}".format(token, cookies))

    #     try:
    #         html = self.sess.get(r'https://mp.weixin.qq.com/cgi-bin/home?t=home/index&lang=zh_CN&token=%s' % token, timeout=(30, 60), headers={"Cookie":cookies})
    #     except Exception as e:
    #         log.debug("无cookie.json或失效 - %s" %e)
            
    
    #     if "登陆" not in html.text:
    #         log.debug("cookie有效,无需浏览器登陆")
    #         return token, cookies
        
    #     # todo selenium 登录获取
    #     return "", ""