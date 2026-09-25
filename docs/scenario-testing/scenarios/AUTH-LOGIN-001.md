---
id: AUTH-LOGIN-001
name: 正确凭据登录建立会话并返回用户信息
description: 验证登录核对口令成功后建立会话并返回一致用户信息
status: approved
tags:
  - core
---

## 目的

使用正确的邮箱与口令登录时建立新会话，并返回与该账号一致的用户信息。

## 前置条件

- 非生产环境，仅使用合成数据。
- 已有可登录账号：本场景用当前 Run 前缀 `luowang-<runId>-` 注册创建，或使用环境预置账号。
- 具备可发出 JSON 登录请求的受控能力。

## 步骤

1. 准备一个账号并确认其注册邮箱与口令。
2. 调用 `POST /api/auth/login`，提交正确邮箱与口令。
3. 观察响应与会话 Cookie，并读取 `GET /api/auth/status`。

## 期望

- 登录请求成功（2xx），并设置会话 Cookie（`sid`）。
- `GET /api/auth/status` 返回 `authenticated` 为 true，且 `user.email` 与 `user.displayName` 与所登录账号一致。

## 需要记录

- 登录响应状态与会话 Cookie 设置情况。
- `GET /api/auth/status` 响应内容。
- Run 标记账号的登记、清理与清理后核验。
