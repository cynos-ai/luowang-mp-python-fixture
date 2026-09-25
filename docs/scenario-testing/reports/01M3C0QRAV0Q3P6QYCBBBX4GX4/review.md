# 审核记录 · Run `01M3C0QRAV0Q3P6QYCBBBX4GX4`

## 审核范围与依据

- 固定版本：base `c3600561fb3a0b65bcd1c13a4fb35be049b34539` → target `6d3f87c2f36544eddcf1b78569a454be5cb644c0`，`includedCommits` 空；`scenarioMode=review-all`；`scenarioChanges: null`。
- 唯一执行集合来自 plan.md `## execution_scenarios`：`CLEANUP-SEED-001`（顺序一致）。
- 动态上下文 `selectedScenarioSnapshot` 已冻结 `CLEANUP-SEED-001` 正文（`redacted=false`，`contentSha256=3d3694cd…`），与 plan 引用的场景读取回执 `contentHash` 一致（回执 `85c05577-…`，full-file）。本 Run 无 `scenario-changes.patch`，`scenarioChanges` 为 null，计划亦声明不新增/修改/废弃场景，故不存在"已维护"的变更声明需要核对。
- Plan 元数据 `planHash=e5c4db89abde2b340e14dcd27d23b8841208021221164112ceb932998e428393`，与 `query_source_reads(scope=plan)` 返回的 `planHash` 一致；plan 来源引用（`list_target_files`、`list_target_changes`、场景正文、spec、PROJECT.md、app.py 等）均校验通过。`app.py` 回执 `b8190128-…` 为 `returned-range` 且 `redacted=true`，即计划对实现的陈述属部分读取，本审核不把该实现描述当作运行结论依据。
- `browserRequired=false`：本场景验证对象为 HTTP 请求（清理/余量、`POST /api/auth/login`），无页面显示或 Cookie 属性观察需求；结合计划与执行的纯 HTTP 性质，声明与范围相符，无浏览器执行，也不存在需要读取浏览器格式证据的场景。
- 证据核对方式：先读 operation 原始记录（`operation-1…10.json`）形成独立判断，再打开 `execution.md` 对照。无图片证据，故不涉及视觉读取。

## 原始证据独立核对（形成于打开 execution.md 之前）

**CLEANUP-SEED-001 原始 operation 序列**（均 `targetCommit=6d3f87c2…`，同一 Run）：

| 序号 | source / 操作 | 关键观察 |
| --- | --- | --- |
| 1 | `scenario-progress` `begin_scenario_execution` | 10:11:55.898Z，`declared=true`，`completed=[]` |
| 2 | `scenario-progress` `start_scenario` | 10:11:56.734Z，`scenarioId=CLEANUP-SEED-001` |
| 3 | `controlled-run-cleanup-http` `GET` account-count，`runIdKind=current` | 200，`{"deleted":0,"remaining":0,"runId":"01M3C0QRAV0Q3P6QYCBBBX4GX4"}` |
| 4 | `controlled-test-http` `POST /api/auth/register`，`clientId=runseed` | **400** `{"error":"INVALID_ACCOUNT"}`，无 cookie |
| 5 | `controlled-test-http` `POST /api/auth/register`，`clientId=runseed` | 201，`displayName=luowang-01M3C0QRAV0Q3P6QYCBBBX4GX4-seed`，`email=luowang-01m3c0qrav0q3p6qycbbbx4gx4-seed@example.test`，`setCookieNames=["sid"]` |
| 6 | `controlled-run-cleanup-scope`（复合记录） | `currentRunId=01M3C0QRAV0Q3P6QYCBBBX4GX4`，`controlRunId=01E5P39W1902R2FHXJAFZVNS99`，`controlRegistrationStatus=201`，`before={current:1,control:1}`，`currentCleanup:0`，`after={current:0,control:1}`，`controlCleanup:0`，`controlRemaining:0`，`passed=true` |
| 7 | `controlled-run-cleanup-http` `GET` account-count，`runIdKind=current` | 200，`{"deleted":0,"remaining":0,...}` |
| 8 | `controlled-test-http` `POST /api/auth/login`，`clientId=seedlogin` | 201，`user.displayName="预设测试员"`，`email` 已脱敏，`setCookieNames=["sid"]` |
| 9 | `controlled-test-http` `GET /api/auth/status`，`clientId=seedlogin` | 200，`{"authenticated":true,...}` |
| 10 | `scenario-progress` `finish_scenario` | 10:12:06.759Z，`completed=["CLEANUP-SEED-001"]` |

**Reviewer 独立判断**：对照 Run `01E5P39W1902R2FHXJAFZVNS99` 为 26 位、仅用 Crockford 许可字符、与当前 Run `01M3C0QRAV0Q3P6QYCBBBX4GX4`（同为 26 位）在第 3 位即不同、互不构成前缀包含，满足"合法且可区分"的要求。`before.control=1` 非零，故"1→1"不是 0→0 的弱证据；`before.current=1`（seq 5 新建账号）→ `after.current=0` 说明本 Run 清理确实生效。对照账号若落在当前 Run 前缀，清理时会被一并删除而 `after.control` 不可能仍为 1 —— 该行为被并发观察，反向印证 `control` 读数确属另一 Run 前缀。SEQ 8/9 用独立 `clientId=seedlogin`（区别于 `runseed`），新签发 `sid`，非复用被清理账号会话。

## 逐场景结果

### CLEANUP-SEED-001 · 预置账号与其他 Run 账号免于本 Run 清理 → **passed**

| 期望（冻结正文） | 实际观察 | 判定 |
| --- | --- | --- |
| A. 预置账号在本 Run 清理后仍能登录成功 | `operation-8` 登录 201 且返回预置身份 `displayName=预设测试员`；`operation-9` 同客户端 `GET /api/auth/status` 返回 `authenticated:true`。时序上发生在 `operation-6`/`operation-7` 确认本 Run 清理后余量为 0 之后 | 满足 |
| B. 另一个 Run ID 的余量在清理前后保持一致 | `operation-6`：对照 Run 清理前 `control=1`、本 Run 清理后 `after.control=1`，其间 `current` 由 1 降为 0；对照 Run 自身收尾 `controlCleanup=0`、`controlRemaining=0` | 满足 |

**时序链**：`operation-3`（清理前本 Run 余量 0）→ `operation-5`（创建本 Run 前缀账号）→ `operation-6`（对照前读 1/1 → 本 Run 清理 → 后读 0/1 → 对照收尾 0）→ `operation-7`（本 Run 清理后 0）→ `operation-8`/`operation-9`（预置账号登录与状态）。操作时间戳（10:11:57 → 10:12:05）单调递增，逻辑顺序无倒置。

两项适用期望均有充分实际观察支持，无违反证据，场景判定 **passed**。本批未发现已确认的产品缺陷。

## 与 execution.md 的对照

- execution.md 的清单、结果顺序、通过项与我的原始证据判断一致；`execution.md` 对 `operation-3/5/6/7/8/9` 的转述与原始记录逐字相符，未夸大。
- 我的独立判断先于阅读 execution.md 形成，结论与之相同，属 Reviewer 自身观察，不因一致而弱化核对。

## 计划观察要点核对

- **期望 B 非平凡性**：对照 Run 清理前余量为 1（非零），"1→1"能排除"本 Run 清理误删其他 Run 账号"。满足。
- **对照 Run 合法性识别**：`operation-6` 显式区分 `currentRunId` / `controlRunId`，不以下一个（不存在的）非法 ID 或当前 Run 读数冒充；且如上述行为面印证。满足。
- **时序**：由 operation 序列与时间戳支持。满足。
- **独立登录**：`clientId=seedlogin` 独立于 `runseed`。满足。
- **对照收尾**：`controlRemaining=0`、本 Run `remaining=0`，均已留痕。满足。

## 偏差、限制与覆盖缺口（均不改变上述结论）

1. **`operation-6` 为复合聚合记录（证据强度限制，非阻塞）**：期望 B 所需的对照 Run 清理前/后读数只存在于这一条 `controlled-run-cleanup-scope` 聚合记录中，没有与该聚合记录对应的、可分别独立读取的两次对照 Run `GET` 原始 HTTP 记录。该记录确实逐 Run 区分返回（`before.control`/`after.control` 与 `current` 并列），并含 `controlRegistrationStatus=201`、`controlRunId` 等具体值，故我判定其足以支持期望 B；但需如实说明：这一支撑是单条聚合记录内部的读数，未由第二份独立原始 HTTP 证据交叉印证。该限制不构成阻塞，因其内容具体、可区分且与 `current` 读数相互约束。
2. **`operation-4` 的失败原因归属未在原始记录中留存（归因缺口，非阻塞）**：seq 4 为一次 400 `INVALID_ACCOUNT`；原始记录只捕获响应体，未见请求载荷，故"因字段名 `display_name` 非法所致"是 Runner 在 `execution.md` 偏差 1 中的解释，属其推断而非原始证据可核事实（我不对未返回的请求内容作事实认定）。该尝试为场景正文之外的准备步骤，其后 seq 5 以本 Run 前缀成功注册，故不影响任一期望的判定；记录为归因缺口即可。
3. **范围外场景未重跑**：本 Run 仅执行 `CLEANUP-SEED-001`，其余 approved 场景沿用历史记录，本批不改判；计划声明未写 scenario patch，`scenarioChanges=null`，与"未维护场景"一致，无"已维护"叙述需要纠正。
4. **`CLEANUP-CONFIG-001`（draft）不在执行集**，spec 第 4 条"清理接口默认关闭 / 短 Token 拒绝启用"本批无运行覆盖，属已知缺口而非豁免。
5. **口令/Token/邮箱脱敏**：原始记录中登录响应 `email` 字段已脱敏（`[REDACTED]`），未见口令或 Token 值被复述；本审核亦不复述任何口令值。`operation-4/5/8/9` 未捕获请求载荷，故"未记录口令"的边界仅限已捕获的响应/记录字段，不代表对全部请求体做过扫描。
6. **清理收尾**：本 Run 自身前缀账号已在场景内被清理（余量 0），登记条目 `luowang-01M3C0QRAV0Q3P6QYCBBBX4GX4-seed`（`cleanupScope=website-accounts`）状态为 `registered`，待 Harness 在最终 Main 后统一收尾；对照 Run 账号由工具自行清理并报告余量 0。该收尾不属本次审核范围，也不改功能结论。

## 结论

- `CLEANUP-SEED-001`：**passed**（期望 A、B 均满足）。
- 未发现已确认的产品缺陷、场景设计错误或执行偏差导致期望降级。
- 整体无阻塞项；上述限制（聚合记录的单点支撑、`operation-4` 归因缺口、范围外场景与 draft 场景未覆盖）均如实保留，供最终 Main 直接整理，无需回读运行记录补判断。
