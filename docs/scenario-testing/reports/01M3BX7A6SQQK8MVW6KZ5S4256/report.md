---
run_id: 01M3BX7A6SQQK8MVW6KZ5S4256
trigger: manual
base_commit: c3600561fb3a0b65bcd1c13a4fb35be049b34539
target_commit: abf6c24b388bd662ea25b05614871a8c4fbdd5d1
included_commits: []
result: blocked
started_at: "2026-09-25T09:09:31.388Z"
finished_at: "2026-09-25T09:15:31.800Z"
scenario_results:
  - id: AUTH-REGISTRATION-001
    result: passed
  - id: AUTH-REGISTRATION-002
    result: passed
  - id: AUTH-REGISTRATION-003
    result: passed
  - id: AUTH-SESSION-001
    result: passed
  - id: AUTH-LOGIN-001
    result: passed
  - id: AUTH-LOGIN-002
    result: passed
  - id: AUTH-DELETE-001
    result: passed
  - id: AUTH-DELETE-002
    result: passed
  - id: DATA-STORAGE-001
    result: passed
  - id: STORAGE-OBSERVE-001
    result: passed
  - id: CLEANUP-AUTH-001
    result: passed
  - id: CLEANUP-SCOPE-001
    result: passed
  - id: CLEANUP-SEED-001
    result: blocked
confirmed_bugs: []
---

# 最终报告 · Run `01M3BX7A6SQQK8MVW6KZ5S4256`

- 请求（trigger=manual）：对上次全场景 Run `01M3BHYQCY8D4P6WKD01RAPH0E` 因 HTTP 能力不足而 blocked 的 10 个 approved 场景做完整复核，并按需补充注册/会话/存储场景。本轮 Runner 新增 `request_test_http`（隔离 Cookie 客户端、受控口令占位符）与 `probe_run_cleanup`（只限当前 Run 的清理/存储端点）。
- 固定范围：base `c3600561fb3a0b65bcd1c13a4fb35be049b34539`，target `abf6c24b388bd662ea25b05614871a8c4fbdd5d1`，includedCommits 为空。
- 场景模式 `review-all`；`scenarioChanges: null`，本次无 scenario patch，未新增/修改/废弃场景资产。
- 结果口径：计划清单 13 项，全部执行；**12 passed，1 blocked（`CLEANUP-SEED-001`），0 failed**。按 `blocked > failed > passed` 聚合，整体结果为 **blocked**（存在未闭合的适用期望）。
- 来源：本节范围与固定版本沿用 plan.md；逐场景结果、覆盖说明与缺口取自 review.md 的独立审核，未回读运行记录重做审核。

## 范围与环境

- base→target 仅追加了上一次复测的 `report.md` 与 `review.md` 两份文档（plan.md 的 `list_target_changes` 结论），**产品代码与场景资产均无变化**。故本批属于“执行能力变化后的重新验证”，不是代码变更回归，不能据此推断其他提交的行为。
- 执行集来自 plan.md 唯一的 `## execution_scenarios`，13 项 approved 场景（含上次 blocked 的复核项与注册/会话/存储补充项），顺序即执行顺序，均由 review 核对为实际 start 且顺序一致。
- draft 场景 `CLEANUP-CONFIG-001` 未进入执行集（需多实例启动、本批受控能力不提供），plan 的理由被 review 认可为成立。
- 合成数据使用 Run 前缀 `luowang-<runId>-<用途>` 并登记；口令/Token/哈希全文按脱敏规则不复述。

## 逐场景结果（按执行清单顺序）

| 场景 | 结果 | 依据要点（review 独立核对） |
| --- | --- | --- |
| AUTH-REGISTRATION-001 | passed | 浏览器 `POST /api/auth/register => 201`，`sid` Cookie 观察到，`#message` 由截图确认与提交昵称一致；`/api/auth/status` authenticated=true |
| AUTH-REGISTRATION-002 | passed | 重复邮箱注册 `409 ACCOUNT_EXISTS` 且无 Set-Cookie；失败客户端 status=false；原凭据登录 201 且昵称为首值 |
| AUTH-REGISTRATION-003 | passed | 非法邮箱/空昵称 `400 INVALID_ACCOUNT`、短口令 `400 WEAK_PASSWORD`；均无 Cookie、status=false、凭据登录 401 |
| AUTH-SESSION-001 | passed | 匿名 status=false；注册后 true；浏览器重载 `GET /` 后仍 true 且邮箱一致 |
| AUTH-LOGIN-001 | passed | 隔离客户端登录 201 设新 `sid`，status 的 email/displayName 与登录账号一致 |
| AUTH-LOGIN-002 | passed | 未注册邮箱与错误口令均 `401 INVALID_CREDENTIALS`、无 Cookie、status=false；正确凭据随后 201 |
| AUTH-DELETE-001 | passed | 页面删除 `DELETE /api/me => 200`，`#message=账号已删除。`；删除后 status=false、原凭据重登 401、重复删除 401 |
| AUTH-DELETE-002 | passed | 无 Cookie 独立客户端 `DELETE /api/me => 401`；对照账号未受影响，原凭据仍 201 |
| DATA-STORAGE-001 | passed | 存储观察 `{accounts:6, argon2id:6, other:0}`，只读探针复核一致 |
| STORAGE-OBSERVE-001 | passed | 有效 Token `GET .../storage => 200`，体仅 runId/计数，头 `Cache-Control: no-store`；非法 Run ID `400 INVALID_RUN_ID` 不返回计数 |
| CLEANUP-AUTH-001 | passed | 无 Token 与错误 Token 的各端点（含 DELETE）均 401，拒绝体仅 error；随后原凭据登录 201、余量未减少 |
| CLEANUP-SCOPE-001 | passed | 前置 remaining=6 → `DELETE => {deleted:6, remaining:0}` → 独立 GET 0；非法 Run ID 400 无删除；被清理账号凭据 401、原会话 status=false |
| CLEANUP-SEED-001 | blocked | 预置账号清理后仍登录 201（该期望已确认满足）；**跨其他 Run 余量前后一致**因工具只支持当前 Run / 固定非法 ID 而不可观察，期望未闭合 |

计数与口径：13 项场景互斥计数为 12 passed / 1 blocked / 0 failed，与冻结执行集一致；review 明确说明未发现产品不符合期望的项。

## 未闭合项与阻塞

- **`CLEANUP-SEED-001` — blocked**。review 已确认其中期望“预置账号在本 Run 清理后仍能登录”满足（创建 `-seed1` → `DELETE {deleted:1, remaining:0}` → 预置账号登录 201，时序在清理之后），但期望“另一合法 Run ID 的余量清理前后一致”**未验证**：受控工具 `probe_run_cleanup` 只支持当前 Run 与固定非法 ID 两种 `runIdKind`，步骤 1/4 不可观察。因存在适用期望未闭合，本场景保持 blocked；已确认的成功部分如实保留，未降低期望、未改写旧结论。
- 归因性质：该阻塞源于受控工具的跨 Run 观察能力边界，**不是产品缺陷**；本次整体 blocked 即由此项产生。

## 覆盖缺口与限制（承接 review，逐条保留）

1. `CLEANUP-SEED-001` 期望 2（跨其他 Run 余量前后一致）不可观察 → 本批唯一阻塞项；需具备跨 Run 只读余量观察能力的后续流程方可闭合，本轮不构造补测。
2. `CLEANUP-CONFIG-001`（draft）不在执行集，spec 第 4 条“清理接口默认关闭 / 短 Token 拒绝启用”本批**无运行覆盖**，属已知缺口而非豁免。
3. `DATA-STORAGE-001` 的哈希前缀/无明文结论仅由三桶计数（`other=0`）支持，**未直接读持久层 `password_hash` 原文**，为观察口径限制，不改变其通过判定。
4. `AUTH-REGISTRATION-002` 期望 3、`AUTH-DELETE-001`“会话 Cookie 被清除”为**间接支持**（前者依赖失败请求无 Set-Cookie 且发起客户端未登录；后者依赖 `browser_cookie_list` 的 `credentialReferences` 由 `sid` 变为空，其 output 被 Harness 省略），已与直接观察到的功能结果分别记录。
5. `CLEANUP-SCOPE-001` 期望 4 的 SQL / 任意用户 ID 参数条款**未构造专门请求**（端点无相应入参），仅由非法 Run ID 拒绝与删除计数=前缀账号数支持。
6. `#message` 与 `user.displayName` 在快照中按 Harness 规则脱敏，昵称以截图（REGISTRATION-001）与响应体/页面文案交叉确认；未复述口令/Token/哈希值。

## 证据与观察归属

- 证据文件（本次 Run 上下文提供）：2 张截图 `AUTH-REGISTRATION-001-welcome.png`、`AUTH-DELETE-001-after-delete.png`（均 `screenshotInspection.status=detected`，scope=page，sha256 与所列值一致）；若干页面快照、console 日志与大量 `operation-*.json` 操作记录。稳定 URL 形如 `/api/evidence/<token>`，此处不逐条改写。
- **执行归属**：review 说明其核对到 Playwright MCP 浏览器操作回执（`browser_navigate/fill_form/click/network_requests/cookie_list/take_screenshot`），据此将浏览器行为与实际执行关联。证据文件的存在本身不单独证明某执行者做过对应操作，页面文案类判定依据的是 review 交付的截图/快照观察与上述操作回执。
- **时间**：本批记录的时间只用于表达先后顺序与 Harness 记录时间（如 console/page 文件名中的 UTC 时间戳），**不与服务器时钟混用**，不作绝对事件时间结论。
- 审核方法：review 声明其先读计划与冻结场景快照，再独立核对全部 131 个 `operation-*.json`、12 个页面快照、4 个 console 日志、2 张截图，最后与 `execution.md` 对照，且未读取历史 Issue 列表或其他 Session。以上均为 Reviewer 的交付陈述，此处如实转录、不再重做审核。

## Issue 查询覆盖缺口

本次 **0 个已确认产品 Bug**（0 failed，唯一 blocked 项归因于工具能力边界），因此没有 Bug key 需要 `query_issue_candidates`，不存在因查询不可用而未覆盖的 Bug key。`confirmed_bugs` 为空数组。

说明：`issue_action` 的 create/link 在无 confirmed Bug 时不适用；本次不宣称已创建或关联任何 Issue，也不声称跨 Run 无重复。场景资产维护需求（如 draft 场景的后续覆盖）属场景资产事项，不冒充产品 Bug。

## 结论

- 13 项声明执行场景全部执行：**12 passed、1 blocked、0 failed**；整体结果 **blocked**。
- 无已确认产品缺陷；唯一阻塞（`CLEANUP-SEED-001`）源于受控工具不提供跨其他 Run 的余量观察，非产品问题。其余覆盖缺口为观察口径与未直接演练的负向条款，已逐条保留。
- 本次通过仅限所列冻结期望与场景，不扩大为“整个项目没有问题”。
- 测试后临时数据（本 Run 前缀账号）在执行内 `DELETE` 后余量为 0（review 引 operation-131）；**最终清理收尾由 Harness 独立核验**，本报告不提前声称清理已完成，也不填写系统收尾区。

## 必要下一步

- 若要闭合 `CLEANUP-SEED-001`：需要具备**跨 Run 只读余量观察**能力的受控工具或授权范围，由后续 Run 在该能力下重跑本场景；本轮现有权限不提供该能力，替代方案（如以非法 ID 近似）不构成等价验证，不作降级处理。
- 若要覆盖 spec 第 4 条“清理接口默认关闭 / 短 Token 拒绝启用”：需先解除 `CLEANUP-CONFIG-001` 的多实例启动前置，此属另行确认的环境/工具范围，非本批授权。

<!-- luowang-screenshot-inspection -->
## 截图采集标签

- [截图 1](</api/evidence/bHVvd2FuZy9jeW5vcy13ZWJzaXRlL211bHRpLXByb2plY3QtdjA2MS1saXZlLTRkNDIwODQwL3Byb2plY3RzL2RhZjdlNDJkLTIwZDctNDUzYS1hMjZkLWQyYmFiMWMxZjQ3OC9ydW5zLzAxTTNCWDdBNlNRUUs4TVZXNktaNVM0MjU2L0FVVEgtREVMRVRFLTAwMS1hZnRlci1kZWxldGUucG5n>)：页面含可见表单值；检测范围为页面，不代表图片整体安全或人工审核通过。
- [截图 2](</api/evidence/bHVvd2FuZy9jeW5vcy13ZWJzaXRlL211bHRpLXByb2plY3QtdjA2MS1saXZlLTRkNDIwODQwL3Byb2plY3RzL2RhZjdlNDJkLTIwZDctNDUzYS1hMjZkLWQyYmFiMWMxZjQ3OC9ydW5zLzAxTTNCWDdBNlNRUUs4TVZXNktaNVM0MjU2L0FVVEgtUkVHSVNUUkFUSU9OLTAwMS13ZWxjb21lLnBuZw>)：页面含可见表单值；检测范围为页面，不代表图片整体安全或人工审核通过。
<!-- /luowang-screenshot-inspection -->

## Harness 清理收尾

测试数据清理完成；不改变本次功能验证结果。

清理适配器已独立核验 6 项测试数据不存在

全部登记测试数据均已独立核验清理

独立核验：luowang-01M3BX7A6SQQK8MVW6KZ5S4256-welcome · run-scoped-http-cleanup · 2026-09-25T09:15:47.605Z · absent=true · sha256 b371ae4b66605cb892df4d99659a67e0349d59ff76c197d06edc8209c68a6667

独立核验：luowang-01M3BX7A6SQQK8MVW6KZ5S4256-dup · run-scoped-http-cleanup · 2026-09-25T09:15:47.609Z · absent=true · sha256 b371ae4b66605cb892df4d99659a67e0349d59ff76c197d06edc8209c68a6667

独立核验：luowang-01M3BX7A6SQQK8MVW6KZ5S4256-sess · run-scoped-http-cleanup · 2026-09-25T09:15:47.612Z · absent=true · sha256 b371ae4b66605cb892df4d99659a67e0349d59ff76c197d06edc8209c68a6667

独立核验：luowang-01M3BX7A6SQQK8MVW6KZ5S4256-login1 · run-scoped-http-cleanup · 2026-09-25T09:15:47.615Z · absent=true · sha256 b371ae4b66605cb892df4d99659a67e0349d59ff76c197d06edc8209c68a6667

独立核验：luowang-01M3BX7A6SQQK8MVW6KZ5S4256-ctrl · run-scoped-http-cleanup · 2026-09-25T09:15:47.619Z · absent=true · sha256 b371ae4b66605cb892df4d99659a67e0349d59ff76c197d06edc8209c68a6667

独立核验：luowang-01M3BX7A6SQQK8MVW6KZ5S4256-store1 · run-scoped-http-cleanup · 2026-09-25T09:15:47.622Z · absent=true · sha256 b371ae4b66605cb892df4d99659a67e0349d59ff76c197d06edc8209c68a6667
