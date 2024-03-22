import os
import json

from time import sleep, localtime, time, strftime
from math import ceil
import threading
import random

from bs4 import BeautifulSoup
import requests


from .log import log 

class Wechat(object):
    def __init__(self):
        self.sess = requests.Session()
        self.headers = {
            'Host': 'mp.weixin.qq.com',
            'User-Agent': r'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
        }
        self.initpath = os.getcwd()
        self.keyword_search_mode = 0

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
                fakeid, nickname = self.get_subscription(token, query_name)
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
                self.get_articles(token, fakeid)
        except Exception as e:
            log.debug("!!![%s]" % str(e))
            if "list" in str(e):
                log.debug("请删除cookie.json")
                
    def get_subscription(self, token, query):
        # 获取公众号对应的信息。查询会匹配多个，返回第一个
        if (query == ""):
            query = "xinhuashefabu1"
        url = r'https://mp.weixin.qq.com/cgi-bin/searchbiz?action=search_biz&token={0}&lang=zh_CN&f=json&ajax=1&random=0.5182749224035845&query={1}&begin=0&count=5'.format(
            token, query)
        html_json = self.sess.get(url, headers=self.headers, timeout=(30, 60)).json()
        fakeid = html_json['list'][0]['fakeid']
        nickname = html_json['list'][0]['nickname']
        log.debug("fakeid: {}; nickname: {}".format(fakeid, nickname))
        return fakeid, nickname


    def get_articles(self, token, fakeid):
        # title_buf = []
        # link_buf = []
        img_buf = []

        Total_buf = []
        url = r'https://mp.weixin.qq.com/cgi-bin/appmsg?token={0}&lang=zh_CN&f=json&ajax=1&random={1}&action=list_ex&begin=0&count=5&query=&fakeid={2}&type=9'.format(token,  random.uniform(0, 1), fakeid)
        html_json = self.sess.get(url, headers=self.headers, timeout=(30, 60)).json()
        try:
            Total_Page = ceil(int(html_json['app_msg_cnt']) / 5)
            # self.progressBar.setMaximum(Total_Page)
        except Exception as e:
            log.error("!! 失败信息："+html_json['base_resp']['err_msg'])
            # if 'freq control' in html_json['base_resp']['err_msg']:
            #     可能有点问题
            #     if self.lineEdit_user_2.text() != '' and self.lineEdit_pwd_2.text() != '':
            #         self.freq_control = 1
            #         self.Label_Debug("将使用备胎公众号")
            #         username = self.lineEdit_user_2.text()  # 备选公众号的账号
            #         pwd = self.lineEdit_pwd_2.text()  # 备选公众号的密码
            #         [token, cookies] = self.Login(username, pwd)
            #         self.Add_Cookies(cookies)
            #         self.freq_control = 0
            #         self.Get_Articles(token, fakeid)
            return
        table_index = 0

        download_thread = threading.Thread(target=self.download_content)
        download_thread.start()
        self.thread_list.append(download_thread)

        _buf_index = 0
        dates = {}
        for i in range(Total_Page):
            if self.isresume == 1:
                i = i + self.pagenum
            self.Label_Debug("第[%d/%d]页  url:%s, article:%s" % (i + 1, Total_Page, self.linkbuf_cnt, self.download_cnt))
            log.debug("第[%d/%d]页  url:%s, article:%s" % (i + 1, Total_Page, self.linkbuf_cnt, self.download_cnt))
            #self.label_total_Page.setText("第[%d/%d]页  linkbuf_cnt:%s, download_cnt:%s" % (i + 1, Total_Page, self.linkbuf_cnt, self.download_cnt))
            begin = i * 5
            url = r'https://mp.weixin.qq.com/cgi-bin/appmsg?token={0}&lang=zh_CN&f=json&ajax=1&random={1}&action=list_ex&begin={2}&count=5&query=&fakeid={3}&type=9'.format(
                token,  random.uniform(0, 1), begin, fakeid)
            while True:
                try:
                    html_json = self.sess.get(url, headers=self.headers, timeout=(30, 60)).json()
                    break
                except Exception as e:
                    log.debug("连接出错，稍等2s %s"% e)
                    self.Label_Debug("连接出错，稍等2s" + str(e))
                    sleep(2)
                    continue
            try:
                app_msg_list = html_json['app_msg_list']
            except Exception as e:
                self.Label_Debug("！！！操作太频繁，5s后重试！！！")
                log.debug("！！！操作太频繁，5s后重试！！！ %s"% e)
                sleep(5)
                continue
                # os._exit(0)

            if (str(app_msg_list) == '[]'):
                log.debug('结束了')
                self.Label_Debug("结束了")
                break
            for j in range(30):
                try:
                    if (app_msg_list[j]['title'] in Total_buf):
                        self.Label_Debug("本条已存在，跳过")
                        log.debug("本条已存在，跳过")
                        continue
                    if self.keyWord != "":
                        if self.keyWord not in app_msg_list[j]['title']:
                            self.Label_Debug("本条不匹配关键词[%s]，跳过" % self.keyWord)
                            log.debug("本条不匹配关键词[%s]，跳过" % self.keyWord)
                            continue
                    article_time = strftime("%Y%m%d", localtime(int(app_msg_list[j]['update_time'])))  # 当前文章时间戳转为年月日
                    # 只取前两条
                    if dates.get(article_time,0) >1:
                        continue
                    dates[article_time] = dates.get(article_time,0) + 1 

                    log.info("文章：%s, 文章日期：%s" %(article_time,app_msg_list[j]['title']))
                    
                    if (article_time < self.timeStart ):
                        self.Label_Debug("本条[%s]不在时间范围[%s-%s]内，跳过" % (article_time, self.timeStart, self.timeEnd))
                        log.debug("本条[%s]不在时间范围[%s-%s]内，跳过" % (article_time, self.timeStart, self.timeEnd))
                        self.Stop_Run()
                        break
                    if(article_time > self.timeEnd):
                        self.Label_Debug("本条不在时间范围内，继续")
                        log.debug("本条不在时间范围内，继续")
                        # 
                        continue
                        # os._exit(0)
                    self.title_buf.append(app_msg_list[j]['title'])
                    self.link_buf.append(app_msg_list[j]['link'])
                    img_buf.append(app_msg_list[j]['cover'])
                    Total_buf.append(app_msg_list[j]['title'])

                    table_count = self.tableWidget_result.rowCount()
                    if(table_index >= table_count):
                        self.tableWidget_result.insertRow(table_count)
                    self.tableWidget_result.setItem(table_index, 0, QtWidgets.QTableWidgetItem(self.title_buf[_buf_index+j]))  # i*20+j
                    self.tableWidget_result.setItem(table_index, 1, QtWidgets.QTableWidgetItem(self.link_buf[_buf_index+j]))  # i*20+j
                    table_index = table_index + 1

                    self.total_articles += 1
                    dict_in = {"Title": self.title_buf[_buf_index+j], "Link": self.link_buf[_buf_index+j], "Img": img_buf[_buf_index+j]}
                    self.url_json_once(dict_in)
                    with open(self.rootpath + "\spider.txt", 'a+', encoding="utf-8") as fp:
                        fp.write('*' * 60 + '\n【%d】\n  Title: ' % self.total_articles + self.title_buf[_buf_index+j] + '\n  Link: ' + self.link_buf[_buf_index+j] + '\n  Img: ' + img_buf[_buf_index+j] + '\r\n\r\n')
                        # fp.write('【%d】 ' % self.total_articles + '\n' + link_buf[j] + '\r\n')
                        fp.close()
                    self.Label_Debug(">> 第%d条写入完成：%s" % (self.total_articles, self.title_buf[_buf_index+j]))
                    log.debug(">> 第%d条写入完成：%s" % (self.total_articles, self.title_buf[_buf_index+j]))
                    self.conf.set("resume", "total_articles", str(self.total_articles))  # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                    self.conf.write(open(self.cfgpath, "r+", encoding="utf-8"))
                except Exception as e:
                    log.debug(">> 本页抓取结束 - %s"% e)
                    _buf_index += j
                    log.debug("{} {}".format(_buf_index, len(self.title_buf)))
                    log.debug(self.title_buf)
                    break

            self.Label_Debug(">> 一页抓取结束")
            log.debug(">> 一页抓取结束")
            # self.get_content(title_buf, link_buf)
            # title_buf.clear()  # 清除缓存
            # link_buf.clear()  # 清除缓存
            if self.isresume == 1:
                self.linkbuf_cnt = len(self.link_buf) + self.json_read_len
            else:
                self.linkbuf_cnt = len(self.link_buf)
            self.conf.set("resume", "linkbuf_cnt", str(self.linkbuf_cnt))  # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            self.conf.write(open(self.cfgpath, "r+", encoding="utf-8"))
            self.conf.set("resume", "pagenum", str(i))  # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            self.conf.write(open(self.cfgpath, "r+", encoding="utf-8"))
            sleep(self.time_gap)
        
        dates = {}
        self.Label_Debug_Clear()
        self.Label_Debug(">> 列表抓取结束!!! <<")
        log.debug(">> 列表抓取结束!!! <<")
        self.download_end = 1
        
    def get_content(self, title_buf, link_buf):  # 获取地址对应的文章内容
        each_title = ""  # 初始化
        each_url = ""  # 初始化
        if self.keyword_search_mode == 1:
            length = len(title_buf)
        else:
            length = 1

        for index in range(length):
            if self.keyword_search_mode == 1:
                each_title = re.sub(r'[\|\/\<\>\:\*\?\\\"]', "_", title_buf[index])  # 剔除不合法字符
            else:
                each_title = re.sub(r'[\|\/\<\>\:\*\?\\\"]', "_", title_buf)  # 剔除不合法字符
            filepath = self.rootpath + "/" + each_title  # 为每篇文章创建文件夹
            if (not os.path.exists(filepath)):  # 若不存在，则创建文件夹
                os.makedirs(filepath)
            os.chdir(filepath)  # 切换至文件夹

            download_url = link_buf[index] if self.keyword_search_mode==1 else link_buf                
            while True:
                try:
                    html = self.sess.get(download_url, headers=self.headers, timeout=(30, 60))
                    break
                except Exception as e:
                    print("连接出错，稍等2s", e)
                    self.Label_Debug("连接出错，稍等2s" + str(e))
                    sleep(2)
                    continue
            # try:
            #     pdfkit.from_file(html.text, each_title + '.pdf')
            # except Exception as e:
            #     pass
            soup = BeautifulSoup(html.text, 'lxml')
            try:
                article = soup.find(class_="rich_media_content").find_all("p")  # 查找文章内容位置
                No_article = 0
            except Exception as e:
                No_article = 1
                self.Label_Debug("本篇未匹配到文字 ->"+str(e))
                print("本篇未匹配到文字 ->", e)
                pass
            try:
                img_urls = soup.find(class_="rich_media_content").find_all("img")  # 获得文章图片URL集
                No_img = 0
            except Exception as e:
                No_img = 1
                self.Label_Debug("本篇未匹配到图片 ->" + str(e))
                print("本篇未匹配到图片 ->", e)
                pass

            print("*" * 60)
            self.Label_Debug("*" * 30)
            self.Label_Debug(each_title)
            if No_article != 1:
                for i in article:
                    line_content = i.get_text()  # 获取标签内的文本
                    # print(line_content)
                    if (line_content != None):  # 文本不为空
                        with open(each_title + r'.txt', 'a+', encoding='utf-8') as fp:
                            fp.write(line_content + "\n")  # 写入本地文件
                            fp.close()
                self.Label_Debug(">> 保存文档 - 完毕!")
                # print(">> 标题：", each_title)
                print(">> 保存文档 - 完毕!")
            if No_img != 1:
                for i in range(len(img_urls)):
                    re_cnt = 0
                    while True:
                        try:
                            pic_down = self.sess.get(img_urls[i]["data-src"], timeout=(30, 60))  # 连接超时30s，读取超时60s，防止卡死
                            break
                        except Exception as e:
                            print("下载超时 ->", e)
                            self.Label_Debug("下载超时->" + str(e))
                            re_cnt += 1
                            if re_cnt > 3:
                                print("放弃此图")
                                self.Label_Debug("放弃此图")
                                break
                    if re_cnt > 3:
                        f = open(str(i) + r'.jpeg', 'ab+')
                        f.close()
                        continue
                    img_urls[i]["src"] = str(i)+r'.jpeg'  # 更改图片地址为本地
                    with open(str(i) + r'.jpeg', 'ab+') as fp:
                        fp.write(pic_down.content)
                        fp.close()
                self.Label_Debug(">> 保存图片%d张 - 完毕!" % len(img_urls))
                print(">> 保存图片%d张 - 完毕!" % len(img_urls))

            with open(each_title+r'.html', 'w', encoding='utf-8') as f:  # 保存html文件
                f.write(str(soup))
                f.close()
                self.Label_Debug(">> 保存html - 完毕!")
                # pdfkit.from_file('test.html','out1.pdf')
                print(">> 保存html - 完毕!")
            
            # 下载文章评论
            # comments = self.Get_Comments(download_url, self.wechat_uin, self.wechat_key)
            # with open(each_title + r'_comments.txt', 'a+', encoding='utf-8') as fp:
            #     fp.write('\n'.join(comments))  # 写入本地文件
            #     fp.close()
            #     self.Label_Debug(">> 保存评论 - 完毕!")
        
            if self.keyword_search_mode == 1:
                self.Label_Debug(">> 休息 %d s" % self.time_gap)
                print(">> 休息 %d s" % self.time_gap)
                sleep(self.time_gap)


    def KeyWord_Search(self, token, keyword):
        self.url_buf = []
        self.title_buf = []
        header = {
            'Content - Type': r'application/x-www-form-urlencoded;charset=UTF-8',
            'Host': 'mp.weixin.qq.com',
            'User-Agent': r'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome',
            'Referer': 'https://mp.weixin.qq.com/cgi-bin/appmsg?t=media/appmsg_edit&action=edit&type=10&isMul=1&isNew=1&share=1&lang=zh_CN&token=%d' % int(token)
        }
        url = r'https://mp.weixin.qq.com/cgi-bin/operate_appmsg?sub=check_appmsg_copyright_stat'
        data = {'token': token, 'lang': 'zh_CN', 'f': 'json', 'ajax': 1, 'random': random.uniform(0, 1), 'url': keyword, 'allow_reprint': 0, 'begin': 0, 'count': 10}
        html_json = self.sess.post(url, data=data, headers=header).json()
        total = html_json['total']
        total_page = ceil(total / 10)
        log.debug("{} - {}".format(total_page,  total))
        table_index = 0
        for i in range(total_page):
            data = {
                'token': token,
                'lang': 'zh_CN',
                'f': 'json',
                'ajax': 1,
                'random': random.uniform(0, 1),
                'url': keyword,
                'allow_reprint': 0,
                'begin': i*10,
                'count': 10
            }
            html_json = self.sess.post(url, data=data, headers=header).json()
            page_len = len(html_json['list'])
            # print(page_len)
            for j in range(page_len):
                self.url_buf.append(html_json['list'][j]['url'])
                self.title_buf.append(html_json['list'][j]['title'])
                print(j+1, ' - ', html_json['list'][j]['title'])
                table_count = self.tableWidget_result.rowCount()
                if (table_index >= table_count):
                    self.tableWidget_result.insertRow(table_count)
                self.tableWidget_result.setItem(table_index, 0, QtWidgets.QTableWidgetItem(self.title_buf[j]))  # i*20+j
                self.tableWidget_result.setItem(table_index, 1, QtWidgets.QTableWidgetItem(self.url_buf[j]))  # i*20+j
                table_index = table_index + 1
                self.total_articles += 1
                with open(self.rootpath + "/spider.txt", 'a+', encoding="utf-8") as fp:
                    fp.write('*' * 60 + '\n【%d】\n  Title: ' % self.total_articles + self.title_buf[j] + '\n  Link: ' + self.url_buf[j] + '\n  Img: ' + '\r\n\r\n')
                    # fp.write('\n【%d】\n' % self.total_articles + '\n' + url_buf[j] + '\r\n')
                    fp.close()
                    self.Label_Debug(">> 第%d条写入完成：%s" % (j + 1, self.title_buf[j]))
                    print(">> 第%d条写入完成：%s" % (j + 1, self.title_buf[j]))
            print('*' * 60)
            self.get_content(self.title_buf, self.url_buf)
            self.url_buf.clear()
            self.title_buf.clear()
    

def main():
    pass