# 独立审核 — Run `01M3ZWVEN052DCF6X31TXGB14Y`（target `924f1d1f`）

## 审核范围与方法

- 先读 `plan.md` 与 `selectedScenarioSnapshot` 冻结的 4 条场景正文，再读 `scenario-changes.patch`；该文件不存在（`read_run_artifact` 返回“工件不存在”），与计划“本次无 patch、不新增/不修改/不废弃场景”的声明一致。
- 计划内嵌 Harness 元数据 `planHash=3c01ae028c96d0b36f356460daf3e5bef70b32adabcb84f5a60a5ac8934da80b`，与 `query_source_reads(scope=plan)` 返回的 `planHash` 相同；8 条 plan 引用回执状态 `ok`，4 条场景文件均为 `full-file` 且 `contentHash` 与快照 `contentSha256` 逐条一致，`app.py` 回执 `redacted=true`（计划已如实标注）。
- 唯一正式执行集合来自计划 `## execution_scenarios`：`AUTH-LOGIN-001` → `AUTH-SESSION-001` → `AUTH-REGISTRATION-001` → `DATA-STORAGE-001`；`scenario-progress` 事件（operation-4/10/26/45）顺序与之一致。
- 原始证据核对顺序：`list_evidence_files` → 全部 50 条 `operation-*.json`（command）→ 10 份页面快照 / 5 份 console（browser）→ 3 张截图（`read_evidence_image`，实际读取成功并看到画面）；形成判断后才打开 `execution.md` 对照。
- `browserRequired: true` 与真实执行相符：存在 playwright 导航、快照、填表、点击、Cookie 列表操作，且截图确为真实页面状态。`runner-execution` 阶段无源码读取回执（空），Runner 未在执行阶段重读场景源文件，属已知情况，不构成本批阻塞。

## 逐场景结果

### AUTH-LOGIN-001「正确凭据登录建立会话并返回用户信息」— passed（Reviewer 判断）

- 步骤 1：`POST /api/auth/register`（clientId `login-prep`）返回 **201**，`setCookieNames=["sid"]`，响应体含该 Run 前缀账号（operation-5）。
- 步骤 2：全新 clientId `login-fresh`（`sentCookieNames=[]`）`POST /api/auth/login` 返回 **201**（2xx），`setCookieNames=["sid"]`（operation-7）。
- 步骤 3：同 clientId `GET /api/auth/status`（`sentCookieNames=["sid"]`）返回 **200**，`authenticated=true`，`user` 与注册响应一致（operation-8）。
- 适用期望逐条有直接观察支持：登录 2xx ✅、设置会话 Cookie `sid` ✅、`authenticated=true` 且 `user.email`/`user.displayName` 与所登录账号一致 ✅（注册响应 operation-5 与登录/状态响应 operation-7/8 的 `email`、`displayName` 逐字相同）。
- 观察补充（非缺陷）：响应中邮箱为小写形式（`luowang-01m3zwven052dcf6x31txgb14y-login@example.test`），注册响应亦为小写，属大小写归一；请求体未在证据中留存，无法比对提交时的大小写，故不判为不一致。
- 记录层限制：Runner 所述“displayName 逐字等于提交值”中“提交值”本身在记录中脱敏（operation-13/15 的填表值为 `[REDACTED]`），可比对的是注册与登录两次响应的相互一致，该细节不影响期望满足。

### AUTH-SESSION-001「会话状态随 Cookie 正确反映并刷新后保持登录」— passed（Reviewer 判断）

- 步骤 1 冷态：全新 clientId `session-cold`（`sentCookieNames=[]`、`cookieNames=[]`）`GET /api/auth/status` 返回 **200** `{"authenticated":false}`（operation-11），未被“退出后读取”或换页面替代。
- 步骤 2 页面注册：真实浏览器导航 `GET /`（operation-12，快照 page-…-38-378Z 显示三字段表单）→ 填表（operation-15）→ 点击「注册」（operation-17）→ 快照 `status: 你好，[REDACTED]。`（operation-18）；随后浏览器读取 `GET /api/auth/status` 得 `authenticated=true`、`email=luowang-01m3zwven052dcf6x31txgb14y-session@example.test`（operation-20/21）。
- 步骤 3 刷新：浏览器重新加载 `GET /`（operation-22，快照 page-…-48-361Z 为根页面表单）后再读 `GET /api/auth/status`，仍 `authenticated=true` 且 `email` 与步骤 2 完全相同（operation-23/24）。
- 适用期望：步骤 1 `false` ✅；步骤 2 后 `true` 且与所注册账号一致 ✅；步骤 3 刷新后仍 `true` ✅。截图 `AUTH-SESSION-001-after-register.png`（sha256 `3e6e0a9f…`）实际显示 `你好，luowang-01M3ZWVEN052DCF6X31TXGB14Y-session。`，与所注册账号昵称一致。
- 限制：两次状态读取中 `displayName` 均为 `[REDACTED]`，无法逐字比对；“用户信息不变”主要由 `email` 逐字相同支撑，未见反证。此为该记录的脱敏边界，不影响期望成立。

### AUTH-REGISTRATION-001「注册成功后页面显示中文欢迎语并保持登录」— passed（Reviewer 判断）

- 步骤 1：`GET /` 快照确认昵称/邮箱/密码三字段与「注册」按钮可见（operation-28）。
- 步骤 2：填表（operation-29）并提交（operation-30）。
- 步骤 3 `#message` 实际文本：快照 status 区为 `你好，[REDACTED]。`（operation-31）；截图 `AUTH-REGISTRATION-001-welcome.png`（sha256 `e5f9d13a…`）实际显示完整文本 **`你好，luowang-01M3ZWVEN052DCF6X31TXGB14Y-welcome。`**，与计划/场景约定的 `你好，<昵称>。` 模板及本次提交昵称（`luowang-<runId>-welcome`）逐字一致 —— 期望“逐字中文模板”由截图直接确认，未被弱化。
- 步骤 4：浏览器 `GET /api/auth/status` 返回 `authenticated=true`、`email=luowang-01m3zwven052dcf6x31txgb14y-welcome@example.test`（operation-33/34），保持登录。
- 会话 Cookie：`browser_cookie_list` 观察到 `sid`（domain 为被测主机、path=/，值不复述，operation-42）。
- 期望核对：注册成功并设置 `sid` ✅（浏览器会话为 welcome 账号 + `sid` 存在 + 同端点 API 注册返回 201/`setCookieNames=["sid"]` 为 operation-5/46，组合支持）；`#message` 文本 ✅（截图逐字）；`authenticated=true` 且 `displayName` 与提交昵称一致 ✅（邮箱逐字 + 截图昵称逐字）。
- 限制（如实记录，不改变结论）：页面提交的注册请求本身没有直接 2xx 回执 —— `browser_network_requests` 在读取时缓冲已不含该 POST（operation-40/41 只见后续静态请求），故“注册请求成功”依托欢迎语成功路径、`status` 显示已登录为该账号、以及受控存储聚合计数由 1→4（operation-6 与 operation-48）共同支持；`#message` 的 DOM id 未在可访问性快照中直接呈现，观察对象为承载该文本的 `status` 区域。
- Runner 曾用 `navigate_back`（operation-36）后页面呈缓存、status 区为空（operation-39），Runner 已在 execution.md 如实标注为偏差且不影响步骤 3/4 的记录；核对属实（步骤 3 的 operation-31 与步骤 4 的 operation-34 均在提交后即时取得）。

### DATA-STORAGE-001「注册后密码仅以 Argon2id 哈希持久化」— passed（Reviewer 判断，含残余覆盖限制）

- 步骤 1：`POST /api/auth/register`（clientId `storage-client`）用 Run 前缀邮箱注册，返回 **201**、`setCookieNames=["sid"]`（operation-46）。
- 步骤 2 观察：受控存储观察（`controlled-test-account-storage`，`inspect_test_account_storage`）返回本 Run 聚合 `accounts=4, argon2id=4, other=0`（operation-48、operation-49 两次一致）；早期同源观察（operation-6）为 `accounts=1, argon2id=1, other=0`，与该时刻仅 1 个 Run 账号相符，说明该口径按 Run 前缀逐条统计真实注册。
- 期望 1「`accounts == argon2id` 且 `other == 0`」：4 == 4、other = 0 ✅（直接观察）。
- 期望 2「只保存 Argon2id 哈希、不出现明文」：由聚合分类支持 —— 全部 4 个 Run 账号的持久化口令均被归入 `argon2id`，`other` 为 0。
- 残余限制（如实保留，不据以弱化期望）：受部署级 Token 保护的 `GET /api/luowang/test-data/<runId>/storage` 由本 Run 直接调用返回 **401 UNAUTHORIZED**（operation-47），Runner 未持有该 Token；场景步骤 3 的“只读持久层逐条观察 `users.password_hash` 前缀”这一条件式子项未取得，因此 `$argon2id$` 前缀的字符串级观察缺失，证据层级为“按方案的聚合分类”而非“逐条 PHC 串”。若把 `$argon2id$` 前缀本身视为必须逐字观察的独立断言，该子项仍属未观测；但场景期望的实质（仅 Argon2id 持久化、无明文）已由权威聚合口径闭环，故本项判 passed 并保留该缺口说明。
- 口令长度 ≥12 字符在记录中不可逐字核验（值脱敏），仅由注册成功（201）及截图密码掩码宽度间接支持。

## 已确认产品问题

无。本批 4 个场景的全部适用期望均有实际观察支持，未发现与期望冲突的产品行为（无 failed）。

## 计划、执行与报告一致性核对

- 计划声明“无 patch、不新增/不修改/不废弃场景”与实际（`scenario-changes.patch` 不存在、4 条场景 `contentHash` 与快照一致）相符，未出现“已维护”式不实叙述。
- 执行顺序、场景 ID、结果口径与 `execution.md` 汇总表一致（4 场景 / 4 completed / passed×4）；我独立复核了其引用的关键 operation 编号（5/7/8、11/21/24、31/34/42、46/48/49）与截图，均能对上，未见 Runner 将未观测内容写成已观测。
- 需与主判断分别表达的记录问题（不影响产品结果）：①`operation-6`（辅助存储读取）缺少 `scenarioId`/`at` 归属字段，仅可用于佐证；②`operation-35` 的 `browser_find` 以 `isError=true` 结束、`operation-40` 的网络请求缓冲已不含页面注册 POST；③Runner 未在 execution.md 提及 `operation-35/40/41` 等失败/受限的辅助操作，但不影响其引用证据成立。
- 本次审核读取的脱敏记录中未出现明文口令（注册响应体仅含用户信息、填表值为 `[REDACTED]`）；此为对已返回脱敏文本的观察，未执行任何额外扫描，不构成“不存在任何明文口令”的绝对结论。

## 覆盖缺口与未完成项

1. 页面注册的 HTTP 2xx 与 `Set-Cookie` 无直接回执（浏览器网络缓冲不完整），由组合证据支持（详见 AUTH-REGISTRATION-001 限制项）。
2. `displayName` 的逐字比对受脱敏限制（AUTH-LOGIN-001、AUTH-SESSION-001、AUTH-REGISTRATION-001 均受影响）；AUTH-REGISTRATION-001 由截图补足，其余以邮箱逐字一致支撑。
3. DATA-STORAGE-001 的 `$argon2id$` 前缀字符串级观察缺失（Token 端点 401、无只读持久层访问）。
4. `app.py` 在计划阶段即受脱敏，凭据/Token/Cookie 生成行为未见明文；本 Run 期望来源以场景正文与规格回执为准。
5. 无 `baseCommit`、无 `includedCommits`，无法给出 diff 变化分析；不影响本批固定提交回归的结论，但不能据此判断 target 变更内容。

## 测试数据收尾

属 Harness 在最终 Main 之后处理，不在本次审核判定范围。已登记的 Run 前缀账号（login / session / welcome / storage 四条数据路径，共 4 个账号，聚合计数 operation-48/49 与之相符）未在本 Run 清理，Runner 未声明清理完成，符合不越权声明的边界。
