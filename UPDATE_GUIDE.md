# 每日更新说明（给 Muse 或任何自动更新的助手）

这个网站叫「反 AI 焦虑」。目的不是追新闻，是让人别慌：每条新闻都直接告诉读者「不用追 / 顺手试试 / 观望」，语气轻松、带点幽默。

你每天要做的事：**抓过去 24 小时中美两国的 AI 动态，挑出 3 到 8 条，写进 `feed.json`；特别大的事同时写进 `events.json`。然后提交到 `main` 分支。**

推送后 GitHub 会自动检查格式。格式写错了，网站不会更新，保持上一个正常版本。检查结果在仓库的 Actions 页面，失败时按报错修好再提交一次。

## 1. 去哪找

- 中国：36氪、量子位、机器之心、IT之家、财联社、澎湃新闻
- 美国：TechCrunch、The Verge、Axios、Hacker News 首页
- 官方：OpenAI、Anthropic、Google、Meta、xAI、DeepSeek、阿里通义、腾讯混元、字节豆包、月之暗面、智谱、MiniMax 的博客或发布页
- 关停：killedbyai.net、tooldirectory.ai/ai-graveyard
- 再搜几次：「AI 关停」「AI 裁员」「AI 涨价」「AI shutdown」「AI layoffs」「AI price」

范围以**中美两国所有和 AI 有关的事**为主；其他国家的大事（比如 Canva 裁员、欧盟法规、日本韩国的大模型）也收，`r` 填 `other`：新模型、新产品、关停、涨价降价、额度变化、个人 Agent、开源和 skill、大佬言论、上市和股价、裁员、监管、诉讼、芯片、机器人、人事变动（挖人、高管离职），以及 AI 对各行各业和岗位的冲击。

不收：小版本号更新以外没内容的、纯营销稿、已经收过的。

## 2. 怎么判

| 字段 | 含义 |
|---|---|
| `verdict` | `skip` 不用追 · `try` 顺手试试 · `wait` 观望 |
| `panic` | 慌张指数 1–5。普通更新 1–2，大模型发布或大厂关停 3–4，行业级恐慌 5 |

大多数新闻应该是 `skip`。只有零学习成本、马上能用的才给 `try`。

`why` 写一两句话：为什么不用慌，普通人该怎么做。不要写成新闻摘要。

## 3. 写进 feed.json

把新条目放在 `items` 数组**最前面**，同时把顶部 `updated` 改成今天日期。

```json
{
  "d": "2026-11-08",
  "verdict": "skip",
  "panic": 2,
  "t":   {"zh": "中文标题", "ja": "日本語タイトル", "en": "English title"},
  "why": {"zh": "一两句：为什么不用慌。", "ja": "一、二文で。", "en": "One or two sentences."},
  "src": "https://原文链接"
}
```

规则：

- 三种语言都要写，不能留空。
- 日期用 `YYYY-MM-DD`。
- `src` 必须是原文链接。
- `items` 最多保留 80 条，超出的从末尾删掉。

## 4. 大事同时写进 events.json（时间线）

`panic` ≥ 4 的，或者属于关停、人事变动、行业冲击的，在 `events` 数组里再加一条（顺序无所谓，页面会自动排序）：

```json
{
  "d": "2026-11-08",
  "r": "cn",
  "c": "shutdown",
  "p": 4,
  "t": {"zh": "...", "ja": "...", "en": "..."},
  "src": "https://...",
  "ind": "code"
}
```

- `r`：`cn` 中国 · `us` 美国 · `other` 其他国家和地区（如欧洲、日本、韩国、澳大利亚、加拿大的公司或事件）
- `c`：`model` 模型 · `product` 产品 · `price` 价格额度 · `voice` 大佬言论与舆论 · `oss` 开源 · `shutdown` 关停 · `policy` 监管诉讼 · `agent` Agent · `people` 人事变动
- `p`：1–5
- `ind`（可选，行业）：`code` 程序员、`film` 影视短剧、`design` 设计、`music` 音乐、`voice` 配音、`drive` 司机、`factory` 工厂机器人、`logi` 物流、`cs` 客服、`edu` 教育、`lang` 翻译、`care` 心理陪伴、`news` 新闻、`pub` 写作出版、`media` 新媒体、`ecom` 电商直播、`ad` 广告文案、`hr` HR、`office` 白领、`law` 法律、`med` 医疗、`fin` 金融、`sci` 科研、`game` 游戏、`photo` 摄影、`gov` 政务、`bank` 银行、`acct` 会计、`realty` 房产中介

**尽量加上「慌张对照」**：`f` 当时大家在慌什么、`o` 后来怎么样了、`life` 焦虑大概持续了多久。三个字段要么都写，要么都不写，三种语言都要有。网站的「档案室：历史上的同款焦虑」和首页「保质期最短的焦虑」只会挑出带这组字段的事件，不写就进不了这两个板块。结局还不清楚的先不写，等以后有了结局再回头给旧事件补上。

同时尽量填准 `ind`（行业）和 `c`（类型），网站按这两个字段把事件归到对应的焦虑下面（比如 `ind: code` 归到「程序员要失业」，`c: price` 归到「会员太贵」）。

```json
"f":    {"zh": "当时大家在慌什么", "ja": "...", "en": "..."},
"o":    {"zh": "后来怎么样了", "ja": "...", "en": "..."},
"life": {"zh": "约 3 个月", "ja": "約3か月", "en": "~3 months"}
```

## 5. 提交

- 只改 `feed.json` 和 `events.json`，不要动 `index.html`、`.github/` 和 `scripts/`。
- 提交说明写 `feed: 2026-11-08 (5 items)` 这种格式。
- 本地有 Python 的话，可以先跑 `python scripts/validate.py` 自查。
