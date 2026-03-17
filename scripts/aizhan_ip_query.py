#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
爱站网 IP 信息查询技能

该脚本用于通过爱站网查询 IP 地址的归属与历史绑定的域名信息。
"""
import re
import time
import requests
from bs4 import BeautifulSoup
from typing import Dict, Optional, List, Any

def parse_aizhan_response(html_content: str, ip: str) -> Dict[str, Any]:
    """
    解析爱站网 HTML 响应

    Args:
        html_content: HTML 响应内容
        ip: 查询的 IP 地址

    Returns:
        Dict: 解析后的 IP 信息字典
    """
    # 提取基本信息
    result = {
        "ip": "查询失败",
        "domain_count": "查询失败",
        "location": "查询失败",
        "domains": [],
    }

    try:
        # 使用 BeautifulSoup 解析 HTML
        soup = BeautifulSoup(html_content, "html.parser")

        # 检查是否存在关键部分
        dns_infos = soup.find("div", class_="dns-infos")
        if not dns_infos:
            raise ValueError("爱站查询缺乏固定内容，查询失败")

        # 解析 IP 地址
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

        # 提取绑定域名（新的页面结构）
        domain_list = []
        
        # 尝试从新的域名列表区域解析
        # 可能的域名列表容器类名：dns-list, domain-list, site-list等
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
                # 查找所有行
                rows = container.find_all(['tr', 'div'])
                for row in rows:
                    # 查找域名链接
                    domain_links = row.find_all('a', href=True)
                    for link in domain_links:
                        domain = link.get_text(strip=True)
                        if domain and '.' in domain and len(domain) > 3:
                            # 获取描述信息
                            desc = row.get_text(strip=True).replace(domain, '').strip()
                            domain_list.append({"domain": domain, "title": desc})
                            found_domains = True
                
                if found_domains:
                    break
        
        # 如果没有找到域名列表，尝试从其他地方提取
        if not found_domains and result.get("domain_count") and "暂无域名解析到该IP" not in html_content:
            # 尝试从页面中直接提取域名
            domain_candidates = []
            # 查找可能包含域名的文本
            for text in soup.get_text().split():
                if '.' in text and len(text) > 4 and text.startswith(('http', 'www', 'ftp', 'smtp')):
                    domain_candidates.append(text)
            
            # 去重并添加到列表
            seen_domains = set()
            for domain in domain_candidates[:20]:  # 限制数量
                if domain not in seen_domains:
                    seen_domains.add(domain)
                    domain_list.append({"domain": domain, "title": "从页面提取"})
                    found_domains = True
        
        result["domains"] = domain_list[:20]  # 限制最多20个域名

        # 去重
        seen_domains = set()
        unique_domains = []
        for domain_info in domain_list:
            domain = domain_info["domain"]
            if domain not in seen_domains:
                seen_domains.add(domain)
                unique_domains.append(domain_info)

        result["domains"] = unique_domains[:20]  # 限制最多20个域名

    except Exception as e:
        # 捕获所有异常
        return {
            "ip": ip,
            "error": f"解析失败: {str(e)}",
        }

    return result


def aizhan_ip_query(
    ip: str, cookie: str, delay: int = 2
) -> Dict[str, Any]:
    """
    爱站网 IP 信息查询

    Args:
        ip: 目标 IP 地址
        cookie: 爱站网 Cookie，默认从变量读取
        delay: 查询延时时间（秒），默认2秒

    Returns:
        Dict: 查询结果
    """
    # 确保 delay 是正整数，最小为1
    delay = max(1, int(delay))

    # 添加延时
    time.sleep(delay)

    try:
        # 构造 HTTP 请求
        url = f"https://dns.aizhan.com/{ip}/"
        # 构造 headers
        headers = {
            "Host": "dns.aizhan.com",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Encoding": "identity",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.87 Safari/537.36 SE 2.X MetaSr 1.0",
        }
        
        # 如果提供了cookie，添加到headers中
        if cookie:
            headers["Cookie"] = cookie

        # 发送请求并获取响应
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()

        # 解析 HTML 响应
        result = parse_aizhan_response(response.text, ip)
        result.update({"source": "爱站"})

        return result

    except requests.exceptions.RequestException as e:
        error_msg = str(e)
        if "网络" in error_msg or "连接" in error_msg or "timeout" in error_msg.lower():
            return {
                "ip": ip,
                "error": f"网络中断: {error_msg}",
                "source": "爱站",
            }
        elif (
            "403" in error_msg or "429" in error_msg or "forbidden" in error_msg.lower()
        ):
            return {
                "ip": ip,
                "error": f"爱站网禁止请求: {error_msg}",
                "source": "爱站",
            }
        else:
            return {
                "ip": ip,
                "error": f"IP查询失败: {error_msg}",
                "source": "爱站",
            }


def main(ip: str, cookie: str, delay: int = 2) -> Dict[str, Any]:
    """
    主入口

    Args:
        ip: 目标 IP 地址
        cookie: 爱站网 Cookie
        delay: 查询延时时间（秒），默认2秒

    Returns:
        Dict: 查询结果
    """
    # 验证 IP 格式

    try:
        ipv4_pattern = r"^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$"
        if not re.match(ipv4_pattern, ip):
            raise ValueError("IP 格式无效")

        if len(cookie) < 2:
            raise ValueError("Cookie 为空")
    except Exception as e:
        # 捕获所有异常
        return {
            "ip": ip,
            "error": f"解析失败: {str(e)}",
        }
    # 执行查询
    result = aizhan_ip_query(ip=ip, cookie=cookie, delay=delay)

    return result


def quick_query(ip: str, delay: int = 2) -> Dict[str, Any]:
    """
    快速查询函数（不使用Cookie）
    
    Args:
        ip: 目标 IP 地址
        delay: 查询延时时间（秒），默认2秒
        
    Returns:
        Dict: 查询结果
    """
    # 确保 delay 是正整数，最小为1
    delay = max(1, int(delay))
    
    try:
        # 构造 HTTP 请求
        url = f"https://dns.aizhan.com/{ip}/"
        # 构造 headers
        headers = {
            "Host": "dns.aizhan.com",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Encoding": "identity",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.87 Safari/537.36 SE 2.X MetaSr 1.0",
        }

        # 发送请求并获取响应
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()

        # 解析 HTML 响应
        result = parse_aizhan_response(response.text, ip)
        result.update({"source": "爱站"})

        return result

    except requests.exceptions.RequestException as e:
        error_msg = str(e)
        if "网络" in error_msg or "连接" in error_msg or "timeout" in error_msg.lower():
            return {
                "ip": ip,
                "error": f"网络中断: {error_msg}",
                "source": "爱站",
            }
        elif (
            "403" in error_msg or "429" in error_msg or "forbidden" in error_msg.lower()
        ):
            return {
                "ip": ip,
                "error": f"爱站网禁止请求: {error_msg}",
                "source": "爱站",
            }
        else:
            return {
                "ip": ip,
                "error": f"IP查询失败: {error_msg}",
                "source": "爱站",
            }


if __name__ == "__main__":
    """
    命令行入口
    """
    import argparse
    
    # 创建解析器
    parser = argparse.ArgumentParser(description="爱站网 IP 信息查询")
    
    # 添加参数
    parser.add_argument("ip", help="目标 IP 地址")
    parser.add_argument("cookie", nargs='?', default="", help="爱站网 Cookie（可选）")
    parser.add_argument("--delay", type=int, default=2, help="查询延时时间（秒），默认2秒")
    
    # 解析参数
    args = parser.parse_args()
    
    # 调用主函数
    if args.cookie:
        result = main(ip=args.ip, cookie=args.cookie, delay=args.delay)
    else:
        result = quick_query(ip=args.ip, delay=args.delay)
    
    # 打印结果
    import json
    print(json.dumps(result, ensure_ascii=False, indent=2))