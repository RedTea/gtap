# 介绍 #

> 本文档介绍了部署GTAP应用程序的所有步骤。其中搭建GAE开发环境的部分大量参考了Google App Engine Python SDK的帮助文档。

# 搭建GAE开发环境 #
> 使用 App Engine Python 软件开发套件 (SDK) 为 Google App Engine 开发和上传 Python 应用程序。

> 请从 [Python 网站下载](http://python.org/download/) 和安装适合您的平台的 Python 2.x。Mac OS X 10.5 Leopard 用户已安装 Python 2.5

> [下载 App Engine SDK](http://code.google.com/intl/zh-CN/appengine/downloads.html)。按照下载页面中的说明在计算机上安装 SDK。

> 对于本教程，您将使用一个来自 SDK 的命令：appcfg.py，用于将GTAP上传到 App Engine

> 对于 Windows 用户：Windows 安装程序会将这些命令置于命令路径中。安装后，您可以从命令提示符运行这个命令。

> 对于 Mac 用户：Google App Engine 启动程序会将这些命令包含在应用程序中。您可以通过从“GoogleAppEngineLauncher”菜单中选择“Make Symlinks...”将这些命令置于命令路径中。或者，您可以使用启动程序来运行开发网络服务器并部署您的应用程序，而不必运行命令。

> 如果您使用 SDK 的 Zip 归档版本，您将在 google\_appengine 目录中找到这些命令。



# 注册Twitter应用 #

> [在这里](http://twitter.com/apps/) 注册一个Twitter的Application

> 注意，在“Application Type”的地方，选择“Browser ”；在“Default Access type”的地方，选择“Read and Write”或“Read, write, and direct messages”；在“Use Twitter for login”的地方，不要打勾。

> 至于很多人都很关心的“Callback URL”项，则不需要关心，可随意填写，但必须要写。

> 申请成功后会得到Consumer key、Consumer secret这两个数据。

# 注册 Google App Engine 应用程序 #

> 从位于以下网址的 App Engine 管理控制台创建以及管理 App Engine 网络应用程序：

> http://appengine.google.com/

> 使用您的 Google 帐户登录到 App Engine。如果您没有 Google 帐户，可以使用电子邮件地址和密码创建一个 Google 帐户。

> 请点击“创建应用程序”按钮。请按照说明注册一个应用程序 ID，即一个对该应用程序唯一的名称，如gtapserver1。如果您选择使用免费的 appspot.com 域名，那么该应用程序的完整网址将为 http://gtapserver1.appspot.com/ 。您还可以为您的应用程序购买一个顶级域名，或使用一个您已注册的顶级域名。

# 部署 GTAP 应用程序 #

> 从位于以下网址的 GTAP 项目主页下载 gtap-0.4 版的源代码，并解压。

> http://code.google.com/p/gtap/downloads/list

> 编辑 app.yaml 文件，然后将 application: 设置的值从“your\_application\_id”更改为您在google注册的应用程序 ID，如gtapserver1。若因为GFW或什么其他原因而不像(或不能)使用加密传输的HTTP协议，则将该文件第12行的“secure: always”删掉即可。

> 编辑 main.py 文件，将其中第14，15行的内容，分别改为您在Twitter申请应用时获得Consumer key和Consumer secret。

> 运行以下命令，将 GTAP 部署至 Google App Engine:

> appcfg.py update gtap-0.4/

> 在提示下输入您的 Google 用户名和密码。

> 现在您就可以看到您的应用程序在 App Engine 上运行了。如果您创建了免费的 appspot.com 域名，那么您网站的网址将以您的应用程序 ID 开头，在本文档中，为：

> http://gtapserver1.appspot.com/

# 恭喜您！ #

> 关于 App Engine Python SDK 中 appcfg.py 命令的更多使用方法（如gae被墙的情况下如何使用代理上传应用程序），请参阅 App Engine 文档的“[上传和管理 Python 应用程序](http://code.google.com/intl/zh-CN/appengine/docs/python/tools/uploadinganapp.html)”部分。