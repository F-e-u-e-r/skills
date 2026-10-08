<h1 align="center">Skills</h1>

<p align="center">
  <em>從真實經驗萃取的角色導向 skill pack —<br><strong>可重用的 skill,而非保存的對話紀錄。</strong></em>
</p>

<p align="center">
  <a href="LICENSE"><img alt="License: MIT" src="https://img.shields.io/badge/License-MIT-blue.svg"></a>
  <img alt="3 packs" src="https://img.shields.io/badge/packs-3-7aa2ff.svg">
  <img alt="15 skills" src="https://img.shields.io/badge/skills-15-7aa2ff.svg">
  <img alt="Status: alpha" src="https://img.shields.io/badge/status-alpha-orange.svg">
  <a href="https://github.com/F-e-u-e-r/skills/issues"><img alt="PRs welcome" src="https://img.shields.io/badge/PRs-welcome-brightgreen.svg"></a>
  <a href="https://github.com/F-e-u-e-r/skills/actions/workflows/checks.yml"><img alt="checks" src="https://github.com/F-e-u-e-r/skills/actions/workflows/checks.yml/badge.svg"></a>
</p>

<p align="center"><a href="README.md">English</a> · <strong>繁體中文</strong></p>

---

這個 repository 收錄數個聚焦、角色導向的 **skill pack**,全部從真實經驗中萃取。
它們把在規劃、執行、設計、審查與驗證等工作中反覆證明有用的模式,整併成可重用的
skill,而非保存當初那些完整的對話、工作流程或來源素材。

目前出貨三個 pack——**共 15 個 skill**:

| Pack | 領域 | Skill 數 | 版本 |
|---|---|---:|---:|
| **Ops Pack** | 執行治理——rigor、委派、驗證、證據、審查 | 10 | 0.3.0 |
| **Planning Pack** | 可執行的規劃契約與對齊(Planning ↔ Ops) | 2 | 0.1.0 |
| **Design Pack** | UI/UX、動效與設計審查 | 3 | 0.1.0 |

各 pack 版本獨立。這些 pack 目前以 **Claude Code plugin** 形式,透過本 repository
的 marketplace 散佈(見下方[安裝](#安裝)),另有**四個選配 hook**——repo 層級、
手動安裝;沒有任何 plugin 會註冊它們(見[強制層:hooks](hooks/README.md))。
每個 pack 可擇一或任意組合安裝。

這些 pack 也會從觀察到的失敗、貢獻者經驗、open-source 意念、研究與針對性評測中
演進。證據強度始終明示:已測行為、已觀察經驗、研究發現,以及未經探測的指引,絕不
被當成同一回事呈現。

> [!NOTE]
> **狀態:早期 alpha。** Ops Pack 處於 **早期 alpha(`v0.3.0`)**;Planning Pack
> 與 Design Pack 為 `0.1.0`。規則會隨真實 session 暴露的缺口調整,而且這些 pack
> 用它們自己的教條[檢驗自己](evidence/ops-pack-evaluation.md)——包含誠實的 null result。
> 歡迎用具體失敗案例開 issue 或 PR。

**一覽**

|  |  |
|---|---|
| **3** 個角色導向 pack | **共 15** 個 skill |
| **4** 個選配 hook | **CI** 每次 push 跑一致性檢查 |
| **狀態** 早期 alpha | **證據** 經驗 + 研究 + 受控評測,含 null result |

## 目錄

- [安裝](#安裝) · [如何打造這些 pack](#如何打造這些-pack) · [`ops-pack`](#ops-pack紀律-skill) · [`planning-pack`](#planning-pack規劃-skill) · [`design-pack`](#design-pack設計-skill)
- [架構與穩定性](#架構與穩定性) · [維護者筆記](#維護者筆記) · [授權](#授權)

## 如何打造這些 pack

這些 pack 是**從經驗萃取**出來的,不是把經驗照抄下來。流程:

1. **從真實工作出發**——操作 session、觀察到的成功與失敗、維護者與貢獻者經驗,
   再加上有用的 open-source 意念、針對性的 repo 研讀,以及聚焦的研究。
2. **整併成角色導向的 skill**——反覆出現的模式變成小而可重用的 skill,而不是
   保存整段對話或整個來源專案。
3. **核對 provenance 與授權**——意念依價值篩選、不整包照抄;來源與寬鬆式授權的
   notices 都有追蹤。
4. **load-bearing 的改動找獨立審查**——作者不是裁判。
5. **能設閘門的就設閘門**——確定性的一致性檢查,以及在可行處的受控 routing /
   行為 / 執行 probe。
6. **證據強度始終明示**——已測行為、已觀察經驗、研究,以及仍未探測的指引,各自
   標示清楚;限制與 null result 保留而非藏起來。

貫穿其中的是「從經驗萃取」——而不是宣稱每一條規則都有實驗證明。

## 安裝

這些 pack 目前以 **Claude Code plugin** 形式散佈。本 repository 就是那個 **marketplace**;加一次,再挑要裝的 plugin。安裝目標用
`plugin@marketplace` 格式,而 marketplace ID 是 `opus-pack`:

```
/plugin marketplace add F-e-u-e-r/skills
/plugin install ops-pack@opus-pack
/plugin install planning-pack@opus-pack
/plugin install design-pack@opus-pack
```

`ops-pack@opus-pack` 裝紀律 plugin(10 個 skill);`planning-pack@opus-pack` 裝規劃 plugin(2 個 skill);`design-pack@opus-pack`
裝設計 plugin(3 個 skill)。擇一或全部三者都裝。Skills 會以 namespace 形式載入
(`ops-pack:operational-rigor`、`design-pack:ui-design-craft`……),用
`/plugin marketplace update` 更新。沒有任何 plugin 會註冊 hooks——它們改變
harness 行為,必須由使用者手動逐一決定(見[強制層:hooks 設定方法](hooks/README.md))。

**或把 skill 複製到位**——全域,或單一專案。每個區塊各自完整:

```bash
# ops-pack(紀律)skills,全域:
mkdir -p ~/.claude/skills && cp -R ops-pack/skills/* ~/.claude/skills/
# planning-pack(規劃)skills,全域:
mkdir -p ~/.claude/skills && cp -R planning-pack/skills/* ~/.claude/skills/
# design-pack(設計)skills,全域:
mkdir -p ~/.claude/skills && cp -R design-pack/skills/* ~/.claude/skills/
# 只裝進單一專案:把 ~/.claude 換成 <repo>/.claude
```

每個 plugin 擇一方法即可:同一 plugin 既裝又複製,會讓每個 skill 出現兩份
(`ops-pack:<skill>` 與 `<skill>`),自動選用時可能取到任一份。Skill 按需
載入:平時只有 description 佔 context,觸發才讀全文。

> **從 `opus-pack` plugin id 升級。** 紀律 plugin 已更名 `opus-pack` -> `ops-pack`;marketplace id 刻意維持 `opus-pack`,所以安裝 id 現為 `ops-pack@opus-pack`。若你在更名前已啟用 `opus-pack@opus-pack`,請執行 `/plugin marketplace update opus-pack`,再執行一次 `/plugin install ops-pack@opus-pack` —— 你的啟用狀態會沿用(執行前舊 id 會標示為「Renamed to ops-pack」),不會遺失任何 skill。透過 managed(管理員)設定強制的啟用不會自動遷移,需由管理員在該處更新。

## `ops-pack`:紀律 skill

| Skill | 用途 |
|---|---|
| `operational-rigor` | 執行紀律：任務契約、行動闘門、以執行驗證、誠實完工 |
| `delegation-and-review` | 委派、雙評審審査、升級階梯、長任務交接、injection 防護 |
| `ground-truth-gates` | 可執行的驗證闘門（golden / replay / project）；含可直接跑的 `template/` |
| `skill-authoring` | 弱模型可執行的規則格式；provenance、衰變、記憶架構 |
| `security-architect` | 非資安專家用的實用安全：auth、secret、web/backend/DB、不可信投稿接收 |
| `product-roadmap` | Product owner 視角：證據先於意見、Now/Next/Later、milestone、任務三分 |
| `personal-goal-planning` | 教練式三層個人 / 職涯目標，含每週檢討迴圈 |
| `domain-evidence-discipline` | 非程式交付物的證據紀律（行銷/研究/資料/營運） |
| `skill-vetting` | 第三方 skill / plugin / hook 執行前先掃 trojan |
| `cross-model-review` | load-bearing merge 前找**不同模型家族**做對抗審査 |

<p><img alt="Ops Pack version v0.3.0" src="https://img.shields.io/badge/version-v0.3.0-orange.svg"></p>

**紀律血統**——十條最高槓桿原則、刻意捨棄了什麼、skill 與 agent 實際如何被叫用、本包如何退化——收錄於 [`ops-pack/README.md`](ops-pack/README.md)（英文）。給硬性強制的選配 repo 層級 hooks 見 [`hooks/README.md`](hooks/README.md)；評測證據見 [`evidence/ops-pack-evaluation.md`](evidence/ops-pack-evaluation.md)。

## `planning-pack`:規劃 skill

| Skill | 用途 |
|---|---|
| `planning` | 動工前的可執行工作契約：framed intent、可測需求、界定 non-goals、相依排序任務；深度 D0–D3（D0 留給 `operational-rigor`） |
| `plan-reconciliation` | 執行開始後把核准計畫與現實對齊——不再吻合時修訂，完成時收尾——皆附證據 |

`planning` 與 `plan-reconciliation` 組成 **Planning Pack**（Planning ↔ Ops）：它們負責*要蓋什麼、計畫如何變*，而 `ops-pack` 的執行紀律 skill 負責*把它做出來*。Planning 產物從不等於執行授權，Planning 深度也不折抵執行的 rigor。

**已記錄的弱層限制(QUALIFIED-ADOPTABLE)。** Planning Pack 以 **QUALIFIED-ADOPTABLE:14 項行為主張中 13 項乾淨、1 項已記錄的弱層限制、0 項有害行為、D0 保留** 發佈。那唯一未結的主張是一項已記錄的弱層限制,在此載明而非略過。限制內容:`plan-reconciliation` 能可靠保留 revalidation / re-approval / Ops 授權閘門,但在較弱的執行層,它不能可靠地*自行*執行對「缺漏」敏感的整體計畫 orphan 偵測(傾向描述或請求 revalidation,而非自己做)。失效模式是 fail-safe——偵測不足時預設「不可 resume / 升級」,絕不會誤判為「safe to resume」。

> **遷移——Planning 已獨立成自己的 plugin(ops-pack 0.3.0)。** `planning` 與 `plan-reconciliation` 在 v0.2.0 前內含於 `ops-pack` plugin;自 `ops-pack` 0.3.0 起,它們以獨立的 **`planning-pack`** plugin(版本 0.1.0)發佈。這是**有記錄的 namespace 遷移,不是透明相容**:沒有跨 plugin 的 skill 改名橋接,所以原本啟用 `ops-pack@opus-pack`、更新時**未**安裝 `planning-pack` 的使用者,會發現那兩個 skill **直接消失**。該消失是**預期且在此載明的——不是 silent loss**。要恢復完整集合,請**同時**安裝 `ops-pack@opus-pack` **與** `planning-pack@opus-pack`;安裝 `planning-pack` 後,`planning` 與 `plan-reconciliation` 會在 `planning-pack:` namespace 下**恰好一次**回歸。完整的規劃 + 執行設定需要兩者都裝。見 `ARCHITECTURE.md` §3。


## `design-pack`:設計 skill

三個設計工藝 skill，把同一套 doctrine 風格——數值預算、禁用模式、可觀測闘門——應用到視覺設計工作。像任何 plugin 一樣安裝（見上方[安裝](#安裝)）；版本獨立（目前 0.1.0）。這些 skill 可獨立成立——`design-review-gate` 逐字內載 ops-pack 的兩條 load-bearing 條款——與 `ops-pack` 並用更利，但不需要它。

| Skill | 用途 |
|---|---|
| `ui-design-craft` | UI 組構與視覺工藝：版面、階層、字體排印、色彩、狀態品質、反通用設計 |
| `motion-craft` | 動效行為：時長、easing、手勢/彈簧、編排、reduced-motion、效能 |
| `design-review-gate` | 把結構化設計審査化為可量測、可排序的 findings |

**它如何保持一致。** 設計指引不是在三個 skill 之間手抄：它由單一的設計語意 canonical corpus，經確定性建置，投影成各 `SKILL.md` 選擇性取用的 skill 本地參考檔。corpus 是主要權威；pack-local extensions 在其下補充 production 指引。完整 corpus / 投影架構見 [`ARCHITECTURE.md`](ARCHITECTURE.md)。

**證據。** `ui-design-craft` / `motion-craft` 的闘門與 `design-review-gate` §4 已以 smoke 等級 probe 驗證（全新弱層 agent、bare/ruled 兩臂、預期先寫）；審査迴圈 §§1–3 尚未 probe，紀錄保留一輪作廢與一個 NULL（皆在各 skill 自己的 provenance 筆記）。hex 與字體時尚禁令衰變最快——每個模型世代都要重驗。一份獨立的 [Impeccable](https://github.com/pbakaus/impeccable) 相容性研究（只有觀察、未 vendor 任何內容）放在 [`research/design-pack/2026-09-impeccable-compatibility-study/`](research/design-pack/2026-09-impeccable-compatibility-study/)。

## 架構與穩定性

完整 normative 契約:**[`ARCHITECTURE.md`](ARCHITECTURE.md)**——tiers、穩定性、
1.0 前 migration、plugin dependency class、adjacent-skill 規則、routing-contract
變更與 reference grammar 的 canonical source。本節只是摘要投影;**任何不一致以
`ARCHITECTURE.md`(英文)為準。**

**Skill tiers**(`ops-pack` 與 `planning-pack` 的 agent 紀律 skill;canonical map 在
[`metadata/skill-tiers.json`](metadata/skill-tiers.json)):

<!-- BEGIN GENERATED SKILL TIERS -->
| Tier | Skills |
|------|--------|
| Core(7) | `operational-rigor`、`delegation-and-review`、`ground-truth-gates`、`cross-model-review`、`skill-authoring`、`skill-vetting`、`security-architect` |
| Domain adapter(5) | `product-roadmap`、`personal-goal-planning`、`domain-evidence-discipline`、`planning`、`plan-reconciliation` |
<!-- END GENERATED SKILL TIERS -->

Core skill 是共用的 agent 執行 doctrine;domain adapter 把該紀律套到更窄的領域。
skill tier 與 plugin dependency class 是兩條獨立的軸。

<!-- BEGIN GENERATED PLUGIN DEPENDENCIES -->
**Plugin dependency class。** `design-pack` 是 **`recommended-with ops-pack`**:
其 skill 各自能獨立完成主要 workflow(`motion-craft` 完全無跨包依賴;兩條
load-bearing 的跨包條款以逐字方式內載、能獨立成立),而 `ops-pack` 補上其指標
所指的額外 rigor。`planning-pack` 是 **`recommended-with ops-pack`**:它能獨立產出可用的 plan,但會指名它交棒給 Ops 的執行防護(授權、證據、不可回退)。見 `ARCHITECTURE.md` §4。
<!-- END GENERATED PLUGIN DEPENDENCIES -->

**穩定性一句話:** published skill 是穩定介面、預設**加法演進**(additive by
default)——新能力以新 skill 或新 plugin 出現,而非移除、改名、搬移或收窄既有者的
trigger scope;唯一的 breaking-migration 窗口(deprecation notice + transition
window + 相容涵蓋,且須完成而非僅宣告)只在該 skill 所屬 source plugin 的 1.0
之前(各 plugin 版本獨立);該 1.0 之後 published skill 無限期保留、不預先授權任何
破壞性路徑。細節見 `ARCHITECTURE.md` §§2–3。

詳細的評測紀錄、provenance 與研究歷史放在 [`evidence/`](evidence/README.md)（含 [`evidence/ops-pack-evaluation.md`](evidence/ops-pack-evaluation.md) 與 [`evidence/provenance.md`](evidence/provenance.md)）與 [`research/`](research/)。

## 維護者筆記

推送前跑 `python3 .github/checks.py`——CI 跑的同一套一致性閘門(skill
frontmatter、四處版本號一致、README 相對連結、零寬/雙向字符清查、hooks
測試套件在 CI 另行執行)。常設不變量:plugin 套件永遠不得聲明或註冊
hooks(不得有 `hooks/hooks.json`、`plugin.json` 不得有 hooks 欄位)——
安裝段聲明的同意姿態依賴這一點。

這個工作目錄可能有兩份相同的 skill:`ops-pack/skills/` 是發佈源;`.claude/skills/`
是本機即用安裝,已由 git ignore。改任何一份 SKILL.md → 同步另一份
(`cp -R ops-pack/skills/. .claude/skills/`),推 GitHub 前逐一比對每個已發佈 skill
(本機的 project skill 才不會被誤判為漂移):
`for d in ops-pack/skills/*/; do diff -rq "$d" ".claude/skills/$(basename $d)"; done`。
這個迴圈只檢查仍存在於 `ops-pack/skills/` 的目錄(而 `cp -R` 從不刪除),所以移除或
改名一個已發佈 skill 時,要在同一次修改裡手動刪掉 `.claude/skills/` 裡
對應的舊目錄;改任一語言的 README →
同步鏡像另一份。

發版命名:每次 `plugin.json` 版本號提升,都要打對應的 `vX.Y.Z` git tag 並建立 GitHub
Release(仍在 alpha 期間標為 pre-release),README 的版本 badge 也寫 `vX.Y.Z`。`v0.1.16`
之前的 tag 用舊的 `alpha-X.Y.Z` 形式;中間的版本從未個別打過 tag,`v0.1.16` 是第一個正式的 release of record。

## 授權

本 repository 的 skill pack 以 [MIT License](LICENSE) 發佈——Copyright (c) 2026 F-e-u-e-r。

本包納入並改作了採寬鬆式授權(MIT 與 Apache-2.0)的第三方作品;這些授權要求隨附的版權與授權聲明,集中收錄於 [THIRD-PARTY-NOTICES.md](THIRD-PARTY-NOTICES.md)。最具體的一例是 `verify-before-stop` hook——改作自 Curtis Chou(其上游為 Miguok)的 MIT 授權程式碼。整條鏈路不含任何 copyleft(GPL/AGPL/LGPL)。`guideline *.txt` 來源草稿為私人來源素材(擁有者自有,及 firaen22 的私人筆記),不隨發佈散佈(已由 `.gitignore` 排除)。

完整來源歷史與致謝見 [`evidence/provenance.md`](evidence/provenance.md)。
