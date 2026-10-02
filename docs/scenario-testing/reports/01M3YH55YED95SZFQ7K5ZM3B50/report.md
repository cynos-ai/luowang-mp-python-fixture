---
run_id: 01M3YH55YED95SZFQ7K5ZM3B50
trigger: manual
base_commit: 20e0681ba85f02beb5396dab5f7458c76905aa40
target_commit: df309eb9fab78047494c0f50d5fb9c76f8ec716d
included_commits: []
result: passed
started_at: 2026-10-02T14:44:12.575Z
finished_at: 2026-10-02T14:45:25.393Z
scenario_results:
  - id: AUTH-LOGIN-001
    result: passed
confirmed_bugs: []
---

# 最终报告 — Run `01M3YH55YED95SZFQ7K5ZM3B50`

## 1. 请求与范围

- 人工请求：本轮**仅回归已有 approved 场景 `AUTH-LOGIN-001`**，完整验证该场景全部既定期望；使用按本 Run 标记并登记的独立合成账号；注册只作登录场景准备，不扩大到注册或存储场景；另一个项目的环境故障不得改变本项目目标、账号或证据。
- 触发方式：manual。固定版本：base `20e0681ba85f02beb5396dab5f7458c76905aa40` → target `df309eb9fab78047494c0f50d5fb9c76f8ec716d`，`includedCommits` 为空。
- 计划：`plan.md`（`planHash=44b19a06ca47fe031c9c6a48ec9d59c315aa3462a4d133dde906991c8d537087`）。执行清单 `## execution_scenarios` 仅一项：`AUTH-LOGIN-001`。
- 场景维护：计划声明 `scenarioChanges=null`、无 `write_scenario_patch`，与 base→target 无场景/源码/配置变化一致（`list_target_changes` total=2，仅新增上一 Run 的两份报告工件）。本轮初始化未提供场景 patch；本汇总不修改任何场景资产。
- 汇聚依据：本报告仅整理 `plan.md` 与 `review.md` 的已交付内容，未重跑测试、未回读运行记录、未另做证据审核。

## 2. 逐场景结果

### AUTH-LOGIN-001 — 正确凭据登录建立会话并返回用户信息：**passed**

计划的 5 项关键检查（来源为场景 `## 期望` 原文）与独立审核结论对应如下。该场景 `## 期望` 无被排除项，5 项均适用。

| # | 期望 | 判定所用观察（Reviewer 独立核对） | 结果 |
| - | --- | --- | --- |
| 1 | 登录请求成功（2xx） | `POST /api/auth/login`（隔离 clientId `login-01M3YH55`）实际状态 `201` | passed |
| 2 | 设置会话 Cookie（`sid`） | 登录响应 `setCookieNames=["sid"]` | passed |
| 3 | `GET /api/auth/status` 的 `authenticated` 为 true | 同一 clientId 上 status `200`，body `authenticated:true`，且该请求携带 `cookieNames=["sid"]` | passed |
| 4 | `user.email` 与所登录账号一致 | 三处（注册/登录/status）邮箱一致，按小写归一比对 | passed |
| 5 | `user.displayName` 与所登录账号一致 | 三处逐字一致 | passed |

- 会话建立的关键点：登录发生在与注册相互隔离的客户端上，登录响应新下发 `sid`，随后同一客户端携带该 Cookie 读取 status 得到已认证——支持“凭据核对成功后建立会话”，而非复用注册客户端既有会话。此项为 Reviewer 基于原始证据的判断。
- 字段一致性以注册响应为账号事实源，与登录响应、status 响应比对一致；未复述任何 Cookie 值或口令值。
- 判定来源归属：逐项判定与 `passed` 结论由 Reviewer（`review.md`）独立核对后交付；计划中的实现事实（`app.py` 登录/状态路径）为静态来源，计划本身已声明其不代替运行观察。本报告不新增判定。

## 3. 已确认产品问题与 Issue 决策

- 本次审核已确认产品 Bug：**无**。5 项适用期望全部满足，未发现与期望相违的行为。
- 由于无已确认 Bug，无 Bug key 需要 create/link 决策；`confirmed_bugs` 为空数组。
- 为尽去重义务，仍按标题、关键词与 bug key 做了受限查询，结果均为 `empty`（无相似候选）。这不构成“项目无任何同类问题”的声明，仅表示本次查询未返回可关联 Issue。

## 4. 覆盖缺口、限制与未完成项（如实保留，不改变场景判定）

1. **清理与清理后核验未在本 Run 证据中出现**（Reviewer 记录）：场景 `## 需要记录` 含“登记、清理与清理后核验”；证据中仅见注册操作，未见清理调用与清理后“账号不存在”的核验记录。按计划该类属 Harness 收尾事项，其未完成单独记录，不影响 `AUTH-LOGIN-001` 的产品判定。**“清理已完成”不能由本轮证据支持**；测试数据清理由 Harness 在本 Session 结束后统一处理，本报告不声称已完成。
2. **账号登记为过程性记录**（Reviewer 记录）：执行记录声明账号已登记并给出清理范围（`cleanupScope=website-accounts`），但无独立登记工件证据；字段比对所需的账号事实由注册响应提供，足以支撑字段一致性判断。
3. **请求正文未捕获**（Reviewer 记录）：证据记录响应与状态，未含登录请求体（口令）。这不影响 2xx / Cookie / status 期望的判定。
4. **环境故障隔离**：计划要求“另一个项目的环境故障不得改变本项目目标、账号或证据”。审核记录**未观察到**来自其他项目的环境故障信号，本项目端点全程可达，target、账号、证据来源未改变。Reviewer 明确该结论系执行记录陈述、原始证据中无相反事实，但**也无独立外部故障探针证据**，故仅作“未出现”记录，不外推为已证明不存在此类故障。
5. **范围外不推论**：预置账号登录对照、`AUTH-LOGIN-002` 拒绝路径，以及注册/会话/删除/清理/存储等场景本轮均未执行，其既有结论不被本轮改写；本轮结论不外推至整个项目。
6. **历史去重线索**：计划记录 `historyIssuesAvailable=true`，存在已关闭 Issue #4（注册欢迎语语言问题），与登录场景无直接关联，仅作去重线索，不影响本轮范围判断。

## 5. 证据与一致性

- 证据文件：6 份受控 HTTP 操作记录 `operation-1.json` ~ `operation-6.json`（上传收据 6/6，与证据清单一致）。证据 URL 原样引用：
  - [operation-1.json](/api/evidence/bHVvd2FuZy9jeW5vcy13ZWJzaXRlL3Byb2plY3QtY29uY3VycmVuY3ktMjAyNjEwMDIvcHJvamVjdHMvNjIwYjgzYjAtN2VjYi00YWE4LWI4MGItYzFkZjdkY2RiNWExL3J1bnMvMDFNM1lINTVZRUQ5NVNaRlE3SzVaTTNCNTAvb3BlcmF0aW9uLTEuanNvbg)
  - [operation-2.json](/api/evidence/bHVvd2FuZy9jeW5vcy13ZWJzaXRlL3Byb2plY3QtY29uY3VycmVuY3ktMjAyNjEwMDIvcHJvamVjdHMvNjIwYjgzYjAtN2VjYi00YWE4LWI4MGItYzFkZjdkY2RiNWExL3J1bnMvMDFNM1lINTVZRUQ5NVNaRlE3SzVaTTNCNTAvb3BlcmF0aW9uLTIuanNvbg)
  - [operation-3.json](/api/evidence/bHVvd2FuZy9jeW5vcy13ZWJzaXRlL3Byb2plY3QtY29uY3VycmVuY3ktMjAyNjEwMDIvcHJvamVjdHMvNjIwYjgzYjAtN2VjYi00YWE4LWI4MGItYzFkZjdkY2RiNWExL3J1bnMvMDFNM1lINTVZRUQ5NVNaRlE3SzVaTTNCNTAvb3BlcmF0aW9uLTMuanNvbg)
  - [operation-4.json](/api/evidence/bHVvd2FuZy9jeW5vcy13ZWJzaXRlL3Byb2plY3QtY29uY3VycmVuY3ktMjAyNjEwMDIvcHJvamVjdHMvNjIwYjgzYjAtN2VjYi00YWE4LWI4MGItYzFkZjdkY2RiNWExL3J1bnMvMDFNM1lINTVZRUQ5NVNaRlE3SzVaTTNCNTAvb3BlcmF0aW9uLTQuanNvbg)
  - [operation-5.json](/api/evidence/bHVvd2FuZy9jeW5vcy13ZWJzaXRlL3Byb2plY3QtY29uY3VycmVuY3ktMjAyNjEwMDIvcHJvamVjdHMvNjIwYjgzYjAtN2VjYi00YWE4LWI4MGItYzFkZjdkY2RiNWExL3J1bnMvMDFNM1lINTVZRUQ5NVNaRlE3SzVaTTNCNTAvb3BlcmF0aW9uLTUuanNvbg)
  - [operation-6.json](/api/evidence/bHVvd2FuZy9jeW5vcy13ZWJzaXRlL3Byb2plY3QtY29uY3VycmVuY3ktMjAyNjEwMDIvcHJvamVjdHMvNjIwYjgzYjAtN2VjYi00YWE4LWI4MGItYzFkZjdkY2RiNWExL3J1bnMvMDFNM1lINTVZRUQ5NVNaRlE3SzVaTTNCNTAvb3BlcmF0aW9uLTYuanNvbg)
- `requiresBrowser=false`：本场景全部期望位于 HTTP/会话层，无浏览器快照或页面日志证据，声明与执行一致，不构成缺口。本报告未作“证据列表为空”式表述——证据文件为 6 份 JSON 操作记录。
- 执行归属与内容归属分开：上述观察的操作执行与内容由本轮受控 HTTP 操作产生；其独立核对与判定由 Reviewer 交付。本汇总角色未执行测试。
- 进度与顺序：场景进度 `begin→start→finish`，1/1 完成，与计划的执行清单顺序一致。
- 时间：`started_at` / `finished_at` 逐字取自本 Run 动态上下文；报告未对文件时间或事件时间另作绝对换算推断。

## 6. 结论与下一步

- 总结果：**passed**（执行清单 1/1 场景通过；`blockingReasons` 为空，无 Harness 阻塞原因）。
- 已确认产品 Bug：无；无 Issue create/link 动作（`confirmed_bugs: []`）。本次查询为 `empty`，不代表项目不存在同类问题。
- 未解决/待跟进事项：清理与清理后核验记录缺失（Harness 收尾事项），其状态不由本报告或本轮证据表明已完成。
- 当前授权范围内的必要下一步：由 Harness 在 Session 结束后按其登记范围完成测试数据清理与清理后核验，并将该收尾结果单独记录。
- 若需覆盖拒绝路径（`AUTH-LOGIN-002`）、注册/存储/删除/清理等场景或预置账号对照，均超出本轮请求范围，需另行确认后再安排执行。

## Harness 清理收尾

测试数据清理完成；不改变本次功能验证结果。

清理适配器已独立核验 1 项测试数据不存在

全部登记测试数据均已独立核验清理

独立核验：luowang-01M3YH55YED95SZFQ7K5ZM3B50-login-account · run-scoped-http-cleanup · 2026-10-02T14:45:49.235Z · absent=true · sha256 e03ffb816838006bc079fd25c3a399b2dfa49fdcdecd44a0936cc4682bf6448e
