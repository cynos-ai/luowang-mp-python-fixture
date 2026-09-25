---
id: AUTH-DELETE-001
name: 删除账号后会话与旧凭据均失效
description: 验证删除自己账号后 Cookie、会话与原凭据都无法恢复登录
status: approved
tags:
  - core
---

## 目的

用户删除自己的账号后，其会话被清除，旧 Cookie 与原凭据均不能恢复登录。

## 前置条件

- 非生产环境，仅使用合成数据；账号使用当前 Run 前缀 `luowang-<runId>-`。
- 浏览器可访问带「删除账号」按钮的 `GET /`。

## 步骤

1. 通过页面注册一个 Run 标记账号，并确认当前为已登录状态。
2. 点击页面「删除账号」按钮（或调用 `DELETE /api/me`）删除当前账号。
3. 观察响应、页面反馈与会话 Cookie 状态，并读取 `GET /api/auth/status`。
4. 用原邮箱与原口令调用 `POST /api/auth/login`。
5. 再次调用 `DELETE /api/me`。

## 期望

- 删除请求成功（2xx），会话 Cookie 被清除。
- 删除后 `GET /api/auth/status` 为未登录状态。
- 原邮箱与原口令登录被拒绝（非 2xx），不能恢复登录。
- 重复删除请求被拒绝（非 2xx）。

## 需要记录

- 删除响应、页面 `#message` 文本与会话 Cookie 状态。
- 删除后的会话状态、原凭据登录尝试与重复删除的结果。
- Run 标记账号的登记、清理与清理后核验。
