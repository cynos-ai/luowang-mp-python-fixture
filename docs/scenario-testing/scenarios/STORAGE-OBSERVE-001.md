---
id: STORAGE-OBSERVE-001
name: 存储观察端点只返回计数且拒绝非法 Run ID
description: 验证存储观察仅返回本 Run 计数、不泄露敏感字段并拒绝非法参数
status: approved
tags: []
---

## 目的

存储观察端点只返回本 Run 的账号数、Argon2id 数与其他格式数，不返回邮箱、用户 ID、口令或哈希，并拒绝非法 Run ID。

## 前置条件

- 非生产环境；具备部署级 Token（至少 32 字符）与发出请求的受控能力。
- 存在一个以当前 Run 前缀注册的账号。

## 步骤

1. 带有效 Token 请求 `GET /api/luowang/test-data/<runId>/storage`。
2. 检查响应体字段与响应头。
3. 带有效 Token 请求非法 Run ID 的同一端点。

## 期望

- 响应只包含 Run 标识与计数（账号数、Argon2id 数、其他格式数），不含邮箱、用户 ID、口令或哈希。
- 非法 Run ID 请求被拒绝（非 2xx），不返回计数。

## 需要记录

- 响应体字段清单与响应头（缓存相关头作为观察项）。
- 非法 Run ID 请求的响应结果。
- Run 标记账号的登记、清理与清理后核验。
