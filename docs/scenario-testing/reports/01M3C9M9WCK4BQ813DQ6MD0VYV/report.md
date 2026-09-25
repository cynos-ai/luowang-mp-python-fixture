---
run_id: 01M3C9M9WCK4BQ813DQ6MD0VYV
trigger: manual
base_commit: 6d3f87c2f36544eddcf1b78569a454be5cb644c0
target_commit: 749c308754d8ede852ed008475e1457a5b781669
included_commits: []
result: passed
started_at: 2026-09-25T12:48:21.461Z
finished_at: 2026-09-25T12:50:26.004Z
scenario_results:
  - id: CLEANUP-SEED-001
    result: passed
confirmed_bugs: []
---

# 最终报告 — CLEANUP-SEED-001 复测（Run `01M3C9M9WCK4BQ813DQ6MD0VYV`）

本报告依据本 Run 的 `plan.md`（planHash `d8de7edf39ccaefabecad0e0e14c13f1c111bc35849aed3008c0211f77032ef5`）与 Reviewer 的 `review.md` 独立审核整理，不重做证据审核。本 Run 无人工复核，不声称人工已确认。

## 1. 本次范围与固定条件

- 人工请求：只复测 approved 场景 `CLEANUP-SEED-001`；Runner 使用新增的 `verify_run_cleanup_scope` 观察跨 Run 清理作用域，并用预置账号独立登录；账号只用非生产合成数据。
- base `6d3f87c2`、target `749c3087`，`includedCommits` 为空，trigger `manual`，`scenarioMode=review-all`，`scenarioChanges=null`（无 scenario patch，本批不新增/不修改/不废弃场景）。
- 执行集（计划唯一 `## execution_scenarios`）仅 `CLEANUP-SEED-001`；结果与清单完整且有序一致。
- 计划说明 base→target 仅新增 4 份文档工件，产品代码与场景资产无变化，故本批不是代码变更回归，而是「受控观察能力增强后的重新验证」。计划明确不据 diff 推断产品行为改变，旧 Run 结论责任保留在原 Run。
- 冻结场景两条适用期望：**A** 预置账号在本 Run 清理后仍能登录成功；**B** 另一个 Run ID 的余量在清理前后保持一致，未被本 Run 清理改动。

## 2. 逐场景结果

| 场景 | 结果 | 依据 |
| --- | --- | --- |
| CLEANUP-SEED-001 | passed | Reviewer 独立核对 operation 原始证据后认定期望 A、B 均有实际观察支持 |

**Reviewer 交付的判定依据（来源：review.md，归 Reviewer）**

期望 A（支持充分）：`operation-8.json` 中独立 clientId（与注册 clientId 不同）的 `POST /api/auth/login` 返回 201 并回显预置身份、下发 `sid`；`operation-9.json` 同一客户端 `GET /api/auth/status` 返回 200 `authenticated:true`。清理聚合记录时间（12:49:12.583Z）早于登录时间（12:49:15.014Z），可确认登录发生在本次清理之后。邮箱值被 Harness 脱敏不可读，但不影响「清理后预置账号登录成功并建立会话」成立。

期望 B（支持充分）：`operation-7.json`（source `controlled-run-cleanup-scope`）中 `currentRunId=01M3C9M9WCK4BQ813DQ6MD0VYV`、`controlRunId=018T5PNKRHVSPV34G9CY329YRB`，逐 Run 读数 `before={current:1, control:1}` → `after={current:0, control:1}`；对照 Run ID 为 26 位、仅含 Crockford 许可字符、与当前 Run 互不构成前缀包含；对照读数非零且有区分力，`before.control` 与 `after.control` 相等，与本 Run 在同一记录内 1→0 形成有效对照。Reviewer 明确未采用该记录自带的 `passed:true` 字段，判定仅基于可读数值。

前置事实（期望 A/B 共同前提）：`operation-6.json` 中本 Run 前缀合成账号 `POST /api/auth/register` 返回 201，证明本 Run 账号确实创建；`operation-3.json` 无凭据 `GET /api/luowang/test-data/<本 Run>` 返回 401，Reviewer 定性为受控探针而非缺陷。外层 `operation-1/2` 为开始执行、`operation-10` 为 `finish_scenario`（`completed=["CLEANUP-SEED-001"]`）。

期望适用性判断与范围解释归 Reviewer；本报告不改变其结论。

## 3. 已确认产品问题

**无。** Reviewer 独立审核认定期望 A、B 均未被实际观察违反，也未发现与冻结场景/spec 直接冲突的产品行为，因此本批没有 confirmed Bug 候选。

由于本批零 confirmed Bug，未产生任何需要查询相似 Issue 的 Bug key，故不涉及 Issue create/link 决策，也不需要「Issue 查询覆盖缺口」章节；这不代表对产品其他部分的断言。

## 4. 报告与证据的偏差（转述 Reviewer 记录，归 Reviewer 观察）

1. **Runner 的读数口径说明自相矛盾**：execution.md 将 `currentCleanup=0`/`controlCleanup=0` 解释为「删除计数（deleted）」，但若如此则本 Run 账号未被删除、`after.current` 应为 1，与记录中的 0 冲突；Reviewer 认为更自洽的解释是二者为清理后余量（remaining），未采信 Runner 的解释，仅采用可读数值。无论取何种解释，期望 B 依赖的 `before/after.control` 读数不变，结论不变。该口径表述归 Runner，如需保留应修正或标注为待确认。
2. **计划预期的原始 DELETE/清理后独立 GET 记录缺失**：本 Run 的 DELETE 与其后余量读数只出现在 `operation-7.json` 的工具聚合结果中。计划「证据优先级」第 3 条明确允许「明确的聚合记录内部逐 Run 读数」，故该缺口不使期望 B 无法确认，但相对计划写明的证据形态是一处偏差。
3. **两次注册 400 未定性**：`operation-4.json`、`operation-5.json` 的 `POST /api/auth/register` 返回 400 `INVALID_ACCOUNT`，`operation-6.json` 调整字段后 201。Runner 依源码归因为「请求字段与契约不匹配」，但 `app.py` 在本 Run 为脱敏读取、spec 正文不可读，Reviewer 判定该归因属**未验证推断**；该现象不属于本场景适用期望，既不改变 A/B 判定，也不能据此认定产品缺陷。定性需另行授权核实注册契约。

## 5. 未完成事项与覆盖缺口

1. **期望 B 的证据粒度较弱**：对照 Run 的两次读数来自单次工具调用的聚合结果，对照 Run 自身无逐请求 GET/DELETE 原始记录；工具自带的 `passed=true` 不具独立证明力。判定成立的基础是计划明确授权该观察方式、记录内逐 Run 数值可读且非零具区分力、并与 `operation-6.json` 独立事实一致。若后续要求更强的逐请求证据，需新的受控能力；这不改变本次按计划口径的结论。
2. **对照仅单次随机生成，非穷举**：只回答「本 Run 清理不误删某一合法 Run」这一业务承诺，不外推到多 Run 并发或前缀边界情形。
3. **本 Run 清理后余量为 0 的复核**仅取自聚合记录 `after.current=0`，无独立 GET 原始记录（同第 1 条）。
4. **范围外未覆盖**：其余 approved 场景沿用历史记录，本批不重跑、不改判；历史 Run `01M3C0QRAV0Q3P6QYCBBBX4GX4` 的 passed 与 `01M3C8SY94SMQPT6AY19J1XSS1` 的 blocked 结论保留在原 Run，本批不改写。draft `CLEANUP-CONFIG-001` 不在执行集，spec 第 4 条「清理接口默认关闭 / 短 Token 拒绝启用」本批无运行覆盖，属已知缺口而非豁免。
5. **`inspect_test_account_storage` 观察不可用**（Runner 所述，无对应 operation 记录可核）；`app.py` 与 spec 正文脱敏/不可读，使计划中的实现与契约引用无法在本轮独立验证——Reviewer 认定这些均不影响 A/B 的实际行为判定。
6. **脱敏与扫描边界**：记录未复述预置账号口令、清理 Token 或 Cookie 值，与计划一致；本 Run 未执行系统性 Secret 扫描，故不作「不存在任何密码文本」类绝对声明。
7. **测试数据收尾**：本 Run 前缀账号与对照 Run 账号的清理由 Harness 在 Session 结束后统一处理，本报告不提前声称已完成，其成败不改已成立的场景结论。

## 6. 结论与下一步

- `CLEANUP-SEED-001`：**passed**（期望 A、B 均有可读的实际观察支持，判定归 Reviewer 独立审核）。
- 本 Run `blockingReasons` 为空，无失败场景，聚合结果为 `passed`。
- 已确认产品 Bug：无，本批无 Issue 归档动作。
- 需下游注意（保持可见，未闭合）：Runner 读数的 deleted/remaining 口径说明与记录不一致；本 Run 清理仅存于聚合记录，无独立 DELETE 原始证据；两次注册 400 的契约归因未经验证，如需定性须另行授权。
- 本次通过仅覆盖 `CLEANUP-SEED-001` 的两条期望与上述证据范围，不代表项目其他场景或范围外能力无问题。若需更强证据粒度（逐请求清理记录）或注册契约定性，需新的受控能力或另行确认的授权。

## Harness 清理收尾

测试数据清理完成；不改变本次功能验证结果。

清理适配器已独立核验 1 项测试数据不存在

全部登记测试数据均已独立核验清理

独立核验：luowang-01M3C9M9WCK4BQ813DQ6MD0VYV-a1 · run-scoped-http-cleanup · 2026-09-25T12:50:40.888Z · absent=true · sha256 6621efb4f177dcf615cbb31598923cdb0e69690d0e59f7c222117c8736d597a2
