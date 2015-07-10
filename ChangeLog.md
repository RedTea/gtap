  * ### v0.4.1 (2010.09.02) ###
    1. BugFix: [issue 49](https://code.google.com/p/gtap/issues/detail?id=49) . thanks Pro711
    1. Feature: username case insensitive.Need to re-certification from twitter.com
    1. Feature: optimize procedures
  * ### v0.4 (2010.07.02) ###
    1. 只支持 Oauth 方式的身份认证
    1. 可修改 secret key
  * ### v0.3 (2010.03.01) ###
    1. 增加 is\_hop\_by\_hop 函数
    1. 重写了从twitter抓取数据后返回给客户端的部分
  * ### v0.2.2 (2009.12.30) ###
    1. fixed 版本显示的错误
    1. 增加了对search.twitter.com和api.twitter.com的支持，如：
    1. https://search.twitter.com    =>    https://gtapserver1.appspot.com/search
    1. https://api.twitter.com    =>    https://gtapserver1.appspot.com/api
  * ### v0.2.1 (2009.08.03) ###
    1. 在app.yaml中增加了参数secure，强制客户端用https连接
    1. 再一次修改了TwitterFox 1.8.3，现在API和所有在浏览器中打开的链接，均使用HTTPS
  * ### v0.2   (2009.08.02) ###
    1. 修改了身份验证部分，可以更正常的代理API
    1. 完全照模样返回Twitter API的响应
  * ### v0.1   (2009.08.01) ###
    1. 想法+简单实现，我自己可以凑活用了
    1. 可以代理几乎所有REST API(未完全测试)
    1. OAuth没测试过，也没研究过，不知道能不能行。估计是不行
    1. 提供一个API测试地址 http://gtapserver1.appspot.com/
    1. 弄了一个使用上面这个测试地址的 TwitterFox 1.8.3修改版