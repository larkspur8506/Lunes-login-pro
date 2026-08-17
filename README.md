## 🚀 lunes host 自动登录续期（GitHub Actions 多账号版）

这是一个基于 GitHub Actions 的自动化脚本，用于定时登录自动续期 [lunes host](https://lunes.host/) 应用，**现已支持多账号同时自动续期**。

⚠️ **注意**：有 CF 盾，太垃圾的机房节点可能过不了，建议用稍微干净点的节点 [B2proxy住宅代理](https://b2proxy.com/)。

━━━━━━━━━━━━━━━━━━━━━━

### 🔐 Secrets 配置说明

在 GitHub 仓库的 `Settings` -> `Secrets and variables` -> `Actions` 中添加以下变量：

| Secret 名称 | 是否必填 | 说明 |
| :--- | :---: | :--- |
| **ACCOUNT** | ✅ 必填 | lunes 账号列表，支持多账号。格式见下方说明。 |
| **NODE_LINK** | ❌ 可选 | 代理链接，如 `vless://`, `vmess://`, `tuic://`, `hysteria2://`, `socks5://` |
| **TG_BOT_TOKEN**| ❌ 可选 | Telegram Bot Token（用于发送通知） |
| **TG_CHAT_ID** | ❌ 可选 | Telegram Chat ID（接收通知的用户或群组 ID） |

#### 📝 ACCOUNT 格式说明

将你的多个账号按 `邮箱/密码` 的格式填写，**一行一个**。无论密码中是否包含其他特殊字符，都会以第一个 `/` 为界限进行解析：

```
user1@gmail.com/password123
user2@gmail.com/password
user3@outlook.com/password789
```

━━━━━━━━━━━━━━━━━━━━━━

### 代理格式（确认在v2rayN里使用正常的节点）

`NODE_LINK` 支持以下任意一种代理协议的完整分享链接（不配置则直连）：

- **VLESS**：`vless://uuid@server:port?security=reality&sni=...&type=ws&...`
- **VMess**：`vmess://base64encoded...`
- **Trojan**：`trojan://password@server:port?sni=...&type=ws&...`
- **tuic**：`tuic://uuid:password@server:port...`
- **anytls**：`anytls://uuid@server:port...`
- **hysteria2**：`hysteria2://base64@server:port...`
- **SOCKS5**：`socks5://user:pass@server:port` 或 `socks://user:pass@server:port`

### 注意事项
- 尽量添加一个干净的节点，以免过不了cf盾
