# 审核报告 — Run `01M3YGS2GG8RGM2VZ53ZZ7TRRB`

## 审核对象与范围

- target：`20e0681ba85f02beb5396dab5f7458c76905aa40`；base：`9c864dff252814432d4e1ec7776a60c04eac32ae`。
- 请求范围：仅回归 approved 场景 `AUTH-LOGIN-001`，完整验证其全部既定期望。
- `plan.md` 的 `## execution_scenarios` 唯一项为 `AUTH-LOGIN-001`，与 `selectedScenarioSnapshot` 冻结正文一致（`redacted=false`，正文可读，无脱敏缺口）。
- 工件核对：`scenario-changes.patch` 不存在，与 `plan.md`“无场景变更、不提供 patch”声明一致（本次 `scenarioChanges=null`）。
- 计划元数据 `planHash=baa2cb581a06258c3b3a2677e4377006e438053e8b74c4eff75e3f09b792cf7e` 与 `query_source_reads(scope=plan)` 返回的 `planHash` 一致；9 条 sourceReferences 回执 `status=ok`，其中场景正文、spec/intent/PROJECT、上一 Run 报告为 `full-file` 完整受控文本，`app.py` 为 `redacted=true` 全文（其口令/Token 片段未读原文）。来源与范围成立，但仅代表读取覆盖，不代表期望正确或验证充分。

## 证据核对方法

先读取原始 command 证据（`operation-1..6.json`），形成独立判断后，再打开 `execution.md` 对照。`list_evidence_files` 共 6 项，全部为 command 证据，无浏览器快照、无图片证据，与 `browserRequired=false` 及计划“全部为 HTTP/会话层断言”一致。本 Run 无图片需读取。

### 原始证据事实（Reviewer 独立观察）

| seq | source | 操作 | 关键观察 | 场景归属 |
| --- | --- | --- | --- | --- |
| 1 | scenario-progress | `begin_scenario_execution`（auxiliary） | `14:38:17.363Z`，completed=[] | 辅助 |
| 2 | controlled-test-http | `POST /api/auth/register`，clientId `login-run-register` | 状态 `201`；`setCookieNames=["sid"]`；body user 含 displayName/email | 辅助（登录前置） |
| 3 | scenario-progress | `start_scenario` | `14:38:20.344Z`，scenarioId `AUTH-LOGIN-001` | 场景 |
| 4 | controlled-test-http | `POST /api/auth/login`，clientId `login-run-login` | 状态 `201`；`setCookieNames=["sid"]`；body user 字段 | `AUTH-LOGIN-001` |
| 5 | controlled-test-http | `GET /api/auth/status`，clientId `login-run-login` | 状态 `200`；`cookieNames=["sid"]`；`{"authenticated":true,"user":{...}}` | `AUTH-LOGIN-001` |
| 6 | scenario-progress | `finish_scenario`（auxiliary） | `14:38:22.995Z`，completed=["AUTH-LOGIN-001"] | 辅助 |

- 注册（seq2）与登录（seq4）使用**不同** clientId（`login-run-register` vs `login-run-login`），符合计划“客户端隔离”要求；`status` 读取（seq5）复用登录后持有 `sid` 的 `login-run-login`，且请求已带 `cookieNames=["sid"]`。
- 登录响应体、`status` 响应体、注册响应体的 user 字段（displayName 与 email）三者文本一致。**displayName 未被脱敏**，故计划覆盖缺口 1 的降级口径未被触发，`displayName` 与 `email` 均为逐字比对。
- 进度记录时间顺序：注册(17.410) → start(20.344) → 登录(21.285) → status(22.117) → finish(22.995)，先后自洽；这些时间为 Harness 记录时间，无共同服务器时钟基准，仅陈述先后，不换算为服务器事件时刻。

### 与 `execution.md` 的对照

`execution.md` 中的状态码、响应体、`setCookieNames`、clientId 与上述原始证据**逐项一致**，未发现 Runner 拔高或漏报。Runner 的期望核对表与 Reviewer 独立判断相符：Runner 自身结论为 passed（见其“结果：**passed**”）。

## 逐场景判定

### `AUTH-LOGIN-001` — 正确凭据登录建立会话并返回用户信息

**结果：passed**

逐条核对场景原文（`selectedScenarioSnapshot` 冻结正文）的适用期望：

| 期望（场景原文） | 实际观察（原始证据） | 判定 |
| --- | --- | --- |
| 登录请求成功（2xx） | `POST /api/auth/login` → `201`（seq4） | 满足 |
| 设置会话 Cookie（`sid`） | 登录响应 `setCookieNames=["sid"]`；且 `status` 请求 `cookieNames=["sid"]`（seq4、seq5） | 满足 |
| `GET /api/auth/status` 返回 `authenticated` 为 true | 返回 `{"authenticated":true,...}`（seq5） | 满足 |
| `user.email` 与所登录账号一致 | 注册、登录、status 三处 email 文本一致（小写归一） | 满足 |
| `user.displayName` 与所登录账号一致 | 注册、登录、status 三处 displayName 逐字一致，未脱敏 | 满足 |

- 前置条件满足：非生产、合成账号（Run 前缀 `luowang-01m3ygs2gg8rgm2vz53zz7trrb-login`）经同一业务入口创建并确认可登录；具备受控 JSON 请求能力（`controlled-test-http`）。
- 会话建立的直接依据：登录响应显式观察到 `sid` 被设置，随后同一 clientId 的 `status` 请求携带 `sid` 且返回 `authenticated:true`，直接确认会话有效，无需间接推断。
- 全部适用期望均有充分实际观察支持，故判 passed；未发现产品缺陷。

## 已确认产品问题

无。本场景未观察到与期望不符的行为。

## 计划质量与场景维护

- 场景选择合理：`AUTH-LOGIN-001` 为本轮唯一请求范围且为 approved `core`；未选场景（`AUTH-LOGIN-002`、`AUTH-REGISTRATION-*`、`AUTH-SESSION-001`、`AUTH-DELETE-*`、`CLEANUP-*`、`DATA-STORAGE-001`、`STORAGE-OBSERVE-001`）不被本轮改写，符合请求边界。
- 场景正文已完整覆盖登录成功路径（2xx、`sid`、`authenticated:true`、email/displayName 一致），无需新增或修改；`plan.md` 声明“无场景变更、不提供 patch”，与实际无 `scenario-changes.patch` 一致。注册仅作登录前置，未越界为独立注册/存储断言。
- `list_target_changes` 返回 2 项（均为上一 Run 报告/审核落盘），`plan.md` 的“变化依据”描述准确。
- 计划覆盖缺口 1 未被触发（displayName 未脱敏），Runner 如实登记该限制未触发，未借降级口径弱化期望。

## 覆盖缺口与未完成项

1. **账号清理与清理后核验未在本 Run 闭合**：场景“需要记录”含 Run 标记账号的登记、清理与清理后核验。登记信息在 `execution.md` 有述（`cleanupScope=website-accounts`，状态 `registered`），第 2 条证据（注册请求）支持账号已创建；清理与清理后核验按流程属 Harness 收尾事项，本 Run 证据中未出现，不作为本次审核的阻塞项，留待 Harness/最终 Main 处理。
2. **进度记录批注**：`finish_scenario`（seq6）的 `scenarioId` 为 null、`scope=auxiliary`，以 `completed=["AUTH-LOGIN-001"]` 表达完成，而非以场景 ID 显式标注的 finish 事件；这是进度记录形式，不影响已完成的产品观察与结论。
3. **不在本轮范围，不外推**：预置账号登录对照、注册/存储独立断言、清理后核验均未验证；本审核结论仅限 `AUTH-LOGIN-001` 的登录成功路径，不扩及其他未测范围。
4. **时间结论受限**：仅有 Harness 记录时间，无共同服务器时钟基准，不对时间关系作结论。

## 结论

`AUTH-LOGIN-001` 在本 Run、target `20e0681ba85f02beb5396dab5f7458c76905aa40` 上 **passed**：全部既定期望均被原始证据直接支持，无产品缺陷，无执行偏差，无影响判断的覆盖缺口（清理为 Harness 收尾事项）。行动集合与计划 `execution_scenarios` 一致，`execution.md` 与原始证据逐项相符。
