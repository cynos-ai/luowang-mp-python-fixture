---
run_id: 01M3YGS2GG8RGM2VZ53ZZ7TRRB
trigger: manual
base_commit: 9c864dff252814432d4e1ec7776a60c04eac32ae
target_commit: 20e0681ba85f02beb5396dab5f7458c76905aa40
included_commits: []
result: passed
started_at: 2026-10-02T14:37:36.063Z
finished_at: 2026-10-02T14:38:55.877Z
scenario_results:
  - id: AUTH-LOGIN-001
    result: passed
confirmed_bugs: []
---

# 测试报告 — Run `01M3YGS2GG8RGM2VZ53ZZ7TRRB`

## 结论

本次仅回归唯一 approved 场景 `AUTH-LOGIN-001`，在 target `20e0681ba85f02beb5396dab5f7458c76905aa40` 上 **passed**。全部既定期望均有本轮实际执行证据支持，未发现产品缺陷，无阻塞原因（`blockingReasons` 为空），整体结果为 `passed`。

发布状态未在本报告中表达；本报告只陈述测试结果。

## 范围与固定版本

- 请求：本轮仅回归已有的 approved 场景 `AUTH-LOGIN-001`，完整验证该场景全部既定期望；按 Run 创建并登记独立合成账号；注册只作为登录场景的前置准备，不扩大到注册或存储观察场景，不弱化场景期望；不删除预置账号。
- base `9c864dff252814432d4e1ec7776a60c04eac32ae` → target `20e0681ba85f02beb5396dab5f7458c76905aa40`，`included_commits` 为空。
- 计划 `## execution_scenarios` 唯一项为 `AUTH-LOGIN-001`；审核核对 `planHash=baa2cb581a06258c3b3a2677e4377006e438053e8b74c4eff75e3f09b792cf7e` 与来源回执一致，9 条 sourceReferences 回执 `status=ok`。
- 本次 `scenarioChanges=null`，无 `scenario-changes.patch`，与计划“无场景变更、不提供 patch”声明一致（审核亦核对该文件不存在）。
- 按计划，base→target 的 2 项变化均为上一 Run（`01M3YG2E1PC31W3GG4NEX2Z6GA`）的报告/审核落盘，无产品源码、配置或场景文件变化。这是范围事实，计划明确“不等同于已证明行为未变”——行为是否保持由本轮实际执行回答。
- 上一 Run 对 `AUTH-LOGIN-001` 的结论不被本轮改写；本轮是在更后的 target 上重新实际执行同一场景。

## 逐场景结果

### `AUTH-LOGIN-001` — 正确凭据登录建立会话并返回用户信息 — **passed**

场景状态 `approved`，标签 `core`。审核依据原始 command 证据（`operation-1..6.json`）与 `execution.md` 对照后判定通过；本报告沿用审核已交付的结论与依据，不重做证据审核。

| 期望（场景原文） | 实际观察（审核交付的原始证据事实） | 判定 |
| --- | --- | --- |
| 登录请求成功（2xx） | `POST /api/auth/login` → `201` | 满足 |
| 设置会话 Cookie（`sid`） | 登录响应 `setCookieNames=["sid"]`；后续 `status` 请求带 `cookieNames=["sid"]` | 满足 |
| `GET /api/auth/status` 返回 `authenticated` 为 true | 返回 `{"authenticated":true,...}` | 满足 |
| `user.email` 与所登录账号一致 | 注册、登录、status 三处 email 文本一致（小写归一） | 满足 |
| `user.displayName` 与所登录账号一致 | 三处 displayName 逐字一致，未脱敏 | 满足 |

- 前置条件：非生产环境、合成账号经同一业务入口创建并确认可用；受控 JSON 请求能力可用（`controlled-test-http`）。注册（seq2，clientId `login-run-register`）与登录（seq4，clientId `login-run-login`）使用不同 clientId，满足计划的客户端隔离要求；`status` 读取（seq5）复用持有 `sid` 的登录客户端。
- 会话建立的直接依据：登录响应显式观察到 `sid` 被设置，随后同一 clientId 的 `status` 请求携带 `sid` 并返回 `authenticated:true`，直接确认会话有效，无需间接推断。
- 计划覆盖缺口 1（displayName 可能被脱敏）未被触发：审核确认三处 displayName 均未脱敏，逐字比对成立；该限制未被用于弱化期望。

## 已确认产品问题

无。本场景未观察到与期望不符的行为，`confirmed_bugs` 为空。

Bug 候选查询仅作去重辅助，不影响上面的测试结果：本次以关键字 `AUTH-LOGIN-001` 执行了一次受限候选查询，返回 `empty`（无候选），因此无 Bug 需要 create/link 决策。该 `empty` 表示本次受限查询未返回候选，不构成“不存在任何相关 Issue”的绝对声明。

## 记录与证据

- 审核共列出 6 项工件证据（`operation-1.json` … `operation-6.json`，位于本次 Run 的证据目录下，地址见本 Run 动态上下文返回的 evidence URL），全部为 command 证据，无浏览器快照、无图片证据，与 `browserRequired=false` 及计划“全部为 HTTP/会话层断言”一致。
- 证据类别分布：受控 HTTP 操作用于注册（登录前置）、登录、`status` 读取；场景进度记录用于 `begin_scenario_execution`、`start_scenario`、`finish_scenario`。
- 期望核对表在 `execution.md` 中与原始证据逐项一致；审核独立比对后未发现 Runner 拔高或漏报，并载明 Runner 自身结论为 passed。
- 本报告仅转述证据 ID/文件名与结论，不复述账号字段、口令、Cookie 值或 Token。
- 需要说明的边界：证据文件的存在与保存成功本身不单独证明某个执行者在本 Run 做过对应操作；本轮对“实际执行”的归属依据是审核交付的操作记录（command 证据中的 `source`、操作与时间戳）。

## 时间说明

- 时间来源：动态 Run 上下文的 `started_at` / `finished_at`（Harness 时钟），以及审核交付的 Harness 进度记录时间。
- 审核记录的先后次序为：注册（17.410）→ `start_scenario`（20.344）→ 登录（21.285）→ `status`（22.117）→ `finish_scenario`（22.995），顺序自洽。
- 这些时间为 Harness 记录时间，没有共同的服务器时钟基准，因此仅表述先后关系，不换算为服务器事件时刻，也不作绝对时间结论。

## 未完成项、限制与覆盖缺口

以下按计划与审核已交付的内容如实保留，其中“原因未确认”与“审核已确认”分别表述，不将前者写成后者。

1. **账号清理与清理后核验未在本 Run 闭合**（审核列为未完成项）。场景“需要记录”包含 Run 标记账号的登记、清理与清理后核验；登记信息已在 `execution.md` 中述及（`cleanupScope=website-accounts`，状态 `registered`），注册证据支持账号已创建，但清理与清理后核验在本 Run 证据中未出现。按流程该事项属 Harness 在本 Session 结束后统一处理的收尾工作，尚未完成，本报告不提前声称清理已完成；其失败与否单独记录，不改动本场景已成立的产品判定。
2. **进度记录批注**（审核交付）：`finish_scenario` 事件的 `scenarioId` 为 null、`scope=auxiliary`，以 `completed=["AUTH-LOGIN-001"]` 表达完成，而非以场景 ID 显式标注完成。这是进度记录形式问题，不影响已完成的产品观察与结论。
3. **不在本轮范围、不外推**：预置账号登录对照、注册与存储的独立断言、清理后核验均未验证。本轮明确不使用也不删除预置账号，故“预置账号亦可登录”的对照不在本轮范围。本结论仅限 `AUTH-LOGIN-001` 的登录成功路径，不扩及其他未测场景（`AUTH-LOGIN-002`、`AUTH-REGISTRATION-*`、`AUTH-SESSION-001`、`AUTH-DELETE-*`、`CLEANUP-*`、`DATA-STORAGE-001`、`STORAGE-OBSERVE-001`），这些场景的既有结论不被本轮改写。
4. **计划覆盖缺口的状态**：缺口 1（displayName 可能脱敏）未被触发；缺口 3（Cookie 名称观察手段依赖 Runner 能力）本轮未成为限制——`setCookieNames` 与 `cookieNames` 已直接暴露；缺口 4（清理为 Harness 事项）即第 1 条，仍未闭合；缺口 2、5 属范围声明。
5. 本次未涉及需求/规格冲突，未发现影响本场景判断的执行偏差或环境阻塞。

## 计数与口径核对

- 执行场景数：1（`AUTH-LOGIN-001`）。`scenario_results` 与计划 `## execution_scenarios` 完整且有序一致。
- 结果口径：passed 1，failed 0，blocked 0。`blockingReasons` 为空，故整体 `result=passed`。
- confirmed bugs：0（Bug 候选查询返回 `empty`，无需 create/link 决策）。
- 覆盖缺口计数：清理与清理后核验未闭合 1 项（Harness 收尾事项），进度记录形式批注 1 项，范围外未验证项按上文第 3 条列示。上述分类互斥，同一项不重复计入。
- 摘要与明细核对一致；未出现需在两者间选择更乐观说法或补造条目的情形。

## 来源归属

- 逐场景判定、期望适用性、范围解释与结论依据由 Reviewer 在其审核报告中交付；本报告汇总整理，未改写为 Runner 的交付，也未将其疑问或未确认原因补写为已确认。
- 证据事实（状态码、响应体字段、Cookie 名称、clientId、进度记录形式）来自审核交付的原始证据观察与 `execution.md` 对照结果。
- 计划范围、执行安排、判断口径与覆盖缺口来自 `plan.md`。
- 本报告为本次 Run 唯一报告工件，按需落盘。

## Harness 清理收尾

测试数据清理完成；不改变本次功能验证结果。

清理适配器已独立核验 1 项测试数据不存在

全部登记测试数据均已独立核验清理

独立核验：luowang-01M3YGS2GG8RGM2VZ53ZZ7TRRB-login · run-scoped-http-cleanup · 2026-10-02T14:39:16.061Z · absent=true · sha256 25e7b3f75986602c71d55342ea6c5ae983605dc2651800ecdfe4f5a89a46da1f
