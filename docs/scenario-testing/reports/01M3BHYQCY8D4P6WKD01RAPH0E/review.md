# review.md — 独立审核（AUTH/STORAGE/CLEANUP 场景 Run `01M3BHYQCY8D4P6WKD01RAPH0E`）

- Target：`499b00378dec10c2d32dfec2354b144a1731b757`
- 审核对象：`plan.md`（planHash `8739f3e84d8639369dfb9bfc8160b3f72cea934d24423053d44d8fd39ad663d0`）、冻结的 `selectedScenarioSnapshot`（13 个 approved 场景，均 `redacted:false`）、原始命令/MCP 证据、`execution.md`
- 审核角色：Reviewer（只读本 Run 允许工件与证据；未执行任何补测、未访问目标仓库、未读取账号或任意路径）
- 结论摘要：**与 Runner 一致的分布为 1 failed / 2 passed / 10 blocked**；逐场景依据见下。发现 1 项已确认产品缺陷（注册欢迎语语言不符契约），若干记录与报告口径问题，以及关键能力缺口导致的覆盖缺口。

## 0. 审核范围与前置核对

- `scenario-changes.patch` 不存在；`plan.md` 明确声明“本批不产生 scenario patch”。**维护声明成立**：本批无新增/修改/拆分场景，计划也未声称做过维护，两者一致，无需核对 patch 内容。
- `plan.md` 的 `## execution_scenarios` 列出 13 项，与冻结快照的 13 个场景 ID 一一对应，顺序一致；逐场景正文以快照为准（未脱敏（`redacted:false`），无正文遮蔽缺口）。
- `query_source_reads`（scope=plan）返回的 planHash 与计划开头 Harness 元数据一致；24 条引用中 22 条为场景/规范/项目文档 `full-file`，`app.py` 与 `tests/test_app.py` 标记为脱敏读取。计划对实现的判断（英文欢迎语）属**实现事实陈述**，我只把它当作线索，判定依据是场景正文与浏览器实际观察。
- `browserRequired: true` 与执行相符：本 Run 存在真实浏览器操作（Playwright MCP 的导航/填表/点击/快照/截图/网络记录，时间 05:53–05:57），并有 3 张截图与 30 余份快照/控制台记录落盘。计划声明的“需浏览器观察项（#message 文本、刷新保持登录、删除按钮反馈）”确实以浏览器方式执行。
- 时间口径：页面/工具事件时间为 Harness 记录时间，服务器响应头 `date` 为被测服务器时间，二者无共同校准基准；本审核只使用先后顺序与 Harness 记录时间，不据此断言精确时刻。

## 1. 已确认的产品问题

### P1（唯一的直接契约违反）：注册成功后页面状态区显示英文欢迎语

- 期望（冻结场景 AUTH-REGISTRATION-001，`## 期望` 第 2 条）：页面 `#message` 显示文本为 `你好，<昵称>。`。
- 实际（我的独立观察）：
  - 快照 `page-2026-09-25T05-54-08-271Z.yml`、`page-2026-09-25T05-54-22-866Z.yml`：状态区文本为 `Welcome, [REDACTED].`（英文前缀 `Welcome,` 未脱敏，可读）。
  - 截图 `auth-registration-001-welcome-message.png`（我自己用 `read_evidence_image` 打开）：页面正文第 3 行显示 `Welcome, luowang-01M3BHYQCY8D4P6WKD01RAPH0E-welcome2.`，页面上确同时出现中文标题「Python 账号实验站」与中文按钮「注册」「删除账号」。
  - 对照证据：删除路径的状态文本是中文（快照 `page-2026-09-25T05-56-34-953Z.yml` = `账号已删除。`；`page-2026-09-25T05-57-03-602Z.yml` = `删除失败。`）。即同一状态区在删除路径为中文、在注册成功路径为英文。
- 预期/实际差异与复现条件：浏览器打开 `GET /`，用页面表单提交合法昵称/邮箱/≥12 字符口令并注册成功，随后读取状态区文本 → 得到英文 `Welcome, <displayName>.`，而非中文 `你好，<昵称>。`；同一会话的 `POST /api/auth/register` 返回 201 且设置 `sid`（`operation-33/34/35`：201 CREATED、响应体含 `user.displayName`/`user.email`），说明失败点只在页面文案。
- 判定依据归属：期望来自冻结场景正文（不是我补充的要求）。Runner 在 `execution.md` 中记录同一事实并判 failed；我的结论与之一致，但依据为我自行读取的快照与截图。
- 影响：AUTH-REGISTRATION-001 判 **failed**。

## 2. 逐场景独立结果

引用说明：下列 `operation-N` / `command-N` / `page-*.yml` / 截图为本 Run 证据 ID（`list_evidence_files` 中的 name）；我用 `read_command_evidence`、`read_browser_evidence`、`read_evidence_image` 逐一读取。

| # | 场景 | 我的判定 | 依据 |
|---|---|---|---|
| 1 | AUTH-REGISTRATION-001 | **failed** | 见 P1。注册 201（`operation-33/34/35`）+ `sid` 已设置（`operation-30` 记录 `sid` 观察）+ `GET /api/auth/status` = authenticated true 且 email 为提交邮箱（快照 `page-2026-09-25T05-54-12-686Z.yml`）；但状态区为英文 → 违反第 2 条期望。 |
| 2 | AUTH-REGISTRATION-002 | **blocked** | 已确认：第二次同邮箱注册 → 409（`operation-44` 网络列表 `[409] CONFLICT`、`operation-55` 快照状态区 `ACCOUNT_EXISTS`、截图 `auth-registration-002-dup-rejected.png` 我打开后可见页面显示 `ACCOUNT_EXISTS`，无成功文案）；随后会话仍指向原账号（快照 `page-2026-09-25T05-54-36-634Z.yml` = authenticated true 且 email `...-dup@example.test`）。未确认：`POST /api/auth/login`（原邮箱+原口令）从未发出 → “原账号仍可用原凭据登录、昵称为首次值”未验证。 |
| 3 | AUTH-REGISTRATION-003 | **blocked** | 只有页面表单路径：填表后点击「注册」，网络列表为空（`operation-72`），状态区保持空（`operation-73` 快照 `status` 无文本），即浏览器原生校验在客户端拦下，服务端从未收到三类非法请求。场景正文明确“本场景需直接调用接口”，该能力缺失 → 三条期望全部未验证。 |
| 4 | AUTH-LOGIN-001 | **blocked** | 唯一相关动作是对 `/api/auth/login` 的 **GET**：`operation-76` 快照 `Method Not Allowed`，控制台 `console-2026-09-25T05-56-07-276Z.log` = `405 (METHOD NOT ALLOWED) @ /api/auth/login`。无任何 2xx 登录、无 `sid` 建立观察。 |
| 5 | AUTH-LOGIN-002 | **blocked** | 场景窗口（进度序 104→105）内**没有任何**归属该场景的操作记录；错误口令/未知邮箱的请求与其后的正确凭据登录均无证据。 |
| 6 | AUTH-SESSION-001 | **passed** | 匿名：快照 `page-2026-09-25T05-56-10-827Z.yml` = `{"authenticated":false}`，且同刻 `cookie_list` 无 `sid`（`operation-108` 无 credentialReferences）。注册后：`operation-115` 记录 `sid`，快照 `page-2026-09-25T05-56-18-502Z.yml` = authenticated true、email `...-session@example.test`。刷新后：快照 `page-2026-09-25T05-56-21-729Z.yml` 与截图 `auth-session-001-reload.png`（我打开后为 `/api/auth/status` 的 JSON：`{"authenticated":true,"user":{"displayName":"luowang-01M3BHYQCY8D4P6WKD01RAPH0E-session",...}}`）用户信息不变。三条期望均有实际观察支持。 |
| 7 | AUTH-DELETE-001 | **blocked** | 已确认：删除后状态区 `账号已删除。`（快照 `page-2026-09-25T05-56-34-953Z.yml`）、`sid` 被清除（`operation-130` credentialReferences 为空）、随后 `GET /api/auth/status` = false（`operation-134`）、重复删除 → `DELETE /api/me` 401 且页面 `删除失败。`（`operation-138`、`page-2026-09-25T05-56-42-936Z.yml`、控制台 `console-2026-09-25T05-56-39-937Z.log`）。未确认：步骤 4 “原邮箱+原口令 `POST /api/auth/login` 被拒”无任何请求记录 → 该期望未验证。（另注：首次 DELETE 的 2xx 状态行未被保留，删除成功系由文案+Cookie 清除+账号计数间接支持。） |
| 8 | AUTH-DELETE-002 | **blocked** | 已确认：对照账号注册并登录（快照 `page-2026-09-25T05-56-52-265Z.yml` = authenticated true、email `...-delete2@example.test`）；构造未鉴权客户端取自 `browser_cookie_set`（`operation-149`，restore-input 覆盖 `sid`），其 `GET /api/auth/status` = false（快照 `page-2026-09-25T05-56-56-376Z.yml`）；匿名 `DELETE /api/me` → 401（`operation-157`、控制台 `console-2026-09-25T05-57-00-297Z.log`）。未确认：对照账号原凭据仍能登录（无 `POST /api/auth/login`）；“账号未被删除”仅有本 Run 计数 5 的间接支持（`operation-150`）。 |
| 9 | DATA-STORAGE-001 | **passed（附覆盖限制）** | 受控只读存储观察 `operation-56`（accounts 3）与 `operation-133/136/150`（accounts 5、argon2id 5、other 0）：`accounts == argon2id` 且 `other == 0` 成立，与场景期望第 1 条逐字对应。第 2 条（Argon2id PHC、无明文）以该三桶口径支持（非 Argon2id 值计入 `other`，`other=0`）。限制：观察为计数值，未读到哈希字符串前缀，也未直接排除明文；口径依赖契约对 `other` 的定义。 |
| 10 | STORAGE-OBSERVE-001 | **blocked** | 只有无 Token 请求：`operation-.../console-2026-09-25T05-57-20-965Z.log`（`.../<runId>-` 401）与 `console-2026-09-25T05-57-23-229Z.log`（`.../<runId>-/storage` 401）；侦察期另有同端点 401 与 `not-a-valid-run-id` 的 401（`console-2026-09-25T05-53-52/53/55*.log`），均为**鉴权先于 Run ID 校验**，不能证明“带有效 Token 的非法 Run ID 被拒”。响应体字段清单与响应头、带 Token 的成功响应均未观察。 |
| 11 | CLEANUP-AUTH-001 | **blocked** | 仅步骤 1 部分成立：无 Token 的 `GET .../<runId>` 与 `.../storage` 均 401、响应体仅 `{"error":"UNAUTHORIZED"}`（快照 `page-2026-09-25T05-57-20-993Z.yml`、`page-2026-09-25T05-57-23-254Z.yml`）。错误 Token 的 GET/GET/DELETE 与“该账号仍未被删且原凭据仍可登录”全部未执行（无任意请求头能力、无 `POST /api/auth/login`）。 |
| 12 | CLEANUP-SCOPE-001 | **blocked** | 场景窗口内无任何归属操作，无清理前余量、无 `DELETE` 删除数、无独立余量、无非法 Run ID 与凭据失效观察。 |
| 13 | CLEANUP-SEED-001 | **blocked** | 场景窗口内无任何归属操作；另一个合法 Run ID 的余量对照、本 Run 清理执行、预置账号登录均无证据。 |

分布核对：failed 1 + passed 2 + blocked 10 = 13，与 `execution_scenarios` 项数一致，无重复计入或遗漏。

## 3. 计划与场景适当性

- **重要遗漏**：本 Run 唯一直接影响结论的场景集选择问题，是 `CLEANUP-CONFIG-001`（draft）未纳入——计划已说明理由（需以自定义环境变量启动多个实例，是否可构造待确认）。因此 spec 契约第 4 条“清理接口默认关闭 / 短 Token 拒绝启动”在本批**没有任何真实执行覆盖**，属已知缺口而非审核遗漏；draft 状态不在 approved 全集，纳入与否不属于本批“必要场景被豁免”。
- **场景写法**：AUTH-REGISTRATION-003 的前置已写明“页面表单的原生校验会阻止不合法输入提交，因此本场景需直接调用接口”，正确；本 Run 未具备该能力，属能力不足而非场景缺陷。AUTH-DELETE-002 用“无效 `sid`”近似“无会话 Cookie”：对服务端而言两者同为未鉴权（`/api/auth/status` 返回 false、`DELETE` 返回 401），属可接受的等价操作方式，不改变该场景其余期望的未验证结论。
- **是否需要新增场景**：不需要。已有 approved 场景覆盖了本次请求的重点（中文欢迎语、登录/删号、Argon2id 存储观察、Run 范围清理）；缺口源于工具能力，而非场景缺失。

## 4. 执行到位性核对（计划期望 vs 实际）

- 注册成功路径、重复邮箱路径、匿名/登录状态、页面刷新、删除与重复删除、未鉴权删除、存储计数、无 Token 拒绝：均有真实浏览器/受控观察。
- **未执行到位的必要步骤（均为能力缺失导致）**：
  1. 无法发出 `POST /api/auth/login`（页面无登录表单；受控命令禁 `curl`/`wget`/内联解释器代码/任意脚本：`command-4/5/6/12/15/16/17/19~26`；对 `/api/auth/login` 的 GET → 405，`console-2026-09-25T05-54-59-942Z.log`、`console-2026-09-25T05-56-07-276Z.log`）。此外用 `data:text/html` 页面内 `fetch` 的尝试被 CORS 拦下（`console-2026-09-25T05-55-36-678Z.log`：`blocked by CORS policy … origin 'null'`，页面 `ERR:TypeError: Failed to fetch`），该路径不可用。
  2. 无法发出带自定义 `Authorization` 头的请求（清理/存储端点始终 401，未见任何携带部署级 Token 的请求记录）。因此带 Token 的字段/响应头检查、错误 Token 检查、清理范围与余量核验全部无法完成。
- 这些是**验证能力不足**，不是“不适用”。相应适用期望一律保持未验证，未被我或 Runner 降级为可选。

## 5. 与 `execution.md` 的核对

- **结论一致部分**：分布（failed 1 / passed 2 / blocked 10）、失败场景与缺陷描述（英文 `Welcome, <昵称>.`）、各 blocked 的成因分类、能力缺口说明、清理延后至 Harness 的说明，均与我从原始证据得到的判断一致。Runner 引用的 `operation-56/133/136/150`（存储计数 3→5）、`operation-22/33`（`Welcome` 快照）、`operation-72/73`（非法输入未发出请求）、`operation-138`（重复删除 401）、`console-05-55-36-678Z`（CORS）等 ID 与内容我逐条回读后成立。
- **报告口径问题（不影响产品结论，但影响追溯）**：
  1. `execution.md` 第 1 节“可用受控能力/能力缺口”一条存在**截断与错位**：出现 `无法发出带自定义 \`Authorization: [REDACTED]` 后即中断，紧随其后插入了本应属于“偏差”段的“标准偏差：…”整句。该处表述不完整，后续角色据此可能无法完整复原能力边界（实质结论与我观察一致，仅文本残缺）。
  2. DATA-STORAGE-001 在报告中被记为 passed 并以“限制”方式说明“未直接读取单个哈希前缀”。我认可其通过，但请注意这是**依赖 `other` 口径的推断**；若后续要坐实“PHC 前缀/无明文”，仍需带 Token 的存储端点或直接持久层读取。
  3. 报告把 AUTH-DELETE-002 的“对照账号未被删除”写作“符合（计数证据）”。计数 5 只能间接支持（本 Run 结束时存活账号集合与登记列表吻合），我保留为“间接支持”，未写成直接观察。
- **归属声明**：上述第 1 条的记录问题是我在证据中发现的，Runner 未在报告中提及；英文欢迎语缺陷为 Runner 已明确写出、我也独立复现的事实；其余数值（计数、状态码）为我在证据中的直接观察。

## 6. 执行记录异常（与产品结论分开）

- **进度事件标签错位**：`finish_scenario` 事件的 `scenarioId` 指向的是**下一个**场景，而 `completed` 数组列的是刚完成的场景（如序 44：`event=finish_scenario, scenarioId=AUTH-REGISTRATION-002, completed=[…AUTH-REGISTRATION-001]`）。因此不能按 `scenarioId` 字段判断某段操作属于哪个场景；我按 `completed` 语义与操作自身的 `execution.scenarioId` 归属核对。最后一次事件（序 175）把所有 13 项列为 completed，但如第 2 节所示，其中 CLEANUP-SCOPE-001 / CLEANUP-SEED-001 窗口内无任何操作记录——**“最后 completed=13/13”不代表 13 项均已实际执行**。
- 场景之间无“先完成再补执行”的跨场景操作错配；但存在大量与场景无关的侦察操作（`data:text/html` 探测、对 `/api/luowang/test-data/…` 无 Token 探测、`/api/auth/login` GET 探测），其中 `data:` 探测导致浏览器会话 Cookie 被清空的副作用已由 Runner 主动披露（`execution.md` 第 5 节），与证据相符。

## 7. 覆盖缺口与未完成项

1. 所有依赖 `POST /api/auth/login`、以及依赖 `Authorization: Bearer` 的期望未验证（影响 AUTH-REGISTRATION-002、AUTH-DELETE-001/002、AUTH-LOGIN-001/002、STORAGE-OBSERVE-001、CLEANUP-*）。
2. AUTH-REGISTRATION-003 的服务端校验路径完全未触及（仅客户端原生校验）。
3. `CLEANUP-CONFIG-001`（draft）未执行，契约第 4 条的“默认关闭 / 短 Token 启动拒绝”无运行覆盖。
4. 合法 Run ID 清理与“其他 Run 余量不变”“预置账号免于清理”均无观察；本 Run 结束时存储计数仍为 5（`operation-150`），即本 Run 的清理**尚未执行**——按流程这属 Harness 在最终 Main 后的收尾事项，不构成场景阻塞，但 CLEANUP-SCOPE-001/SEED-001 自身的期望仍为未验证。
5. 快照脱敏使 `displayName` 无法逐字比对；AUTH-REGISTRATION-001 中“显示昵称 == 提交昵称”一项只能依据“显示值以提交昵称结尾 + 注册响应邮箱一致”间接支持，主要失败点（语言）不受此影响。
6. 关于口令记录：我读到的证据中，表单值与请求体中的口令均以 `[REDACTED]` 呈现（如 `console-2026-09-25T05-55-36-678Z.log` 的命令行内容、各 `browser_fill_form` 的 `value`），未见复述；我**未执行**系统性 Secret 扫描，故这不构成“记录中不存在任何口令文本”的绝对结论。

## 8. 审核结论

- 本批计划与场景选择可用，无场景 patch 因而无维护声明冲突；执行确实发生在固定 target 的真实浏览器与受控存储观察上（`browserRequired: true` 与执行相符）。
- 13 个场景的独立结果：**passed 2（AUTH-SESSION-001、DATA-STORAGE-001）/ failed 1（AUTH-REGISTRATION-001）/ blocked 10**。
- 已确认产品缺陷 1 项：注册成功后状态区显示英文 `Welcome, <昵称>.`，违反冻结场景与 spec 契约要求的 `你好，<昵称>。`（复现条件见第 1 节）。
- 10 项 blocked 的成因是验证能力不足（无法发出 `POST /api/auth/login`、无法携带 `Authorization` 头、无法发任意 JSON 请求），并非产品行为被判定失败；这些期望保持未验证，不应被改为 passed 或从范围中移除。
- 测试数据收尾（本 Run 前缀账号清理与核验）由 Harness 在最终 Main 后处理，本审核不作判定。
