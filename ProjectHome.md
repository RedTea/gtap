# GTAP = GAE Twitter API Proxy #

  * GoogleAppEngine本身在墙内不是一个所有人都可以稳定使用的服务，用来做代理同样也是不稳定的。
  * 使用类似GTAP这样的代理上Twitter也不是一个安全的方案，至少不是所有人都会或者可以安全的使用。
  * 想要真正的了解和认识一个真实的世界，一个Twitter显然是远远不够的。

基于以上三点，我认为GTAP已经失去了继续存在下去的意义。

请大家更多的选择VPN等其他的翻墙手段，让自己真正的走到墙外去，即便是为此花点小钱，也是值得的。比如 [曲径](https://getqujing.com/?r=109c183a0b) 这个服务就很不错~

2014-05-29



&lt;hr /&gt;



It is a simple solution on Google App Engine which can proxy the HTTP request to twitter's official REST API url .

源于Twitter被“强奸”，并受到GAppProxy项目的启发，一个可以在 Google App Engine上搭建自己独立的 Twitter API Proxy 的简单的开源的解决方案。

download the last stable version : [gtap-0.4.2](http://gtap.googlecode.com/files/gtap-0.4.2.tar.gz)  <-- <font color='red'><b>only support Oauth!</b></font> [INSTALL](http://code.google.com/p/gtap/wiki/INSTALL)

You can use <b><a href='https://gtapserver1.appspot.com/'>https://gtapserver1.appspot.com/</a></b> for some tests.

for example:

https://gtapserver1.appspot.com/   can proxy all requests to http://twitter.com/

https://gtapserver1.appspot.com/api/   can proxy all requests to http://api.twitter.com/

https://gtapserver1.appspot.com/search/   can proxy all requests to http://search.twitter.com/

<font color='red'><b>Don't forget the "/" at the end of your api proxy address!!!</b></font>

thanks [@SAPikachu](http://twitter.com/SAPikachu) for giving us an hacking version with OAuth supporting. [Detail](http://code.google.com/p/gtap/issues/detail?id=9#c73)

ChangeLog