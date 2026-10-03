---
run_id: 01M3ZYK18129P9JM799X1A95DB
trigger: manual
base_commit: null
target_commit: fa65797585b6a196f7d5a41099593ee3376ca4cd
included_commits: []
result: passed
started_at: 2026-10-03T03:58:11.432Z
finished_at: 2026-10-03T04:01:14.275Z
scenario_results:
  - id: AUTH-LOGIN-001
    result: passed
  - id: AUTH-SESSION-001
    result: passed
  - id: AUTH-REGISTRATION-001
    result: passed
  - id: DATA-STORAGE-001
    result: passed
confirmed_bugs: []
---

# 测试报告 — Run `01M3ZYK18129P9JM799X1A95DB`

汇总依据：本 Run 的 `plan.md`（planHash `8e75153fec01d42bea6d98ad35c997bfe57fb36d424e2c38c7f32a2f02d8e878`）与 Reviewer 交付的 `review.md`。本报告是对既有工件的整理，未重新执行测试，也未重做独立证据审核；所有逐场景观察均归属执行与审核环节。

## 范围与固定版本

- 请求：对固定 `scenario-testing` 提交执行已有 approved 核心场景，覆盖「登录后的会话状态」与「一条独立合成数据路径」两类业务结果；使用受控测试账号，新增数据登记并带本 Run ID；截图保留真实页面状态；应用与数据域独立；遵守场景既定期望。
- target：`fa65797585b6a196f7d5a41099593ee3376ca4cd`；base 为 `null`；includedCommits 为空。
- 因此本批为**无 base 的固定提交回归**：没有 diff 依据，无法据此判断 target 相对历史改了什么，也不依据变化清单裁剪范围。该限制由 Reviewer 复核确认，且不影响按场景既定期望判定。
- 本 Run **无 `scenario-changes.patch`**（Reviewer 读取返回不存在），与计划「本次无场景资产变更（不新增、不修改、不废弃）」一致；请求亦要求不修改场景 patch。场景资产维护需求本次未出现，不涉及产品 Bug 性质的资产问题。
- 执行集合（计划唯一 `## execution_scenarios`，顺序即执行顺序）：`AUTH-LOGIN-001` → `AUTH-SESSION-001` → `AUTH-REGISTRATION-001` → `DATA-STORAGE-001`。Reviewer 以命令证据中的 `scenario-progress` 记录核对该顺序，显示声明顺序与实际顺序一致、无跨场景补跑，末次 `completed` 为 4/4。

## 结果汇总

| 场景 | 结果 | 审核依据（Reviewer 交付） |
| --- | --- | --- |
| AUTH-LOGIN-001 | passed | `operation-3/4/5` |
| AUTH-SESSION-001 | passed | `operation-8/13/14/15/18/21` + `auth-session-registered.png` |
| AUTH-REGISTRATION-001 | passed | `operation-28/29/30/32` + `auth-registration-welcome.png` |
| DATA-STORAGE-001 | passed | `operation-37/38/39` |

分布：passed 4 / failed 0 / blocked 0。Harness 阻塞原因为空（`blockingReasons: []`），Runner 未声明 Harness 阻塞；聚合结果按 `blocked > failed > passed` 取 passed。

## 逐场景结果与依据

### AUTH-LOGIN-001 — passed

适用期望及 Reviewer 依据（均归 Reviewer 判断）：

- 登录请求成功并设置会话 Cookie（`sid`）：`operation-4.json` 记录 `POST /api/auth/login`（clientId `login-001`）状态 201，`setCookieNames=["sid"]`，登录前无已发送 Cookie。
- `GET /api/auth/status` 返回 `authenticated=true` 且 `user.email`/`user.displayName` 与所登录账号一致：`operation-5.json` 同客户端带 `sid` 返回 200，正文含 `authenticated:true` 与登录账号一致的用户信息；前置账号由 `operation-3.json` 的本 Run 前缀注册产生（`luowang-<runId>-login`）。Reviewer 记 email 大小写差异为服务端规范化，非不一致。

无偏差，无未验证子项。

### AUTH-SESSION-001 — passed

- 步骤 ①：`operation-8.json`（clientId `anon-session`，无已发送 Cookie）返回 `{"authenticated":false}`；Reviewer 确认是**无任何会话 Cookie 的冷客户端**，非「退出后读取」或换页面替代。
- 步骤 ②：注册在真实浏览器页面完成（`operation-9/10` 导航并确认表单三字段、`operation-11` 页面填表、`operation-12` 一次点击回执 `isError=true`、`operation-13` 点击成功并带快照、`operation-14` 快照显示状态区 `你好，[REDACTED]。`、`operation-15` 观察浏览器 `sid` Cookie、`operation-16` 截图 `auth-session-registered.png`），随后 `operation-17/18` 读出 `authenticated:true` 与含 `…-session@example.test` 的用户信息。
- 步骤 ③：`operation-19` 重新加载 `GET /`（快照 `page-…25-011Z.yml` 为无会话态表单页，状态区为空），`operation-20/21` 再读状态仍 `authenticated=true` 且 email 与步骤 ② 完全一致。

Reviewer 记录的限制（不影响其判定）：状态响应中的 `displayName` 在快照中被脱敏为 `[REDACTED]`，无法字段级逐字读取；账号一致性由可见邮箱两次一致、以及 Reviewer 独立读取截图 `auth-session-registered.png`（sha256 `c9d79a38…`）显示 `你好，luowang-01M3ZYK18129P9JM799X1A95DB-session。` 作旁证。Reviewer 明示 `displayName` 的逐字比对属推断路径而非字段级直接读取。

### AUTH-REGISTRATION-001 — passed

- 注册成功并设置会话 Cookie（`sid`）：页面提交路径**未捕获** `POST /api/auth/register` 的直接 HTTP 回执，Reviewer 判定基于计划「证据优先级 2」的组合口径——`operation-28` 快照显示成功欢迎语、`operation-29` 观察到 `sid`、`operation-32` 显示已登录、`operation-39` 本 Run 聚合 `accounts=4` 与 4 次注册计数一致。该缺环由 Reviewer 如实标注。
- `#message` 实际文本为 `你好，<昵称>。` 且昵称为提交昵称：`operation-28` / `page-…34-198Z.yml` 快照显示 `你好，[REDACTED]。`；Reviewer 独立读取截图 `auth-registration-welcome.png`（sha256 `83d585e5…`），画面中 `#message` 完整文本为 `你好，luowang-01M3ZYK18129P9JM799X1A95DB-welcome。`，即中文模板逐字成立、昵称为计划步骤 ② 指定昵称。
- `GET /api/auth/status` 返回 `authenticated=true` 且 `user.displayName` 与提交昵称一致：`operation-31/32/37-037` 显示 `authenticated:true` 与 `…-welcome@example.test`，`displayName` 脱敏；一致性由截图完整昵称 + 同源邮箱支撑（字段级逐字读取受限）。
- 历史 Issue #4（英文欢迎语）方向：截图中 `#message` 为中文模板，与场景既定期望（中文）无冲突。

口径说明：`execution.md` 曾将该期望记为「部分受限／无法在记录中逐字比对昵称」，Reviewer 明确纠正为「已确认」（快照脱敏不等于证据缺失），并指出截图证据实际支持完整逐字比对。上表采用 Reviewer 的确认口径；`execution.md` 该表述属执行记录中的保守写法，本报告如实保留该口径差异。

### DATA-STORAGE-001 — passed

- 聚合观察 `accounts == argon2id` 且 `other == 0`：`operation-39.json` 受控只读存储观察（`source: controlled-test-account-storage`，runId 为本 Run）返回 `accounts=4, argon2id=4, other=0`；计数口径自洽——本 Run 新建账号 4 条（`operation-3` login、页面 session、页面 welcome、`operation-37` storage），观察在删除之前（`operation-39` 先于 `operation-40` 收尾）。
- 持久层仅存 Argon2id 哈希、不出现明文口令：实质判定依据为上述聚合口径（4/4 为 Argon2id、`other=0`，无其他格式项）；`$argon2id$` 字符串级前缀**未被直接观察**。场景前置允许「带部署级 Token 的端点**或等价的只读持久层观察**」，本次使用等价口径，Reviewer 据此不判期望不适用，并将字符串级细节保留为未取得子项，未上升为缺陷、未改写为期望不适用。

需记录的执行偏差（Reviewer 明确不改变其判定）：场景步骤 2 字面点名的部署级 Token 端点 `GET /api/luowang/test-data/01M3ZYK18129P9JM799X1A95DB/storage` 本次实际返回 **401 `{"error":"UNAUTHORIZED"}`**（`operation-38.json`，clientId `storage-obs`，未携带 Token），即场景点名口径本 Run 不可用，判定改由受控只读存储工具完成。该事实在 `execution.md` 已如实记录，来源归属明确。

## 问题与覆盖缺口

### 产品问题

**本 Run 未确认产品缺陷（failed 0 项，`confirmed_bugs` 为空）**。Reviewer 记录 4 条场景的适用期望均未出现与期望相反的实际观察；`operation-14/28` 显示中文欢迎语模板，与历史英文欢迎语问题方向相反的结论由本 Run 记录支持。

### Issue 查询

因无已确认产品 Bug 候选，本 Run 未发起 `query_issue_candidates`。不存在 unavailable 重试或预算耗尽情形，故**无「Issue 查询覆盖缺口」需要列出**；此处的无候选来自审核确认 failed 为 0，而非查询不可用或被伪装成 empty。因此本次不产出任何 create/link 决策，也未创建、关联或修改任何 Issue；场景资产维护需求本次亦未出现。

### 执行记录与环境问题（Reviewer 交付，均不影响其判定）

1. **`execution.md` 遗漏两次失败的工具调用**：`operation-12.json`（`browser_click`，`isError:true`）与 `operation-33.json`（`browser_find`，`isError:true`）未在报告中提及。两者之后均有成功的同义操作（`operation-13` 点击、`operation-34` 查找）且后续状态自洽，Reviewer 归为重试噪声；但执行报告写「偏差：无」时未涵盖该事实，属报告完整性问题，非产品问题。
2. **页面注册无直接 2xx 回执**：`AUTH-SESSION-001` 与 `AUTH-REGISTRATION-001` 的浏览器注册均未产生 `POST /api/auth/register` 的 HTTP 记录，仅由欢迎语 + `sid` + 已登录状态 + 本 Run 账号计数组合支撑；缺环在两场景中均已标注，符合计划证据优先级 2。
3. **`displayName` 逐字读取受限**：两处场景的账号/昵称一致性均为推断路径（可见邮箱 + 页面昵称/截图），而非字段级直接读取。
4. **`$argon2id$` 字符串级观察未取得**：场景点名的 Token 端点返回 401，改用等价聚合口径；字符串级细节保留为未取得子项。
5. **清理未在本 Session 完成**：`operation-39` 时本 Run 4 条 `luowang-01M3ZYK18129P9JM799X1A95DB-` 账号仍存在。按计划与流程，清理属 Harness 在最终 Main 之后的收尾事项，其失败单独记录、不改变本批测试结论；本报告**不预判清理结果，也不声称清理已完成**。上一同类 Run 报告记载其清理未完成，该事实属上一 Run 的背景提示，不预设本 Run 结果。
6. **实现细节来源受限**：计划阶段读取 `app.py` 为 `redacted:true` 全文，故实现细节来源受限；本批期望来源取自场景正文与 `docs/PROJECT.md`、`docs/changes/python-registration/spec.md`（均 full-file、未脱敏），来源归属成立。
7. **历史查询为有限结果**：计划阶段 `query_run_history` 对相关场景与欢迎语关键词返回 `empty`，属有限查询结果，不等于全库无历史。

### 范围限定（不作扩大解释）

- 未选场景（`AUTH-DELETE-001`、`AUTH-REGISTRATION-002`、`CLEANUP-AUTH-001`、`CLEANUP-SCOPE-001`，以及未选的 `AUTH-LOGIN-002`、`AUTH-REGISTRATION-003`、`STORAGE-OBSERVE-001`、`CLEANUP-SEED-001` 与 draft `CLEANUP-CONFIG-001`）本次未执行，本 Run 不改写其结论；其保持原状态。
- 本次 4 条场景 passed **仅代表本批范围内、固定 target 上的执行结果**，不代表整个项目不存在其他问题，也不构成对未选场景或后续提交的通过结论。
- 浏览器能力由 Harness 在实际执行时检查（计划声明 `requiresBrowser=true`）；Reviewer 以证据中存在 Playwright MCP 的导航/快照/填表/点击/Cookie 列表/截图回执（`operation-9`…`operation-34`）确认声明与执行相符。证据与执行归属的对应关系以 Reviewer 交付为准。

## 证据引用

以下为本 Run 证据材料的稳定 URL 与身份（sha256 前缀取自证据清单，与审核清单一致）：

- 页面截图：`auth-registration-welcome.png` — `/api/evidence/bHVvd2FuZy9jeW5vcy13ZWJzaXRlL3J1bi1yZWxpYWJpbGl0eS1maW5hbC0yMDI2MTAwMy9wcm9qZWN0cy82YTQ1ZmQ0Ni0wYjZkLTRhMDktYTgxMS0zMTFkYjJhY2Q3YzcvcnVucy8wMU0zWllLMTgxMjlQOUpNNzk5WDFBOTVEQi9hdXRoLXJlZ2lzdHJhdGlvbi13ZWxjb21lLnBuZw`（sha256 `83d585e5…`）
- 页面截图：`auth-session-registered.png` — `/api/evidence/bHVvd2FuZy9jeW5vcy13ZWJzaXRlL3J1bi1yZWxpYWJpbGl0eS1maW5hbC0yMDI2MTAwMy9wcm9qZWN0cy82YTQ1ZmQ0Ni0wYjZkLTRhMDktYTgxMS0zMTFkYjJhY2Q3YzcvcnVucy8wMU0zWllLMTgxMjlQOUpNNzk5WDFBOTVEQi9hdXRoLXNlc3Npb24tcmVnaXN0ZXJlZC5wbmc`（sha256 `c9d79a38…`）
- 受控 HTTP / 存储观察与浏览器操作回执：`operation-1.json` … `operation-40.json`（同批 Run 证据目录，URL 前缀同上直至 `.../runs/01M3ZYK18129P9JM799X1A95DB/`，如 `operation-39.json` — `/api/evidence/bHVvd2FuZy9jeW5vcy13ZWJzaXRlL3J1bi1yZWxpYWJpbGl0eS1maW5hbC0yMDI2MTAwMy9wcm9qZWN0cy82YTQ1ZmQ0Ni0wYjZkLTRhMDktYTgxMS0zMTFkYjJhY2Q3YzcvcnVucy8wMU0zWllLMTgxMjlQOUpNNzk5WDFBOTVEQi9vcGVyYXRpb24tMzkuanNvbg`）
- 页面快照与浏览器控制台日志：`page-2026-10-03T03-59-15-778Z.yml`、`page-2026-10-03T03-59-19-870Z.yml`、`page-2026-10-03T03-59-22-971Z.yml`、`page-2026-10-03T03-59-25-011Z.yml`、`page-2026-10-03T03-59-25-848Z.yml`、`page-2026-10-03T03-59-30-144Z.yml`、`page-2026-10-03T03-59-34-198Z.yml`、`page-2026-10-03T03-59-37-037Z.yml`；`console-2026-10-03T03-59-15-697Z.log`、`console-2026-10-03T03-59-24-959Z.log`、`console-2026-10-03T03-59-30-103Z.log`（均位于同一 Run 证据目录，文件名可原样对应清单）。

所有时间戳均为 Harness 记录的 UTC 时间（`Z`），来源单一，Reviewer 仅用于说明先后次序；本报告不据此换算绝对事件时间。

## 未完成与后续

1. 测试数据清理由 Harness 在本 Session 结束后统一处理；本 Run 4 条 `luowang-<runId>-` 账号清理结果**尚待核验**，本报告不声称其已完成。
2. `DATA-STORAGE-001` 的 `$argon2id$` 字符串级观察未取得；如后续需要该粒度的证据，须在另行确认的访问条件（部署级 Token 或只读持久层）下补测。
3. `displayName` 字段级逐字读取受限；如需字段级直接证据，须在另行确认的读取口径下补测。
4. `execution.md` 对两次失败工具调用的遗漏与对昵称逐字比对的口径差异，已在本报告保留；其修正属执行/审核记录层面，不影响本批产品结论。
5. 本次未创建或关联任何 Issue；如后续在另行确认的范围内发现已确认产品缺陷，再按受控归档流程处理。

<!-- luowang-screenshot-inspection -->
## 截图采集标签

- [截图 1](</api/evidence/bHVvd2FuZy9jeW5vcy13ZWJzaXRlL3J1bi1yZWxpYWJpbGl0eS1maW5hbC0yMDI2MTAwMy9wcm9qZWN0cy82YTQ1ZmQ0Ni0wYjZkLTRhMDktYTgxMS0zMTFkYjJhY2Q3YzcvcnVucy8wMU0zWllLMTgxMjlQOUpNNzk5WDFBOTVEQi9hdXRoLXJlZ2lzdHJhdGlvbi13ZWxjb21lLnBuZw>)：页面含可见表单值；检测范围为页面，不代表图片整体安全或人工审核通过。
- [截图 2](</api/evidence/bHVvd2FuZy9jeW5vcy13ZWJzaXRlL3J1bi1yZWxpYWJpbGl0eS1maW5hbC0yMDI2MTAwMy9wcm9qZWN0cy82YTQ1ZmQ0Ni0wYjZkLTRhMDktYTgxMS0zMTFkYjJhY2Q3YzcvcnVucy8wMU0zWllLMTgxMjlQOUpNNzk5WDFBOTVEQi9hdXRoLXNlc3Npb24tcmVnaXN0ZXJlZC5wbmc>)：页面含可见表单值；检测范围为页面，不代表图片整体安全或人工审核通过。
<!-- /luowang-screenshot-inspection -->

## Harness 清理收尾

测试数据清理未完成，需要处理；不改变本次功能验证结果。

有 4 项测试数据未通过清理适配器核验

仍有 4 项测试数据未确认清理

待处理：luowang-01M3ZYK18129P9JM799X1A95DB-login（rejected：清理适配器执行或独立查询失败）

待处理：luowang-01M3ZYK18129P9JM799X1A95DB-session（rejected：清理适配器执行或独立查询失败）

待处理：luowang-01M3ZYK18129P9JM799X1A95DB-storage（rejected：清理适配器执行或独立查询失败）

待处理：luowang-01M3ZYK18129P9JM799X1A95DB-welcome（rejected：清理适配器执行或独立查询失败）
