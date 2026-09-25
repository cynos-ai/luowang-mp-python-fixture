---
id: CLEANUP-AUTH-001
name: 清理与存储端点仅接受部署级 Token
description: 验证无 Token 或错误 Token 时清理与存储观察请求均被拒绝
status: approved
tags:
  - core
---

## 目的

清理与存储观察端点只接受部署级 Token；无 Token 或错误 Token 的请求被拒绝，且不删除账号、不返回账号计数或敏感数据。

## 前置条件

- 非生产环境，仅使用合成数据；存在一个以当前 Run 前缀注册的账号。
- 具备发出带或不带 Authorization 请求的受控能力。

## 步骤

1. 不带 Authorization 请求 `GET /api/luowang/test-data/<runId>` 与 `GET /api/luowang/test-data/<runId>/storage`。
2. 带错误 Token 请求上述两个端点。
3. 带错误 Token 调用 `DELETE /api/luowang/test-data/<runId>`。
4. 用原凭据登录该 Run 标记账号。

## 期望

- 所有无 Token 与错误 Token 请求均被拒绝（401）。
- 拒绝响应不包含账号计数、邮箱、用户 ID、口令或哈希。
- 该 Run 标记账号仍未被删除，原凭据仍能登录成功。

## 需要记录

- 各请求的响应状态与响应体字段（确认未返回计数或敏感数据）。
- 该账号在请求前后可登录性的核验结果。
- Run 标记账号的登记、清理与清理后核验。
