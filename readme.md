1. 多公众号支持



表设计

1. 公众号表
public_account

|   id  | name  | fakeid | create_time | bak |
|  ---- | ----  | ----   | ----       | ----  | 
|自增id | 公众号名|唯一标识| 创建时间|备用字段|


2. 文章下载表

article

|   id  | p_id  | name | link | status | create_time | update_time | 
|  ---- | ----  | ----   | ----       | ----  |  ----   | ----   
|自增id | 公众号id| 名称| 链接|状态 0 未下载 1下载完成| 创建时间| 修改时间|


3. 下载状态表

 | p_id  | start_time | end_time | status | pagenum | link_cnt | down_cnt | total| 
 | ----  | ----   | ----       | ----  |  ----   | ----   |  ----   | ---- |
| 公众号id| 开始时间| 结束时间|状态 0 待执行 1 执行完成| 页码| 创建链接数| 下载数| 总数|