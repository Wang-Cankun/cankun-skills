# 配图管线 — Wikimedia 抓取 · 目检 · 内嵌

目标：每个图位一张**主体正确、授权干净、哈希唯一**的照片，base64 内嵌保持单文件。

## 1 · 抓取

用 `scripts/fetch_images.py <spec.json> <outdir>`。spec 每项 = 语义文件名 → 查询词列表（由宽到窄准备 2–3 个）：

```json
{ "pisac": ["Pisac Inca terraces", "Pisac ruins Peru"] }
```

脚本内置过滤：仅 jpeg、宽 ≥1100px、标题排除 map/karte/plan/diagram。命中即下载 1100px 缩略图，
压缩至 ≤155 KB（q75 起步降到 q45），写 `credits.json`（Commons 文件名 + 授权）。
Commons API 会 429 限流——脚本自带指数退避，别并发狂抓。

## 2 · 目检（不可跳过）

把新图拼 contact sheet（PIL 缩略拼图）**用眼睛看**。搜索命中 ≠ 主体正确，本管线实际淘汰过：
河流查询命中**地图**、城镇查询命中**1979 年老照片**和**博物馆面具墙**、广场查询命中**仪仗兵特写**、
黑白历史照。跑偏就换更窄的查询词 + 标题 want/ban 过滤重抓，或直接按候选标题精确取文件。

## 3 · 去重与分配

对全部 `<img>` 的 base64 前 2KB 做 md5——**每个哈希只允许出现一次**。同一地点想出现两次就抓第二张不同的图。
分配原则：日程页配当日主景；reader 页配该页主题；纯文字页可插 22–26 mm 矮幅图但必须过 strip check。

## 4 · 内嵌

`base64.b64encode` 拼 `data:image/jpeg;base64,` 写入 src。裁切交给 CSS：`object-fit:cover` +
按构图调 `object-position`（天空多就 `center 55%`）。全书图片总量控制在 ~2.5 MB 内（成品 PDF ≤ 7 MB）。

## 5 · 授权

个人用途下资料来源页写总述即可：来源 Wikimedia Commons、授权系列（CC0/CC BY/CC BY-SA）、
完整清单在 credits.json。若成品要公开分发，改为逐张署名。
