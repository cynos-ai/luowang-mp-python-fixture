# review.md — 独立审核（target `08d5d82a358c507ba29a32646e01674991e1be93`，Run `01M3C8SY94SMQPT6AY19J1XSS1`）

## 审核范围与方法

- 审核对象：`plan.md` 的唯一 `## execution_scenarios` 清单（13 项，顺序执行）、`selectedScenarioSnapshot` 中 Harness 于正式 Runner 前冻结的场景正文、`execution.md`，以及本 Run 的原始证据。
- 本 Run 无 `scenario-changes.patch`（工具返回「工件不存在」），与计划「本批不新增/不修改/不废弃场景」一致；计划 `plan.md` 头部 Harness 元数据 `planHash=937b0e6c1b22284a23d9c6a3a70f0226f4422565369ae52b32043d346380b9e1`，与 `query_source_reads(scope=plan)` 返回的 `planHash` 一致，引用来源校验通过。
- 先独立读取原始证据（`list_evidence_files` 所列 operation-*.json 命令/MCP 记录、page-*.yml 浏览器快照、console-*.log、4 张截图），形成判断后再打开 `execution.md` 对照。证据读取均为 Reviewer 本人观察；下文「我确认」为我（模型 Reviewer）的独立结论，「Runner 记录」为 `execution.md` 原文转述。**本 Run 无人工复核记录，不声称人工确认。**
- 计划源码读取回执（`query_source_reads`）显示 `app.py` 以 `redacted=true`、`fullSafeText=true` 全量受控读取，`tests/test_app.py` 亦为脱敏全量；计划中「当前 target 注册分支为中文欢迎语」是**实现线索**，计划自身已声明「仅作线索、不代替执行」，本审核不以其作为通过依据。
- `browserRequired=true` 声明与真实执行一致：证据中有 `browser_navigate`/`browser_snapshot`/`browser_click`/`browser_cookie_list`/`browser_take_screenshot`/`browser_network_requests` 的实际操作记录（operation-5…14、23…28、54…63、71…77 等），非仅有快照/日志。

## 总体结论

| 场景 | 我的判定 | 与 execution.md 一致？ |
| --- | --- | --- |
| AUTH-REGISTRATION-001 | passed | 一致 |
| AUTH-REGISTRATION-002 | passed | 一致 |
| AUTH-REGISTRATION-003 | passed | 一致 |
| AUTH-LOGIN-001 | passed | 一致 |
| AUTH-LOGIN-002 | passed | 一致 |
| AUTH-SESSION-001 | passed | 一致 |
| AUTH-DELETE-001 | passed | 一致 |
| AUTH-DELETE-002 | passed | 一致 |
| DATA-STORAGE-001 | passed（附覆盖限制） | 一致（Runner 也标注了限制） |
| STORAGE-OBSERVE-001 | passed | 一致 |
| CLEANUP-AUTH-001 | passed | 一致 |
| CLEANUP-SCOPE-001 | passed（附覆盖限制，见下） | 一致（Runner 未单列该限制） |
| CLEANUP-SEED-001 | blocked（期望 B 未验证） | 一致 |

计数：passed 12、blocked 1、failed 0、未执行 0。**未发现已确认产品 Bug**；场景集与清单一致，13 项均实际执行并逐项 `start/finish` 声明（operation-3、4、18、19…117、125），无缺失或改写。

## 逐场景依据

### AUTH-REGISTRATION-001 — passed
- 页面：`browser_navigate` `GET /` 后表单可见（page-…12-39-18）；填表提交后页面状态区文本为 `你好，<昵称>。`（page-…12-39-23；operation-10）。截图 `auth-reg-001-welcome.png` 我实际读取：昵称输入框为 `luowang-01M3C8SY94SMQPT6AY19J1XSS1-welcome`，同一账号的状态区显示 `你好，luowang-01M3C8SY94SMQPT6AY19J1XSS1-welcome。`——**提交昵称与显示昵称逐字一致**（快照 yml 中该值被脱敏，但截图可见）。
- 注册网络请求 `POST /api/auth/register → 201`（operation-13）；`sid` Cookie 已设置（operation-11）；浏览器内 `GET /api/auth/status` 返回 `authenticated:true` 且 email `…-welcome@example.test`（operation-16 / page-…12-39-27）。
- 三项期望（注册成功并设 sid；`#message` 为中文欢迎语且昵称一致；status authenticated 且 displayName 一致）均满足。旧 Run 的英文欢迎语未在当前 target 复现；此结论仅来自本次实际页面观察，非据源码推断。

### AUTH-REGISTRATION-002 — passed
- 首次注册同邮箱 201 且设 `sid`（operation-20）；同邮箱再次注册 409 `ACCOUNT_EXISTS`、未设 Cookie（operation-21）；原邮箱原口令 `POST /api/auth/login` 201，`displayName` 为首次昵称 `…-dup`（operation-22）。页面侧第二次提交状态区显示 `ACCOUNT_EXISTS`（page-…12-39-45；截图 `auth-reg-002-dup.png` 我读得同样文本），非注册成功。
- 期望满足：第二次非 2xx 且页面不显示成功；原凭据仍可登录且昵称为第一次；失败请求未替换会话（409 无 sid）。注：页面以原始错误码 `ACCOUNT_EXISTS` 作为反馈文案，符合「不显示注册成功」期望，不构成违规，仅记为产品文案观察。

### AUTH-REGISTRATION-003 — passed
- 三次直接接口调用：邮箱不含 `@` → 400 `INVALID_ACCOUNT`（operation-31）；昵称为空 → 400 `INVALID_ACCOUNT`（operation-32）；口令短于 12 字符 → 400 `WEAK_PASSWORD`（operation-33）。三次后 `GET /api/auth/status` 均 `authenticated:false`（operation-34/35/36），均未设 Cookie。三组凭据登录均 401 `INVALID_CREDENTIALS`（operation-37/38/39）。
- 期望满足：三次非 2xx、未建会话、status 未登录、无可用账号产生。执行记录未复述口令值。

### AUTH-LOGIN-001 — passed
- 正确凭据登录 201 并设 `sid`，返回 `user.email`/`user.displayName`（operation-42）；随后 status 200 `authenticated:true` 且用户信息一致（operation-43）。期望满足。

### AUTH-LOGIN-002 — passed
- 错误口令 401、未注册邮箱 401（operation-47/46），均未设 Cookie；两次后 status 均 `authenticated:false`（operation-48/49）；随后正确凭据 201（operation-50）。期望满足（失败尝试未破坏账号）。

### AUTH-SESSION-001 — passed
- 匿名客户端 status `authenticated:false`（operation-53）；页面注册 `…-session` 后浏览器 status `authenticated:true` 且 email `…-session@example.test`（page-…12-40-09、operation-59）；重新加载 `GET /`（operation-60/61）后 status 仍 `authenticated:true` 且用户信息不变（operation-62）。截图 `auth-session-001-refresh.png` 我读得刷新后 `{"authenticated":true,"user":{"displayName":"luowang-01M3C8SY94SMQPT6AY19J1XSS1-session",…}}`。期望满足。

### AUTH-DELETE-001 — passed
- 注册 `…-del` 201 设 `sid`（operation-66）；`DELETE /api/me` 200 `{"deleted":true}` 且 `setCookieNames:["sid"]`（清除 Cookie，operation-67）；随后 status `authenticated:false`（operation-68）；原凭据登录 401（operation-70）；再次 `DELETE /api/me` 401 `UNAUTHORIZED`（operation-69）。页面侧复验：注册后点击「删除账号」，状态区显示 `账号已删除。`（page-…12-40-28、operation-76；截图 `auth-delete-001-page.png` 我读得同一文本）。四项期望满足。

### AUTH-DELETE-002 — passed
- 无 Cookie 客户端 `DELETE /api/me` 401 `UNAUTHORIZED`（operation-80，无删除成功结果）；匿名 status `authenticated:false`（operation-82）；对照账号注册 201（operation-81）且其原凭据登录仍 201（operation-83，未被删除）。期望满足。

### DATA-STORAGE-001 — passed（附覆盖限制）
- 注册 `…-storage` 201（operation-86）。受控只读汇总 `inspect_test_account_storage` → `accounts:5, argon2id:5, other:0`（operation-87）；`probe_run_cleanup GET storage` 同口径 `accounts:5, argon2id:5, other:0`（operation-90）。
- 期望核心（`accounts == argon2id`、`other == 0`、不出现明文/其他格式）满足。**覆盖限制（我认可 Runner 的标注）**：受控观察只提供聚合计数，`argon2id` 桶由应用对 `$argon2id$` PHC 前缀的归类得出；未取得单条哈希正文或独立持久层的逐条前缀观察。计划的证据优先级已将「三桶计数」列为该场景可接受口径，故不影响判定，但「形如 `$argon2id$` 前缀」这一具体化仅由聚合归类间接支持。

### STORAGE-OBSERVE-001 — passed
- 带有效 Token `GET …/storage` 200，响应体仅 `accounts/argon2id/other/runId`，`Cache-Control: no-store`（operation-90）；另带有效 Token 读 account-count 200 `deleted:0,remaining:5`（operation-91）。非法 Run ID 的 `GET …/storage` 400 `INVALID_RUN_ID`（operation-92）、`GET …/<runId>` 400（operation-93），均不含计数。期望满足：响应只含 Run 标识与三个计数，无邮箱/用户 ID/口令/哈希；非法 Run ID 非 2xx。

### CLEANUP-AUTH-001 — passed
- 无 Authorization：`GET …/<runId>` 401（operation-97）、`GET …/storage` 401（operation-96）；错误 Token：`GET …/<runId>` 401（operation-99）、`GET …/storage` 401（operation-98）、`DELETE …/<runId>` 401（operation-100）。拒绝体均为 `{"error":"UNAUTHORIZED"}`，不含计数/邮箱/用户 ID/口令/哈希。随后原凭据登录该 Run 账号 201（operation-102），有效 Token 复核 `remaining:5`（operation-101）。期望满足（无/错误 Token 全 401、无敏感泄露、账号未被删）。

### CLEANUP-SCOPE-001 — passed（附覆盖限制）
- 清理前有效 Token `GET` → `deleted:0, remaining:5`（operation-105）；`DELETE` → `deleted:5, remaining:0`（operation-106）；独立 `GET` → `remaining:0`（operation-107）、storage → `accounts:0`（operation-108）。非法 Run ID 的 `DELETE` 400 与 `GET` 400（operation-109/110）。被清理账号原凭据登录 401（operation-111）。越界核验：清理后再注册 `…-probe` 使余量回到 1（operation-112/114），此间再次非法 Run ID `DELETE` 仍 400（operation-113），随后有效 Token 清理该探针 `deleted:1, remaining:0`（operation-115）。
- 期望满足：清理后独立 GET 余量 0 且删除数 5 与本 Run 前缀账号数一致；非法 Run ID 非 2xx 且不删除；被清理账号原凭据失效、无法再登录；删除范围由完整 `luowang-<runId>-` 前缀决定。
- **覆盖限制（Runner 未单列，我补充）**：期望第 4 条中「不接受任意用户 ID/SQL/跨 Run 参数」这一注入面未被执行——受控清理工具只接受 `runId`（current/invalid 两类），无法提交任意用户 ID、SQL 或另一合法 Run ID；「跨 Run 不删除」仅由「非法 Run ID 拒绝 + 删除后不误删」间接体现。核心可测面（按完整前缀删除、删除数一致、非法 ID 拒绝）已由证据充分支持，故仍判 passed，但该注入子句属未直接验证项，跨 Run 正向对照的缺失与 CLEANUP-SEED-001 期望 B 同源。

### CLEANUP-SEED-001 — blocked
- **期望 A（预置账号免于本 Run 清理）已验证**：注册本 Run 账号 `…-seed` 201（operation-118）；预置账号清理前登录 201（operation-119）；有效 Token `DELETE` 本 Run → `deleted:1, remaining:0`（operation-122）；清理后预置账号登录 201（operation-124，未被误删），而本 Run 账号登录 401（operation-123）。
- **期望 B（另一合法 Run ID 余量前后一致）未验证**：`probe_run_cleanup` 仅支持当前 Run/固定非法 ID；`request_test_http` 无法注入部署级 Token，对另一 Run ID（`01M3BHYQCY8D4P6WKD01RAPH0E`）的 `GET /api/luowang/test-data/<otherRunId>` 返回 401 `UNAUTHORIZED`（operation-121），未取得余量读数。计划已预先规定「无法取得另一 Run 余量观察则维持未验证、场景 blocked、不降级」，Runner 依此判定。
- 判定：含两个必检期望，期望 B 无受控观察手段 → **blocked**（期望 A 已确认成功，该成功不因 blocked 被撤销）。未改变期望、未改用等价断言——与共同规则一致。

## 已确认产品问题

无。本批 12 个 passed 场景的明列期望均有实际观察支持，未发现违反期望的行为。以下仅为**观察项，非缺陷**：
- 重复邮箱注册时页面状态区以原始错误码 `ACCOUNT_EXISTS` 呈现（page-…12-39-45、`auth-reg-002-dup.png`），符合「不显示注册成功」的原文期望；是否应本地化文案不影响本场景结论。

## 覆盖缺口与未完成项

1. **CLEANUP-SEED-001 期望 B（另一 Run 余量对照）**：受控工具无法携带部署级 Token 读取指定合法 Run ID 的余量，期望 B 未验证，场景 blocked。所需能力：可带 Token 读取指定合法 Run ID 余量的受控入口，或 Harness 跨 Run 隔离核验。与 CLEANUP-SCOPE-001 第 4 条的跨 Run 注入面同源缺口。
2. **DATA-STORAGE-001 持久层正文**：仅有聚合三桶计数，未直接观察单条 `$argon2id$` 哈希正文或明文；不影响「聚合全部为 Argon2id、无其他格式」的期望判断，但具体前缀文本为间接支持。
3. **CLEANUP-SCOPE-001 注入子句**：任意用户 ID/SQL/跨 Run 参数不可经现有工具提交，该子句未直接验证（见上）。
4. **CLEANUP-CONFIG-001（draft）未执行**：需以自定义环境变量启动多实例，非当前受控环境可构造；计划已列为已知限制且未列入 `execution_scenarios`。draft 不构成执行授权，排除合理。
5. **脱敏缺口**：page-*.yml 中昵称/邮箱/Cookie 值被脱敏，仅状态区结构与语义可读；昵称逐字一致性由截图（可见值）补足。此外 `execution.md` 对截图多记为「清单确认存在」而非描述画面内容，画面内容由我另行读取 4 张截图核对，未发现与记录矛盾。

## 与 execution.md 的核对

- 结果顺序与计数一致：13 项、passed 12 / blocked 1 / failed 0、无未执行；无清单外场景被执行。
- 逐场景证据引用（operation 编号、page yml、截图名）与原始证据吻合；未发现把 HTTP 等价断言当作页面契约、或把局部可见泛称为整页的情况。
- 差异/补注（不影响结论）：(i) `execution.md` 未把 CLEANUP-SCOPE-001 第 4 条「任意用户 ID/SQL/跨 Run 参数」列为覆盖限制，我在上文补记；(ii) `AUTH-SESSION-001` 记录以 operation-59 标注 status 读取，原始为 `browser_snapshot` 捕获的状态 JSON，性质相符；(iii) `AUTH-DELETE-001` 页面侧注册账号 `…-delpage` 的邮箱取值在脱敏证据中不可见，属 Runner 输入命名，不可独立复核，亦不影响期望判断。
- 未发现执行记录复述口令/Token/Cookie 值；`execution.md`「口令、Token、Cookie 值均未在记录中复述」的声明与我所见记录一致，且未作「不存在任何密码文本」之类超范围绝对声明。本审核亦未复述任何口令值。

## 时间与来源说明

- 时间均为 Harness 记录时间（operation `at`/`startedAt`/`finishedAt`，2026-09-25T12:39–12:41Z 区间，UTC）；未取得被测服务 `date` 响应头，二者无共同校准时基，仅用于先后顺序与 Harness 记录时间，未作精确时刻断言，也未作跨 Run 时间对比。
- 本报告结论由 Reviewer 依据原始证据独立得出；`execution.md` 的 passed/blocked 判定为 Runner 记录，我据此核对而非直接采信。

## 测试数据收尾

场景内已自行删除的账号（`-del`、页面注册账号、`-probe`）与 CLEANUP-SCOPE-001/SEED-001 的受控清理见 operation-67/75/115/122；执行结束时当前 Run 余量 `remaining:0`（operation-126，属执行后的辅助读取）。测试后临时数据清理由 Harness 在最终 Main 之后独立核验，不属于本次审核或阻塞事项。
