# ADJUDICATION — Award-Site 研究 → Design Pack doctrine 調解紀錄

**狀態:研究/裁決紀錄(research record),非 pack 能力。** 本文記錄 owner 對
`REVIEW.md` 第 5 節候選方向的裁決、如何落到 canonical corpus、以及佐證的限制。
它**不被任何 loader 讀取、不隨 plugin 出貨**。

**關鍵原則:research evidence ≠ runtime doctrine。** `REVIEW.md` / `SOURCES.md`
是對 2023–2026 得獎站的抽樣觀察,它可以**支持** corroboration、heuristic 精煉、
spectacle 詞彙;它**不建立**:普世設計法則、完整得獎站普查、特定站用特定字體、
新的 a11y/效能例外、未來趨勢永久性。canonical rule 內不嵌任何 award-site 的
hex 值或流行字體名。

編製:2026-10-15。對應 pack:design-pack 0.1.0(本 pass 不決定版本)。
調解前 corpus SHA `16ad01fb…`(sealed, merge `44f1044`);本 pass 之後的工作樹
corpus SHA `86702b24…`（= `CANONICAL_CORPUS_SHA256`，目前權威 byte identity；merge SHA 依 owner §2 Option A 維持 `44f1044`，見 §4 provenance 語意）。

---

## 1. 裁決矩陣(owner 核定)

| # | 對應 canonical 擁有者 | 裁決 | 落點 |
|---|---|---|---|
| **A1** font 禁令 | `ui-design-craft §1`(prose;Fraunces/Instrument Serif) | **KEEP / CORROBORATED** | 黑名單不動;不新增字體 allowlist。正面 lesson(表現型 display 當結構才合法,非換裝飾字體)折入 B2 的 `TYPO-1006` heuristic,保持 generic |
| **A2** color 禁令 | `ui-design-craft §1`(prose;indigo/violet、premium-beige/brass、earth) | **KEEP / CORROBORATED** | 不動;**不**因得獎樣本缺席而升級為新硬色禁令(樣本非普查,多數 hex 未經 orchestrator 複驗) |
| **B1** palette heuristic | `COLOR-1001`(corpus,heuristic/contextual/none) | **ACCEPT-CHANGE** | `effective_semantics.scope` + `public_expression` 加入:單一飽和 accent 壓中性/近黑/低彩底為強預設,一個 accent 扛階層;**保留** accent-count 預算、對比/a11y、product fit、無強制 dark mode |
| **B2** type-pairing heuristic | `TYPO-1006`(corpus,heuristic/contextual/none) | **ACCEPT-CHANGE** | `scope` + `public_expression` 加入:表現型 display 當 identity/結構、body/介面文字節制可讀、對比 intentional 且 role-based;**非**強制字體配對;**保留** readability/hierarchy/density/typography budget |
| **C** spectacle lane | `ANTISLOP-2008`(corpus,override 已含 agency/Awwwards/experimental) | **ACCEPT-CHANGE(enrich;gate 不放寬)** | `override` + `public_expression` 補裝置**例子**(spatial/room/world scroll、scrollytelling、horizontal narrative、typography-as-grid/structure、reactive cursor、kinetic/variable type、organic/asymmetric、WebGL/3D-as-composition、grain/noise-serving-composition);並**加嚴**:明寫「these devices are examples that may qualify only when composition justifies them, never defaults for ordinary product or app UI」。既有 gate「device serves a real composition」原文保留 |
| **D1** glass/blur | `STRUCT-1009`(corpus,blur=avoid) | **REJECT-RELAXATION / HELD** | 不動。2026 fluid/frosted-glass 回潮僅 research context;不加裝飾性 glass 例外到 production UI。若要全面開放 = 另案 corpus 變更 + 效能/對比成本,須 owner 決策 |
| **D2** maximalism/motion/dark | `motion-craft` ≤500ms、`§3` accent≤2、`§1` light-default、`§6` reduced-motion、狀態覆蓋(prose) | **KEEP / CORROBORATED** | production doctrine 全部保留;`motion.md` body 本 pass **byte-identical 未動**。得獎「單-accent 紀律 / CSS 效率 / bento 效能風險」反而**印證**既有節制姿態(外部收斂),記錄為 production↔spectacle 刻意分歧 |
| **D3** tactile brutalism | `STRUCT-1004/1006`(flat elevation 須配合所選 style) | **CORROBORATED / NO-CHANGE** | 2026 零陰影/硬邊屬 corpus 已承認的 style-consistent flat,非衝突。僅此處記錄,不新增 corpus 條目 |
| **E** 既有 anti-slop | `§7` litmus、icon-circle grid / placeholder people / emoji-as-icon / fake div-UI、`ANTISLOP-2001` em-dash | **CORROBORATED / NO-CHANGE** | 得獎站身分強、不見這些 tell → 現有 ban 仍貼合真實品味。僅記錄 corroboration,**不**複製成重複 corpus 條目 |

**語意 delta = 恰好 3 筆 corpus 記錄(COLOR-1001、TYPO-1006、ANTISLOP-2008)。
零 SKILL.md body 編輯。** A1/A2 的 production 禁令本就存在於 `ui-design-craft §1`
prose,未動。

## 2. 被明確「拒絕 / 保留(held)」的放寬

- **blur/glass 放寬到 production UI**(D1)— 拒絕。
- **把 maximalism / 重 motion / dark-default / WebGL-first 匯入 ordinary app UI**
  (D2)— 拒絕;spectacle 僅限 `ANTISLOP-2008` override 既有 gate 之內。
- **放寬 ≤500ms / reduced-motion floor / 狀態覆蓋**(§8 motion 邊界)— 未觸碰;
  `motion.md` 未動,本 pass 不走 prose 偷渡任何 motion 放寬。
- **把 award 樣本的缺席升級為新硬色禁令、或把流行字體名寫入 canonical**
  (A1/A2)— 拒絕。

## 3. 佐證限制(忠實轉錄自 `SOURCES.md` / `REVIEW.md`)

- **非普查**:~69 筆為抽樣(2023:14 / 2024:17 / 2025:18 / 2026:20);2026 偏年末
  live 窗口、**無 SOTY/FOTY 2026**。故任何「所有得獎站都…」或「某配置最佳」皆
  **不可**由此宣稱。
- **font→site 歸屬最薄**:四年皆**無法**把具體字體綁到特定得主(平台頁不公開字體
  欄);代理**拒絕杜撰**。故 B2/A1 的 heuristic 保持 generic(角色/結構),
  **不**命名「某站用 Clash Display/Satoshi…」。
- **color hex** 多為平台頁研究當日實測值,**非逐一由 orchestrator 複驗**;故
  B1 heuristic **不**嵌任何 hex,僅表達「單一飽和 accent 壓中性/近黑底」的結構。
- **indigo/violet 缺席、Pantone 年度色未上得主** = corroboration,**非**完整census;
  不升級為新禁令(A2 保留現狀)。
- **2026 多為二手 recap**(Tactile Brutalism、fluid-glass、Invisible Architecture),
  已於 REVIEW 標「(recap)」弱權威;據此僅做 corroboration(D3)或 held(D1),
  不做 production 變更。
- **工具限制**:平台為 JS-SPA,WebSearch 摘要/一般 WebFetch 會幻覺;研究以
  Playwright/jina-proxy/靜態新聞稿補強並已披露。

## 4. 確切變更的 canonical 條目 / surfaces

- `corpus/design-pack/public_records.json`:`COLOR-1001`(scope+public_expression)、
  `TYPO-1006`(scope+public_expression)、`ANTISLOP-2008`(override+public_expression)。
- generator `design-pack/tools/project_corpus.py`:`CANONICAL_CORPUS_SHA256`
  `16ad01fb…`→`86702b24…`(編輯 canonical 後的強制重 pin);`CANONICAL_MERGE_SHA`
  `44f1044…` **維持原值**（owner §2 Option A：歷史性 canonical-lineage／semantic-publication checkpoint；過渡期曾暫標為 `uncommitted-working-tree-pending-owner-integration`，本 readiness repair 已依 Option A 還原為 `44f10443c16e926515af86ebdd1d52e003ed98cc`，**不**另建 commit/PR 回填、不追逐 commit 自身 hash）。
- generated(由 generator 重生,**非手改**):`generated/runtime.json`、
  `manifest.json`、各 skill `references/generated/{color,typo,antislop}.md`(語意),
  其餘 shard header 的 SHA 行(cosmetic 傳播)。
- 手維護 `design-pack/generated/README.md`：2 行 SHA 參照同步更新（內部一致；SHA-256 = `86702b24…`、merged = `44f1044`）。

**Provenance 語意（owner §2 Option A／§4，明確記錄）**：`CANONICAL_MERGE_SHA` 是歷史性 canonical-lineage checkpoint，**非**宣稱為「含目前調解後 corpus bytes 的 commit」；目前 corpus byte identity 由 `CANONICAL_CORPUS_SHA256`（`86702b2419d75372e345448728fc9d0b92b82bcc8e80b169bf422787280f2b94`）擁有，即 fail-closed 位元身分，由既有 generator／projection 驗證消費。本 pass **不**把此釐清擴大為 schema 改名（未來 `CANONICAL_LINEAGE_SHA` 之類屬另案，未授權）。

**未觸碰(刻意)**:全部 SKILL.md body、`motion.md` body、`STRUCT-1009`、
所有 prose 禁令、`normative-*.json`、2026-09 impeccable study(其 `16ad01fb` 參照
為**歷史性**,描述當時 sealed 狀態,無 live validator 對 moving corpus 重驗之)。

**凍結行為證據（未改寫）**：`behavioral-proof/evidence/PROPOSED_*.md` 的 projection header 保留 proof-time 的 `uncommitted-…` 標記，為當時快照之歷史事實；本 readiness repair 依 owner §7 不改寫凍結行為結果，且該目錄非 generator 對 `design-pack/` 的輸出、不被任何 §8 靜態閘掃描。

## 5. 驗證指標

- static:`.github/design_pack_checks.py`、`design-pack/tools/test_projection_checks.py`
  (two-sided)、`.github/checks.py`、`git diff --check`、deterministic regen(run×2 無差)
  — 結果見交付封包 D/E。
- behavioral:pre-registered focused battery(model `claude-haiku-4-5-20251001`),
  結果見 `./behavioral-proof/RESULTS.md`(pre-registration 於
  `./behavioral-proof/PRE-REGISTRATION.md`,跑任何一臂前凍結)。

## 6. 版本 / 發布

本 pass **不**決定版本、不 commit/push/PR/tag/release。semantic delta(3 筆 corpus
heuristic 擴充,無 production 放寬)確立後,由 owner 另行決定 patch / minor /
research-only 與 tracked 整合。merge SHA 依 owner §2 Option A 已定（維持 `44f1044` 為 lineage checkpoint，不隨整合 commit 回填、不追逐 commit 自身 hash）。
