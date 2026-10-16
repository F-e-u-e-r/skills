# Award-Site 設計趨勢 Review / Moodboard（2023–2026）

**狀態：研究紀錄（research record），非 pack 能力。** 本文不改動任何 skill、corpus 或 generated reference，不被任何 loader 讀取，不隨 plugin 出貨。它只是把 Awwwards / FWA / Webby 近四年的得獎作品整理成趨勢與 moodboard，並**提出**可融入 Design Pack 的候選方向；是否採用由 owner 決定。

編製日期：2026-10-10。對應 pack 版本：design-pack 0.1.0（corpus sha `16ad01fb…`，merge `44f1044`）。

---

## 0. 一句話結論

近四年得獎作品的「簽名」不是放縱，而是**高紀律的放大**：**雙色節制 + 單一飽和 accent 壓在近黑/中性底**、**超大表現型 display 字當結構 + 樸素 grotesque 當內文**、**以 WebGL/3D「空間化 scroll」把頁面變成體驗**。這些大多落在 Design Pack 既有的 **spectacle / Awwwards override lane**（`ANTISLOP-2008`、`motion-craft` When-NOT）之內，且**反而印證**了多條既有禁令。真正要 owner 決策的，只有少數「會放寬規則」的張力點（glass/blur、重 motion、dark-default）。

---

## 1. 證據基礎與方法

**抽樣與驗證。** 四個並行研究子代理（每年一個）以防杜撰約束蒐集 Awwwards / FWA / Webby 得獎站；orchestrator 再**親自重抓抽樣 URL 驗證**。共 **~69 筆已驗證得獎站**（2023:14 / 2024:17 / 2025:18 / 2026:20，另各有少量 held-out）。完整清單與每筆來源見 `SOURCES.md`。

**四個 nouns（evidence discipline）。**
- **最小證據集**：治理文件＝Design Pack 三個 skill + generated corpus shards（已開啟 ui-design-craft、color/typo/struct/antislop、motion-craft）；主體事實＝真實得獎站（outward claims，即時 fetch）。
- **權威順序**：得獎平台頁 owns「誰得獎」；設計專業媒體 > listicle/aggregator owns 趨勢脈絡；corpus owns「我們的 doctrine 是什麼」（canonical shards > pack-local prose > orchestration）；我的記憶/品味最後且標註。
- **觀察式驗證**：每個具名得主溯源到已開啟的 URL + 取用日期；不杜撰 hex/字體名；具體屬性無來源則略去或標弱。
- **fraud table（審查者應獵殺）**：phantom winners、stale-as-current、cherry-picked 當代表、杜撰 hex/font、未開啟的 sources、trend inflation、**cutoff laundering**（把 2026 的記憶臆測當成實測現況）。

**本研究實際攔下的問題（誠實披露）：**
1. **SOTD ≠ SOTY（獎項層級膨脹）。** Awwwards 的 `sites_of_the_year/` 是**多年份 showcase，不是單一年度大獎**。我直接抓 `lusion-v3`、`igloo-inc` 頁面：只有 `Site of the Day` badge，「Site of the Year」**NOT PRESENT**。兩個代理也獨立證實該 collection 跨年混放。**處置**：2023/2024 一律報為 **SOTD honorees**；「Site of the Year」只保留給我親自在 `annual-awards/winners` 頁確認的 **Lando Norris（2025）**。2023 真正可確認的旗艦 = **Lusion v3 = FWA of the Year 2023**（已確認）。
2. **JS-SPA 工具陷阱。** Awwwards/FWA/Webby-gallery 皆為 client-rendered SPA；**WebSearch AI 摘要與一般 WebFetch 會幻覺/依 slug 臆測**（代理曾因此誤把 2019/2015 頁當 2023、誤收 Studio Kiln/Thredd，後自行撤回）。可靠讀取需 Playwright DOM / `r.jina.ai` proxy / 靜態 Webby 新聞稿。我的重抓凡回傳**具體數據（確切日期/分數/清單）者**即為真內容、可信。
3. **訓練 cutoff = 2026-01。** 故 2026 幾乎全靠即時查證；且 2026 年只走約 10 個月，**無 SOTY/FOTY 2026**（年度獎要 2027 初才揭曉，未杜撰），daily-award 樣本集中在 9 月底–10 月初（平台 live 窗口），**非全年普查**。
4. **font-pairing 是最薄維度。** 四年都無法把具體字體綁到特定得主（平台頁不公開字體欄）；代理**拒絕杜撰**字體名，改以平台級線索（font facet、best-free-fonts 頁）與二手來源描述。color hex 多為**平台頁實測值**（研究當日讀取，非逐一由我複驗）。

---

## 2. 逐年快照

| 年 | 已驗證旗艦例（節錄） | 該年關鍵調性 |
|---|---|---|
| **2023** | Lusion v3（FWA of the Year 2023 + Awwwards SOTD）、The Search for Work Happiness（Three.js/GSAP/Nuxt headless）、Noomo Agency、Mana Yerba Mate；Loewe × Howl's Moving Castle（FWA People's Choice）；Webby 27th：Discord、Patagonia、Spotify 2022 Wrapped | WebGL/3D + scrollytelling 成形；超大字當 grid；Pantone Viva Magenta 帶起飽和色；bento 被命名為趨勢 |
| **2024** | Igloo Inc、Don't Board Me、Opal Tadpole（Awwwards SOTD）；The Maison of All Victories（LVMH, FWA FOTD+FOTM）、Omega Clearspace、IBM Catch Fishy AI（FWA）；Webby 28th：Locomotive（Technical Achievement）、Sculpting Harmony（Best Visual Design, Getty×Resn）、The Impossible Bedtime Story（Accessible Tech） | 3D/WebGL 從新奇變**預設 tag**；品牌站做成可探索「世界/樓層」；duotone 節制；bento 卡片成名 |
| **2025** | Lando Norris（**Site of the Year 2025**, OFF+BRAND）、Messenger（Developer SOTY, abeto）、Scout Motors（E-commerce SOTY, Locomotive）、Cartier Watches & Wonders（Awwwards+FWA, Immersive Garden）、FlowFest、State of AI；Webby 29th：Lady Gaga 數位主場、Climate TRACE、Pinterest Predicts | 3D/WebGL「世界」站成旗艦格式；**CSS 吃掉 JS**（container queries/`:has()`/`text-wrap:balance`/View Transitions）；museum/room scroll |
| **2026**（部分） | The Renaissance Edition（Webby Best Home Page + Awwwards SOTD, Shopify）、Odyssée（NIGHTJAR）、Santioni Spirits（Active Theory）、Colonia Zacamil（Adoratorio+60fps）；FWA FOTD：Nocturnal Dream、1minus1；Webby 2026：Signs（DEPT, Accessible Tech）、Warhol Art（BL/S）、WWF Blue Corridors（Ode） | **「Invisible Architecture」**：CSS 取代重 WebGL（省電）、semantic/MX 讓 AI agent 可讀；Tactile Brutalism 與 fluid-glass 並存；有機/破格版面取代 bento |

---

## 3. 跨年趨勢綜合（五維度 × 演進）

> 標註慣例：得主頁實測者視為一手；recap 部落格者標「(recap)」弱權威。

### (a) Architecture / tech — 「重 WebGL 攀升 → 2026 回擺到 CSS 效率 + 機器可讀」
- **2023→2025 單向加重**：Three.js + GSAP + WebGL 從「有一個 collection」變成得主**預設技術 tag**，最終 2025 由兩個 WebGL「世界」站（Messenger、Lando Norris）拿下 Awwwards 前二。底層普遍是 no-code（Webflow/Framer/Wix Studio）+ GSAP + headless。
- **2025 伏筆**：Smashing Magazine 列出 container queries、`:has()`、`text-wrap:balance`、View Transitions、Anchor Positioning 為該年前端標配 → **CSS 開始接手互動**。
- **2026 明顯回擺 (recap)**：「Invisible Architecture」＝semantic HTML / Machine-Experience(MX) 讓 AI agent/crawler 可解析；**以 CSS 特效取代重 JS/WebGL 以省電**；bento 被點名為「DOM 過重時的行動裝置效能風險」。AI 進入流程（Figma Make、Framer AI）。

### (b) Design elements — 「沉浸/空間化上升，2026 出現反拋光逆流」
- reactive cursor、scroll-triggered animation、microinteractions **四年穩定**。
- **空間/世界隱喻反覆出現**：2024 The Maison「樓層」→ 2025 Cartier 六個 3D「alcove」房間，scroll 像逛展。
- **2026 (recap)**：**Tactile Brutalism**（刻意粗糙但精準：1px 邊框、零陰影、硬邊）與 **fluid/frosted glass** 並存；3D cursor-reactive hero、scroll 驅動 3D 場景解構、kinetic type。

### (c) Font pairing — 「表現型 display 當結構 + 樸素 grotesque 當內文」（最薄但訊號一致）
- **耐久核心**：超大/表現型 **display 字當版面結構**（2023 Anzo Studio、Synchrodogs「字即是 grid」；Awwwards 自選 2023 #1 趨勢＝creative typography）貫穿四年。
- **平台推的字（非 Fraunces/Instrument Serif）**：Awwwards 的 sites-of-the-year **font facet** 露出 Aeonik / ABC(Dinamo) / Futura；best-free-fonts 頁推 **Clash Display、Satoshi、Cabinet Grotesk、Geist、PP Mori、HK Grotesk**，並稱「serif 與 display 當道、混搭是基本功」。
- **2026 (recap)**：Neo-Serif × Monospace 對比、viewport(`vw`)-scaled 單字鋪滿、kinetic/variable-weight；三路線 Wide&Loud / Anti-Design / Timeless Luxury。variable fonts 為使能技術。
- 具體「某站用某字」四年皆無法證實；不杜撰。

### (d) Color palette — 「雙色節制 + 單一飽和 accent 壓在近黑/中性底」
- **跨年最強訊號＝duotone（兩色）節制**，且反覆是**一個飽和 accent 對一個中性/近黑底**。平台實測 hex：
  - 2024：Opal `#FFDB01`/`#ffffff`、Don't Board Me `#E33529`/`#AFD8FB`、Igloo `#b6bac5`/`#383e4e`
  - 2025：Lando `#D2FF00`/`#111112`、State of AI `#CAF35A`/`#39175B`、FlowFest `#F3A20F`/`#F97028`、Scout `#FF5432`/`#D7D4D3`、Messenger `#81BFBC`/`#C9D5C3`
  - 2026 (recap)：「chromatic extremes」近黑/炭底 + 單一酸色（cyan/magenta/chartreuse），`#000000` 為 OLED 省電；另有 neo-mint/digital-pastel 柔色逆流、dopamine neon-on-neutral。
- **兩個重要「缺席」**：
  - **Pantone 年度色全部沒出現在得主上**（Viva Magenta 2023、Peach Fuzz 2024、Mocha Mousse 2025）。得獎色盤 ≠ 產業色票。
  - **indigo/violet 完全缺席**，premium beige/brass、olive/clay/terracotta 等「不研究的預設」也未見於得主。

### (e) Layout — 「bento 達峰後疲勞 → 2026 轉有機/破格 + 實驗導覽；spatial scroll 常駐」
- **bento** 在 2023（被命名）→ 2024（Apple/Hopscotch/Bolt 卡片）達峰，**2026 出現效能疲勞**並轉向。
- **spatial / room-based / horizontal scroll 常駐**：2024 Maison 樓層、2025 Cartier alcove、State of AI 明確 tag「Horizontal Layout」。
- **超大字當結構**貫穿四年。
- **2026 (recap)**：退出剛性 12-col，轉向有機/非對稱/重疊/對角；實驗式非線性導覽（radial menu、hidden drawer、互動地圖）。

---

## 4. Moodboard（結構化；色票為研究當日平台頁實測值，非逐一複驗）

**Palette families（得獎簽名）**
1. **Acid-on-near-black dopamine duotone** — `#D2FF00`/`#111112`（Lando）、`#CAF35A`/`#39175B`（State of AI）、2026 酸色/`#000000`。*能量、科技、motorsport。*
2. **Vivid accent on warm neutral** — `#FF5432`/`#D7D4D3`（Scout）、`#FFDB01`/`#ffffff`（Opal）。*消費科技、乾淨。*
3. **Soft "storybook" muted duotone** — `#81BFBC`/`#C9D5C3`（Messenger）、`#b6bac5`/`#383e4e`（Igloo）。*溫和、敘事。*
4. **2026 逆流** — neo-mint / digital pastel（柔、信任感）。
> 共同點：**最多兩色、一個 accent 扛階層**（與 pack 的 accent≤2 高度一致）。

**Type motifs**
- 超大/表現型 **display 當結構** + 樸素 **grotesque 內文**；「混搭即對比」。
- 詞彙：Clash Display / Satoshi / Cabinet Grotesk / Geist / Aeonik / Futura / ABC Dinamo；2026 加 Neo-Serif×Mono、`vw`-scaled、variable/kinetic。
- **不是** Fraunces / Instrument Serif（那是 AI 預設 tell，不是得獎詞彙）。

**Layout / motion motifs**
- spatial「房間/世界」scroll、scrollytelling、horizontal layout、字即 grid、有機/非對稱（2026）。
- reactive cursor、microinteractions、page-as-experience（motion 常破 500ms）。
- tech：WebGL/Three.js/GSAP on no-code + headless；2026 轉 CSS 效率 + semantic/MX。

---

## 5. 融合進 Design Pack：候選建議（本文的重點）

**治理前提（務必遵守）：** canonical corpus > pack-local extensions（prose）> orchestration。**pack-local 只能「新增/加嚴」，要「放寬/反轉/擴張」corpus 規則必須動 canonical corpus，經 owner 核准 + `tools/project_corpus.py` 重生。** 以下皆為**候選**；本文提議、owner 處置。另：font-fashion 與 hex 禁令的重訪是 `ui-design-craft` provenance **自己邀請**的（「衰退最快、每代模型要重訪」）。

| # | 類型 | 對應條目 | 趨勢證據 → 建議 | 摩擦 / 誰決定 |
|---|---|---|---|---|
| **A1** | 重訪 font 禁令 | `ui-design-craft §1`（Fraunces/Instrument Serif 禁令） | 四年得獎詞彙是 **grotesque/display（Clash/Satoshi/Cabinet/Geist/Aeonik/Futura）**，Fraunces/Instrument Serif **缺席** → **保留禁令**（它仍準確分辨「AI 預設 tell」vs「得獎品味」）。可選加一句正面指引：表現型 display 合法，前提是**當結構**（scale/weight/media），非「一個字穿戲服」。 | 低；確認為主。owner 可選加正面句 |
| **A2** | 重訪 hex 禁令 | `ui-design-craft §1`（`#6366f1…` indigo/violet；premium beige；earth 預設） | ~30 個得獎色盤**無一** indigo/violet；Pantone 的 brown/peach 也未上得主 → **保留並確認**三類色 tell 仍成立。 | 低；確認為主 |
| **B1** | 餵軟 heuristic | `COLOR-1001`（palette，heuristic/none） | 以得獎「**單一飽和 accent 壓中性/近黑底**」當正面範例，呼應 §3 accent≤2 與「無 accent 階層」禁令。 | 低；heuristic 可直接補例 |
| **B2** | 餵軟 heuristic | `TYPO-1006`（heading/body pairing，heuristic/none） | 編入耐久配對邏輯：**表現型 display 標題 + 樸素 grotesque 內文、刻意混搭對比**；呼應 §3「階層靠 weight/spacing 非只靠 size」。 | 低；heuristic 可直接補例 |
| **C** | 具體化 spectacle lane | `ANTISLOP-2008`（override 已含「agency/Awwwards/experimental」）+ `motion-craft` When-NOT | 把 override 的**裝置詞彙講具體**：WebGL/3D「房間/世界」spatial scroll、scrollytelling、horizontal layout、字即 grid、reactive cursor、grain/noise、kinetic/variable type、有機/非對稱。維持 override 既有門檻「device 須服務真實構圖」（得主靠 craft 掙得，正是門檻）。motion：得獎站常破 500ms＝**典型 spectacle 範例**，但 reduced-motion floor（§6）與「motion 確認狀態、不表演狀態」**仍然生效**。 | 低；豐富既有 override，不放寬任何規則 |
| **D1** | 張力（會放寬） | `STRUCT-1009`（background blur = avoid，除 modal/sheet 消隱） | 2026 fluid/frosted glass 回潮，但 blur 有效能/對比成本。**建議：production 不放寬 `STRUCT-1009`**；裝飾性 glass 僅限 spectacle lane；若 owner 要全面開放＝corpus 變更 + 效能/§3 對比成本註記。 | 高；**owner + corpus**（勿以 prose 放寬） |
| **D2** | 張力（會放寬） | `§3` accent≤2 / `motion-craft` ≤500ms / `§1` light-default / `§4` 狀態覆蓋 | 得獎美學 maximalist、重 motion、常 dark。**建議：production doctrine 全部保留**；注意張力其實比表面窄——得獎「單 accent 紀律」本就吻合 accent≤2；真正分歧只在 motion 預算與 3D 重量（效能/a11y），屬 spectacle。**切勿把 maximalism 匯入 APP UI。** 另：2026 的「Invisible Architecture / CSS 效率 / bento 效能風險」**反而印證** pack 的節制/效能姿態（外部收斂）。 | 高；多為「維持現狀」+ 記錄為 production↔spectacle 刻意分歧 |
| **D3** | 相容（非衝突） | `STRUCT-1004/1006`（elevation 一致、須配合所選 style） | 2026 Tactile Brutalism（零陰影/硬邊）屬 corpus 已承認的「flat」style，只要**內部一致**即合規，非真衝突。 | 無；註記相容即可 |
| **E** | 印證（無需改動） | `§7` 身分/editorial litmus、`§1` icon-circle grid / placeholder people / emoji-as-icon / fake div-UI 禁令、`ANTISLOP-2001` em-dash | 得獎站**身分強烈**（過 identity/editorial litmus）、**不見** 3-col icon-circle grid、假人、emoji 當 icon、假 div-UI → 現有 ban corpus **仍貼合真實品味**。 | 無；回報「仍成立」 |

**一句話給實作者：** 想「讓它像 Awwwards」時，走 **C 的 spectacle lane 詞彙**；但 **A/B/E 的 production 禁令與預算照常生效**，**D 的放寬一律先問 owner**。

---

## 6. 限制與後續

- **非普查**：~69 筆為抽樣；2026 偏年末 live 窗口、無年度大獎；Webby gallery 歷史年份頁常 fallback 到當年。
- **font-pairing / 部分 2026 色彩**為 recap 二手來源，已標註；具體「某站用某字」未證實。
- **工具限制**：平台為 JS-SPA，WebSearch 摘要/一般 WebFetch 不可靠；本研究以 Playwright/jina-proxy/靜態新聞稿補強並已披露。
- **若要升級為正式 study**：可補 `METHODOLOGY.md`、每站截圖佐證、擴大 2026 月度樣本、對 A1/A2 做一次 corpus 候選 diff 交 owner 審。

**完整得獎清單、每筆來源 URL、被剔除的非得主與工具註記見 `SOURCES.md`。**
