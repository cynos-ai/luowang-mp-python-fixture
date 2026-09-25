---
id: CLEANUP-SEED-001
name: 预置账号与其他 Run 账号免于本 Run 清理
description: 验证清理作用域不误删预置账号和其他 Run 的账号
status: approved
tags: []
---

## 目的

本 Run 的清理不删除环境预置账号，也不改变其他 Run 前缀账号的存在与余量。

## 前置条件

- 非生产环境；环境配置了预置账号（`CYNOS_TEST_ACCOUNT_EMAIL` 与口令）。
- 具备部署级 Token、可发出登录请求，并存在另一个合法 Run ID 可用于余量对照。

## 步骤

1. 记录另一个合法 Run ID 的清理余量对照值。
2. 创建本 Run 前缀账号，并带有效 Token 执行本 Run 的 `DELETE` 清理。
3. 用预置账号的邮箱与口令调用 `POST /api/auth/login`。
4. 重新读取另一个 Run ID 的余量。

## 期望

- 预置账号在本 Run 清理后仍能登录成功。
- 另一个 Run ID 的余量在清理前后保持一致，未被本 Run 清理改动。

## 需要记录

- 预置账号登录结果与另一个 Run ID 清理前后的余量数值。
- 本 Run 账号的创建登记、清理执行与清理后核验。
