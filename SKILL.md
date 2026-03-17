---
name: aizhan-ip-query
description: 爱站网IP查询技能，用于查询IP地址的地理位置、运营商信息以及解析到该IP的所有域名。主要用于网络安全分析、SEO信息收集、网络空间测绘和威胁情报分析。当需要获取IP详细归属信息、域名关联分析或进行网络资产发现时使用此技能。
---

# 爱站网IP查询技能（安全版）

## 概述

本技能提供通过爱站网(dns.aizhan.com)查询IP地址的详细信息服务，包括地理位置、运营商信息、解析域名等。**必须使用Cookie**，确保查询质量和数据准确性，保护用户隐私。

## 使用场景

### 🔍 网络安全分析
- IP溯源定位攻击源
- 威胁情报收集
- 网络空间测绘
- 安全事件响应

### 📈 SEO信息收集
- 网站服务器位置分析
- 域名关联关系梳理
- 竞争对手网站架构分析
- SEO优化建议

### 🔧 网络管理
- IP地址归属验证
- CDN节点识别
- 服务器集群分析
- 网络拓扑图构建

## 快速开始

### 必要条件：配置Cookie
**所有查询都必须使用Cookie**，请先运行配置向导：
```bash
python3 scripts/setup_cookie.py
```

### 基本查询
```python
from scripts.aizhan_ip_query_secure import query_ip

# 自动从配置文件读取Cookie
result = query_ip("8.8.8.8", delay=3)
print(result)
```

### 指定Cookie查询
```python
from scripts.aizhan_ip_query_secure import query_ip

# 直接指定Cookie（覆盖配置文件）
cookie = "your_aizhan_cookie_here"
result = query_ip("8.8.8.8", delay=2, cookie=cookie)
print(result)
```

## 主要功能

### 1. IP地址基本信息查询
```python
from scripts.aizhan_ip_query_secure import query_ip

# 查询IP基本信息（自动使用配置的Cookie）
result = query_ip("114.114.114.114")
print(f"IP: {result['ip']}")
print(f"位置: {result['location']}")
print(f"域名数量: {result['domain_count']}")
```

### 2. 域名解析查询
```python
# 查询解析到该IP的所有域名
domains = result.get('domains', [])
for domain_info in domains:
    print(f"域名: {domain_info['domain']}")
    print(f"标题: {domain_info['title']}")
```

### 3. 批量查询
```python
from scripts.aizhan_ip_query_secure import query_ip

ips = ["8.8.8.8", "1.1.1.1", "114.114.114.114"]
results = []

for ip in ips:
    result = query_ip(ip, delay=3)  # 自动使用配置的Cookie
    results.append(result)
    print(f"IP {ip}: {result.get('domain_count', 'N/A')} 个域名")
```

## 配置说明

### Cookie配置（必须）
**必须配置爱站网Cookie才能使用**：

1. **获取Cookie方法**：
   - 打开爱站网(dns.aizhan.com)
   - 正常访问登录或浏览
   - 浏览器开发者工具 → Network → 选择任意请求 → Headers → 复制Cookie值

2. **配置向导**（推荐）：
```bash
python3 scripts/setup_cookie.py
```
这个交互式工具会指导您安全地获取和配置Cookie。

3. **手动配置**：
   编辑 `config/config.env` 文件：
   ```
   AIZHAN_COOKIE=PHPSESSID=xxx; userId=1234; userName=test%40aizhan.com
   ```

### 请求延时配置
为避免被反爬虫机制识别，建议设置延时：

- **首次使用**：3-5秒
- **日常使用**：1-3秒
- **批量查询**：2-5秒（每个IP间隔）

```python
# 设置延时的查询
result = quick_query("8.8.8.8", delay=3)  # 延时3秒
```

## API函数详解

### quick_query(ip, delay=2)
**参数：**
- `ip`: 目标IP地址（必需）
- `delay`: 查询延时时间（秒），默认2

**返回格式：**
```json
{
  "ip": "8.8.8.8",
  "domain_count": "1,234",
  "location": "美国加利福尼亚州谷歌公司",
  "domains": [
    {
      "domain": "dns.google",
      "title": "Google Public DNS"
    }
  ],
  "source": "爱站"
}
```

### aizhan_ip_query(ip, cookie, delay=2)
**参数：**
- `ip`: 目标IP地址（必需）
- `cookie`: 爱站网Cookie（可选）
- `delay`: 查询延时时间（秒），默认2

**返回格式：**
同quick_query，数据更完整

## 高级用法

### 错误处理
```python
try:
    result = quick_query("8.8.8.8", delay=2)
    if "error" in result:
        print(f"查询失败: {result['error']}")
    else:
        print("查询成功")
except Exception as e:
    print(f"网络异常: {e}")
```

### 结果分析
```python
def analyze_ip_result(result):
    """分析查询结果"""
    ip = result.get('ip', 'Unknown')
    location = result.get('location', 'Unknown')
    domain_count = result.get('domain_count', '0')
    
    print(f"IP地址: {ip}")
    print(f"地理位置: {location}")
    print(f"解析域名数: {domain_count}")
    
    # 判断是否搜索引擎IP
    if 'google' in location.lower() or 'baidu' in location.lower():
        print("类型: 可能是搜索引擎IP")
    elif domain_count == '0':
        print("类型: 可能是纯净IP或私有IP")
    else:
        print("类型: 可能是服务器或VPS")

# 使用示例
result = quick_query("8.8.8.8", delay=2)
analyze_ip_result(result)
```

## 注意事项

### ⚠️ 法律合规
- 仅用于合法的安全研究和SEO分析
- 不要用于非法渗透测试或恶意用途
- 遵守网站使用条款

### ⚠️ 使用限制
- 控制查询频率，避免被反爬虫
- 批量查询建议设置较大延时
- 结果仅供参考，需结合其他数据源验证

### ⚠️ 数据准确性
- IP位置信息可能存在偏差
- 域名信息实时更新
- 建议多源数据交叉验证

## 故障排除

### 常见问题

**1. 查询失败**
```python
# 现象：返回 {"ip": "8.8.8.8", "error": "爱站网禁止请求"}
# 解决：增加延时时间或配置Cookie
result = quick_query("8.8.8.8", delay=5)  # 增加到5秒
```

**2. 域名数量为0**
```python
# 现象：domains为空数组
# 正常情况：说明该IP没有解析域名
# 也可能是：IP被保护或配置有问题
```

**3. 网络连接超时**
```python
# 现象：超时错误
# 解决：检查网络连接，调整延时
result = quick_query("8.8.8.8", delay=3)
```

## 相关资源

- **API文档**: [references/api_docs.md](references/api_docs.md) - 详细的技术文档和配置指南
- **使用示例**: 查看 `scripts/aizhan_ip_query.py` 获取更多代码示例

## 🚀 发布给其他人使用

### 安全发布指南

**1. 用户隐私保护**
- ✅ **Cookie不包含在发布包中** - 用户需要自行配置
- ✅ **敏感信息分离** - 配置文件独立存储
- ✅ **清晰的配置说明** - 提供setup向导

**2. 部署步骤**

**Step 1: 基础包**
```bash
# 核心文件必须包含
├── scripts/
│   ├── aizhan_ip_query_secure.py    # 主要查询脚本
│   └── setup_cookie.py             # 配置向导
└── config/
    └── config.env                  # 配置模板（空文件）
```

**Step 2: 用户配置流程**
```bash
# 用户第一次使用时运行
python3 scripts/setup_cookie.py
```

**Step 3: 使用说明**
- 运行配置向导，获取爱站网Cookie
- 配置后即可使用查询功能
- Cookie信息只存储在本地，不上传不共享

**3. 兼容性说明**
- ✅ Python 3.7+
- ✅ requests库
- ✅ BeautifulSoup4库
- ✅ 无其他外部依赖

**4. 故障排除**
- 用户忘记Cookie：运行setup_cookie.py重新配置
- 网络问题：增加延时参数 --delay 5
- 配置错误：检查config/config.env文件内容

### 完整发布清单

**必含文件：**
- `scripts/aizhan_ip_query_secure.py` - 核心查询功能
- `scripts/setup_cookie.py` - 配置向导
- `config/config.env` - 配置模板
- `SKILL.md` - 使用说明
- `README.md` - 项目概述

**可选文件：**
- `examples/` - 使用示例
- `tests/` - 测试用例

### 安全注意事项

⚠️ **用户须知**：
- Cookie包含个人账户信息，请妥善保管
- 不要将配置文件分享给他人
- 定期更新Cookie以保持查询效果

🔒 **发布者责任**：
- 确保不包含任何用户隐私信息
- 提供清晰的配置指导
- 说明Cookie的获取方法和用途

## 维护说明

- 定期检查爱站网页面结构变化
- 更新User-Agent和headers以避免被识别为爬虫
- 监控反爬虫机制调整