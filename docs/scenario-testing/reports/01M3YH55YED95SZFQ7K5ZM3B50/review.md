# 审核报告 — Run `01M3YH55YED95SZFQ7K5ZM3B50`

## 审核范围与依据

- 计划：`plan.md`（`planHash=44b19a06ca47fe031c9c6a48ec9d59c315aa3462a4d133dde906991c8d537087`，与计划开头 Harness 元数据一致；`query_source_reads(scope=plan)` 校验通过，planHash 相同）。执行集 `## execution_scenarios` 唯一场景 `AUTH-LOGIN-001`。
- 场景正文：动态上下文 `selectedScenarioSnapshot` 中 Harness 冻结的 `AUTH-LOGIN-001` 正文（`redacted=false`，contentSha256 与计划读取回执 `6a95af26-...` 的 contentHash 一致）。
- 变更：`scenario-changes.patch` 不存在；`list_target_changes` total=2 仅新增上一 Run 的两份报告工件，base→target 无源码/配置/场景变化，与计划“无维护动作”声明一致。
- 原始证据：先读 `list_evidence_files` 与 6 份 command 证据（operation-1..6.json），形成证据判断后才打开 `execution.md` 对照。
- `browserRequired=false`：本场景全部期望位于 HTTP/会话层，无浏览器快照/日志证据，声明与执行一致，不构成缺口。

## 逐场景结果

### AUTH-LOGIN-001 — 正确凭据登录建立会话并返回用户信息

**判定：passed**

场景 `## 期望` 共 2 组、拆为 5 个可观察点，均有实际观察支持：

| # | 期望（场景原文） | 独立核对的原始观察 | 判定 |
| - | --- | --- | --- |
| 1 | 登录请求成功（2xx） | operation-4.json：`POST /api/auth/login`（clientId `login-01M3YH55`）status `201` | passed |
| 2 | 设置会话 Cookie（`sid`） | operation-4.json：登录响应 `setCookieNames=["sid"]` | passed |
| 3 | `GET /api/auth/status` 返回 `authenticated` 为 true | operation-5.json：同一 clientId `GET /api/auth/status` status `200`，body `authenticated:true`，且请求 `cookieNames=["sid"]`（客户端持有登录会话 Cookie） | passed |
| 4 | `user.email` 与所登录账号一致 | operation-3/4/5.json 三处均为 `luowang-01m3yh55yed95szfq7k5zm3b50-login@example.test` | passed |
| 5 | `user.displayName` 与所登录账号一致 | operation-3/4/5.json 三处逐字均为 `Run Login 01M3YH55` | passed |

要点说明（基于原始证据，非 Runner 转述）：

- 会话建立：登录发生在与注册相互隔离的 `login-01M3YH55` 客户端上，登录响应新下发 `sid`（`setCookieNames=["sid"]`），随后该同一客户端携带 `sid` 读取 status 得 `authenticated:true`。这直接支持“凭据核对成功后建立会话”，而非复用注册客户端既有会话。
- 字段一致性以注册响应（operation-3.json）为账号事实源，与登录响应、status 响应三处比对一致；邮箱按小写归一比对，与实现 `strip().lower()` 行为一致。
- 未复述任何 Cookie 值或口令值；证据仅含 Cookie 名称集合与用户字段。

## 已确认产品问题

无。本场景 5 项适用期望全部满足，未发现与期望相违的行为。

## 场景设计与理解依据

- 场景选取恰当：本轮人工请求限定回归唯一 approved `core` 场景 `AUTH-LOGIN-001`，`## execution_scenarios` 与该请求一致，无重要漏测（不扩大到 `AUTH-LOGIN-002` 拒绝路径、注册/存储/删除/清理等场景属请求明确的边界）。
- 计划的实现事实（`app.py` 登录/状态路径）为静态来源、已如实标注“不代替运行观察”；本轮结论系由实际受控 HTTP 观察得出，未依赖静态推断。
- 注册仅作登录前置，未对注册路径另立断言；执行记录未将注册的 `sid` 设置计为登录场景判定，符合范围限定。
- 无场景维护动作：`scenarioChanges=null`，与 base→target 无场景变更的事实一致，“无维护”叙述成立。

## 覆盖缺口与未完成项（如实保留，不改变本场景判定）

1. **清理与清理后核验未在本 Run 证据中出现**：场景 `## 需要记录` 含“登记、清理与清理后核验”。证据中仅有注册操作（operation-3.json）本身，未见清理调用与清理后“账号不存在”核验记录。按计划该类属 Harness 收尾事项，其未完成单独记录，不影响 `AUTH-LOGIN-001` 产品判定。**该缺口不阻塞本场景，但“清理已完成”不能由本轮证据支持。**
2. **账号登记为过程性记录**：执行记录声明账号已登记（`luowang-01M3YH55YED95SZFQ7K5ZM3B50-login-account`，`cleanupScope=website-accounts`），但无独立登记工件证据；比对所需的账号事实由注册响应（operation-3.json）提供，足以支撑字段一致性判断。
3. **请求正文未捕获**：证据记录响应与状态，未含登录请求体（口令）。这不影响 2xx/Cookie/status 期望的判定；隔离客户端登录成功并新发 `sid` 已足以支持“正确凭据建立会话”的观察。
4. **范围外不推论**：预置账号对照、拒绝路径、会话/删除/存储等均未执行，本结论不外推至这些范围。

## 环境与一致性

- 未观察到来自其他项目的环境故障信号；本项目端点全程可达，target、账号、证据来源未被外部故障改变，符合请求的隔离硬约束。此为执行记录的陈述，原始证据中无相反事实可推翻，但也无独立外部故障探针证据，故仅作“未出现”记录。
- 证据上传收据 6/6（operation-1..6.json），与 `list_evidence_files` 一致；场景进度顺序 `begin→start→finish`，与计划一致，1/1 完成。

## 结论

- 逐场景：`AUTH-LOGIN-001` = **passed**（5/5 适用期望有实际观察支持，无排除项）。
- 已确认产品 Bug：无。
- 未验证/缺口：清理及清理后核验记录缺失（Harness 收尾事项，非本场景阻塞项）；其余范围外场景未执行、既有结论不被本轮改写。
- 与 `execution.md` 对照：Runner 的清单、顺序与通过判定与本人独立核对一致；Runner 未对清理完成作声明，一致。
