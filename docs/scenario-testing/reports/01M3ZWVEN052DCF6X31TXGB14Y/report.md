---
run_id: 01M3ZWVEN052DCF6X31TXGB14Y
trigger: manual
base_commit: null
target_commit: 924f1d1f7bdd9ff72b152e779684427fc0138e9f
included_commits: []
result: passed
started_at: 2026-10-03T03:27:49.617Z
finished_at: 2026-10-03T03:31:29.233Z
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

# 测试报告 — Run `01M3ZWVEN052DCF6X31TXGB14Y`

## 范围与依据

- 请求要点：对固定 `scenario-testing` 提交执行已有 approved 核心场景，覆盖「登录后的会话状态」与「一条独立合成数据路径」；使用受控测试账号，新增数据登记并带本 Run ID，截图保留真实页面状态；应用与数据域独立；遵守场景既定期望。
- target：`924f1d1f7bdd9ff72b152e779684427fc0138e9f`；`baseCommit=null`、`includedCommits=[]`（无基线、无变化清单），故本批为**无 base 的固定提交回归**，不依据 diff 裁剪范围，也不能据此判断 target 变更内容。
- 执行集合来自计划唯一的 `## execution_scenarios`，共 4 条，顺序为 `AUTH-LOGIN-001` → `AUTH-SESSION-001` → `AUTH-REGISTRATION-001` → `DATA-STORAGE-001`；审核核对 `scenario-progress` 事件顺序与之一致。
- 场景资产维护：本次无 `scenario-changes.patch`（计划声明不新增/不修改/不废弃；审核独立核对后确认该工件不存在、4 条场景 `contentHash` 与快照一致）。因此**未有任何场景被修订**，也不存在“修订后场景未重新执行”的情形。
- 范围外场景（`AUTH-DELETE-001`、`AUTH-REGISTRATION-002/003`、`AUTH-LOGIN-002`、`CLEANUP-AUTH-001`、`CLEANUP-SCOPE-001`、`STORAGE-OBSERVE-001` 及 draft 的 `CLEANUP-CONFIG-001`）本次未执行，其结论不被本 Run 改写，本报告不对其作任何通过/失败表述。

## 总体结果

- 结果：**passed**（`blocked > failed > passed` 聚合；`blockingReasons` 为空，本次无 failed、无 blocked）。
- 4 条执行场景全部 passed；**本次无已确认产品 Bug**，`confirmed_bugs` 为空。
- 来源区分：以下逐场景结论中，「期望是否适用」「证据是否充分」的判定由 Reviewer 在 `review.md` 独立作出（Reviewer 实际读取了 50 条 `operation-*.json`、10 份页面快照、5 份 console 与 3 张截图）；本报告只做结果聚合与口径核对，不重做证据审核。计划中的范围限定与覆盖缺口来自 `plan.md`，归计划作者。

## 逐场景结果

### AUTH-LOGIN-001「正确凭据登录建立会话并返回用户信息」— passed

- 适用期望均有直接观察支持（Reviewer 判断）：注册返回 201 且 `setCookieNames=["sid"]`（operation-5）；全新无 Cookie 客户端 `POST /api/auth/login` 返回 201（2xx）并设置 `sid`（operation-7）；同客户端 `GET /api/auth/status` 返回 200、`authenticated=true`，`user.email`/`user.displayName` 与注册响应逐字一致（operation-8）。
- 观察补充（非缺陷）：响应中邮箱为小写形式，注册响应亦为小写，属大小写归一；请求体未留存，无法比对提交时大小写，故不判为不一致（Reviewer 记录）。
- 记录层限制：注册与登录两次响应的相互一致可比对，但“提交值”本身在记录中脱敏（填表值为 `[REDACTED]`）；该限制不改变期望成立。

### AUTH-SESSION-001「会话状态随 Cookie 正确反映并刷新后保持登录」— passed

- 步骤 1 冷态：全新 clientId 无任何 Cookie 读取 `GET /api/auth/status` 返回 200 `authenticated=false`（operation-11），未被“退出后读取”或换页面替代。
- 步骤 2 页面注册：真实浏览器导航 `GET /`（operation-12，快照显示三字段表单）→ 填表（operation-15）→ 点击「注册」（operation-17）→ 状态区显示中文欢迎语（operation-18）→ 浏览器读 `GET /api/auth/status` 得 `authenticated=true` 且 `email` 为本次 Run 前缀 session 账号（operation-20/21）。
- 步骤 3 刷新：重新加载 `GET /`（operation-22）后再读 `GET /api/auth/status`，仍 `authenticated=true` 且 `email` 与步骤 2 逐字相同（operation-23/24）。
- 截图 `AUTH-SESSION-001-after-register.png` 实际显示 `你好，luowang-01M3ZWVEN052DCF6X31TXGB14Y-session。`，与所注册账号昵称一致。
- 限制：两次状态读取的 `displayName` 均为 `[REDACTED]`，无法逐字比对；“用户信息不变”主要由 `email` 逐字相同支撑，未见反证（Reviewer 记录，属脱敏边界，不影响期望成立）。

### AUTH-REGISTRATION-001「注册成功后页面显示中文欢迎语并保持登录」— passed

- 步骤 1：`GET /` 快照确认昵称/邮箱/密码三字段与「注册」按钮可见（operation-28）。
- 步骤 3 `#message` 实际文本：快照状态区为 `你好，[REDACTED]。`（operation-31）；截图 `AUTH-REGISTRATION-001-welcome.png` 实际显示完整文本 **`你好，luowang-01M3ZWVEN052DCF6X31TXGB14Y-welcome。`**，与场景约定的 `你好，<昵称>。` 模板及本次提交昵称逐字一致 —— “逐字中文模板”由截图直接确认，未被弱化为近似或等价表述。
- 步骤 4：浏览器 `GET /api/auth/status` 返回 `authenticated=true` 且 `email` 为本次 Run 前缀 welcome 账号（operation-33/34），保持登录；会话 Cookie `sid` 由 `browser_cookie_list` 观察到（domain 为被测主机、path=/，值不复述，operation-42）。
- 限制（Reviewer 如实记录，不改变结论）：页面提交的注册 POST 无直接 2xx 回执（浏览器网络缓冲已不含该请求，operation-40/41 仅见后续静态请求）；“注册成功并设置 `sid`”由欢迎语成功路径、`status` 显示已登录为该账号、`sid` Cookie 存在、同端点 API 注册返回 201/`setCookieNames=["sid"]`（operation-5/46）及存储聚合计数由 1→4（operation-6 与 operation-48）组合支持。`#message` 的 DOM id 未在可访问性快照中直接呈现，观察对象为承载该文本的 `status` 区域。
- 偏差：Runner 曾用 `navigate_back`（operation-36）后页面呈缓存、状态区为空（operation-39），已在 `execution.md` 如实标注为偏差且不影响步骤 3/4 记录；审核核对属实（步骤 3 与步骤 4 的记录均在提交后即时取得）。

### DATA-STORAGE-001「注册后密码仅以 Argon2id 哈希持久化」— passed（含残余覆盖限制）

- 步骤 1：`POST /api/auth/register` 用 Run 前缀邮箱注册，返回 201、`setCookieNames=["sid"]`（operation-46）。
- 步骤 2 观察：受控存储观察返回本 Run 聚合 `accounts=4, argon2id=4, other=0`（operation-48、operation-49 两次一致）；早期同源观察为 `accounts=1, argon2id=1, other=0`（operation-6），与该时刻仅 1 个 Run 账号相符，说明该口径按 Run 前缀逐条统计真实注册。
- 期望 1「`accounts == argon2id` 且 `other == 0`」：4 == 4、other = 0，直接观察支持。
- 期望 2「仅保存 Argon2id 哈希、不出现明文」：由聚合分类支持 —— 全部 4 个 Run 账号的持久化口令均被归入 `argon2id`，`other` 为 0。
- 残余限制（如实保留，未据以弱化期望）：受部署级 Token 保护的 `GET /api/luowang/test-data/<runId>/storage` 由本 Run 直接调用返回 **401 UNAUTHORIZED**（operation-47），Runner 未持有该 Token；计划已把“只读持久层逐条观察 `users.password_hash` 前缀”写为**条件式子项**，该子项未取得，因此 `$argon2id$` 前缀的字符串级观察缺失。审核据此判定：场景期望的实质（仅 Argon2id 持久化、无明文）已由权威聚合口径闭环，本项 passed，并保留该缺口说明。
- 口令长度 ≥12 字符在记录中不可逐字核验（值脱敏），仅由注册成功（201）及截图密码掩码宽度间接支持。

## 计数口径核对

- 执行场景数：4（`passed` 4 / `failed` 0 / `blocked` 0），与 `plan.md` 的 `## execution_scenarios` 完整且有序一致，与审核逐场景明细一致。
- 已确认产品 Bug 数：0。因此无需为 Bug 发起 `query_issue_candidates`，也不存在需 `create` 或 `link` 的 Bug 候选，`issue_action` 不适用。
- 未验证项：不计入场景结果分类，单列于下方「覆盖缺口与未完成项」；同一项不在互斥分类中重复计入。
- 摘要与明细核对：计划声明的 4 条场景、审核的 4 条 passed 明细与本报告表头 `scenario_results` 三者一致，未发现矛盾，未据计数需要增删事实。

## 覆盖缺口与未完成项

1. 页面注册的 HTTP 2xx 与 `Set-Cookie` 无直接回执（浏览器网络缓冲不完整），由组合证据支持。
2. `displayName` 逐字比对受记录脱敏限制（影响 AUTH-LOGIN-001、AUTH-SESSION-001、AUTH-REGISTRATION-001）；其中 AUTH-REGISTRATION-001 由截图补足，其余以 `email` 逐字一致支撑。
3. DATA-STORAGE-001 的 `$argon2id$` 前缀字符串级观察缺失（Token 端点 401、未获只读持久层访问），属计划已声明的条件式子项缺口。
4. 无 `baseCommit`、无 `includedCommits`，无法给出 diff 变化分析；不影响本批固定提交回归结论，但不能据此判断 target 变更内容。
5. 计划阶段 `app.py` 读取即受脱敏（`redacted=true`），凭据/Token/Cookie 生成行为未见明文；期望来源以场景正文与规格/PROJECT 回执为准。
6. 计划记录 `query_run_history` 对本项目相关场景返回 `empty`，属有限查询结果，不等于全库无历史；历史 Issue #4（注册欢迎语问题）状态 closed，本 Run 按场景既定期望执行，不据历史状态声称「已修复」。

## 记录与归属问题（不影响产品结果）

以下由 Reviewer 在一致性核对中记录，归 Reviewer；本报告照录，不改写为 Runner 的交付：

- `operation-6`（辅助存储读取）缺少 `scenarioId`/`at` 归属字段，仅可用于佐证。
- `operation-35` 的 `browser_find` 以 `isError=true` 结束；`operation-40` 的网络请求缓冲已不含页面注册 POST。
- Runner 未在 `execution.md` 提及 `operation-35/40/41` 等失败/受限的辅助操作；审核判断这不影响其引用证据成立。
- 审核对测试数据收尾的表述保持不变：已登记的 Run 前缀账号（login / session / welcome / storage 四条数据路径，共 4 个账号，与聚合计数相符）未在本 Run 清理，Runner 未声明清理完成。

## 证据与操作归属

- 证据文件（3 张截图 + 10 份页面快照 + 5 份 console + 50 条 `operation-*.json`）由本次 Run 上下文提供，审核已实际读取截图画面、页面快照与 operation 明细；`browserRequired=true` 与真实浏览器执行相符（存在 playwright 导航、快照、填表、点击、Cookie 列表操作，截图确为真实页面状态）。
- 审核记录：Runner 执行阶段无源码读取回执（空），未在执行阶段重读场景源文件，属已知情况，不构成本批阻塞。
- 本 Run 的证据仅出现脱敏记录，未见明文口令；这是对已返回脱敏文本的观察，审核未执行额外扫描，**不构成“不存在任何明文口令”的绝对结论**，本报告不作此声明。
- 时间口径：本报告 `started_at` / `finished_at` 逐字取自本次动态 Run 上下文；证据文件名中的时间戳为 Harness 记录时间，未与页面日志事件时间建立共同时钟基准，故不据此换算或声称任何绝对事件时间。本次无人工复核记录，`review.md` 的判定来自 Reviewer 模型角色，不代表人工已确认。

## 结论与后续

- 本次授权范围内的 4 条 approved 核心场景（登录后会话状态、一条注册产生的独立合成数据路径）已执行并全部 passed；未发现与场景既定期望冲突的产品行为，无已确认产品 Bug，因此本 Run 不作 Issue create/link 决策（无可提 Issue 的候选）。
- 上述覆盖缺口为记录脱敏、证据链完整性与部署级 Token 能力边界所致，**不改变已成立的测试结论**；若需闭合 DATA-STORAGE-001 的 `$argon2id$` 字符串级观察或 AUTH-REGISTRATION-001 的注册请求 2xx 直接回执，需另行确认部署级 Token 或只读持久层访问能力与网络捕获配置，属本次授权范围之外，须重新确认后再执行。
- 测试数据清理由 Harness 在本 Session 结束后统一按 Run 作用域处理，本报告不声称清理已完成。

<!-- luowang-screenshot-inspection -->
## 截图采集标签

- [截图 1](</api/evidence/bHVvd2FuZy9jeW5vcy13ZWJzaXRlL3J1bi1yZWxpYWJpbGl0eS1jb3JyZWN0aW9uLTIwMjYxMDAzL3Byb2plY3RzL2RhZjA3MDI1LTZiMDgtNDMzMC05NWY0LWZkZTU5YjA0OTM1My9ydW5zLzAxTTNaV1ZFTjA1MkRDRjZYMzFUWEdCMTRZL0FVVEgtUkVHSVNUUkFUSU9OLTAwMS1zdGF0dXMucG5n>)：页面含可见表单值；检测范围为页面，不代表图片整体安全或人工审核通过。
- [截图 2](</api/evidence/bHVvd2FuZy9jeW5vcy13ZWJzaXRlL3J1bi1yZWxpYWJpbGl0eS1jb3JyZWN0aW9uLTIwMjYxMDAzL3Byb2plY3RzL2RhZjA3MDI1LTZiMDgtNDMzMC05NWY0LWZkZTU5YjA0OTM1My9ydW5zLzAxTTNaV1ZFTjA1MkRDRjZYMzFUWEdCMTRZL0FVVEgtUkVHSVNUUkFUSU9OLTAwMS13ZWxjb21lLnBuZw>)：页面含可见表单值；检测范围为页面，不代表图片整体安全或人工审核通过。
- [截图 3](</api/evidence/bHVvd2FuZy9jeW5vcy13ZWJzaXRlL3J1bi1yZWxpYWJpbGl0eS1jb3JyZWN0aW9uLTIwMjYxMDAzL3Byb2plY3RzL2RhZjA3MDI1LTZiMDgtNDMzMC05NWY0LWZkZTU5YjA0OTM1My9ydW5zLzAxTTNaV1ZFTjA1MkRDRjZYMzFUWEdCMTRZL0FVVEgtU0VTU0lPTi0wMDEtYWZ0ZXItcmVnaXN0ZXIucG5n>)：页面含可见表单值；检测范围为页面，不代表图片整体安全或人工审核通过。
<!-- /luowang-screenshot-inspection -->

## Harness 清理收尾

测试数据清理未完成，需要处理；不改变本次功能验证结果。

有 4 项测试数据未通过清理适配器核验

仍有 4 项测试数据未确认清理

待处理：luowang-01M3ZWVEN052DCF6X31TXGB14Y-login（rejected：清理适配器执行或独立查询失败）

待处理：luowang-01M3ZWVEN052DCF6X31TXGB14Y-session（rejected：清理适配器执行或独立查询失败）

待处理：luowang-01M3ZWVEN052DCF6X31TXGB14Y-storage（rejected：清理适配器执行或独立查询失败）

待处理：luowang-01M3ZWVEN052DCF6X31TXGB14Y-welcome（rejected：清理适配器执行或独立查询失败）
