---
id: AUTH-SESSION-001
name: 会话状态随 Cookie 正确反映并刷新后保持登录
description: 验证未登录、注册登录后与会话保持的状态表现
status: approved
tags:
  - core
---

## 目的

会话状态按服务端会话与 `sid` Cookie 正确反映：匿名访问为未登录，注册或登录后为已登录，页面刷新后仍保持登录。

## 前置条件

- 非生产环境，仅使用合成数据；账号使用当前 Run 前缀 `luowang-<runId>-`。
- 浏览器可访问 `GET /` 与 `GET /api/auth/status`。

## 步骤

1. 在无会话 Cookie 的客户端读取 `GET /api/auth/status`。
2. 通过页面注册一个 Run 标记账号并确认已登录。
3. 重新加载 `GET /` 后再次读取 `GET /api/auth/status`。

## 期望

- 步骤 1 返回 `authenticated` 为 false。
- 步骤 2 后返回 `authenticated` 为 true，并包含与所注册账号一致的用户信息。
- 步骤 3 刷新后仍为 `authenticated` 为 true，且用户信息不变。

## 需要记录

- 三次会话状态读取的响应内容与所处客户端及 Cookie 状态。
- Run 标记账号的登记、清理与清理后核验。
