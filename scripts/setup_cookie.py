#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
爱站网Cookie设置向导
帮助用户安全配置爱站网Cookie
"""

import os
import sys
import webbrowser
import time
from typing import Optional

def create_config():
    """创建配置文件"""
    config_path = os.path.join(os.path.dirname(__file__), "..", "config", "config.env")
    os.makedirs(os.path.dirname(config_path), exist_ok=True)
    
    # 检查是否已存在配置
    if os.path.exists(config_path):
        print("⚠️  配置文件已存在")
        choice = input("是否覆盖现有配置？(y/N): ").strip().lower()
        if choice != 'y':
            print("取消操作")
            return
    
    print("\n🔧 爱站网Cookie设置向导")
    print("=" * 40)
    
    # 步骤1：打开爱站网
    print("\n步骤1: 打开爱站网")
    print("- 请在浏览器中访问: https://dns.aizhan.com")
    print("- 登录您的账号或正常浏览页面")
    print("- 完成后按 Enter 继续")
    
    input("\n按 Enter 继续...")
    
    # 步骤2：获取Cookie
    print("\n步骤2: 获取Cookie")
    print("- 按F12打开开发者工具")
    print("- 切换到 Network (网络) 标签页")
    print("- 刷新页面或任意点击页面")
    print("- 点击任意请求")
    print("- 在 Headers 标签页找到 'Cookie' 字段")
    print("- 复制完整的Cookie值")
    
    print("\n📋 Cookie示例:")
    print("PHPSESSID=xxx; userId=1234; userName=test%40aizhan.com; userSecure=xxx")
    
    cookie = input("\n请输入您的爱站网Cookie: ").strip()
    
    if not cookie:
        print("❌ Cookie不能为空")
        return
    
    # 步骤3：验证Cookie
    print("\n步骤3: 验证Cookie有效性")
    print("- 正在测试Cookie...")
    
    # 导入查询模块测试
    try:
        sys.path.append(os.path.dirname(__file__))
        from aizhan_ip_query_secure import query_ip
        
        # 使用一个简单IP测试
        test_result = query_ip("1.1.1.1", delay=1, cookie=cookie)
        
        if "error" in test_result:
            print(f"❌ Cookie验证失败: {test_result['error']}")
            return
        else:
            print("✅ Cookie验证成功！")
            print(f"   IP: {test_result['ip']}")
            print(f"   位置: {test_result['location']}")
            print(f"   域名数: {test_result.get('domain_count', 'N/A')}")
    
    except Exception as e:
        print(f"❌ 验证过程出错: {e}")
        return
    
    # 步骤4：保存配置
    print("\n步骤4: 保存配置")
    
    config_content = f"""# 爱站网配置文件
# 格式：KEY=VALUE
# 示例：AIZHAN_COOKIE=PHPSESSID=xxx; userToken=xxx

# 爱站网Cookie（必填）
# 获取方式：打开dns.aizhan.com → 登录/浏览 → 浏览器开发者工具 → Network → 复制Cookie
AIZHAN_COOKIE={cookie}
"""
    
    try:
        with open(config_path, 'w', encoding='utf-8') as f:
            f.write(config_content)
        
        print("✅ 配置文件保存成功!")
        print(f"📍 配置位置: {config_path}")
        
        # 步骤5：使用说明
        print("\n📖 使用说明:")
        print("1. 现在可以直接使用查询命令:")
        print("   python3 scripts/aizhan_ip_query_secure.py 8.8.8.8")
        print("2. 或者使用指定Cookie:")
        print("   python3 scripts/aizhan_ip_query_secure.py 8.8.8.8 --cookie 'your_cookie'")
        print("3. Cookie将自动从配置文件读取")
        
    except Exception as e:
        print(f"❌ 保存配置失败: {e}")

def show_config():
    """显示当前配置"""
    config_path = os.path.join(os.path.dirname(__file__), "..", "config", "config.env")
    
    if not os.path.exists(config_path):
        print("❌ 配置文件不存在")
        return
    
    print("\n📋 当前配置:")
    print("=" * 40)
    
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip() and not line.startswith('#'):
                    if '=' in line:
                        key, value = line.split('=', 1)
                        if key.strip() == 'AIZHAN_COOKIE':
                            # 隐藏敏感信息
                            cookie = value.strip()
                            if len(cookie) > 20:
                                masked = cookie[:10] + '*' * (len(cookie) - 20) + cookie[-10:]
                            else:
                                masked = '*' * len(cookie)
                            print(f"{key.strip()}=已设置 ({len(cookie)} 字符)")
                        else:
                            print(f"{key.strip()}={value.strip()}")
                    else:
                        print(line.strip())
    except Exception as e:
        print(f"❌ 读取配置失败: {e}")

def reset_config():
    """重置配置"""
    config_path = os.path.join(os.path.dirname(__file__), "..", "config", "config.env")
    
    if not os.path.exists(config_path):
        print("❌ 配置文件不存在")
        return
    
    choice = input("确定要删除配置文件吗？(y/N): ").strip().lower()
    if choice == 'y':
        try:
            os.remove(config_path)
            print("✅ 配置文件已删除")
        except Exception as e:
            print(f"❌ 删除失败: {e}")
    else:
        print("取消操作")

def main():
    """主菜单"""
    while True:
        print("\n🔧 爱站网Cookie管理")
        print("=" * 40)
        print("1. 设置Cookie")
        print("2. 查看配置")
        print("3. 重置配置")
        print("4. 退出")
        
        choice = input("\n请选择操作 (1-4): ").strip()
        
        if choice == '1':
            create_config()
        elif choice == '2':
            show_config()
        elif choice == '3':
            reset_config()
        elif choice == '4':
            break
        else:
            print("❌ 无效选择，请重新输入")

if __name__ == "__main__":
    main()