#企查查每日新增企业数据抓取
* 接口
   * 使用企查查获取token接口 qccspider/common/utils.py 可以看到
   * 抓取每日新增数据接口 qccspider/getnewdata.py 可以看到

* 尚未完成的工作：
    * redis数据转存mysql
    * 代理池尚未设置
    * 企查查限制，每分钟请求大概不能超过30次，所有功能未加并发，请不要使用代理并发，会封账户的
* 已经完成工作
    * 每天定时抓取
    * 自动刷新token
    * 省份、市的所有代码
    * token自动刷新
    * 根据地址自动将省份、市、区县进行分割
    * 所有数据存到redis里面
    * 可以自动登录，账号需要独立
    * getnewdata.py 项目主入口
    * other放城市和省份代码
    * common公用方法
    * getmoredata.py 获取更多的企业数据，包括经营范围、联系方式等
    * getnewdata.py 获取每日新增企业数据
    * 摒弃以前所用方法，采用新的思路
    * 新增将数据写入文本
    * 本代码只做学习交流，请勿用于非法渠道！！！
   ![话不多说，看图](https://github.com/zhaoboy9692/qccspider/blob/master/demo.png)
