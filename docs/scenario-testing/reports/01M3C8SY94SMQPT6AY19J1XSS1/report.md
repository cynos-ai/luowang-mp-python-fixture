---
run_id: 01M3C8SY94SMQPT6AY19J1XSS1
trigger: manual
base_commit: 6d3f87c2f36544eddcf1b78569a454be5cb644c0
target_commit: 08d5d82a358c507ba29a32646e01674991e1be93
included_commits: []
result: blocked
started_at: 2026-09-25T12:37:44.196Z
finished_at: 2026-09-25T12:43:20.423Z
scenario_results:
  - id: AUTH-REGISTRATION-001
    result: passed
  - id: AUTH-REGISTRATION-002
    result: passed
  - id: AUTH-REGISTRATION-003
    result: passed
  - id: AUTH-LOGIN-001
    result: passed
  - id: AUTH-LOGIN-002
    result: passed
  - id: AUTH-SESSION-001
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

# 最终报告 — Python 账号场景复核（target `08d5d82a`，Run `01M3C8SY94SMQPT6AY19J1XSS1`）

## 概述与请求

本 Run 对上一次全场景 Run `01M3BHYQCY8D4P6WKD01RAPH0E` 中因 HTTP 能力不足而 blocked 的 10 个 approved 场景执行完整复核，并补充相关注册/会话/存储场景。执行依据 plan.md 唯一 `## execution_scenarios` 清单共 13 项全部 approved 场景，覆盖注册（3）、登录（2）、会话（1）、删除（2）、存储（2）、清理（4）。本次认定以 review.md 独立审核结论与既有执行证据为据，不复做检验。

- base：`6d3f87c2f36544eddcf1b78569a454be5cb644c0`；target：`08d5d82a358c507ba29a32646e01674991e1be93`；includedCommits：`[]`
- 本 Run 无 `scenario-changes.patch`（工具返回「工件不存在」），与计划「本批不新增/不修改/不废弃场景」一致；`planHash` 经 `query_source_reads(scope=plan)` 校验通过。

## 范围与变化说明

`list_target_changes`（base→target）只新增两份文档工件，产品代码、测试与场景资产在本区间无变化。因此本批并非代码变更回归，而是「受控验证能力变化（`request_test_http`、`probe_run_cleanup`）+ 场景覆盖补齐」驱动的重新验证。计划已声明：不能据 diff 推断产品行为，也不能据代码未变声称旧结论仍成立，旧结论责任仍在原 Run。计划对当前 target 注册欢迎语文案的源码观察已明确标注「实现线索，仅作线索、不代替执行」。

## 逐场景结果

结果与依据取自 review.md 独立审核（Reviewer 通过 `query_source_reads` 校验来源、独立读取原始证据后形成判断，并与 execution.md 逐项核对一致）。以下「Runner 记录」为 execution.md 原文转述，「Reviewer 判定」为独立审核结论。

1. **AUTH-REGISTRATION-001 — passed。** 页面 `GET /` 表单可见，提交注册后状态区 `#message` 显示中文欢迎语且昵称与提交昵称一致；注册 `POST /api/auth/register → 201` 并设置 `sid`；`GET /api/auth/status` 为 authenticated 且 `user.displayName` 一致。旧 Run 的英文欢迎语未在当前 target 复现，结论仅来自本次实际页面观察。
2. **AUTH-REGISTRATION-002 — passed。** 首次注册 201 并设 `sid`；同邮箱再次注册 409 `ACCOUNT_EXISTS` 且未设 Cookie；原邮箱原口令登录 201 且 `displayName` 为首次昵称；页面侧第二次提交显示非注册成功。失败尝试未替换会话。
3. **AUTH-REGISTRATION-003 — passed。** 三次直接接口调用（邮箱不含 `@`、昵称为空、口令短于 12 字符）分别 400 `INVALID_ACCOUNT` / 400 `INVALID_ACCOUNT` / 400 `WEAK_PASSWORD`；三次后 status 均未登录、均未设 Cookie；三组凭据登录均 401 `INVALID_CREDENTIALS`。无可用账号产生。
4. **AUTH-LOGIN-001 — passed。** 正确凭据登录 201 并设 `sid`，返回 `user.email`/`user.displayName`；随后 status authenticated 且用户信息一致。
5. **AUTH-LOGIN-002 — passed。** 错误口令 / 未注册邮箱两次登录均 401、未设 Cookie、status 未登录；随后正确凭据 201 成功，失败尝试未破坏账号。
6. **AUTH-SESSION-001 — passed。** 匿名客户端 status 未登录；页面注册后浏览器 status authenticated 且邮箱一致；重新加载 `GET /` 后 status 仍 authenticated 且用户信息不变。
7. **AUTH-DELETE-001 — passed。** 注册 201 设 `sid`；`DELETE /api/me` 200 `{"deleted":true}` 且清除 `sid` Cookie；随后 status 未登录、原凭据登录 401、重复删除 401 `UNAUTHORIZED`；页面侧点击「删除账号」显示「账号已删除。」。
8. **AUTH-DELETE-002 — passed。** 无 Cookie 客户端 `DELETE /api/me` 401 `UNAUTHORIZED`（无删除成功结果）；匿名 status 未登录；对照账号未被删除、原凭据仍可登录。
9. **DATA-STORAGE-001 — passed（附覆盖限制）。** 受控只读汇总与清理端点 storage 均返回 `accounts:5, argon2id:5, other:0`，满足 `accounts == argon2id`、`other == 0`。**覆盖限制（Reviewer 认可 Runner 标注）**：受控观察仅提供聚合计数，`argon2id` 桶由应用对 `$argon2id$` PHC 前缀的分类得出，未取得单条哈希正文或独立持久层的逐条前缀观察。计划证据优先级已将「三桶计数」列为可接受口径，故不影响判定，但「形如 `$argon2id$` 前缀」仅为间接支持。
10. **STORAGE-OBSERVE-001 — passed。** 带有效 Token `GET …/storage` 200，响应体仅 `accounts/argon2id/other/runId`，`Cache-Control: no-store`；非法 Run ID 的 `GET …/storage` 400 `INVALID_RUN_ID`、`GET …/<runId>` 400，均不含计数。响应无邮箱/用户 ID/口令/哈希。
11. **CLEANUP-AUTH-001 — passed。** 无 Authorization 与错误 Token 的 `GET …/<runId>`、`GET …/storage`、`DELETE …/<runId>` 均 401，拒绝体 `{"error":"UNAUTHORIZED"}` 不含计数/邮箱/用户 ID/口令/哈希；随后原凭据登录该 Run 账号 201，有效 Token 复核 `remaining:5`，账号未被删除。
12. **CLEANUP-SCOPE-001 — passed（附覆盖限制）。** 清理前 `deleted:0, remaining:5`；`DELETE → deleted:5, remaining:0`；独立 `GET` 余量 0、storage `accounts:0`；非法 Run ID 的 `DELETE`/`GET` 均 400 且不删除；被清理账号原凭据登录 401；清理后重建探针并使余量回 1，再次非法 Run ID `DELETE` 仍 400，随后有效 Token 清理 `deleted:1, remaining:0`。**覆盖限制（Runner 未单列，Reviewer 补充）**：期望第 4 条「不接受任意用户 ID/SQL/跨 Run 参数」的注入面未直接执行——受控清理工具只接受 `runId`（current/invalid 两类）；「跨 Run 不删除」仅由「非法 Run ID 拒绝 + 删除后不误删」间接体现。核心可测面（按完整前缀删除、删除数一致、非法 ID 拒绝）证据充分，故仍判 passed。
13. **CLEANUP-SEED-001 — blocked。** **期望 A（预置账号免于本 Run 清理）已验证**：预置账号清理前登录 201，本 Run `DELETE → deleted:1, remaining:0`，清理后预置账号仍 201 而本 Run 账号 401。**期望 B（另一合法 Run ID 余量前后一致）未验证**：`probe_run_cleanup` 仅支持当前 Run/固定非法 ID；`request_test_http` 无法注入部署级 Token，对另一 Run ID 的 `GET /api/luowang/test-data/<otherRunId>` 返回 401 `UNAUTHORIZED`，未取得余量读数。计划已预先规定「无法取得另一 Run 余量观察则维持未验证、场景 blocked、不降级」，Runner 依此判定；期望 B 无受控观察手段 → **blocked**（期望 A 的已确认成功不因 blocked 被撤销）。

计数口径：执行场景 13 项，passed 12、blocked 1、failed 0、未执行 0。同一项不重复计入互斥分类。

## 结果判定与聚合

- 最终结果 **blocked**：CLEANUP-SEED-001 含两个必检期望，其中期望 B 尚无受控观察手段，场景不能确认通过，按 `blocked > failed > passed` 聚合，整体为 blocked。
- **未发现已确认产品 Bug**。12 个 passed 场景的明列期望均有实际观察支持；本报告 `confirmed_bugs` 为空数组。

## 已确认产品问题

无。Reviewer 独立审核未发现违反期望的行为。以下仅为**观察项，非缺陷**：

- 重复邮箱注册时页面状态区以原始错误码 `ACCOUNT_EXISTS` 呈现（快照 `page-2026-09-25T12-39-45-202Z.yml` 与截图 `auth-reg-002-dup.png`）。Reviewer 明确判定其符合 AUTH-REGISTRATION-002「不显示注册成功」的原文期望，是否本地化文案不影响该场景结论，**不构成产品缺陷**，故不进入 `confirmed_bugs`，也无 issue_action。

## Issue 查询

本 Run 无本次已确认产品 Bug 候选，`confirmed_bugs: []`，因此无需 create/link，无待归档项。

## Issue 查询覆盖缺口

无。本批 `confirmed_bugs` 为空数组，不涉及 Bug 去重覆盖缺口；上文观察项按审核结论明确为非缺陷，不冒充产品 Bug。为核对文案观察项是否已有同类记录，我以 title/keywords 对该观察项执行了一次相似 Issue 查询（关键词涉及重复邮箱注册的错误码呈现），返回状态为 `empty`（未发现相似候选），非 `unavailable`；该结果仅作核对，不改变其「非缺陷」的审核结论。计划提及的历史 Issue #4「注册成功后页面状态区显示英文欢迎语」状态为 closed，与本批观察项不同，且本批结论不据历史改写旧 Run 结论。

## 覆盖缺口与未完成项

1. **CLEANUP-SEED-001 期望 B（另一 Run 余量对照）**：受控工具无法携带部署级 Token 读取指定合法 Run ID 的余量，期望 B 未验证，场景 blocked。所需能力：可带 Token 读取指定合法 Run ID 余量的受控入口，或 Harness 跨 Run 隔离核验。与 CLEANUP-SCOPE-001 第 4 条的跨 Run 注入面同源。
2. **DATA-STORAGE-001 持久层正文**：仅有聚合三桶计数，未直接观察单条 `$argon2id$` 哈希正文或明文；不影响「聚合全部为 Argon2id、无其他格式」的期望判断，但具体前缀文本为间接支持。
3. **CLEANUP-SCOPE-001 注入子句**：任意用户 ID/SQL/跨 Run 参数不可经现有工具提交，该子句未直接验证。
4. **CLEANUP-CONFIG-001（draft）未执行**：需以自定义环境变量启动多实例，非当前受控环境可构造；计划已列为已知限制且未列入 `execution_scenarios`，draft 不构成执行授权，排除合理。此属场景执行缺口，不改其它场景结论。
5. **脱敏缺口**：`page-*.yml` 中昵称/邮箱/Cookie 值被脱敏，仅状态区结构与语义可读；昵称逐字一致性由截图（可见值）补足。`execution.md` 对截图多记为「清单确认存在」而非描述画面内容，画面内容由 Reviewer 另行读取 4 张截图核对，未发现与记录矛盾。
6. **受控 Secret 边界**：本报告未执行系统性 Secret 扫描，不作「不存在任何密码文本」类绝对声明。记录与审核均未复述口令、Token 或 Cookie 值。

## 证据引用

以下证据 URL 原样取自本 Run 动态上下文，未自行编码或改写；证据清单与 review.md 所列一致。

- 页面截图：`auth-delete-001-page.png`、`auth-reg-001-welcome.png`、`auth-reg-002-dup.png`、`auth-session-001-refresh.png`
- 浏览器/页面快照（`page-*.yml`，共 16 份，含脱敏）：`page-2026-09-25T12-39-18-534Z.yml`、`page-2026-09-25T12-39-23-539Z.yml`、`page-2026-09-25T12-39-27-651Z.yml`、`page-2026-09-25T12-39-40-732Z.yml`、`page-2026-09-25T12-39-45-202Z.yml`、`page-2026-09-25T12-40-05-281Z.yml`、`page-2026-09-25T12-40-09-350Z.yml`、`page-2026-09-25T12-40-10-618Z.yml`、`page-2026-09-25T12-40-12-897Z.yml`、`page-2026-09-25T12-40-13-742Z.yml`、`page-2026-09-25T12-40-21-418Z.yml`、`page-2026-09-25T12-40-26-130Z.yml`、`page-2026-09-25T12-40-28-280Z.yml`
- 控制台日志：`console-2026-09-25T12-39-18-475Z.log`、`console-2026-09-25T12-39-40-698Z.log`、`console-2026-09-25T12-40-05-252Z.log`、`console-2026-09-25T12-40-12-866Z.log`、`console-2026-09-25T12-40-21-385Z.log`
- 操作记录：`operation-1.json` … `operation-126.json`（HTTP 请求、浏览器操作、清理/存储端点调用的命令/MCP 记录）

Reviewer 在阅读证据时另有：`browser_navigate`/`browser_snapshot`/`browser_click`/`browser_cookie_list`/`browser_take_screenshot`/`browser_network_requests` 的实际操作归属记录（非仅有快照/日志），说明这些内容与实际执行关联；证据文件本身的存在不单独证明执行归属，属本次操作的来源以相应操作记录为准。

## 时间与来源说明

- 时间均为 Harness 记录时间（operation `at`/`startedAt`/`finishedAt`，UTC，集中在 2026-09-25T12:39–12:41Z 区间）；未取得被测服务 `date` 响应头，二者无共同校准时基，仅用于先后顺序与 Harness 记录时间，未作精确时刻断言，也未作跨 Run 时间对比。
- 来源归属：Runner 的 passed/blocked 判定为 execution.md 记录；逐场景依据的独立结论、CLEANUP-SCOPE-001 第 4 条覆盖限制的补充及各项覆盖限制的认可，均归 Reviewer（独立审核）。本报告按既定聚合规则汇总，不复做证据审核。
- 本 Run 无人工复核记录，不声称人工确认。
- **发布状态与测试结果分别表达**：本报告只陈述测试结果，不主张任何发布、归档或 Issue 创建动作已完成。

## 测试数据收尾

测试数据清理由 Harness 在本 Session 结束后统一处理并独立核验，本报告不提前声称已完成。执行结束时当前 Run 余量为 0（属执行后的辅助读取），Run 前缀账号已登记。场景内自行删除的账号与受控清理记录见相应 operation（与 review.md 一致），收尾核验不属于本次审核或阻塞事项。

<!-- luowang-screenshot-inspection -->
## 截图采集标签

- [截图 1](</api/evidence/bHVvd2FuZy9jeW5vcy13ZWJzaXRlL211bHRpLXByb2plY3QtdjA2MS1saXZlLTRkNDIwODQwL3Byb2plY3RzL2RhZjdlNDJkLTIwZDctNDUzYS1hMjZkLWQyYmFiMWMxZjQ3OC9ydW5zLzAxTTNDOFNZOTRTTVFQVDZBWTE5SjFYU1MxL2F1dGgtZGVsZXRlLTAwMS1wYWdlLnBuZw>)：页面含可见表单值；检测范围为页面，不代表图片整体安全或人工审核通过。
- [截图 2](</api/evidence/bHVvd2FuZy9jeW5vcy13ZWJzaXRlL211bHRpLXByb2plY3QtdjA2MS1saXZlLTRkNDIwODQwL3Byb2plY3RzL2RhZjdlNDJkLTIwZDctNDUzYS1hMjZkLWQyYmFiMWMxZjQ3OC9ydW5zLzAxTTNDOFNZOTRTTVFQVDZBWTE5SjFYU1MxL2F1dGgtcmVnLTAwMS13ZWxjb21lLnBuZw>)：页面含可见表单值；检测范围为页面，不代表图片整体安全或人工审核通过。
- [截图 3](</api/evidence/bHVvd2FuZy9jeW5vcy13ZWJzaXRlL211bHRpLXByb2plY3QtdjA2MS1saXZlLTRkNDIwODQwL3Byb2plY3RzL2RhZjdlNDJkLTIwZDctNDUzYS1hMjZkLWQyYmFiMWMxZjQ3OC9ydW5zLzAxTTNDOFNZOTRTTVFQVDZBWTE5SjFYU1MxL2F1dGgtcmVnLTAwMi1kdXAucG5n>)：页面含可见表单值；检测范围为页面，不代表图片整体安全或人工审核通过。
- [截图 4](</api/evidence/bHVvd2FuZy9jeW5vcy13ZWJzaXRlL211bHRpLXByb2plY3QtdjA2MS1saXZlLTRkNDIwODQwL3Byb2plY3RzL2RhZjdlNDJkLTIwZDctNDUzYS1hMjZkLWQyYmFiMWMxZjQ3OC9ydW5zLzAxTTNDOFNZOTRTTVFQVDZBWTE5SjFYU1MxL2F1dGgtc2Vzc2lvbi0wMDEtcmVmcmVzaC5wbmc>)：范围内未检测到可见表单值；检测范围为页面，不代表图片整体安全或人工审核通过。
<!-- /luowang-screenshot-inspection -->

## Harness 清理收尾

测试数据清理完成；不改变本次功能验证结果。

清理适配器已独立核验 7 项测试数据不存在

全部登记测试数据均已独立核验清理

独立核验：luowang-01M3C8SY94SMQPT6AY19J1XSS1-welcome · run-scoped-http-cleanup · 2026-09-25T12:43:44.431Z · absent=true · sha256 8d26915c0e5e442f78849b80e13cce5fed3f9c52c3e358cd3d40329ac68bbadb

独立核验：luowang-01M3C8SY94SMQPT6AY19J1XSS1-dup · run-scoped-http-cleanup · 2026-09-25T12:43:44.435Z · absent=true · sha256 8d26915c0e5e442f78849b80e13cce5fed3f9c52c3e358cd3d40329ac68bbadb

独立核验：luowang-01M3C8SY94SMQPT6AY19J1XSS1-session · run-scoped-http-cleanup · 2026-09-25T12:43:44.438Z · absent=true · sha256 8d26915c0e5e442f78849b80e13cce5fed3f9c52c3e358cd3d40329ac68bbadb

独立核验：luowang-01M3C8SY94SMQPT6AY19J1XSS1-del · run-scoped-http-cleanup · 2026-09-25T12:43:44.442Z · absent=true · sha256 8d26915c0e5e442f78849b80e13cce5fed3f9c52c3e358cd3d40329ac68bbadb

独立核验：luowang-01M3C8SY94SMQPT6AY19J1XSS1-ctrl · run-scoped-http-cleanup · 2026-09-25T12:43:44.445Z · absent=true · sha256 8d26915c0e5e442f78849b80e13cce5fed3f9c52c3e358cd3d40329ac68bbadb

独立核验：luowang-01M3C8SY94SMQPT6AY19J1XSS1-storage · run-scoped-http-cleanup · 2026-09-25T12:43:44.448Z · absent=true · sha256 8d26915c0e5e442f78849b80e13cce5fed3f9c52c3e358cd3d40329ac68bbadb

独立核验：luowang-01M3C8SY94SMQPT6AY19J1XSS1-probe · run-scoped-http-cleanup · 2026-09-25T12:43:44.453Z · absent=true · sha256 8d26915c0e5e442f78849b80e13cce5fed3f9c52c3e358cd3d40329ac68bbadb
