# 审核报告 — Run `01M3ZYK18129P9JM799X1A95DB`

审核角色：Reviewer（独立审核）。审核对象：`plan.md`（planHash `8e75153fec01d42bea6d98ad35c997bfe57fb36d424e2c38c7f32a2f02d8e878`，与工件头部 Harness 元数据一致，经 `query_source_reads(scope=plan)` 核对）、`selectedScenarioSnapshot`（Harness 在 Runner 开始前冻结的 4 条场景正文，均 `redacted:false`）、`execution.md`、本 Run 的命令/浏览器/截图证据。

- 本 Run **无 `scenario-changes.patch`**（`read_run_artifact` 返回不存在），与计划「本次无场景资产变更」的声明一致，未发现「已维护」类虚述。
- target `fa65797585b6a196f7d5a41099593ee3376ca4cd`，base `null`、includedCommits `[]`：无 diff 依据，本批只能作固定提交回归，计划已如实声明该限制。
- `browserRequired: true` 有真实执行支撑：证据中存在 Playwright MCP 的 `browser_navigate`/`browser_snapshot`/`browser_fill_form`/`browser_click`/`browser_cookie_list`/`browser_take_screenshot` 回执（`operation-9`…`operation-34`），并有页面快照与两张页面截图；声明与执行相符。
- 证据基础核对：`operation-3/4/5/8/37/38/39` 为受控 HTTP / 受控存储观察记录；`operation-9`…`operation-34` 为浏览器操作回执；`operation-14/18/21/25/28/32` 与 `page-*.yml`、`console-*.log`、两张 png 为观察材料。所有时间均为 Harness 记录 UTC 时间戳（`Z`），来源单一，仅用于说明先后次序。

## 执行集合核对

计划 `## execution_scenarios`（唯一执行授权）：`AUTH-LOGIN-001` → `AUTH-SESSION-001` → `AUTH-REGISTRATION-001` → `DATA-STORAGE-001`，与 4 条冻结场景正文一一对应。命令证据中的 `scenario-progress` 记录（`operation-1/2/6/7/22/23/35/36/40`）显示声明顺序与实际顺序一致，无跨场景补跑；末次 `completed` 为 4/4。

## 逐场景结果

### AUTH-LOGIN-001 — 结论：passed

原文适用期望与核对：

1. 「登录请求成功（2xx）并设置会话 Cookie（`sid`）」——`operation-4.json`：`POST /api/auth/login`（clientId `login-001`）**status 201**，`setCookieNames=["sid"]`，登录前 `sentCookieNames=[]`。符合。
2. 「`GET /api/auth/status` 返回 `authenticated=true`，`user.email` 与 `user.displayName` 与所登录账号一致」——`operation-5.json`：同客户端带 `sid` 请求返回 200，正文 `{"authenticated":true,"user":{"displayName":"luowang-01M3ZYK18129P9JM799X1A95DB-login","email":"luowang-01m3zyk18129p9jm799x1a95db-login@example.test"}}`。与前置账号（`operation-3.json` 注册响应 `displayName=luowang-01M3ZYK18129P9JM799X1A95DB-login`，email 同值）一致；email 大小写差异为服务端规范化，非不一致。符合。

前置账号为本 Run 前缀账号（`luowang-01M3ZYK18129P9JM799X1A95DB-login`），符合场景前置「本 Run 前缀注册创建，或使用环境预置账号」。无偏差，无未验证子项。

### AUTH-SESSION-001 — 结论：passed（含 displayName 逐字读取受限，见下）

原文适用期望与核对：

1. 「步骤 1 返回 `authenticated=false`」——`operation-8.json`：clientId `anon-session`，`sentCookieNames=[]`，200，正文 `{"authenticated":false}`。确为无 Cookie 的独立客户端，非「退出后读取」。符合。
2. 「步骤 2 后返回 `authenticated=true`，并包含与所注册账号一致的用户信息」——页面路径：`operation-9/10` 导航 `GET /` 并确认表单三字段；`operation-11` 页面填写、`operation-12` 一次点击回执 `isError=true`、`operation-13` 点击成功并带页面快照；`operation-14.json` 快照显示状态区 `你好，[REDACTED]。`；`operation-15.json` 观察到浏览器 `sid` Cookie（domain `luowang-rr-live-final-python-app`，`path=/`，值不入记录）；`operation-16.json` 截图 `auth-session-registered.png`。随后 `operation-17/18` 读出 `{"authenticated":true,…"email":"luowang-01m3zyk18129p9jm799x1a95db-session@example.test"}`。注册在**真实浏览器页面**完成，非仅 API。符合。
3. 「步骤 3 刷新后仍 `authenticated=true`，且用户信息不变」——`operation-19` 重新加载 `GET /`（快照 `page-…25-011Z.yml` 为无会话态表单页，状态区为空），`operation-20/21` 再读状态仍为 `authenticated=true` 且 email 同值；`operation-17/18` 与 `operation-20/21` 两次读取的 email 完全一致。符合。

独立观察到的限制（不影响上判）：状态响应中的 `displayName` 在快照中被 Harness 脱敏为 `[REDACTED]`，无法从快照逐字读出；邮箱字段明文可见且两次一致。我另外读取了截图 `auth-session-registered.png`（sha256 `c9d79a386a0baf67e021a38d561dee93b1a820630a395f2cdf00d6ab585c7915`），画面显示状态区为 `你好，luowang-01M3ZYK18129P9JM799X1A95DB-session。`，与状态响应中的 `…-session@example.test` 账号互为同一账号的旁证。因此「用户信息与所注册账号一致 / 刷新后不变」由「邮箱逐字一致 + 页面昵称与账号同源 + 两次状态读取一致」支撑；`displayName` 的逐字比对本身仍是推断而非直接读取。

### AUTH-REGISTRATION-001 — 结论：passed

原文适用期望与核对：

1. 「注册请求成功，并设置会话 Cookie（`sid`）」——页面提交路径未捕获直接 HTTP 回执（浏览器注册无 `POST /api/auth/register` 的记录），由组合证据支撑：`operation-28/34-198` 快照显示成功欢迎语、`operation-29.json` 观察到 `sid`、`operation-32.json` 显示已登录；`operation-39` 本 Run 聚合 `accounts=4` 与本次 4 次注册（login/session/welcome/storage）计数一致。缺环如实存在，判定基于计划「证据优先级 2」的组合口径。符合（组合证据）。
2. 「`#message` 实际显示文本为 `你好，<昵称>。`，`<昵称>` 为提交昵称」——`operation-28.json` / `page-…34-198Z.yml` 快照显示 `status [ref=f4e12]: 你好，[REDACTED]。`；我独立读取截图 `auth-registration-welcome.png`（sha256 `83d585e51111a2393c345e8408afe91a6d8542d1f123e0275688595f6b276495`），画面中 `#message` 完整文本为 `你好，luowang-01M3ZYK18129P9JM799X1A95DB-welcome。`，即**中文模板逐字成立且昵称为计划步骤 2 指定的昵称**。符合。
   - 需纠正一处强调：`execution.md` 将该期望记为「部分受限／无法在记录中逐字比对昵称」。这是 Runner 的保守表述——截图证据实际支持完整逐字比对（快照脱敏不等于证据缺失）。结论方向一致，但审核口径应为「已确认」，而非「受限」。
3. 「`GET /api/auth/status` 返回 `authenticated=true` 且 `user.displayName` 与提交昵称一致」——`operation-31/32/37-037`：`{"authenticated":true,…"email":"luowang-01m3zyk18129p9jm799x1a95db-welcome@example.test"}`，`displayName` 脱敏；昵称一致性由截图中的完整昵称 + 同源邮箱支撑。符合（`displayName` 字段本身逐字读取受限）。
4. 历史 Issue #4（英文欢迎语）方向：截图 `#message` 为中文模板，无英文欢迎语。与场景既定期望（中文）无冲突。

其他观察：截图中昵称/邮箱输入框内文字显示被输入框宽度截断（`luowang-01M3ZYK18129P9.`），这是控件宽度导致的视觉截断，`#message` 文本本身完整，不构成对期望的偏差。

### DATA-STORAGE-001 — 结论：passed（`$argon2id$` 字符串级子项未取得，如实保留）

原文适用期望与核对：

1. 「该 Run 聚合观察显示 `accounts` 等于 `argon2id`，且 `other` 为 0」——`operation-39.json`：受控存储观察（`source: controlled-test-account-storage`，`runId` 为本 Run）返回 `accounts=4, argon2id=4, other=0`。符合。计数口径自洽：本 Run 新建账号 4 条（`operation-3` login、页面 session、页面 welcome、`operation-37` storage），观察在删除之前（`operation-39` 先于 `operation-40` 收尾）。
2. 「持久层保存 Argon2id 哈希（形如 `$argon2id$` 前缀的 PHC 字符串），不出现明文口令」——实质判定依据为上述聚合口径（4/4 为 Argon2id、`other=0`，无其他格式项）；`$argon2id$` 字符串级前缀**未被直接观察**。场景前置允许「带部署级 Token 的端点**或等价的只读持久层观察**」，本次使用等价口径，故不判不适用；字符串级细节保留为未取得子项，不改写为期望不适用，也不上升为缺陷。

需记录的执行偏差（不改变上述判定）：场景步骤 2 字面提到的部署级 Token 端点 `GET /api/luowang/test-data/01M3ZYK18129P9JM799X1A95DB/storage` 实际返回 **401 `{"error":"UNAUTHORIZED"}`**（`operation-38.json`，clientId `storage-obs`，未携带 Token）。即场景点名口径本 Run 不可用，判定改由受控只读存储工具完成。这一点 `execution.md` 已如实记录，来源归属清楚。

## 已确认产品问题

**未发现产品缺陷（0 项 failed）**。4 条场景的适用期望均未出现与期望相反的实际观察；`operation-14/28` 显示中文欢迎语模板，与历史英文欢迎语问题相反的结论由本 Run 记录支持。

## 执行记录问题与覆盖缺口（均不影响上判，供最终 Main 如实保留）

1. **`execution.md` 遗漏两次失败的工具调用**：`operation-12.json`（`browser_click`，`isError:true`）与 `operation-33.json`（`browser_find`，`isError:true`）在报告中未提及。两者之后均有成功的同义操作（`operation-13` 点击、`operation-34` 查找）且后续状态自洽，属重试噪声；但报告写「偏差：无」时未涵盖该事实，属报告完整性问题，非产品问题。
2. **AUTH-SESSION-001 / AUTH-REGISTRATION-001 的页面注册无直接 2xx 回执**：浏览器注册未产生 `POST /api/auth/register` 的 HTTP 记录，仅由欢迎语 + `sid` + 已登录状态 + 本 Run 账号计数组合支撑；该缺环在两场景中均已如实标注，符合计划的证据优先级 2。
3. **`displayName` 逐字读取受限**：状态响应中的 `displayName` 在快照中脱敏。AUTH-SESSION-001 的账号一致性靠可见邮箱 + 页面昵称旁证；AUTH-REGISTRATION-001 的`displayName` 一致性靠截图完整昵称 + 同源邮箱。两处均为推断路径而非字段级直接读取。
4. **DATA-STORAGE-001 的 `$argon2id$` 字符串级观察未取得**（无部署级 Token / 只读持久层），已在上述场景内说明。
5. **清理未在本 Session 完成**：`operation-39` 时本 Run 4 条账号仍在。按计划与流程，清理属 Harness 在最终 Main 之后的收尾事项，其失败单独记录，不改变本批测试结论；本报告不预判清理结果。
6. 计划读取 `app.py` 为 `redacted:true` 全文（`query_source_reads` receipt `ac04c0e2…`），故实现细节来源受限；本批期望来源取自场景正文与 `docs/PROJECT.md`、`docs/changes/python-registration/spec.md`（均 `full-file`、未脱敏），来源归属成立。
7. 未选场景（`AUTH-DELETE-001`、`AUTH-REGISTRATION-002`、`CLEANUP-AUTH-001`、`CLEANUP-SCOPE-001` 等）本次未执行，本 Run 不改写其结论；本次请求范围（登录后会话状态 + 一条独立合成数据路径）内未识别到重要漏测。

## 场景选择与计划质量

计划的 4 条场景与请求的两类业务结果直接对应，均为固定 target 中存在的 `approved`+`core` 场景，正文与冻结快照哈希一致；未新增/修改/废弃场景，与「无 patch」的事实相符。计划未把任何明列期望降为可选，且预先声明了脱敏与 `$argon2id$` 子项限制，本批执行与之一致。未发现计划层面的矛盾（如「归还/恢复」类断言冲突）。

## 汇总

| 场景 | Reviewer 结论 | 依据 |
| --- | --- | --- |
| AUTH-LOGIN-001 | passed | operation-3/4/5 |
| AUTH-SESSION-001 | passed（displayName 逐字受限） | operation-8/13/14/15/18/21 + auth-session-registered.png |
| AUTH-REGISTRATION-001 | passed（昵称逐字已由截图确认） | operation-28/29/30/32 + auth-registration-welcome.png |
| DATA-STORAGE-001 | passed（`$argon2id$` 字符串级未取得） | operation-37/38/39 |

- 分布：passed 4 / failed 0 / blocked 0；未验证项：无（受限于读取口径的子项已在对应场景说明，不构成 blocked）。
- 数据清理：本 Run 4 条 `luowang-01M3ZYK18129P9JM799X1A95DB-` 账号待 Harness 在最终 Main 后收尾核验。
