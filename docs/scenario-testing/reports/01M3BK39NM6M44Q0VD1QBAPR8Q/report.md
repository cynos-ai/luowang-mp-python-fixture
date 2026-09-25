---
run_id: 01M3BK39NM6M44Q0VD1QBAPR8Q
trigger: manual
base_commit: null
target_commit: c3600561fb3a0b65bcd1c13a4fb35be049b34539
included_commits: []
result: passed
started_at: 2026-09-25T06:12:33.159Z
finished_at: 2026-09-25T06:14:14.642Z
scenario_results:
  - id: AUTH-REGISTRATION-001
    result: passed
confirmed_bugs: []
---

# 测试报告：注册成功欢迎语修复复测（AUTH-REGISTRATION-001）

## 一、本次范围与目标

- 请求（trigger=manual）：针对刚合入的注册成功欢迎语修复，复测 `AUTH-REGISTRATION-001`，按固定提交的实际代码与场景证据判断；重点核对页面完整中文文本、注册响应、会话、截图与 Run 范围清理；其他场景沿用历史 blocked 记录，本次不以复测改判。
- target：`c3600561fb3a0b65bcd1c13a4fb35be049b34539`；base：`null`；includedCommits：空。
- 计划 `## execution_scenarios` 唯一列表项为 `AUTH-REGISTRATION-001`（approved，core），本 Run 共 1 个执行场景，`scenarioMode: review-all` 下收窄为"仅针对受影响场景复测"（修复且契约不变）。
- 场景维护：计划声明无新增/修改/废弃场景；`scenarioChanges` 为 null，本 Run 无 scenario patch 工件。本次不修改场景资产。

## 二、逐场景结果

| 场景 ID | 结果 | 依据 |
|---|---|---|
| AUTH-REGISTRATION-001 | passed | Reviewer 独立审核，依据本 Run 冻结场景正文及原始证据 |

### AUTH-REGISTRATION-001 · 注册成功后页面显示中文欢迎语并保持登录（passed）

Reviewer 结论：三条期望均有本 Run 原始证据支持，判定 **passed**。逐条摘要如下（均出自 review.md；证据编号沿用审核交付的引用）：

1. 注册请求成功并设置会话 Cookie：`POST /api/auth/register` 返回 `201 CREATED`；同浏览器上下文存在 `sid` cookie；重导航后 `/api/auth/status` 返回 `authenticated:true`，说明会话 Cookie 被服务端接受（operation-7、operation-10、operation-11、operation-12/13）。
2. 页面 `#message` 显示 `你好，<昵称>。`：Reviewer 实际读取截图，状态区完整文本为 `你好，luowang-<runId>-welcome。`（中文文案，未复现英文 `Welcome, ...`）；对应快照 `status [ref=e12]: 你好，[REDACTED]。`（operation-9 截图、operation-8 快照）。
3. `/api/auth/status` 的 `authenticated` 为 true 且 `user.displayName` 与提交昵称一致：响应中 `authenticated:true` 与 `user.email`（与提交邮箱一致）已确认；`displayName` 在该快照中被 Harness 脱敏（operation-12/13）。

步骤落位：冻结正文 4 个步骤均有对应操作（打开 `GET /` 且表单可见 → 填表提交 → 读取 `#message` → 读取 `/api/auth/status`）；"需要记录"各项均有对应工件。

## 三、证据情况与来源归属

- 本 Run 证据文件（动态上下文提供）：1 张页面截图（`auth-registration-001-message.png`，screenshotInspection 状态 detected、scope=page）、16 份 operation 记录、3 份页面快照、1 份 console 日志。
- 执行归属：Reviewer 核对 operation 序列与场景归属一致——operation-1 `begin_scenario_execution` → operation-2 `start_scenario("AUTH-REGISTRATION-001")` → operation-3..15 均标注该 scenarioId、`declared:true` → operation-16 `finish_scenario`，`completed:["AUTH-REGISTRATION-001"]`；navigate / fill_form / click / network_requests / cookie_list / snapshot / screenshot / close 均为本次 Run 的 Playwright MCP 工具回执，截图与两次页面快照由 navigate/click 触发并带 sha256，属实际执行。
- 来源区分：场景执行观察与判定来自 Reviewer（review.md）；计划中关于 `app.py` 实现事实、`docs/changes/python-registration/spec.md` 第 1 条、历史 Run 与 Issue #4 的陈述属 Main（计划）的阅读与陈述；Reviewer 无源码与历史列表读取权限，未独立复核这些来源，且其判定不以上述实现/历史陈述为前提。
- 限制：命令证据中填表参数值被 `[REDACTED]` 遮蔽；截图内口令输入框为圆点掩码。本 Run 未做系统性 Secret 扫描，故不对"记录中不存在任何口令文本"作绝对声明。

## 四、未确认事项与限制（保留 Reviewer 的疑问与限定）

1. **期望 3 的记录脱敏残留**：`/api/auth/status` 响应中的 `displayName` 逐字值被 Harness 脱敏，Reviewer 未逐字读到该字段。Reviewer 认为产品结果仍有充分支持（`authenticated:true` 与 `user.email` 逐字一致，且同一 Run 页面状态区由该用户 `displayName` 渲染并显示昵称与提交昵称一致），故未降级为 blocked；该残留属记录脱敏限制（计划「覆盖缺口与限制」第 4 条已预先声明），非产品缺陷。审核同时指出：如需 100% 逐字核验 status 的 `displayName`，需在可读原文条件下由授权角色复核。此未闭合点如实保留，本报告不将其改写为"已确认"。
2. **Runner 与 Reviewer 的观察差异**：Runner 报告称"截图仅记录文件存在与捕获时序、未做图片内容审查"，其对期望 2 的判定依据为被脱敏的 accessibility 快照；Reviewer 实际读图后确认截图中状态区为完整未脱敏中文文案，从而对期望 2 提供了强于 Runner 记录的独立观察。该判定归 Reviewer，不改写为 Runner 交付。
3. **其他 12 个场景**：本 Run 不执行，沿用历史记录，其适用期望在本 Run 仍为未验证；审核与本次复测均不作改判（含 `AUTH-REGISTRATION-002/003`、`AUTH-LOGIN-001/002`、`AUTH-DELETE-001/002`、`STORAGE-OBSERVE-001`、`CLEANUP-AUTH-001`、`CLEANUP-SCOPE-001`、`CLEANUP-SEED-001`；`AUTH-SESSION-001`、`DATA-STORAGE-001` 历史 passed 不重跑）。`CLEANUP-CONFIG-001` 为 draft，未进入执行清单。
4. **能力缺口未声明解决**：前序报告记录的能力缺口（无法发出 `POST /api/auth/login`、无法携带自定义 `Authorization` 头、无法直接调用接口绕过页面原生校验）本次未声明已解决；本场景不依赖这些能力，故不影响本场景结论。
5. **无 base 提交**：`list_target_changes` 返回 `no_baseline`，无法提供逐文件变化清单，本次判断依据为冻结场景正文与本 Run 证据，不能据 diff 缩小范围。
6. **注册响应头口径**：注册响应头回执未显示 `Set-Cookie` 行，会话 Cookie"已设置"的依据是 cookie 列表与后续 `authenticated:true`，而非该响应头。此属证据口径说明，不影响期望 1 判定。
7. **次要观察（不影响判定）**：邮箱输入框内容为小写 runId 前缀地址，昵称与状态区为原始大小写 runId，两者均以 `luowang-` + 本 Run 标记 + `-welcome` 构造，满足合成数据要求；控制台含一条 `favicon.ico` 404，与本场景期望无关。
8. **数据收尾**：Run 内已登记 1 个账号（账户库存计数 1，登记不代表已清理）。测试数据清理由 Harness 在本 Session 结束后按 Run 范围统一处理，本报告不声称清理已完成，清理失败将单独记录且不改功能结论。

## 五、产品缺陷与 Issue 决策

- 本次审核未发现需登记的产品缺陷；修复点（英文 `Welcome, ...` → 中文 `你好，<昵称>。`）已由页面实际渲染确认生效，英文文案未复现。因此本次无 confirmed Bug，无 Issue create/link 决策，亦无需要执行的候选查询。
- 说明：本 Run 未发现新 Bug 不代表项目范围整体无问题，仅为本次选定场景范围内的结论；其他场景沿用历史记录，未在本次验证。

## 六、总体结论

- `result: passed`。本 Run 唯一执行场景 `AUTH-REGISTRATION-001` 通过（`blocked > failed > passed` 聚合后无 failed/blocked 项），无 confirmed Bug，无 Issue 操作。
- 已确认：中文欢迎语文案在页面实际渲染中生效；注册响应 201、会话 Cookie 与会话状态与场景期望一致。
- 保留未闭合点：`/api/auth/status` 的 `displayName` 逐字值因记录脱敏未被 Reviewer 逐字读到（计划已预先声明的记录限制）；其余 12 个场景本 Run 未执行，沿用历史记录。
- 当前授权范围内的下一步（如需闭合上述残留）：由具备原文可读条件的授权角色复核 status 的 `displayName` 逐字值；其他场景的复测需另行规划与授权，本 Run 不据此改判。

<!-- luowang-screenshot-inspection -->
## 截图采集标签

- [截图 1](</api/evidence/bHVvd2FuZy9jeW5vcy13ZWJzaXRlL211bHRpLXByb2plY3QtdjA2MS1saXZlLTRkNDIwODQwL3Byb2plY3RzL2RhZjdlNDJkLTIwZDctNDUzYS1hMjZkLWQyYmFiMWMxZjQ3OC9ydW5zLzAxTTNCSzM5Tk02TTQ0UTBWRDFRQkFQUjhRL2F1dGgtcmVnaXN0cmF0aW9uLTAwMS1tZXNzYWdlLnBuZw>)：页面含可见表单值；检测范围为页面，不代表图片整体安全或人工审核通过。
<!-- /luowang-screenshot-inspection -->

## Harness 清理收尾

测试数据清理完成；不改变本次功能验证结果。

清理适配器已独立核验 1 项测试数据不存在

全部登记测试数据均已独立核验清理

独立核验：luowang-01M3BK39NM6M44Q0VD1QBAPR8Q-welcome · run-scoped-http-cleanup · 2026-09-25T06:14:29.304Z · absent=true · sha256 6ab7457cf4dc5a94efdee4d27bf74cfa8087e5e3dfc548d4d9f5675d398ba977
