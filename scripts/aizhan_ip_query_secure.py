#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
爱站网 IP 信息查询技能

安全版本 - 只支持带Cookie的查询，保护用户隐私
"""

import re
import time
import os
import json
import requests
from bs4 import BeautifulSoup
from typing import Dict, Optional, List, Any

def load_config() -> Dict[str, str]:
    """加载配置文件"""
    config = {}
    config_path = os.path.join(os.path.dirname(__file__), "..", "config", "config.env")
    
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    if '=' in line:
                        key, value = line.split('=', 1)
                        config[key.strip()] = value.strip()
    except Exception:
        pass
    
    return config

def parse_aizhan_response(html_content: str, ip: str) -> Dict[str, Any]:
    """解析爱站网 HTML 响应"""
    result = {
        "ip": "查询失败",
        "domain_count": "查询失败", 
        "location": "查询失败",
        "domains": [],
    }

    try:
        soup = BeautifulSoup(html_content, "html.parser")
        dns_infos = soup.find("div", class_="dns-infos")
        if not dns_infos:
            raise ValueError("爱站查询缺乏固定内容，查询失败")

        # 解析IP地址
        ip_strong = dns_infos.find("strong", class_="red")
        if ip_strong:
            result["ip"] = ip_strong.get_text(strip=True)

        # 解析归属地和运营商
        strong_tags = dns_infos.find_all("strong")
        if len(strong_tags) >= 2:
            location_info = strong_tags[1].get_text(strip=True)
            result["location"] = location_info

        # 解析域名解析数量
        domain_count_span = dns_infos.find("span", class_="red")
        if domain_count_span:
            result["domain_count"] = domain_count_span.get_text(strip=True)

        # 提取绑定域名
        domain_list = []
        domain_containers = [
            soup.find("div", class_="dns-list"),
            soup.find("div", class_="domain-list"),
            soup.find("div", class_="site-list"),
            soup.find("div", class_="dns-content"),
            soup.find("table"),
            soup.find("tbody")
        ]
        
        found_domains = False
        for container in domain_containers:
            if container:
                rows = container.find_all(['tr', 'div'])
                for row in rows:
                    domain_links = row.find_all('a', href=True)
                    for link in domain_links:
                        domain = link.get_text(strip=True)
                        if domain and '.' in domain and len(domain) > 3:
                            desc = row.get_text(strip=True).replace(domain, '').strip()
                            domain_list.append({"domain": domain, "title": desc})
                            found_domains = True
                
                if found_domains:
                    break
        
        result["domains"] = domain_list[:20]
        result["source"] = "爱站"

    except Exception as e:
        return {
            "ip": ip,
            "error": f"解析失败: {str(e)}",
            "source": "爱站"
        }

    return result

def aizhan_ip_query(
    ip: str, cookie: str, delay: int = 2
) -> Dict[str, Any]:
    """爱站网 IP 信息查询（必须使用Cookie）"""
    delay = max(1, int(delay))
    time.sleep(delay)

    try:
        url = f"https://dns.aizhan.com/{ip}/"
        headers = {
            "Host": "dns.aizhan.com",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Encoding": "identity",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.87 Safari/537.36 SE 2.X MetaSr 1.0",
        }
        
        if cookie:
            headers["Cookie"] = cookie

        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()

        result = parse_aizhan_response(response.text, ip)
        result.update({"source": "爱站"})

        return result

    except requests.exceptions.RequestException as e:
        error_msg = str(e)
        if "网络" in error_msg or "连接" in error_msg or "timeout" in error_msg.lower():
            return {
                "ip": ip,
                "error": f"网络中断: {error_msg}",
                "source": "爱站"
            }
        elif "403" in error_msg or "429" in error_msg or "forbidden" in error_msg.lower():
            return {
                "ip": ip,
                "error": f"爱站网禁止请求: {error_msg}",
                "source": "爱站"
            }
        else:
            return {
                "ip": ip,
                "error": f"IP查询失败: {error_msg}",
                "source": "爱站"
            }

def get_cookie_from_config() -> str:
    """从配置文件获取Cookie"""
    config = load_config()
    cookie = config.get("AIZHAN_COOKIE", "")
    
    if not cookie:
        raise ValueError("未配置爱站网Cookie，请编辑config/config.env文件设置AIZHAN_COOKIE")
    
    return cookie

def query_ip(ip: str, delay: int = 2, cookie: str = None) -> Dict[str, Any]:
    """
    查询IP信息（必须使用Cookie）
    
    Args:
        ip: 目标IP地址
        delay: 查询延时时间（秒），默认2秒
        cookie: 爱站网Cookie，如果为None则从配置文件读取
    
    Returns:
        Dict: 查询结果
    """
    # 验证IP格式
    try:
        ipv4_pattern = r"^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$"
        if not re.match(ipv4_pattern, ip):
            raise ValueError("IP格式无效")
    except Exception as e:
        return {
            "ip": ip,
            "error": f"参数错误: {str(e)}",
            "source": "爱站"
        }
    
    # 获取Cookie
    if not cookie:
        try:
            cookie = get_cookie_from_config()
        except Exception as e:
            return {
                "ip": ip,
                "error": str(e),
                "source": "爱站"
            }
    
    # 执行查询
    result = aizhan_ip_query(ip=ip, cookie=cookie, delay=delay)
    return result

def main(ip: str, cookie: str = None, delay: int = 2) -> Dict[str, Any]:
    """主入口"""
    return query_ip(ip, delay, cookie)

def quick_query(ip: str, delay: int = 2) -> Dict[str, Any]:
    """快速查询函数（已弃用，请使用query_ip）"""
    return query_ip(ip, delay, None)

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="爱站网 IP 信息查询（安全版）")
    parser.add_argument("ip", help="目标IP地址")
    parser.add_argument("--cookie", help="爱站网Cookie（可选，默认从配置文件读取）")
    parser.add_argument("--delay", type=int, default=2, help="查询延时时间（秒），默认2秒")
    
    args = parser.parse_args()
    result = main(args.ip, args.cookie, args.delay)
    
    print(json.dumps(result, ensure_ascii=False, indent=2))