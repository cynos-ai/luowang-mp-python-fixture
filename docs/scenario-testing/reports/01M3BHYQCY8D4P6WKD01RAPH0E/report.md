---
run_id: 01M3BHYQCY8D4P6WKD01RAPH0E
trigger: manual
base_commit: null
target_commit: 499b00378dec10c2d32dfec2354b144a1731b757
included_commits: []
result: blocked
started_at: 2026-09-25T05:52:34.951Z
finished_at: 2026-09-25T06:00:58.947Z
scenario_results:
  - id: AUTH-REGISTRATION-001
    result: failed
  - id: AUTH-REGISTRATION-002
    result: blocked
  - id: AUTH-REGISTRATION-003
    result: blocked
  - id: AUTH-LOGIN-001
    result: blocked
  - id: AUTH-LOGIN-002
    result: blocked
  - id: AUTH-SESSION-001
    result: passed
  - id: AUTH-DELETE-001
    result: blocked
  - id: AUTH-DELETE-002
    result: blocked
  - id: DATA-STORAGE-001
    result: passed
  - id: STORAGE-OBSERVE-001
    result: blocked
  - id: CLEANUP-AUTH-001
    result: blocked
  - id: CLEANUP-SCOPE-001
    result: blocked
  - id: CLEANUP-SEED-001
    result: blocked
confirmed_bugs:
  - key: AUTH-REGISTRATION-001-WELCOME-LANGUAGE
    title: 注册成功后页面状态区显示英文欢迎语「Welcome, <昵称>.」，不符合契约规定的中文「你好，<昵称>。」
    scenario_ids:
      - AUTH-REGISTRATION-001
    issue_action: create
---

# 最终报告：Python 账号场景（目标 499b0037）

本报告汇总计划 `plan.md`（planHash `8739f3e84d8639369dfb9bfc8160b3f72cea934d24423053d44d8fd39ad663d0`）与独立审核 `review.md` 的逐场景结果、依据、限制与缺口，不重做执行或审核。无初始化修补（`scenario-changes.patch` 不存在，且当前角色无权读取），无场景变更需回归。

- 目标提交：`499b00378dec10c2d32dfec2354b144a1731b757`
- 基线：无（`base_commit: null`，计划记录 `list_target_changes` 返回 `no_baseline`）
- 模式：`review-all`，对目标现存 approved 场景全集做一次完整执行
- 请求：执行固定 scenario-testing 的 Python 账号场景，重点核对注册后中文欢迎语、登录与删号、Argon2id 存储观察及 Run 范围清理；只依据真实证据判定
- 动态 Run 时间：`started_at` / `finished_at` 逐字取自本次 Run 上下文（Harness 记录时间）。页面与工具事件时间同属 Harness 记录，未被用作精确时刻断言

## 结果分布

| 结果 | 场景数 |
|---|---|
| passed | 2（AUTH-SESSION-001、DATA-STORAGE-001） |
| failed | 1（AUTH-REGISTRATION-001） |
| blocked | 10 |

合计 13，与 `## execution_scenarios` 的 13 项一一对应且顺序一致，无重复计入或遗漏。

聚合结果按 `blocked > failed > passed` 规则为 **blocked**。本次 `blockingReasons` 为空，但存在 10 个场景的适用期望未验证（源于验证能力不足），报告整体结论为 blocked，且已确认的产品失败（AUTH-REGISTRATION-001）同时保留。测试数据收尾由 Harness 在本 Session 结束后统一处理，本报告不提前声称已完成。

## 逐场景结果与依据

以下依据与判定来自审核 `review.md` 第 2 节的独立读证，未回读原始证据重做审核。

### passed（2）

- **AUTH-SESSION-001（passed）**：匿名 `GET /api/auth/status` 返回 `{"authenticated":false}`（快照 `page-2026-09-25T05-56-10-827Z.yml`），同刻 `cookie_list` 无 `sid`（`operation-108`）；注册后 `operation-115` 记录 `sid`，快照 `page-2026-09-25T05-56-18-502Z.yml` 为 authenticated true 且 email 为该场景账号；刷新后快照 `page-2026-09-25T05-56-21-729Z.yml` 与截图 `auth-session-001-reload.png` 显示用户信息不变。三条期望均有实际观察支持。
- **DATA-STORAGE-001（passed，附覆盖限制）**：受控只读存储观察 `operation-56`（accounts 3）与 `operation-133/136/150`（accounts 5、argon2id 5、other 0），`accounts == argon2id` 且 `other == 0`，与场景期望第 1 条逐字对应；第 2 条以“non-Argon2id 计入 `other`、`other=0`”的三桶口径支持。限制（审核交付）：观察为计数值，未读到哈希字符串前缀，也未直接排除明文，该口径依赖契约对 `other` 的定义。

### failed（1）

- **AUTH-REGISTRATION-001（failed）**：见“已确认产品问题 P1”。注册侧 201 与 `sid` 建立、`GET /api/auth/status` authenticated（快照 `page-2026-09-25T05-54-12-686Z.yml`）成立，但状态区欢迎语文案不符第 2 条期望。

### blocked（10）

以下场景均存在适用期望尚未确认（验证能力不足，非“不适用”）；未确认项不被改判为 passed，也不从范围移除。

- **AUTH-REGISTRATION-002（blocked）**：已确认部分——同邮箱二次注册返回 409（`operation-44` 网络列表 `[409] CONFLICT`、`operation-55` 快照状态区 `ACCOUNT_EXISTS`、截图 `auth-registration-002-dup-rejected.png`），会话仍指向原账号（快照 `page-2026-09-25T05-54-36-634Z.yml`）。未确认——“原账号仍可用原凭据登录、昵称为首次值”因从未发出 `POST /api/auth/login` 而未验证。
- **AUTH-REGISTRATION-003（blocked）**：仅走页面表单路径，点击「注册」后网络列表为空（`operation-72`），状态区无文本（`operation-73`），浏览器原生校验在客户端拦下，服务端从未收到三类非法请求；场景正文明确“需直接调用接口”，该能力缺失，三条期望全部未验证。
- **AUTH-LOGIN-001（blocked）**：唯一相关动作是对 `/api/auth/login` 的 GET，`operation-76` 快照 `Method Not Allowed`、控制台 `console-2026-09-25T05-56-07-276Z.log` 记 405；无任何 2xx 登录与 `sid` 建立观察。
- **AUTH-LOGIN-002（blocked）**：场景窗口内无归属操作记录，错误口令/未知邮箱请求与其后正确凭据登录均无证据。
- **AUTH-DELETE-001（blocked）**：已确认部分——删除后状态区 `账号已删除。`（快照 `page-2026-09-25T05-56-34-953Z.yml`）、`sid` 被清除（`operation-130`）、随后 `GET /api/auth/status` 为 false（`operation-134`）、重复删除返回 401 且页面显示 `删除失败。`（`operation-138`、`page-2026-09-25T05-56-42-936Z.yml`、控制台 `console-2026-09-25T05-56-39-937Z.log`）。未确认——步骤 4“原邮箱+原口令登录被拒”无任何请求记录。审核备注：首次 DELETE 的 2xx 状态行未被保留，删除成功系由文案、Cookie 清除与账号计数间接支持。
- **AUTH-DELETE-002（blocked）**：已确认部分——对照账号注册并登录（快照 `page-2026-09-25T05-56-52-265Z.yml` authenticated true），未鉴权客户端（`operation-149`，restore-input 覆盖 `sid`）`GET /api/auth/status` 为 false（快照 `page-2026-09-25T05-56-56-376Z.yml`），匿名 `DELETE /api/me` 返回 401（`operation-157`、控制台 `console-2026-09-25T05-57-00-297Z.log`）。未确认——“对照账号原凭据仍能登录”无 `POST /api/auth/login` 记录；“账号未被删除”仅有本 Run 计数 5（`operation-150`）的间接支持（审核将其保留为间接支持，未写成直接观察）。
- **STORAGE-OBSERVE-001（blocked）**：仅有未带 Token 的请求（控制台 `console-2026-09-25T05-57-20-965Z.log`、`console-2026-09-25T05-57-23-229Z.log` 均为 401，侦察期另有同端点 401 与 `not-a-valid-run-id` 401），属鉴权先于 Run ID 校验，不能证明“带有效 Token 的非法 Run ID 被拒”；响应体字段清单、响应头与带 Token 的成功响应均未观察。
- **CLEANUP-AUTH-001（blocked）**：仅步骤 1 部分成立——无 Token 的 `GET .../<runId>` 与 `.../storage` 均 401、响应体仅 `{"error":"UNAUTHORIZED"}`（快照 `page-2026-09-25T05-57-20-993Z.yml`、`page-2026-09-25T05-57-23-254Z.yml`）。错误 Token 的 GET/GET/DELETE 与“该账号仍未被删且原凭据仍可登录”均未执行。
- **CLEANUP-SCOPE-001（blocked）**：场景窗口内无归属操作，清理前余量、`DELETE` 删除数、独立余量、非法 Run ID 与凭据失效观察全部缺失。
- **CLEANUP-SEED-001（blocked）**：场景窗口内无归属操作，另一合法 Run ID 余量对照、本 Run 清理执行、预置账号登录均无证据。

## 已确认产品问题

### P1：注册成功后页面状态区显示英文欢迎语（契约违反）

- 期望来源：冻结场景 AUTH-REGISTRATION-001 `## 期望` 第 2 条，页面 `#message` 文本应为 `你好，<昵称>。`
- 实际观察（审核独立读证）：
  - 快照 `page-2026-09-25T05-54-08-271Z.yml`、`page-2026-09-25T05-54-22-866Z.yml` 状态区文本为 `Welcome, [REDACTED].`（英文前缀 `Welcome,` 未脱敏，可读）。
  - 截图 `auth-registration-001-welcome-message.png`（审核人自行打开）页面正文显示 `Welcome, luowang-01M3BHYQCY8D4P6WKD01RAPH0E-welcome2.`；页面上同时存在中文标题「Python 账号实验站」与中文按钮「注册」「删除账号」。
  - 对照：删除路径同一状态区为中文（快照 `page-2026-09-25T05-56-34-953Z.yml` = `账号已删除。`；`page-2026-09-25T05-57-03-602Z.yml` = `删除失败。`）。
- 复现条件：浏览器打开 `GET /`，用页面表单提交合法昵称/邮箱/≥12 字符口令注册成功，随后读取状态区文本，得到英文 `Welcome, <displayName>.`；同会话 `POST /api/auth/register` 返回 201 并设置 `sid`（`operation-33/34/35`），失败点只在页面文案。
- 归属：期望来自冻结场景正文（非审核补充）。Runner 已记录同一事实并判 failed；审核基于自读快照与截图独立复现该事实，判定一致。
- 影响场景：AUTH-REGISTRATION-001 = failed。
- 关联限制（审核交付）：快照脱敏使 `displayName` 无法逐字比对，“显示昵称 == 提交昵称”仅能由“显示值以提交昵称结尾 + 注册响应邮箱一致”间接支持；主要失败点（语言）不受此影响。

## Issue 去重决策

- 已确认产品 Bug 候选 1 项：`AUTH-REGISTRATION-001-WELCOME-LANGUAGE`。
- 受限候选查询按 title、keywords 及 bug_key 多次执行，均返回 `empty`（无候选）。即“查无匹配”，因此选择 `issue_action: create`。
- 该决策是交给后续受控归档 owner 的动作，本报告不代表 Issue 已创建或关联；`create` 仍可能在后续归档产生新 Issue，不声称跨 Run 无重复保证。
- 场景资产维护需求不冒充产品 Bug；本批无需新增或修改场景。

## 覆盖缺口与限制

1. 无 base 提交：不能提供“本次变化清单”，无法用 diff 缩小范围，已按 `review-all` 全量处理。
2. 验证能力不足（非“不适用”）导致 10 项 blocked 的适用期望保持未验证：
   - 无法发出 `POST /api/auth/login`（页面无登录表单；受控命令禁用 curl/wget/内联解释器代码/任意脚本；对 `/api/auth/login` 的 GET 返回 405；以 `data:text/html` 页面内 `fetch` 的尝试被 CORS 拦下，控制台 `console-2026-09-25T05-55-36-678Z.log` 记 `blocked by CORS policy … origin 'null'`）。
   - 无法发出带自定义 `Authorization` 头的请求（清理/存储端点始终 401，未见任何携带部署级 Token 的请求记录），因此带 Token 的字段与响应头检查、错误 Token 检查、清理范围与余量核验均无法完成。
3. AUTH-REGISTRATION-003 的服务端校验路径完全未触及，仅客户端原生校验。
4. `CLEANUP-CONFIG-001`（draft）未纳入执行清单，契约第 4 条“清理接口默认关闭 / 短 Token 拒绝启动”在本批无任何运行覆盖；计划已说明原因（需以自定义环境变量启动多个实例，是否可构造待确认），属已知缺口而非审核遗漏。
5. 合法 Run ID 清理、“其他 Run 余量不变”“预置账号免于清理”均无观察；本 Run 结束时存储计数仍为 5（`operation-150`），即本 Run 的清理尚未执行。按流程该清理是 Harness 在最终 Main 之后的收尾事项，不构成场景阻塞，但 CLEANUP-SCOPE-001 / CLEANUP-SEED-001 自身的期望仍为未验证。
6. 口令与账号相关字段：审核读到的证据中，表单值与请求体口令均以 `[REDACTED]` 呈现，未见复述；审核明确其**未执行**系统性 Secret 扫描，故不构成“记录中不存在任何口令文本”的结论。本报告亦不复述任何账号、口令或 Token 值。
7. 时间口径：页面/工具事件时间为 Harness 记录时间，服务器响应头 `date` 为被测服务器时间，二者无共同校准基准；本次仅使用先后顺序与 Harness 记录时间，未据此断言精确时刻。

## 执行记录异常（与产品结论分开）

审核在 `review.md` 第 6 节交付以下记录层面异常，保留如下：

- **进度事件标签错位**：`finish_scenario` 事件的 `scenarioId` 指向下一个场景，而 `completed` 数组列的是刚完成的场景（如序 44）。因此不能按 `scenarioId` 字段判断操作归属；审核按 `completed` 语义与操作自身 `execution.scenarioId` 核对。最后一次事件（序 175）把 13 项全列为 completed，但按第 2 节，CLEANUP-SCOPE-001 / CLEANUP-SEED-001 窗口内无任何操作记录——**“最后 completed=13/13”不代表 13 项均已实际执行**。
- 场景之间无“先完成再补执行”的跨场景操作错配；存在大量与场景无关的侦察操作，其中 `data:text/html` 探测导致浏览器会话 Cookie 被清空的副作用已由 Runner 主动披露（`execution.md` 第 5 节），与证据相符。
- **报告口径问题（不影响产品结论，影响追溯）**：`execution.md` 第 1 节“可用受控能力/能力缺口”一条存在截断与错位（在 `无法发出带自定义 Authorization` 处中断，插入本应属“偏差”段的“标准偏差：…”整句）；该处表述不完整，后续角色可能无法完整复原能力边界，实质结论与审核观察一致，仅文本残缺。此为审核在证据中发现、Runner 未在报告中提及。

## 与审核的一致性说明

- 本报告逐场景结果、分布与审核第 2 节及第 8 节结论一致（passed 2 / failed 1 / blocked 10）。CLEANUP-SCOPE-001 / CLEANUP-SEED-001 的窗口内无归属操作记录，与上节异常说明一致。
- 审核内部矛盾核对：审核第 2 节对 AUTH-REGISTRATION-001 判 failed 并给出完整依据，第 8 节结论亦为 failed，未发现需按聚合规则另行处理的冲突；数据存储观察与实际执行、时间归因按审核交付保留。
- 已确认产品失败在聚合为 blocked 的同时保留；未确认项不表述为“产品行为失败”，也不改写为 passed。

## 下一步建议（当前授权范围内）

- 为依赖 `POST /api/auth/login` 与携带 `Authorization` 头的场景补齐验证能力（受控 HTTP 客户端或等价能力），以闭合 10 项 blocked 的适用期望。
- AUTH-REGISTRATION-003 需具备直接调用接口、绕过页面原生校验的能力。
- `CLEANUP-CONFIG-001`（draft）如需覆盖 spec 第 4 条，需具备以自定义环境变量启动多个应用实例的能力；该前置是否可构造须经确认。
- 上述能力或环境变更超出当前范围，须另行确认授权，不能视为现有权限。

<!-- luowang-screenshot-inspection -->
## 截图采集标签

- [截图 1](</api/evidence/bHVvd2FuZy9jeW5vcy13ZWJzaXRlL211bHRpLXByb2plY3QtdjA2MS1saXZlLTRkNDIwODQwL3Byb2plY3RzL2RhZjdlNDJkLTIwZDctNDUzYS1hMjZkLWQyYmFiMWMxZjQ3OC9ydW5zLzAxTTNCSFlRQ1k4RDRQNldLRDAxUkFQSDBFL2F1dGgtcmVnaXN0cmF0aW9uLTAwMS13ZWxjb21lLW1lc3NhZ2UucG5n>)：页面含可见表单值；检测范围为页面，不代表图片整体安全或人工审核通过。
- [截图 2](</api/evidence/bHVvd2FuZy9jeW5vcy13ZWJzaXRlL211bHRpLXByb2plY3QtdjA2MS1saXZlLTRkNDIwODQwL3Byb2plY3RzL2RhZjdlNDJkLTIwZDctNDUzYS1hMjZkLWQyYmFiMWMxZjQ3OC9ydW5zLzAxTTNCSFlRQ1k4RDRQNldLRDAxUkFQSDBFL2F1dGgtcmVnaXN0cmF0aW9uLTAwMi1kdXAtcmVqZWN0ZWQucG5n>)：页面含可见表单值；检测范围为页面，不代表图片整体安全或人工审核通过。
- [截图 3](</api/evidence/bHVvd2FuZy9jeW5vcy13ZWJzaXRlL211bHRpLXByb2plY3QtdjA2MS1saXZlLTRkNDIwODQwL3Byb2plY3RzL2RhZjdlNDJkLTIwZDctNDUzYS1hMjZkLWQyYmFiMWMxZjQ3OC9ydW5zLzAxTTNCSFlRQ1k4RDRQNldLRDAxUkFQSDBFL2F1dGgtc2Vzc2lvbi0wMDEtcmVsb2FkLnBuZw>)：字段检测未完成；检测范围为页面，不代表图片整体安全或人工审核通过。
<!-- /luowang-screenshot-inspection -->

## Harness 清理收尾

测试数据清理完成；不改变本次功能验证结果。

清理适配器已独立核验 5 项测试数据不存在

全部登记测试数据均已独立核验清理

独立核验：luowang-01M3BHYQCY8D4P6WKD01RAPH0E-welcome · run-scoped-http-cleanup · 2026-09-25T06:01:27.778Z · absent=true · sha256 4f45cded329fa8a9a15ff65ffe82a97a1d35e24c74a7c93cb4a35ff6fd6e830e

独立核验：luowang-01M3BHYQCY8D4P6WKD01RAPH0E-welcome2 · run-scoped-http-cleanup · 2026-09-25T06:01:27.782Z · absent=true · sha256 4f45cded329fa8a9a15ff65ffe82a97a1d35e24c74a7c93cb4a35ff6fd6e830e

独立核验：luowang-01M3BHYQCY8D4P6WKD01RAPH0E-session · run-scoped-http-cleanup · 2026-09-25T06:01:27.786Z · absent=true · sha256 4f45cded329fa8a9a15ff65ffe82a97a1d35e24c74a7c93cb4a35ff6fd6e830e

独立核验：luowang-01M3BHYQCY8D4P6WKD01RAPH0E-delete2 · run-scoped-http-cleanup · 2026-09-25T06:01:27.789Z · absent=true · sha256 4f45cded329fa8a9a15ff65ffe82a97a1d35e24c74a7c93cb4a35ff6fd6e830e

独立核验：luowang-01M3BHYQCY8D4P6WKD01RAPH0E-dup · run-scoped-http-cleanup · 2026-09-25T06:01:27.792Z · absent=true · sha256 4f45cded329fa8a9a15ff65ffe82a97a1d35e24c74a7c93cb4a35ff6fd6e830e
