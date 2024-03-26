

from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Boolean,Column,Integer,String, TIMESTAMP, ForeignKey

# from db.sqlite import engine
from sqlalchemy import create_engine


SQLiteURL = 'sqlite:///wechat.db'
# 创建engine，即数据库驱动信息
engine = create_engine(
    url=SQLiteURL,
    echo=True,    # 打开sqlalchemy ORM过程中的详细信息
    connect_args={
        'check_same_thread':False   # 是否多线程
    }
)



# 数据表的基类（定义表结构用）
Base = declarative_base()

class MyAccount(Base):
    """自身公众号"""
    __tablename__='my_account'
    id = Column(Integer, primary_key=True, autoincrement=True,comment="公众号id")
    name = Column(String(32),unique=True,index=True,comment="公众号名称")
    cookie = Column(String(32),unique=True,index=True,comment="公众号名称")
    token = Column(String(32),unique=True,index=True,comment="公众号token")
    isactivate = Column(Integer, default=0, comment="是否作为当前爬取公号,0 不激活 1激活， 默认0")

class Account(Base):
    # 公众号表
    __tablename__='account'
    id = Column(Integer, primary_key=True, autoincrement=True,comment="公众号id")
    fake_id = Column(String(32),index=True,comment="公众号唯一标识，系统给定")
    name = Column(String(32),unique=True,index=True,comment="公众号名称")
    create_time = Column(TIMESTAMP,comment="在系统添加时间")
 

class Article(Base):
    # 文章链接表
    __tablename__='article'
    aid = Column(String(32),primary_key=True,index=True,comment="文章id,具有唯一标识")
    pid = Column(Integer, ForeignKey('account.id'), comment="公众号id")
    name = Column(String(128),comment="文章标题")
    link = Column(String(256),comment="文章链接")
    cover = Column(String(256),comment="封面链接")
    status = Column(Integer,comment="状态 0 未下载 1下载完成")
    create_time = Column(TIMESTAMP,comment="记录创建时间")
    update_time = Column(TIMESTAMP,comment="记录更新时间")
 

class TaskStatus(Base):
    # 下载任务状态表
    __tablename__='task_status'
    id = Column(Integer, primary_key=True, autoincrement=True,comment="任务id")
    pid = Column(Integer, ForeignKey('account.id'),comment="公众号id")
    start_time = Column(TIMESTAMP,comment="任务开始时间")
    end_time = Column(TIMESTAMP,comment="任务结束时间")
    keyword = Column(String(32), default="",comment="查询关键字")
    status = Column(Integer,comment="任务状态0 待运行 1运行中 2 运行完成")
    pagenum = Column(Integer,comment="上次运行页码")
    timegap = Column(Integer, comment="下载间隔时间")
    link_cnt = Column(Integer,comment="上次记录的文章链接数")
    down_cnt = Column(Integer,comment="上次下载的文章数")
    total  = Column(Integer,comment="上次的文章总数")
    create_time = Column(TIMESTAMP,comment="任务创建时间")
    update_time = Column(TIMESTAMP,comment="任务修改时间")
    



# 创建表
# checkfirst=True 默认也是 True，即如果数据库存在则不再创建
Base.metadata.create_all(engine, checkfirst=True)

# session 与数据库交互
Session = sessionmaker(bind=engine) 
session = Session() 
