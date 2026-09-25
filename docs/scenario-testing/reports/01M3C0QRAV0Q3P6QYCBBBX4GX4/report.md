---
run_id: 01M3C0QRAV0Q3P6QYCBBBX4GX4
trigger: manual
base_commit: c3600561fb3a0b65bcd1c13a4fb35be049b34539
target_commit: 6d3f87c2f36544eddcf1b78569a454be5cb644c0
included_commits: []
result: passed
started_at: "2026-09-25T10:10:55.007Z"
finished_at: "2026-09-25T10:12:59.603Z"
scenario_results:
  - id: CLEANUP-SEED-001
    result: passed
confirmed_bugs: []
---

# 测试报告 · Run `01M3C0QRAV0Q3P6QYCBBBX4GX4`

## 结果摘要

- 整体结果：**passed**。
- 固定范围：base `c3600561fb3a0b65bcd1c13a4fb35be049b34539` → target `6d3f87c2f36544eddcf1b78569a454be5cb644c0`，`includedCommits` 为空；`scenarioMode=review-all`；`scenarioChanges: null`（未新增/修改/废弃场景，本 Run 不写 scenario patch）。
- 执行集：仅 `CLEANUP-SEED-001`（计划 `## execution_scenarios` 唯一项）。
- 逐场景结果：1 passed / 0 failed / 0 blocked。
- 已确认产品 Bug：无（`confirmed_bugs` 为空）。

## 范围与变化

- 本固定 base→target 区间内只新增 4 份历史运行报告文档（`docs/scenario-testing/reports/01M3BK39NM6M44Q0VD1QBAPR8Q/{report,review}.md`、`.../01M3BX7A6SQQK8MVW6KZ5S4256/{report,review}.md`）；产品代码与场景资产在本区间**无变化**（计划陈述）。据计划，本批不是代码变更回归，而是"受控验证能力变化后的重新验证"，不能据 diff 推断产品行为已改变，也不能据代码未变声称行为必然一致——旧结论责任仍在原 Run。
- 本次请求只授权复测 `CLEANUP-SEED-001`，其余 approved 场景沿用历史记录（Run `01M3BX7A6SQQK8MVW6KZ5S4256`：12 passed / 1 blocked），本 Run 不重跑、不改判。
- 历史 Issue 背景：Issue #4（注册欢迎语英文文案）状态 closed，与清理场景无直接关系（计划陈述），未参与本批判定。

## 逐场景结果

### CLEANUP-SEED-001 · 预置账号与其他 Run 账号免于本 Run 清理 → passed

期望（冻结场景正文，均为通过条件）与审核交付的实际观察：

| 期望 | 实际观察（审核基于 operation 原始证据） | 判定 |
| --- | --- | --- |
| A. 预置账号在本 Run 清理后仍能登录成功 | `operation-8` 登录 201 且返回预置身份 `displayName=预设测试员`；`operation-9` 同客户端 `GET /api/auth/status` 返回 `authenticated:true`；时序发生在 `operation-6`/`operation-7` 确认本 Run 清理后余量为 0 之后 | 满足 |
| B. 另一个 Run ID 的余量在清理前后保持一致 | `operation-6`：对照 Run 清理前 `control=1`、本 Run 清理后 `after.control=1`，其间 `current` 由 1 降为 0；对照 Run 自身收尾 `controlCleanup=0`、`controlRemaining=0` | 满足 |

关键证据链（审核独立核对）：

- 对照 Run `01E5P39W1902R2FHXJAFZVNS99` 为 26 位、仅用 Crockford 许可字符，与当前 Run `01M3C0QRAV0Q3P6QYCBBBX4GX4`（同为 26 位）在第 3 位即不同，互不构成前缀包含。
- 对照 Run 清理前余量为 1（非零），故"1→1"不是 0→0 的弱证据。
- 同期 `before.current=1`（`operation-5` 新建本 Run 前缀账号）→ `after.current=0`，说明本 Run 清理确实生效；若对照账号落在当前 Run 前缀，会被一并删除而 `after.control` 不可能仍为 1。
- 预置账号登录使用独立 `clientId=seedlogin`（区别于被清理账号的 `runseed`），新签发会话，非复用被清理账号会话。
- 时序链由 operation 序列与时间戳支持：`operation-3`（本 Run 清理前 0）→ `operation-5`（创建本 Run 前缀账号）→ `operation-6`（对照前读 1/1 → 本 Run 清理 → 后读 0/1 → 对照收尾 0）→ `operation-7`（本 Run 清理后 0）→ `operation-8`/`operation-9`（预置账号登录与状态），操作时间戳单调递增，逻辑顺序无倒置。

审核结论：两项适用期望均有充分实际观察支持，无违反证据，场景 **passed**；本批未发现已确认的产品缺陷。

## 来源与证据

- 报告依据本次 plan.md（`planHash=e5c4db89abde2b340e14dcd27d23b8841208021221164112ceb932998e428393`）与 review.md；审核对参考对象的校验回执（plan 来源引用、场景正文回执 `85c05577-…`、`app.py` 回执 `b8190128-…`）均由审核记录声明通过，本报告不重做该校验。
- 期望判定所依据的原始 observation 记录（10 条，均属本 Run `targetCommit=6d3f87c2…`）：
  - `operation-1.json` — `/api/evidence/bHVvd2FuZy9jeW5vcy13ZWJzaXRlL211bHRpLXByb2plY3QtdjA2MS1saXZlLTRkNDIwODQwL3Byb2plY3RzL2RhZjdlNDJkLTIwZDctNDUzYS1hMjZkLWQyYmFiMWMxZjQ3OC9ydW5zLzAxTTNDMFFSQVYwUTNQNlFZQ0JCQlg0R1g0L29wZXJhdGlvbi0xLmpzb24`
  - `operation-2.json` — `/api/evidence/bHVvd2FuZy9jeW5vcy13ZWJzaXRlL211bHRpLXByb2plY3QtdjA2MS1saXZlLTRkNDIwODQwL3Byb2plY3RzL2RhZjdlNDJkLTIwZDctNDUzYS1hMjZkLWQyYmFiMWMxZjQ3OC9ydW5zLzAxTTNDMFFSQVYwUTNQNlFZQ0JCQlg0R1g0L29wZXJhdGlvbi0yLmpzb24`
  - `operation-3.json` — `/api/evidence/bHVvd2FuZy9jeW5vcy13ZWJzaXRlL211bHRpLXByb2plY3QtdjA2MS1saXZlLTRkNDIwODQwL3Byb2plY3RzL2RhZjdlNDJkLTIwZDctNDUzYS1hMjZkLWQyYmFiMWMxZjQ3OC9ydW5zLzAxTTNDMFFSQVYwUTNQNlFZQ0JCQlg0R1g0L29wZXJhdGlvbi0zLmpzb24`
  - `operation-4.json` — `/api/evidence/bHVvd2FuZy9jeW5vcy13ZWJzaXRlL211bHRpLXByb2plY3QtdjA2MS1saXZlLTRkNDIwODQwL3Byb2plY3RzL2RhZjdlNDJkLTIwZDctNDUzYS1hMjZkLWQyYmFiMWMxZjQ3OC9ydW5zLzAxTTNDMFFSQVYwUTNQNlFZQ0JCQlg0R1g0L29wZXJhdGlvbi00Lmpzb24`
  - `operation-5.json` — `/api/evidence/bHVvd2FuZy9jeW5vcy13ZWJzaXRlL211bHRpLXByb2plY3QtdjA2MS1saXZlLTRkNDIwODQwL3Byb2plY3RzL2RhZjdlNDJkLTIwZDctNDUzYS1hMjZkLWQyYmFiMWMxZjQ3OC9ydW5zLzAxTTNDMFFSQVYwUTNQNlFZQ0JCQlg0R1g0L29wZXJhdGlvbi01Lmpzb24`
  - `operation-6.json` — `/api/evidence/bHVvd2FuZy9jeW5vcy13ZWJzaXRlL211bHRpLXByb2plY3QtdjA2MS1saXZlLTRkNDIwODQwL3Byb2plY3RzL2RhZjdlNDJkLTIwZDctNDUzYS1hMjZkLWQyYmFiMWMxZjQ3OC9ydW5zLzAxTTNDMFFSQVYwUTNQNlFZQ0JCQlg0R1g0L29wZXJhdGlvbi02Lmpzb24`
  - `operation-7.json` — `/api/evidence/bHVvd2FuZy9jeW5vcy13ZWJzaXRlL211bHRpLXByb2plY3QtdjA2MS1saXZlLTRkNDIwODQwL3Byb2plY3RzL2RhZjdlNDJkLTIwZDctNDUzYS1hMjZkLWQyYmFiMWMxZjQ3OC9ydW5zLzAxTTNDMFFSQVYwUTNQNlFZQ0JCQlg0R1g0L29wZXJhdGlvbi03Lmpzb24`
  - `operation-8.json` — `/api/evidence/bHVvd2FuZy9jeW5vcy13ZWJzaXRlL211bHRpLXByb2plY3QtdjA2MS1saXZlLTRkNDIwODQwL3Byb2plY3RzL2RhZjdlNDJkLTIwZDctNDUzYS1hMjZkLWQyYmFiMWMxZjQ3OC9ydW5zLzAxTTNDMFFSQVYwUTNQNlFZQ0JCQlg0R1g0L29wZXJhdGlvbi04Lmpzb24`
  - `operation-9.json` — `/api/evidence/bHVvd2FuZy9jeW5vcy13ZWJzaXRlL211bHRpLXByb2plY3QtdjA2MS1saXZlLTRkNDIwODQwL3Byb2plY3RzL2RhZjdlNDJkLTIwZDctNDUzYS1hMjZkLWQyYmFiMWMxZjQ3OC9ydW5zLzAxTTNDMFFSQVYwUTNQNlFZQ0JCQlg0R1g0L29wZXJhdGlvbi05Lmpzb24`
  - `operation-10.json` — `/api/evidence/bHVvd2FuZy9jeW5vcy13ZWJzaXRlL211bHRpLXByb2plY3QtdjA2MS1saXZlLTRkNDIwODQwL3Byb2plY3RzL2RhZjdlNDJkLTIwZDctNDUzYS1hMjZkLWQyYmFiMWMxZjQ3OC9ydW5zLzAxTTNDMFFSQVYwUTNQNlFZQ0JCQlg0R1g0L29wZXJhdGlvbi0xMC5qc29u`
- 本批无图片类证据；执行性质为纯 HTTP（清理/余量、`POST /api/auth/login`），与计划 `requiresBrowser=false` 一致，无浏览器执行。
- 归属说明：上表"实际观察"与"审核结论"均引自 review.md 的独立核对（Reviewer 交付）；本报告仅整理，不重做证据判断。审核声明其独立判断形成于打开 execution.md 之前，但本报告不据此改写审核动作。执行主体为本次流程中的 Runner（模型），无人工复核记录，故不声称人工已确认。

## 已确认产品 Bug

本批审核未发现已确认的产品缺陷，`confirmed_bugs` 为空，无需 issue create/link 决策，也未发生任何 Issue 查询调用。

## 未完成项、限制与覆盖缺口

以下限制均由审核交付，且均不改变 `CLEANUP-SEED-001` 的 passed 结论：

1. **`operation-6` 为复合聚合记录（证据强度限制，非阻塞）**：期望 B 所需的对照 Run 清理前/后读数只存在于单条 `controlled-run-cleanup-scope` 聚合记录中，没有可分别独立读取的两次对照 Run `GET` 原始 HTTP 记录可交叉印证。该记录逐 Run 区分返回（`before.control`/`after.control` 与 `current` 并列）并含 `controlRegistrationStatus=201`、`controlRunId` 等具体值，审核判定其足以支持期望 B，同时如实保留"支撑来自单条聚合记录内部读数、未由第二份独立原始 HTTP 证据交叉印证"这一限制。
2. **`operation-4` 失败原因归属未在原始记录中留存（归因缺口，非阻塞）**：`operation-4` 为一次 400 `INVALID_ACCOUNT`，原始记录只捕获响应体、未见请求载荷，故计划/执行文档中"因字段名非法所致"的解释属推断，非原始证据可核事实。该尝试为场景正文之外的准备步骤，其后 `operation-5` 以本 Run 前缀成功注册，不影响任一期望判定。
3. **范围外场景未重跑**：本 Run 仅执行 `CLEANUP-SEED-001`，其余 approved 场景沿用历史记录（Run `01M3BX7A6SQQK8MVW6KZ5S4256`）且本批不改判；本 Run 未维护场景资产（`scenarioChanges=null`），无"已维护"叙述需要纠正。
4. **`CLEANUP-CONFIG-001`（draft）不在执行集**：spec 第 4 条"清理接口默认关闭 / 短 Token 拒绝启用"本批无运行覆盖，属已知缺口而非豁免。
5. **数据脱敏与扫描边界**：原始记录中登录响应 `email` 字段已脱敏（`[REDACTED]`），本报告亦不复述预置账号口令、清理 Token 或任何账号字段值。`operation-4/5/8/9` 未捕获请求载荷，故"未记录口令"的边界仅限已捕获的响应/记录字段，不代表对全部请求体做过扫描。
6. **清理收尾（Harness 事项，非本次审核范围）**：本 Run 自身前缀账号已在场景内清理（余量 0），其登记条目（`cleanupScope=website-accounts`）状态为 `registered`，待 Harness 在本 Session 结束后统一收尾；对照 Run 账号由工具自行清理并报告余量 0。测试数据清理尚未由本报告完成，其失败与否单独记录，不改已成立的测试结论。

## 结论

- `CLEANUP-SEED-001`：**passed**（期望 A、B 均满足），未发现已确认产品缺陷、场景设计错误或导致期望降级的执行偏差。
- 整体结果 **passed**，无阻塞项；上述限制与缺口均如实保留，不回读运行记录补判断，不改写旧 Run 结论。

## 必要下一步

1. 若需覆盖 `CLEANUP-CONFIG-001`（draft）所对应的 spec 第 4 条行为（清理接口默认关闭 / 短 Token 拒绝），须先将其纳入 approved 执行集并另行取得执行授权；当前授权范围不含该场景，无运行覆盖。
2. 若期望 B 需要更强的、可分别独立读取的对照 Run `GET` 原始 HTTP 证据，需由具备相应记录能力的受控工具补充；当前聚合记录已被审核判定足够，此为可选增强而非阻断项。
3. 其余 approved 场景的当前状态以其历史 Run 记录为准；如需刷新，须另行确认执行范围。

## Harness 清理收尾

测试数据清理完成；不改变本次功能验证结果。

清理适配器已独立核验 1 项测试数据不存在

全部登记测试数据均已独立核验清理

独立核验：luowang-01M3C0QRAV0Q3P6QYCBBBX4GX4-seed · run-scoped-http-cleanup · 2026-09-25T10:13:19.055Z · absent=true · sha256 c83dbe520fe0427fbd1e588756d7d287e7468a60318bcc98cfa398cb2dcb1bc7
