---
id: CLEANUP-SCOPE-001
name: 有效 Token 按完整 Run 前缀清理并提供独立余量
description: 验证清理只作用于完整 Run 前缀账号、独立 GET 返回余量且拒绝非法 Run ID
status: approved
tags:
  - core
---

## 目的

持有效部署级 Token 时，清理端点只删除以完整 `luowang-<runId>-` 前缀标识的账号及其级联会话，独立 GET 返回余量，非法 Run ID 与越界参数不产生删除。

## 前置条件

- 非生产环境，仅使用合成数据；存在若干以当前 Run 前缀注册的账号（本 Run 标记）。
- 具备部署级 Token（至少 32 字符），其值不在记录中复述。

## 步骤

1. 带有效 Token `GET /api/luowang/test-data/<runId>` 读取清理前余量。
2. 带有效 Token `DELETE /api/luowang/test-data/<runId>`，记录删除数。
3. 独立 `GET /api/luowang/test-data/<runId>` 复核余量。
4. 带有效 Token 请求非法 Run ID（不符合 26 位格式）的 `DELETE` 与 `GET`。
5. 用被清理账号的原凭据尝试登录。

## 期望

- 删除后独立 GET 返回余量为 0，且删除数与本 Run 前缀账号数一致。
- 非法 Run ID 请求被拒绝（非 2xx），不删除任何账号。
- 被清理账号的会话及原凭据失效，原凭据无法再登录。
- 清理不接受任意用户 ID、SQL 或跨 Run 参数，删除范围仅由完整前缀决定。

## 需要记录

- 各调用的响应状态与 runId、deleted、remaining 数值。
- 非法 Run ID 请求的响应结果。
- 被清理账号原凭据的登录结果与创建登记、清理后核验。
