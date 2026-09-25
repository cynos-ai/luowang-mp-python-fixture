# 审核报告 · Run `01M3BX7A6SQQK8MVW6KZ5S4256`

- target：`abf6c24b388bd662ea25b05614871a8c4fbdd5d1`；base `c3600561fb3a0b65bcd1c13a4fb35be049b34539`，includedCommits 空
- 计划 Hash（plan.md 元数据）`4c69cc2bd07c46117acb07e0ad8e3a5f9adfab38c1caef3670f1e71baa8848b1`，与 `query_source_reads(scope=plan)` 返回一致
- scenarioMode `review-all`；`scenarioChanges: null`（无 scenario-changes.patch）
- `browserRequired: true`；实际存在 Playwright MCP 浏览器操作回执（`browser_navigate/fill_form/click/network_requests/cookie_list/take_screenshot`），声明与执行相符
- 执行集：`## execution_scenarios` 13 项，实际 `start_scenario` 13 项、顺序完全一致（operation-16/29/35/46/59/64/71/88/95/100/104/113/124）
- 审核方法：先读计划与冻结场景快照，再独立核对全部 131 个 `operation-*.json`、12 个页面快照、4 个 console 日志、2 张截图，最后与 `execution.md` 对照。未读取历史 Issue 列表、其他 Session 或任意路径。

## 计划与场景资产核对

- 计划声明“不新增/修改/废弃场景、不写 patch”，与 `scenarioChanges: null`、`planCoverage` 相符；未沿用“已维护”叙述，与实际一致。
- 计划逐项列出 13 个 approved 场景（含上次 blocked 的 10 项 + 注册/会话/存储补充），与冻结快照中的场景正文一致；`CLEANUP-CONFIG-001`（draft）未纳入执行集，理由（需多实例启动、本批受控能力不提供）成立。
- 计划对“能力边界”的预判（跨其他 Run 余量不可取得 / 非法 Run ID 可请求 / 无 Token 与错误 Token 可构造 / 短口令与错误口令占位符可用 / 预置账号存在）经本轮证据逐条落实，见下。

## 逐场景结果

| 场景 | 结果 |
| --- | --- |
| AUTH-REGISTRATION-001 | passed |
| AUTH-REGISTRATION-002 | passed |
| AUTH-REGISTRATION-003 | passed |
| AUTH-SESSION-001 | passed |
| AUTH-LOGIN-001 | passed |
| AUTH-LOGIN-002 | passed |
| AUTH-DELETE-001 | passed |
| AUTH-DELETE-002 | passed |
| DATA-STORAGE-001 | passed |
| STORAGE-OBSERVE-001 | passed |
| CLEANUP-AUTH-001 | passed |
| CLEANUP-SCOPE-001 | passed |
| CLEANUP-SEED-001 | blocked |

合计：12 passed（互斥），1 blocked，0 failed；与冻结执行集 13 项一致。

**AUTH-REGISTRATION-001 — passed**
浏览器注册 `-welcome`：`POST /api/auth/register => 201`（operation-21/23），`browser_cookie_list` 观察到 `sid`（operation-25，`credentialReferences` 含 `sid`）。`#message` 实际文本经截图 `AUTH-REGISTRATION-001-welcome.png`（sha256 `d5599d…efb1`）确认为 `你好，luowang-01M3BX7A6SQQK8MVW6KZ5S4256-welcome。`（含全角句号，与提交昵称一致；快照 operation-22 对昵称脱敏）。浏览器内 `GET /api/auth/status` 返回 `{"authenticated":true,...,"email":"luowang-…-welcome@example.test"}`（operation-26/27）。三条期望均满足。截图展示了表单与页面状态，未为取证改动页面。

**AUTH-REGISTRATION-002 — passed**
`-dup` 注册 201 并设 `sid`（operation-30）；同邮箱第二次注册 → `409 ACCOUNT_EXISTS`，`setCookieNames: []`（operation-31）；失败请求客户端 `GET /api/auth/status` → `authenticated:false`（operation-33）；原邮箱+首口令登录 → `201`，返回 `displayName=luowang-…-dup`（operation-32）。三条期望均满足。
- 覆盖说明（不影响判定）：期望第 3 条“会话仍指向原账号（未被失败请求替换）”是通过“失败请求无 Set-Cookie、其发起客户端保持未登录、原账号凭据仍有效”综合支持；执行未在第 2 步后回读第 1 步建立的原会话本身，故该条为间接支持而非逐字观察。

**AUTH-REGISTRATION-003 — passed**
邮箱不含 `@` → `400 INVALID_ACCOUNT`（operation-36）；昵称为空 → `400 INVALID_ACCOUNT`（operation-37）；短口令 → `400 WEAK_PASSWORD`（operation-38，`__SHORT_PASSWORD__` 能力可用）；三次均 `setCookieNames: []`；对应客户端 `GET /api/auth/status` 均 false（operation-39/40/41），凭据登录均 `401 INVALID_CREDENTIALS`（operation-42/43/44）。三条期望满足。

**AUTH-SESSION-001 — passed**
匿名客户端 status false（operation-47）；浏览器注册 `-sess` => 201（operation-52），页面 `#message` 显示 `你好，[REDACTED]。`（operation-51），浏览器内 status `authenticated:true,email=…-sess@example.test`（operation-54）；随后重新加载 `GET /`（operation-55）再读 status 仍 `authenticated:true` 且同一邮箱（operation-56/57）。三条期望满足。

**AUTH-LOGIN-001 — passed**
注册 `-login1`（operation-60）后，在隔离客户端 `POST /api/auth/login` => `201` 并设新 `sid`（operation-61）；该客户端 status `authenticated:true`，`displayName=luowang-…-login1`、`email=luowang-…-login1@example.test`（operation-62）。两条期望满足；登录在注册会话之外的新客户端建立，符合计划观察要点。

**AUTH-LOGIN-002 — passed**
未注册邮箱 → `401 INVALID_CREDENTIALS`（operation-65）；正确邮箱+错误口令 → `401 INVALID_CREDENTIALS`（operation-66）；两者无 Cookie，status 均 false（operation-67/68）；正确凭据登录 => `201`（operation-69）。两条期望满足。

**AUTH-DELETE-001 — passed**
浏览器注册 `-del1` => 201、`#message` 欢迎语（operation-76/77）；点击「删除账号」→ `DELETE /api/me => [200] OK`（operation-79），页面 `#message = 账号已删除。`（operation-80，快照 `page-2026-09-25T09-12-01-784Z.yml`；截图 `AUTH-DELETE-001-after-delete.png` sha256 `4ba3b1…7704`）；删除后浏览器内 status `authenticated:false`（operation-83/84）；原凭据重登 `401`（operation-86）；重复 `DELETE /api/me` `401`（operation-85）。四条期望满足。
- 覆盖说明：`browser_cookie_list`（operation-81）的 output 被 Harness 省略，其 `credentialReferences` 为空（注册后 operation-25 曾含 `sid`），据此与删除后 status=false 共同支持“会话 Cookie 被清除”；该条属间接支持。

**AUTH-DELETE-002 — passed**
对照账号 `-ctrl` 注册 201（operation-89）、可登录 201（operation-90）；无 Cookie 独立客户端 `DELETE /api/me` → `401 UNAUTHORIZED`（operation-91），该客户端 status false（operation-92）；对照账号原凭据再登录 => `201`（operation-93）。三条期望满足。

**DATA-STORAGE-001 — passed**
注册 `-store1` 201（operation-96）后，本 Run 前缀账号恰为 6 个（welcome/dup/sess/login1/ctrl/store1），存储观察 `{"accounts":6,"argon2id":6,"other":0}`（operation-97），只读探针复核一致（operation-98）。期望 `accounts==argon2id && other==0` 满足。
- 记录口径限制（如实保留）：受控存储端点只返回计数，未逐字读到 `$argon2id$` 前缀或直接排除明文；第 2 条由“非 Argon2id 归入 other、other=0”的三桶口径支持。此为观察口径限制，不改变本场景通过判定。

**STORAGE-OBSERVE-001 — passed**
有效 Token `GET …/storage` => 200，响应体仅 `runId/accounts/argon2id/other`，响应头 `Cache-Control: no-store`（operation-101），不含邮箱/用户 ID/口令/哈希；有效 Token + 非法 Run ID 同一端点 => `400 INVALID_RUN_ID` 且不返回计数（operation-102）。两条期望满足。

**CLEANUP-AUTH-001 — passed**
无 Authorization：account-count 与 storage 均 `401 UNAUTHORIZED`（operation-105/106）；错误 Token：两端点均 401（operation-107/108）；错误 Token `DELETE` => 401（operation-109）；拒绝响应体仅含 `error:UNAUTHORIZED`。随后 `-store1` 原凭据登录 => 201（operation-110），`configured` GET 复核 `remaining=6` 未减少（operation-111）。三条期望满足。

**CLEANUP-SCOPE-001 — passed**
`configured` 前置余量 `remaining=6`（operation-114）→ `DELETE` => `{"deleted":6,"remaining":0}`（operation-115，删除数与本 Run 前缀账号数一致）→ 独立 GET `remaining=0`（operation-116）→ 非法 Run ID 的 `DELETE`/`GET` 均 `400 INVALID_RUN_ID` 且无删除（operation-117/118）→ 被清理账号 `-store1`、`-ctrl` 原凭据登录均 `401`（operation-119/120），清理前已持 `sid` 的会话客户端 status `authenticated:false`（operation-121/122，Cookie 仍在但会话失效，证明级联删除）。四条期望满足。
- 覆盖说明：期望第 4 条“清理不接受任意用户 ID、SQL 或跨 Run 参数”中，“非法 Run ID（非 26 位）被拒 + 删除范围恰等于完整前缀账号数”已实测；SQL 注入 / 任意用户 ID 参数未构造专门请求（端点无相应入参），为未直接演练的负向条款。

**CLEANUP-SEED-001 — blocked**
- 期望“预置账号在本 Run 清理后仍能登录成功”→ **已确认满足**：创建 `-seed1`（operation-126）、`DELETE` => `{"deleted":1,"remaining":0}`（operation-127）后，环境预置账号登录 => `201`，返回昵称“预置测试员”（operation-128），时序在清理之后。
- 期望“另一个 Run ID 的余量在清理前后保持一致”→ **未验证**：`probe_run_cleanup` 仅支持当前 Run 与固定非法 ID 两种 `runIdKind`（operation-125/129 为 current / invalid），无任何“另一合法 Run 余量”读数，步骤 1/4 不可观察。
- 因任一适用期望未闭合，场景按 **blocked** 保留，已确认的成功部分如实保留；未降低期望、未改写旧结论。

## 已确认产品缺陷

本次未发现产品不符合期望的项（0 failed）。12 项 passed 场景的期望均有实际响应/Cookie/页面观察支持；`AUTH-REGISTRATION-001`、`AUTH-DELETE-001` 的页面文案均由截图确认，浏览器行为真实发生（Playwright MCP 回执）。无 Bug 可复现。

## 覆盖缺口与限制（如实保留）

1. `CLEANUP-SEED-001` 期望 2（跨其他 Run 余量前后一致）因受控工具只支持当前 Run / 固定非法 ID 而不可观察 → 场景 blocked。这是本批唯一阻塞项，属能力边界而非产品问题。
2. `CLEANUP-CONFIG-001`（draft）不在执行集，spec 第 4 条“清理接口默认关闭 / 短 Token 拒绝启用”本批无运行覆盖（已知缺口，非豁免）。
3. `DATA-STORAGE-001` 的哈希前缀/无明文结论仅由三桶计数（`other=0`）支持，未直接读持久层 `password_hash` 原文。
4. `AUTH-REGISTRATION-002` 期望 3、`AUTH-DELETE-001` 期望 1 的“会话 Cookie 被清除”为间接支持（前者依赖失败请求无 Set-Cookie 且发起客户端未登录；后者依赖 `browser_cookie_list` 的 `credentialReferences` 由 `sid` 变为空，其 output 被 Harness 省略），已与直接观察到的功能结果分别记录。
5. `CLEANUP-SCOPE-001` 期望 4 的 SQL/任意用户 ID 参数条款未构造专门请求，仅由非法 Run ID 拒绝与删除计数=前缀账号数支持。
6. `#message` 与 `user.displayName` 在快照中按 Harness 规则脱敏，昵称以截图（REGISTRATION-001）与响应体/页面文案交叉确认；未复述口令/Token/哈希值。

## 与 execution.md 的对照

`execution.md` 的逐场景叙述与我独立核对原始证据的结论一致：结果顺序、计数（6→0）、状态码、错误标识、会话状态、时序均相符，未发现夸大或与证据矛盾之处。其对 `CLEANUP-SEED-001` 的 blocked 归因（跨 Run 观察不可取得）与我一致；对 `AUTH-REGISTRATION-002` 期望 3 与 `AUTH-DELETE-001` 会话 Cookie 的表述亦以可获得的观察为准。执行记录中“13 场景按序 start/finish、无乱序或事后补报”经 operation 序列核对成立。

## 结论

- 13 项声明执行场景全部执行：12 passed，1 blocked（`CLEANUP-SEED-001`），0 failed。
- 无已确认产品缺陷。唯一阻塞源于受控工具不提供跨其他 Run 的余量观察，非产品问题；其余覆盖缺口为观察口径与未直接演练的负向条款，已逐条说明。
- 剩余验证：需具备跨 Run 只读余量观察能力的后续流程方可闭合 `CLEANUP-SEED-001` 期望 2；本轮不构造补测。
- 测试后临时数据（本 Run 前缀账号）已由执行内 `DELETE` 清空（operation-131 `accounts=0`）；最终清理收尾由 Harness 独立核验，本报告不提前声称清理完成。
