def main():
    print("#" * 25)
    print("   Lunes 自动登录续期 (多账号版)")
    print("#" * 25)

    global EMAIL, PASSWORD
    
    # 1. 读取换行格式的 ACCOUNT 环境变量
    accounts_str = os.environ.get("ACCOUNT", "")
    accounts = []
    
    if accounts_str:
        # 按换行符分割，逐行解析
        for line in accounts_str.strip().split('\n'):
            line = line.strip()
            # 忽略空行
            if not line:
                continue
            # 以第一个 '/' 为界分割邮箱和密码
            if '/' in line:
                e, p = line.split('/', 1)
                accounts.append({"email": e.strip(), "password": p.strip()})

    # 2. 兼容旧的单账号逻辑
    if not accounts:
        print("⚠️ 未找到多账号配置(ACCOUNT)，尝试回退到单账号模式...")
        if EMAIL and PASSWORD:
            accounts = [{"email": EMAIL, "password": PASSWORD}]
        else:
            print("❌ 未配置任何账号！请在 GitHub Secrets 中配置 ACCOUNT。")
            return

    is_proxy = os.environ.get("IS_PROXY", "false").lower() == "true"
    sb_kwargs = {"uc": True, "headless": False}
    
    if is_proxy:
        # ⚠️ 【修复点】动态读取系统环境变量中的 PROXY_SERVER，兼容不同的代理端口
        proxy_str = os.environ.get("PROXY_SERVER", "socks5://127.0.0.1:1080")
        print(f"🔗 挂载代理: {proxy_str}")
        sb_kwargs["proxy"] = proxy_str
    else:
        print("🌐 未使用代理，直连访问")

    # 3. 遍历账号依次执行
    for index, acc in enumerate(accounts):
        EMAIL = acc.get("email", "")
        PASSWORD = acc.get("password", "")

        print(f"\n" + "="*45)
        print(f"🚀 开始处理账号 [{index+1}/{len(accounts)}]: {EMAIL}")
        print("="*45)

        with SB(**sb_kwargs) as sb:
            print("✅ 浏览器已启动")
            try:
                sb.open("https://api.ip.sb/ip")
                print(f"🌐 当前出口真实 IP: {sb.get_text('body')}")
            except Exception:
                pass

            if login(sb):
                print("\n✅ 登录成功，正在处理服务器续期...")
                success, info = visit_server(sb)
                if success:
                    extra = f"服务器: {info['server_name']}\nID: {info['server_id']}"
                    send_tg_message("✅", "续期成功", extra)
                else:
                    error_msg = info.get('error', '未知错误')
                    print(f"❌ 访问服务器失败: {error_msg}")
                    extra = f"错误: {error_msg}"
                    if 'server_id' in info:
                        extra += f"\n服务器ID: {info['server_id']}"
                    send_tg_message("❌", "续期失败", extra)
            else:
                print("\n❌ 登录失败，终止该账号的后续续期操作。")
                send_tg_message("❌", "登录失败", "")
                
        # 账号之间间隔 10 秒
        time.sleep(10)
