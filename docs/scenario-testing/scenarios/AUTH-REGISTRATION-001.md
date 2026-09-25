---
id: AUTH-REGISTRATION-001
name: 注册成功后页面显示中文欢迎语并保持登录
description: 验证注册成功路径在页面显示中文欢迎语且会话保持登录
status: approved
tags:
  - core
---

## 目的

注册成功后，页面显示中文欢迎语 `你好，<昵称>。`，并保持登录状态。

## 前置条件

- 非生产环境，仅使用合成数据；账号昵称与邮箱使用当前 Run 前缀 `luowang-<runId>-`。
- 浏览器可访问 `GET /`，注册表单包含昵称、邮箱、密码三个字段。
- 口令长度不少于 12 字符（合成值，不在记录中复述）。

## 步骤

1. 打开 `GET /`，确认注册表单可见。
2. 填写昵称 `luowang-<runId>-welcome`、邮箱 `luowang-<runId>-welcome@example.test`、不少于 12 字符的口令，提交注册。
3. 读取页面状态区 `#message` 的实际显示文本。
4. 读取 `GET /api/auth/status` 观察当前会话。

## 期望

- 注册请求成功，并设置会话 Cookie（`sid`）。
- 页面 `#message` 显示文本为 `你好，<昵称>。`，其中 `<昵称>` 为步骤 2 提交的昵称。
- `GET /api/auth/status` 返回 `authenticated` 为 true，且 `user.displayName` 与提交昵称一致（保持登录）。

## 需要记录

- 注册响应状态、`#message` 实际文本（截图或快照）与会话 Cookie 是否设置。
- `GET /api/auth/status` 的响应内容。
- 该 Run 标记账号的登记、清理方式及清理后的核验结果。
