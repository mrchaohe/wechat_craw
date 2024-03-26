1. 多公众号支持



一. 表设计

1. 公众号表
public_account

|   id  | name  | fakeid | create_time | bak |
|  ---- | ----  | ----   | ----       | ----  | 
|自增id int| 公众号名 string|唯一标识 string| 创建时间|备用字段|


2. 文章下载表

article

|   aid  | p_id  | name | link | status | create_time | update_time | 
|  ---- | ----  | ----   | ----       | ----  |  ----   | ----   
|公众号文章自身id | 公众号id| 名称| 链接|状态 0 未下载 1下载完成| 创建时间| 修改时间|


3. 下载状态表

 | p_id  | start_time | end_time | status | pagenum | link_cnt | down_cnt | total| 
 | ----  | ----   | ----       | ----  |  ----   | ----   |  ----   | ---- |
| 公众号id| 开始时间| 结束时间|状态 0 待执行 1 执行中 2执行完成| 页码| 创建链接数| 下载数| 总数|



二. 接口设计
2.1 自身公众号
自身公众号信息

2.1.1 设置公众号

请求方法：post
路由url： myaccount
请求参数：
```json
{
    "account": string //自身公众号名称
}
```

2.1.2 获取自身公众号

请求方法：get
路由url： myaccount
请求参数：
```json
{
    "data":[
        "account": string //自身公众号名称
        "id": int
    ]
    
}
```

2.1.3 设置Cookie

请求方法：put
路由url： cookie
请求参数：
```json
{
    "token":string,
    "cookie": string,
    "isactivate": 0,   // 0 不激活 1激活， 默认0
    "id": int //自身公众号id
}
```





2.2 公众号
爬取公众号信息
2.2.1 设置公众号
请求方法：post
路由url： acount
请求参数：
```json
{
    "account":string,
}
```
2.2.2 获取公众号
请求方法：get
路由url： account
请求参数：
```json
{
    "account":string,
    "fackid": string,
    "id": int,
    "create_time": string
}
```

2.3 下载任务

2.3.1 创建下载任务
请求方法：post
路由url： task
请求参数：
```json
{
    "fackid": string,
    "start_time":string,
    "end_time": string,
    "timegap": int,    //时间间隔数
    "keyword": stirng  // 查询关键字，暂不实现
}
```
新建立即执行，根据fackid， 判断有无创建任务。如果有，则考虑和已有合并，如果没有，则新建任务。

2.3.2 查看任务执行情况
请求方法：get
路由url： task
请求参数：
```json

{
    "status":0,  // 状态
    "msg": string, // 错误信息
    "data":[
        {   
            "account":string,
            "fackid": string,
            "start_time":string,
            "end_time": string,
            "status": int,
            "timegap": int, // "下载间隔时间"
            "link_cnt"： int, // 上次记录的文章链接数量
            "down_cnt": int, // 下载数量
            "total": int // 文章总数

        },
    ]
}
```

2.3.2 执行下载任务
  针对未执行完的继续执行,异步处理
请求方法：PUT
路由url： task
请求参数：
```json
{
    "ids": [id1, id2]
}
```

2.4 文章链接

2.4.1查看文章链接
请求方法：get
路由url： link
响应参数：
```json
{
    "fackid": string,
    "status": int,  // 状态，可选，默认返回所有
}
```
请求参数：
```json
{
    "status":0,  // 状态
    "msg": string, // 错误信息
    "data":[
        {   
            "account":string,
            "fackid": string,
            "start_time":string,
            "end_time": string,
            "status": int,
            "timegap": int, // "下载间隔时间"
            "link_cnt"： int, // 上次记录的文章链接数量
            "down_cnt": int, // 下载数量
            "total": int // 文章总数

        },
    ]
}
```
2.4.2 执行下载下载文章
  针对未执行完文章的继续执行,异步处理
请求方法：PUT
路由url： link
请求参数：
```json
{
    "ids": [id1, id2]
}
```