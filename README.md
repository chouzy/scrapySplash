# scrapySplash

> Scrapy 框架整合 Splash练习项目
>
> 测试网站：https://spa5.scrape.center

### 核心

使用`scrapy_splash`库，官方文档：[scrapy-plugins/scrapy-splash](https://github.com/scrapy-plugins/scrapy-splash#readme)

#### 使用

1. 修改`settings.py`

```python
# 配置 SPLASH_URL
SPLASH_URL = 'http://192.168.59.103:8050'

# 配置 MIDDLEWARES
DOWNLOADER_MIDDLEWARES = {
    'scrapy_splash.SplashCookiesMiddleware': 723,
    'scrapy_splash.SplashMiddleware': 725,
    'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware': 810,
}
SPIDER_MIDDLEWARES = {
    'scrapy_splash.SplashDeduplicateArgsMiddleware': 100,
}

# 配置去重类 DUPEFILTER_CLASS
DUPEFILTER_CLASS = 'scrapy_splash.SplashAwareDupeFilter'

# 配置 Cache 存储 HTTPCACHE_STORAGE
HTTPCACHE_STORAGE = 'scrapy_splash.SplashAwareFSCacheStorage'
```

2. 修改`Spider`

```python
# yield Request(detail_url, callback=self.parse_detail)
# 使用 SplashRequest 替换所有 Request 请求
yield SplashRequest(detail_url, callback=self.parse_detail, priority=2, 
                    args={'lua_source': script}, endpoint='execute')
```

### 运行

#### 安装依赖

```shell
pip install -r requirement.txt
```

#### 安装 Splash

> 推荐 docker 方式安装

#### 运行

```shell
scrapy crawl book
```

