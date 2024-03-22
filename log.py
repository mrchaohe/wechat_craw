import logging 

log = logging.getLogger(__file__)
log.setLevel(logging.DEBUG)

# 建立一个filehandler来把日志记录在文件里，级别为debug以上
fh = logging.FileHandler("log.log")
fh.setLevel(logging.INFO)

# 建立一个streamhandler来把日志打在CMD窗口上，级别为error以上
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

formatter = logging.Formatter("%(asctime)s line:%(lineno)4d %(levelname)6s - %(message)s")
ch.setFormatter(formatter)
fh.setFormatter(formatter)

#将相应的handler添加在logger对象中
log.addHandler(ch)
log.addHandler(fh)
#logging.basicConfig(level=logging.DEBUG, filename="./log", datefmt="%Y-%m-%d %H:%M:%S",format="%(asctime)s line:%(lineno)4d %(levelname)6s - %(message)s")
