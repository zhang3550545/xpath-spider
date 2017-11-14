### 爬取的网站是多玩图库

爬取的网站是：http://tu.duowan.com/m/bxgif

使用fiddler软件抓包分析：

    在浏览器中输入上面的url，加载到30条需要的数据，随着滚动条往下拖动，数据再次加载且浏览器的url没有变化
    初步判断采用的是ajax框架加载数据，通过抓包工具找到加载的url。

ajax加载的url：

    http://tu.duowan.com/m/bxgif?offset=30&order=created&math=0.2097926790117744
    url返回的json数据格式：
    {
        "html": "...",
        "more": true,
        "offset": 60,
        "enabled": true
    }
    http://tu.duowan.com/m/bxgif?offset=60&order=created&math=0.9387482944610999
    {
        "html": "...",
        "more": true,
        "offset": 90,
        "enabled": true
    }

    注：html字段是html中的"<li>..."的html数据，可以使用lxml和xpath解析，具体看代码

通过查看html页面的源码，可以发现，offset是json数据返回的offset，order字段是固定的，math字段是一个（0,1）的随机数。