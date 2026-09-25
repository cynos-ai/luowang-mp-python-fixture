# 审核报告 — CLEANUP-SEED-001（Run `01M3C9M9WCK4BQ813DQ6MD0VYV`，target `749c3087`）

审核角色：Reviewer（独立只读审核）。结论基于本 Run 受控 operation 原始证据；execution.md 仅用于对照，不作为证据。本 Run 无人工复核，不声称人工已确认。

## 审核范围与依据

- 计划 `plan.md`（planHash `d8de7edf39ccaefabecad0e0e14c13f1c111bc35849aed3008c0211f77032ef5`，与 Harness 元数据一致），唯一 `## execution_scenarios` = `CLEANUP-SEED-001`；`scenarioChanges=null`，无 `scenario-changes.patch`，计划声明不新增/不修改/不废弃场景，与实际一致。
- 冻结场景正文（`selectedScenarioSnapshot`，sha256 `3d3694cd…2dceca`，`redacted=false`）两条适用期望：
  - **A. 预置账号在本 Run 清理后仍能登录成功。**
  - **B. 另一个 Run ID 的余量在清理前后保持一致，未被本 Run 清理改动。**
- `browserRequired=false`：场景四条步骤为 HTTP 契约验证，无页面显示/刷新要求；本 Run 未见浏览器操作记录，也未要求浏览器证据，声明与场景性质一致，不存在能力矛盾。
- 计划引用来源（`query_source_reads` scope=plan）返回 10 条 receipt，planHash 与计划元数据一致；其中 `app.py` 为 `redacted:true` 的全量受控读取，其余为 full-file/returned-range 的脱敏文本。引用校验只说明来源与范围成立，`app.py` 内容被脱敏，故计划中的实现陈述在本审核中只能作为线索。

## 逐场景结果

### CLEANUP-SEED-001 — **passed**（两项适用期望均有实际观察支持；见下方口径限制）

原始证据（按 Harness `at` 时间，同一 Run 时钟基准，单调递增，无逻辑倒置）：
`operation-3.json` → `operation-6.json` → `operation-7.json` → `operation-8.json` → `operation-9.json`，外层 `operation-1/2` 为 `begin_scenario_execution`/`start_scenario`，`operation-10` 为 `finish_scenario`（`completed=["CLEANUP-SEED-001"]`）。

**前置与清理生效（期望 A/B 共同前提）**
- `operation-6.json`（12:49:08.960Z，`clientId=cleanup-seed-register3`）：`POST /api/auth/register` → **201**，响应体为本 Run 前缀账号 `luowang-01M3C9M9WCK4BQ813DQ6MD0VYV-a1`，`setCookieNames=["sid"]`，证明真实环境中本 Run 合成账号确实创建成功。
- `operation-3.json`（12:49:02.104Z）：无凭据 `GET /api/luowang/test-data/<本 Run>` → 401 `UNAUTHORIZED`（受控探针，未携带凭据），非缺陷。
- 本 Run 清理的发生与效果仅在 `operation-7.json` 的聚合读数中可读（`currentCleanup=0`、`after.current=0`，且与 `operation-6.json` 的 `before.current=1` 对照为 1→0）。**没有单独的 DELETE 原始请求记录**（见「覆盖缺口」第 1 条）。

**期望 A — 支持充分**
- `operation-8.json`（12:49:15.014Z，`clientId=cleanup-seed-seedlogin`，与注册 clientId 不同，属独立客户端）：`POST /api/auth/login` → **201**，响应体 `{"user":{"displayName":"预置测试员","email":"[REDACTED]"}}`，`setCookieNames=["sid"]`。
- `operation-9.json`（12:49:16.088Z，同一 `clientId=cleanup-seed-seedlogin`）：`GET /api/auth/status` → **200** `{"authenticated":true,"user":{"displayName":"预置测试员","email":"[REDACTED]"}}`。
- 时序：清理聚合记录 12:49:12.583Z < 登录 12:49:15.014Z，可确认登录发生在本次清理之后。显示名回显为预置身份、邮箱被 Harness 脱敏，与计划所述「用预置账号凭据登录」一致；脱敏使邮箱具体值不可读，但不影响「清理后预置账号登录成功并建立会话」这一期望成立。

**期望 B — 支持充分（依据为聚合记录内的逐 Run 读数，非工具判定字段）**
- `operation-7.json`（12:49:12.583Z，source `controlled-run-cleanup-scope`）：`currentRunId=01M3C9M9WCK4BQ813DQ6MD0VYV`，`controlRunId=018T5PNKRHVSPV34G9CY329YRB`；`controlRegistrationStatus=201`；**`before={current:1, control:1}` → `after={current:0, control:1}`**；`controlCleanup=0`、`controlRemaining=0`。
- 对照 Run ID 为 26 位、仅含 Crockford 许可字符（排除 I/L/O/U），与当前 Run 互不构成前缀包含，符合计划对合法性与可区分性的要求。
- 期望 B 的关键读数 **`before.control=1`（非零，具区分力）与 `after.control=1` 相等**，且本 Run 在同一记录内 1→0，形成有效对照。
- 我未采用该记录自带的 `"passed": true` 作为证据；判定仅基于上述数值读数。这些读数与独立观察到的 `operation-6.json`（本 Run 账号 201 存在，对应 `before.current=1`）相互一致，增强了可信度。

## 已确认的产品问题

**无。** 本次适用期望 A、B 均未被实际观察违反，也未发现与冻结场景/spec 直接冲突的产品行为。

## 报告与证据的差异（不影响已成立结论，但须记录）

1. **Runner 的读数口径说明自相矛盾。** execution.md 称 `currentCleanup=0`/`controlCleanup=0` 是「删除计数（deleted）」。若 `currentCleanup` 真是删除计数 0，则 `operation-6.json` 已创建的账号不会被删除，`after.current` 应为 1，与记录中的 `0` 冲突。因而「deleted 计数」这一解释与记录不符；更自洽的解释是二者为**清理后余量（remaining）**。该口径表述归 Runner（execution.md「读数口径说明」段），我未采信其解释，仅采用可读数值；无论取何种解释，期望 B 所依赖的 `before/after.control` 两读数不变，故结论不变。Runner 若需保留该说明，应修正口径或标注为待确认。
2. **计划预期的原始 DELETE/清理后 GET 记录缺失。** 计划「预期证据」要求清理 GET/DELETE 各对应原始 operation 记录；实际本 Run 的 DELETE 与其后余量读数只出现在 `operation-7.json` 的工具聚合中。计划「证据优先级」允许「明确的聚合记录内部逐 Run 读数」，故此缺口不使期望 B 无法确认，但相对计划写明的证据形态是一处偏差。
3. **两次注册 400 未定性。** `operation-4.json`、`operation-5.json` 的 `POST /api/auth/register` 分别返回 400 `INVALID_ACCOUNT`，`operation-6.json` 调整字段后 201。Runner 归因为「请求字段与契约不匹配」（依源码），但 `app.py` 在本 Run 为脱敏读取，spec 正文我也无法读取，故**该归因属未验证推断**。该现象不属于本场景适用期望，既不改变 A/B 判定，也不能据此认定产品缺陷；如需定性须另行授权核实注册契约。

## 覆盖缺口与未验证事项

1. **期望 B 的证据粒度较弱（如实保留）。** 对照 Run 的两位读数来自单次工具调用的聚合结果，对照 Run 自身的 GET/DELETE 请求没有逐请求原始记录；工具自身 `passed=true` 不具独立证明力。判定成立的基础是「计划明确授权该观察方式」+「记录内逐 Run 数值可读且非零具区分力」+「与 `operation-6.json` 独立事实一致」。若后续要求更强的逐请求证据，需新的受控能力；这不改变本次按计划口径的结论。
2. **对照仅单次随机生成，非穷举。** 只回答「本 Run 清理不误删某一合法 Run」这一承诺，不外推到多 Run 并发或前缀边界情形。
3. **本 Run 清理后的独立复核余量为 0** 仅取自聚合记录 `after.current=0`，无独立 GET 原始记录（同第 1 条）。
4. **范围外未覆盖**：其余 approved 场景沿用历史 Run 记录，本批不重跑、不改判（历史 `01M3C0QRAV0Q3P6QYCBBBX4GX4` 的 passed 与 `01M3C8SY94SMQPT6AY19J1XSS1` 的 blocked 结论保留在原 Run，本审核不改写）；draft `CLEANUP-CONFIG-001` 不在执行集，spec 第 4 条「清理接口默认关闭 / 短 Token 拒绝启用」本批无运行覆盖，属已知缺口而非豁免。
5. **`inspect_test_account_storage` 观察不可用**（Runner 所述，无对应 operation 记录可核）、**`app.py` 与 spec 正文脱敏/不可读**，使计划中的实现与契约引用无法在本轮独立验证——这些均不影响 A/B 的实际行为判定。
6. **敏感信息**：记录未复述预置账号口令、清理 Token 或 Cookie 值，与计划一致；本 Run 未执行系统性 Secret 扫描，故不作「不存在任何密码文本」类绝对声明。

## 结论

- `CLEANUP-SEED-001`：**passed**（期望 A、期望 B 均有可读的实际观察支持）。
- 已确认产品 Bug：无。
- 需下游注意：Runner 的 `currentCleanup/controlCleanup` 口径说明与记录不一致（本审核按可读数值判定，不受其影响）；本 Run 清理执行仅存于聚合记录，无独立 DELETE 原始证据；注册 400 的契约归因未经验证。
- 测试数据收尾（本 Run 前缀账号与对照 Run 账号的清理由 Harness 在最终 Main 后处理）不属于本次审核范围，其成败不改已成立的场景结论。
