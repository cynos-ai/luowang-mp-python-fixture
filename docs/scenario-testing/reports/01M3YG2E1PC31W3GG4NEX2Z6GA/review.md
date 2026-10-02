# 审核记录 — 会话状态与合成数据路径核心场景（Run `01M3YG2E1PC31W3GG4NEX2Z6GA`，target `9c864dff252814432d4e1ec7776a60c04eac32ae`）

## 审核范围与依据

- 固定 target：`9c864dff252814432d4e1ec7776a60c04eac32ae`；本次无 `scenario-changes.patch`（工件不存在），与计划「本批不新增/不修改/不废弃场景」的声明一致；`planHash` = `49340ecf…cedf13`，与 `plan.md` 顶部 Harness 元数据及 `query_source_reads(scope:plan)` 返回一致。
- 执行集合（计划唯一的 `## execution_scenarios`，共 4 项）：`AUTH-LOGIN-001` → `AUTH-SESSION-001` → `AUTH-REGISTRATION-001` → `DATA-STORAGE-001`。
- 本审核独立按 `list_evidence_files` 逐条读取原始 `operation-*.json`、`page-*.yml`、`console-*.log` 与 4 张截图，先形成判断后再打开 `execution.md` 对照；下述观察除明确标注为「Runner 陈述」外均为 Reviewer 自证据得出。
- `browserRequired=true` 与真实执行一致：确有 Playwright MCP 的 `browser_navigate`/`browser_snapshot`/`browser_fill_form`/`browser_click`/`browser_take_screenshot` 与页面快照、控制台记录（`operation-9`–`21`、`24`–`40`）。`browserRequired` 本身未被当作能力或结果证明。
- 计划来源校验：`query_source_reads` 显示 `docs/PROJECT.md`、`spec.md`、`intent.md`、4 份场景正文、历史 Run 报告为 `fullSafeText=true`、`redacted=false` 全文读取；`app.py` 为 `fullSafeText=true`、`redacted=true`（脱敏全文）。引用校验通过只证明来源与范围成立，本审核不据此改写任何期望。

## 逐场景结论

### AUTH-LOGIN-001 — passed

- 前置与操作（Reviewer 自证据）：`operation-3`（14:26:22.575Z）以 clientId `login-001` 调用 `POST /api/auth/register` 得 **201**、`setCookieNames:["sid"]`，响应用户为 Run 前缀账号（`…-login@example.test`，邮箱小写归一）；`operation-4`（14:26:23.795Z）以独立 clientId `login-001-fresh` 调用 `POST /api/auth/login` 得 **201**、`setCookieNames:["sid"]`，响应用户与注册账号一致；`operation-5`（14:26:25.153Z）同 client 读 `GET /api/auth/status` 得 **200**、`{"authenticated":true,"user":{…-login@example.test}}`、`cookieNames:["sid"]`、`setCookieNames:[]`。
- 期望核对：登录请求成功（2xx：201）且设置会话 Cookie（`sid`）→ 满足；`status` `authenticated` true 且 `user.email`/`displayName` 与所登录账号一致 → 满足（登录响应体与 `status` 响应体的用户字段相同）。
- 记录：口令值未在证据中复述；账号用 Run 前缀。

### AUTH-SESSION-001 — passed

- 步骤 1（匿名）：`operation-8`（14:26:28.243Z）以 `session-anon` 客户端读 `GET /api/auth/status` → **200**、`{"authenticated":false}`、`cookieNames:[]`、`setCookieNames:[]`。该读取发生在浏览器会话被注册预热之前（浏览器首次导航为 `operation-9`，14:26:29.181Z），满足计划「匿名对照必须冷态」的要求。
- 步骤 2（页面注册并已登录）：`operation-9/10` 导航并快照 `GET /`（表单：昵称/邮箱/密码 + 注册按钮）；`operation-11` 填表、`operation-13` 点击注册（注意 `operation-12` 为一次带 `isError:true` 的 `browser_click`，属工具参数被拒，见下）；`operation-14` 快照显示状态区 `status` 实际文本 `你好，[REDACTED]。`、表单值仍在；同浏览器会话 `operation-15/16` 导航 `GET /api/auth/status` 得 `{"authenticated":true,…,"email":"…-session@example.test"}`。Run 前缀邮箱成立。
- 步骤 3（刷新后保持）：`operation-17/18` 重新导航 `GET /`（快照为应用页，表单与状态区为空，符合刷新后页面初始态），`operation-18/19` 再读 `status` 得 `{"authenticated":true,…,"email":"…-session@example.test"}`，与步骤 2 邮箱完全一致。
- 期望核对：三条期望均满足。用户信息「不变」以邮箱逐字一致 + 同一浏览器会话为依据；两处 `displayName` 均被 Harness 脱敏为 `[REDACTED]`，无法逐字比对，属记录层限制（见覆盖缺口第 3 条），不影响该判定。
- 截图：`session-001-after-register.png`（`operation-21`，14:26:42.533Z）实际内容为刷新后的 `GET /` 页面（表单空白、状态区空白），并非「显示已登录状态」的画面；本场景的已登录证据来自 `operation-16`/`operation-19` 的 `status` 快照，不依赖该截图。Runner 对该截图的描述与之不符，见「报告符合性」第 1 条。

### AUTH-REGISTRATION-001 — passed

- 步骤 1：`operation-24/25` 导航 `GET /`，快照确认昵称、邮箱、密码三字段与「注册」按钮可见。
- 步骤 2–3（主次注册）：`operation-26` 填表、`operation-27` 点击（14:26:49.265Z）后 `operation-28` 快照状态区 `status [ref=f5e12]` 实际文本 `你好，[REDACTED]。`；随后 `operation-30/31` 读 `GET /api/auth/status` 得 `{"authenticated":true,…,"email":"…-welcome@example.test"}`，与场景指定邮箱 `luowang-<runId>-welcome@example.test` 一致。为取得「欢迎语可见」的页面截图，Runner 在同一场景窗口内又经页面注册 `…-welcome2`（`operation-35/36/37`），提交后状态区同为 `你好，[REDACTED]。`，`operation-38` 截图 `registration-001-welcome-visible.png`，`operation-40` 读 `status` 得 `authenticated:true`、邮箱 `…-welcome2@example.test`。
- Reviewer 对截图的独立判读：`registration-001-welcome-visible.png`（`screenshotInspection: detected`，sha256 `08a39ee5…`）显示真实页面：「Python 账号实验站」标题、三字段表单（昵称与邮箱框内为 `luowang-01M3YG2E1PC31W3GG4NEX2Z6GA-welcome2` 系列 Run 前缀值，密码框为掩码）、页面状态区文本 **`你好，luowang-01M3YG2E1PC31W3GG4NEX2Z6GA-welcome2。`**、下方「删除账号」按钮。即：欢迎语为中文模板「你好，<昵称>。」，且昵称位就是同页表单中所填的昵称值。
- 期望核对：
  - 「注册请求成功」→ 满足（页面注册后同会话 `status` 为 `authenticated:true` 且为用户账号）。
  - 「并设置会话 Cookie（`sid`）」→ 支持但为间接：页面表单提交的响应头未被捕获，`Set-Cookie: sid` 未直接观察；依据是同一浏览器会话在页面注册后变为已认证（`operation-16`、`operation-31`），且该应用会话仅能由 `sid` Cookie 承载；此外 HTTP 侧 `POST /api/auth/register` 在 `operation-3` 明确观察到 201 + `setCookieNames:["sid"]`。本审核按「充分但不直接」采纳，并记 1 条覆盖限制（见覆盖缺口第 2 条）。
  - 「`#message` 显示文本为 `你好，<昵称>。`，昵称为步骤 2 提交值」→ 满足（截图逐字可见；快照文本同模板，昵称位因脱敏为 `[REDACTED]`）。
  - 「`status` `authenticated` 为 true 且 `user.displayName` 与提交昵称一致」→ 满足但组合支持：`status` 的 `displayName` 被脱敏，无法直接比对；一致性由「截图显示状态区渲染出的昵称 = 表单所填昵称」+「`status` 邮箱与提交邮箱一致」共同支持。
- 偏差：为补截图而注册的第二个账号昵称为 `…-welcome2`，非场景步骤 2 字面值 `…-welcome`（该字面值已由首次注册的邮箱 `…-welcome@example.test` 与对应快照满足）。该偏差是同一表单、同一 Run 前缀、同类型账号的等价操作，改变的是账号标识而非断言语义，不影响期望判定；Runner 已在正文说明该取舍。

### DATA-STORAGE-001 — passed（保留聚合口径限制）

- 观察口径与结果：`operation-43`（14:27:07.228Z，`controlled-run-cleanup-http`，`authorization: "configured"`，`runIdKind: "current"`）`GET` storage 资源 → **200**、`cache-control: no-store`、`{"accounts":4,"argon2id":4,"other":0,"runId":"01M3YG2E1PC31W3GG4NEX2Z6GA"}`；`operation-44`（`controlled-test-account-storage`）给出同一组计数 `accounts=4, argon2id=4, other=0`。
- 期望核对：
  - 「该 Run 聚合观察 `accounts == argon2id` 且 `other == 0`」→ 直接满足（4 == 4，other 为 0）。
  - 「持久层保存形如 `$argon2id$` 前缀的 PHC 字符串、不出现明文口令」→ 间接支持：`argon2id` 桶与 `accounts` 全等、`other` 为 0，意味着本 Run 全部账号的持久值均归入按 `$argon2id$` 前缀归类的桶、且无其他格式值；但未读到任何单条 `users.password_hash` 正文。本审核按计划保留的覆盖缺口处理，记为间接支持，不改写为「已直接观察」，也不据此弱化或强化该子项。
- 本 Run 4 个账号 (login/session/welcome/welcome2) 与 `accounts=4` 计数自洽。
- 注意：Runner 称 `operation-43` 与 `operation-44` 为「两个独立通道」。二者是**同一聚合数据源**经两种受控工具读取（计数完全相同），相互印证但不能算作两条独立证据来源；这是叙述口径问题，不改变该场景判定。

## 已确认的产品问题

- 本次 4 个场景未发现产品不符合预期：无 failed。中文欢迎语、会话建立/保持、Argon2id 聚合持久化在本次实际观察中均与场景期望一致。
- 明确不对历史 Issue #4（英文欢迎语）作「已修复」等结论：本次只记录实际观察到的页面文本为中文；历史状态不作为本次判定依据，本次也不更新历史结论。
- 页面控制台存在 1 条 `favicon.ico` 404 与 1 条 autocomplete 建议（`console-2026-10-02T14-26-29-319Z.log`）：均不在 4 个场景的适用期望内，不判为产品缺陷，如实记录。

## 覆盖缺口与未验证项

1. **无 base 基线**：`baseCommit=null`、`includedCommits=[]`，无法给出变化清单/diff，不能判断 target 的变更内容；场景选择依据当前 target 正文与历史线索，此为范围限制，非代码结论。
2. **`sid` Set-Cookie（页面注册路径）未直接观察**：`AUTH-REGISTRATION-001` 的页面表单提交响应头未被捕获，`sid` 设置由同会话已认证状态与 HTTP 侧注册观察间接支持，非直接证据。
3. **`displayName` 逐字比对不可得**：`AUTH-SESSION-001`（两次读取）与 `AUTH-REGISTRATION-001`（`status` 读取）的 `displayName` 均被脱敏为 `[REDACTED]`。「用户信息不变」「displayName 与提交昵称一致」由邮箱逐字一致、同一会话及可见截图组合支持，未做逐字比对。
4. **DATA-STORAGE-001 持久层正文未观察**：仅有聚合计数；`$argon2id$` 前缀与「无明文」为归类结果推得的间接支持。场景步骤 3 本身为条件式（「如可获得只读持久层访问」），本次未获得，作为既有覆盖缺口保留。
5. **口令强度前置未独立核验**：页面填表参数与密码框内容均被脱敏，无法验证「不少于 12 字符」的前置条件；该条为前置条件而非期望，未影响期望判定结果，但记录为不可独立核对项。
6. **账号登记/清理与清理后核验**：证据中无清理动作或清理后核验记录；Runner 声明显式将清理交由 Harness 收尾，登记状态为 `registered`（其中 3 项在 `execution.md` 中被脱敏）。按共同规则，测试数据收尾属 Harness 事项，其未完成不改变已成立的产品结论；此处仅记为待办，不构成本次阻塞。
7. **未选场景未执行**：计划列出的 `AUTH-LOGIN-002`、`AUTH-REGISTRATION-002/003`、`AUTH-DELETE-*`、`CLEANUP-*`、`STORAGE-OBSERVE-001` 不在本请求范围，本次未执行，其结论不被本次改写。

## 报告符合性（`execution.md` 与原始证据的差异）

1. **截图说明不符**：Runner 称 `session-001-after-register.png`「在 AUTH-SESSION-001 的已登录页面状态下拍摄」。该图（`operation-21`）内容为刷新后的 `GET /` 页面（表单空白、状态区空白），其 sha256 `0bcd605f…` 与 `registration-001-welcome-page.png` **完全相同**，画面中不含任何已登录标识。已登录状态实际由 `operation-16`/`operation-19` 的 `status` 快照支持。该差异属证据描述问题，不改变场景判定；下游若引用该图说明「已登录页面」，会超出图面实际内容。
2. **「两个独立通道」表述偏强**：见 DATA-STORAGE-001 条，实为同一聚合数据的两次读取。
3. **汇总表略强于正文**：汇总表将 `AUTH-REGISTRATION-001` 依据写作「status authenticated true 且 displayName 一致」，而正文已自承 `displayName` 为脱敏呈现；判定仍成立，但下游应采用正文口径（组合支持）。
4. **可核对的陈述均被证据支持**：执行的场景与顺序、`start/finish_scenario` 配对（`operation-1/2/6/7/22/23/41/42/45`，无越序）、事件时间线、`operation-12` 的 `browser_click` 被 schema 拒绝后重试、`registration-001-welcome.png` 实为状态端点截图等，经 Reviewer 逐条核对与 Runner 描述一致（细节补充：`registration-001-welcome.png` 的图面确为 `{"authenticated":true,…-welcome@example.test}` 的 JSON 页面）。

## 汇总

| 场景 | 结果 | 关键依据 |
| --- | --- | --- |
| AUTH-LOGIN-001 | passed | `operation-4`（登录 201 + `sid`）、`operation-5`（`status` true，用户一致） |
| AUTH-SESSION-001 | passed | `operation-8`（冷态匿名 false）、`operation-14/16`（页面注册后 `#message` 中文 + `status` true）、`operation-18/19`（刷新后 true，邮箱一致） |
| AUTH-REGISTRATION-001 | passed | `operation-24/25`（表单可见）、`operation-28/37`（`#message` `你好，…。`）、`registration-001-welcome-visible.png`（昵称与欢迎语一致）、`operation-31/40`（`status` true，邮箱一致） |
| DATA-STORAGE-001 | passed（保留聚合口径限制） | `operation-43`/`operation-44`（`accounts=4=argon2id`，`other=0`） |

- 计数：执行场景 4；passed 4；failed 0；blocked 0。已确认产品 Bug 0；上述覆盖缺口 7 条（其中第 2、3、4 条为影响判定强度的记录/口径限制，不构成阻塞；第 6 条为 Harness 收尾待办）。
- 本审核未执行任何命令、未读取账号或仓库路径、未做补测；缺口与待办依授权交由后续流程与 Harness 收尾处理。
