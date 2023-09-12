# Scraper

小红书、微信公众号、马蜂窝笔记爬虫

安装：`pip install beautifulsoup4 requests`

注：cookie过期时请尝试浏览器开发者模式 -> Network -> 刷新网页 -> Request headers -> raw，复制后用mfw_scraper.py内的parse_header函数进行解析，保存为header

## 输出格式

### 小红书

支持`xhslink.com/xxx`和`www.xiaohongshu.com/explore/xxx`两种url

| 键名              | 类型           | 说明                                                         |
| ----------------- | -------------- | ------------------------------------------------------------ |
| `source_platform` | str            | "xhs"                                                        |
| `url`             | str            | 帖子原始链接                                                 |
| `title`           | str            | 帖子标题                                                     |
| `content`         | str            | 帖子正文                                                     |
| `img_urls`        | List[str]      | 帖子中图片的链接                                             |
| `author`          | dict           | 作者信息。"nickname"：昵称；"avatar"：头像链接；"city"：发布地点，可能为null（例如较早的帖子）；"userId"：用户id |
| `liked_count`     | int            | 点赞数                                                       |
| `collected_count` | int            | 收藏数                                                       |
| `comment_count`   | int            | 评论数                                                       |
| `comments`        | List[dict]     | 评论。"content"：评论内容；"user"：发布者；"is_from_author"：是否为原贴作者发布 |
| `time`            | str            | 发布日期，注意只有日期（与微信公众号不同）                   |
| `trip_infos`      | [Optional]dict | 游玩信息，由原贴作者提供。通常包含“玩法类型”、“游玩时长”、“人均成本”三个key，其value可能为“-”或包含省略号“...”。可能为null |

示例

```json
{
    "source_platform": "xhs",
    "url": "https://www.xiaohongshu.com/explore/63bc025e000000001b027f3c",
    "title": "上海压马路必备攻略｜魔都超好逛14个街区🌟",
    "content": "《魔都14大潮流必逛街区清单》 里面有你去过的吗❓ · 🌟好逛店清单见图片哦 · 1️⃣慎余里 2022年下半年魔都重磅新地标！", //omitted
    "img_urls": [
        "http://sns-webpic-qc.xhscdn.com/202309091941/e84e2311528f0579eccff06e755b3444/1000g0081s5637paf00004a554633je8efb18lhg!nd_whgt34_nwebp_prv_1?imageView2/format/jpg|imageMogr2/strip",
        "http://sns-webpic-qc.xhscdn.com/202309091941/771822dce05de6613629ac08583e05a0/1000g0081s5637paf00004a554633je8efb18lhg!nd_whgt34_nwebp_wm_1?imageView2/format/jpg|imageMogr2/strip" //omitted

    ],
    "author": {
        "nickname": "上海有个号",
        "avatar": "https://sns-avatar-qc.xhscdn.com/avatar/1000g2jo2odlbou4k40004a554633je8em0jr4sg",
        "userId": "5af10639e8ac2b69814fb90e",
        "city": null
    },
    "liked_count": "1w+",
    "collected_count": "1w+",
    "comment_count": "100+",
    "share_count": "1w+",
    "comments": [
        {
            "content": "去过九个",
            "user": "冬暖夏凉",
            "is_from_author": false
        },
        {
            "content": "没人提名徐家汇？？？美罗城港汇天钥桥还有个徐家汇书院等等等等，真的很好逛啊[笑哭R]",
            "user": "宇宙小小王",
            "is_from_author": false
        }
    ],
    "time": "2023-01-09",
    "tags": [
        "#上海",
        "#上海探店",
        "#上海旅游",
        "#魔都",
        "#魔都探店",
        "#上海魔都探店",
        "#街区",
        "#潮流艺术",
        "#压马路",
        "#上海压马路",
        "#我在上海压马路"
    ],
    "keywords": [
        "建筑",
        "探店",
        "潮流",
        "艺术",
        "吴界攻略",
        "张园攻略",
        "黑石公寓旧址攻略",
        "M+马利攻略",
        "慎余里攻略",
        "锦和越界陕康里攻略",
        "创想塔宠物店攻略",
        "张园·丰盛里攻略",
        "现所攻略",
        "衡山路8号攻略",
        "上生新所攻略",
        "今潮8弄攻略",
        "武夷MIX320攻略",
        "永平里攻略",
        "旅行",
        "南京西路",
        "休闲玩乐",
        "复兴中路",
        "上海魔都探店",
        "城市出行",
        "购物",
        "买手店"
    ],
    "location": "张园"
}
```



### 微信公众号

支持`mp.weixin.qq.com/s/xxx`

| 键名              | 类型 | 说明                                                         |
| ----------------- | ---- | ------------------------------------------------------------ |
| `source_platform` | str  | "wx"                                                         |
| `url`             | str  | 帖子原始链接                                                 |
| `title`           | str  | 帖子标题                                                     |
| `content`         | str  | 帖子正文                                                     |
| `img_urls`        | null | 微信公众号中的图像多而杂乱，且不用于OCR，因此不进行提取      |
| `author`          | dict | 作者信息。"user"：作者昵称；"profile"：公众号名称；"city"：发布地点，可能为null（例如较早的帖子） |
| `time`            | str  | 发布时间，注意包括小时和分钟（与小红书、马蜂窝不同）         |

示例

```json
{
    "source_platform": "wx",
    "url": "https://mp.weixin.qq.com/s/XqAr2Ic2Zp3HIsWO2gwqAQ",
    "title": "两碗鸭血粉丝汤 吃出一点幸福感",
    "content": "就像每\n个上海人心中都有一家钟爱的面馆，每个南京人心中也有一碗自己喜欢的鸭血粉丝汤，所以周末一早开车去南京，差不多中午到，我们也没有费力寻找，就到一个名叫锁金村的地方，就近吃了街拐角的两家。\n金原鸭血粉丝汤开了有二十多年，分店也开出好几家，但锁金总店据说是很多老南京人最挂念的味道。\n", //omitted
    "author": {
        "user": "Chi Xin",
        "profile": "一片吃心",
        "city": "江苏"
    },
    "time": "2023-08-19 09:13"
}
```



### 马蜂窝

支持`imfw.cn/l/xxx`和`m.mafengwo.cn/mweng/wengdetailssr/weng?id=xxx`两种url

| 键名              | 类型                | 说明                                                         |
| ----------------- | ------------------- | ------------------------------------------------------------ |
| `source_platform` | str                 | "mfw"                                                        |
| `url`             | str                 | 帖子原始链接                                                 |
| `title`           | str                 | 帖子标题                                                     |
| `content`         | str                 | 帖子正文                                                     |
| `img_urls`        | List[str]           | 帖子中图片的链接                                             |
| `author`          | dict                | 作者信息。"nickname"：昵称；"avatar"：头像链接；"city"：发布地点，可能为null（例如较早的帖子） |
| `liked_count`     | str                 | 点赞数。不是int类型，因为可能是"10+"，"100+"等               |
| `collected_count` | str                 | 收藏数                                                       |
| `comment_count`   | str                 | 评论数                                                       |
| `share_count`     | str                 | 分享数                                                       |
| `comments`        | List[dict]          | 评论。"content"：评论内容；"user"：发布者；"is_from_author"：是否为原贴作者发布 |
| `time`            | str                 | 发布日期，注意只有日期（与微信公众号不同）                   |
| `tags`            | [Optional]List[str] | 标签列表，由原贴作者提供，每个标签以“#”开头。可能为null      |
| `keywords`        | [Optional]List[str] | 关键词列表，由小红书生成。可能为null                         |
| `location`        | [Optional]str       | 定位，注意只有一个点（与马蜂窝不同）。可能为null             |

示例

```json
{
    "source_platform": "mfw",
    "url": "https://m.mafengwo.cn/mweng/wengdetailssr/weng?id=1762141883764452",
    "title": "上海周末|外滩小众高级citywalk打卡攻略！",
    "content": "✅外滩相信大家都很熟悉，外滩观景平台也是常年都是人👩‍👩‍👧‍👦，网上外滩拍的陆家嘴照也是随处可见。\n✅来外滩只知道在景观平台打卡📸吗？其实外滩附近还有很多值得打卡逛逛的地方，90%的人都不知道外滩周围还可以这么逛🚶。\n", //omitted
    "img_urls": [
        "https://weng.mafengwo.net/img/6f/a9/e8161ac09af680801a3cdb4b4c93dc1f.jpeg?imageMogr2%2Fthumbnail%2F750x%2Fstrip%2Fquality%2F90%7Cwatermark%2F1%2Fimage%2FaHR0cDovL21mdy1mYXN0ZGZzLTEyNTgyOTUzNjUuY29zLmFwLWJlaWppbmcubXlxY2xvdWQuY29tL3MxOS9NMDAvQzAvOUEvckJSYmhHSnFpTEF6MjZBekFBSGxpWmU5cmhRLnBuZz9pbWFnZU1vZ3IyJTJGdGh1bWJuYWlsJTJGMTIweCUyRnN0cmlwJTJGcXVhbGl0eSUyRjkw%2Fgravity%2FSouthWest%2Fdx%2F13%2Fdy%2F13",
        "https://weng.mafengwo.net/img/cb/9f/1a642ee96c6a88193fff68cee9b1a37f.jpeg?imageMogr2%2Fthumbnail%2F750x%2Fstrip%2Fquality%2F90%7Cwatermark%2F1%2Fimage%2FaHR0cDovL21mdy1mYXN0ZGZzLTEyNTgyOTUzNjUuY29zLmFwLWJlaWppbmcubXlxY2xvdWQuY29tL3MxOS9NMDAvQzAvOUEvckJSYmhHSnFpTEF6MjZBekFBSGxpWmU5cmhRLnBuZz9pbWFnZU1vZ3IyJTJGdGh1bWJuYWlsJTJGMTIweCUyRnN0cmlwJTJGcXVhbGl0eSUyRjkw%2Fgravity%2FSouthWest%2Fdx%2F13%2Fdy%2F13" //omitted
    ],
    "pois": [
        "外滩",
        "北京东路",
        "沙美大楼",
        "上海滇池路",
        "礼和洋行旧址",
        "外滩中央广场",
        "汉口路",
        "上海福州路文化街",
        "广东路"
    ],
    "author": {
        "nickname": "小西环游记",
        "avatar": "https://p1-q.mafengwo.net/s19/M00/CD/CE/CoNJ9WOS3ZYOE95-AADcexi01E4.jpeg",
        "city": "上海"
    },
    "liked_count": "219",
    "collected_count": "31",
    "comment_count": "6",
    "comments": [
        {
            "content": "这一圈走完要多久？",
            "user": "玉帝老子",
            "is_from_author": false
        },
        {
            "content": "很有用心思的文章和照片 讚",
            "user": "馬卡龍小姐",
            "is_from_author": false
        }
    ],
    "time": "2023-04-03",
    "trip_infos": {
        "玩法类型": "走过外滩百...",
        "游玩时长": "2小时以下",
        "人均成本(元)": "100"
    }
}
```