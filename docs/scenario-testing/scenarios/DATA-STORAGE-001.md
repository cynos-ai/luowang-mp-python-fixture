---
id: DATA-STORAGE-001
name: 注册后密码仅以 Argon2id 哈希持久化
description: 验证真实持久层只保存 Argon2id 哈希且不含明文口令
status: approved
tags:
  - core
---

## 目的

注册成功后，账号口令在真实持久层中只以 Argon2id 哈希保存，不保存明文。

## 前置条件

- 非生产环境，仅使用合成数据；账号使用当前 Run 前缀 `luowang-<runId>-`。
- 具备受控存储观察能力：带部署级 Token 的 `GET /api/luowang/test-data/<runId>/storage`，或等价的只读持久层观察。

## 步骤

1. 用当前 Run 前缀邮箱与不少于 12 字符的口令注册一个账号。
2. 读取该 Run 的存储观察结果（`accounts`、`argon2id`、`other`）。
3. 如可获得只读持久层访问，另行观察该账号 `users.password_hash` 的前缀与是否出现明文口令。

## 期望

- 该 Run 的聚合观察显示 `accounts` 等于 `argon2id`，且 `other` 为 0。
- 持久层中保存的是 Argon2id 哈希（形如 `$argon2id$` 前缀的 PHC 字符串），不出现明文口令。

## 需要记录

- 使用的观察口径（受控端点或只读持久层）与聚合计数。
- 哈希格式特征（如 `$argon2id$` 前缀），不复述口令值与哈希全文。
- Run 标记账号的登记、清理与清理后核验。
