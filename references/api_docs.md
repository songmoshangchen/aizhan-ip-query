# 爱站网IP查询API文档

## 功能概述

爱站网IP查询技能提供通过爱站网查询IP地址归属地和域名信息的能力，主要用于网络安全分析、SEO信息收集和空间测绘。

## 主要功能

### 1. IP地址归属地查询
- 查询IP地址的地理位置
- 获取运营商信息
- 提供IP基本信息

### 2. 域名解析查询
- �解析到该IP的所有域名
- 获取每个域名的标题信息
- 显示域名解析数量

### 3. 安全性分析
- 判断IP是否为搜索引擎爬虫
- 分析IP的网络用途
- 提供安全相关的IP情报

## 使用场景

- **网络安全**：IP溯源、威胁情报分析
- **SEO分析**：域名关联分析、网站结构分析
- **空间测绘**：网络资产发现
- **竞争对手分析**：分析竞争对手的网站服务器信息

## 配置说明

### Cookie配置（可选）

爱站网可能需要Cookie才能正常访问，建议配置：

```python
# 获取Cookie的方法：
# 1. 打开爱站网(dns.aizhan.com)
# 2. 登录或正常访问
# 3. 浏览器开发者工具 → Network → 找到请求 → Headers → Cookie
# 4. 复制Cookie值
```

### 请求延时配置

为了防止被反爬虫机制识别，建议设置合适的延时：

- 延时范围：1-10秒
- 默认值：2秒
- 建议：首次使用3秒，后续可适当降低

## API函数

### aizhan_ip_query(ip, cookie, delay=2)

**参数：**
- `ip`: 目标IP地址（必需）
- `cookie`: 爱站网Cookie（可选）
- `delay`: 查询延时时间，秒（默认2）

**返回值：**
```json
{
  "ip": "目标IP",
  "domain_count": "解析域名数量",
  "location": "地理位置信息",
  "domains": [
    {
      "domain": "域名",
      "title": "标题"
    }
  ],
  "source": "爱站",
  "error": "错误信息（如果有）"
}
```

### quick_query(ip, delay=2)

**参数：**
- `ip`: 目标IP地址（必需）
- `delay`: 查询延时时间，秒（默认2）

**返回值：**
同aizhan_ip_query函数，但不使用Cookie

## 错误处理

### 常见错误类型

1. **网络错误**
   - 症状：`error`字段包含"网络中断"
   - 解决：检查网络连接，增加延时

2. **反爬虫限制**
   - 症状：`error`字段包含"爱站网禁止请求"或403/429错误
   - 解决：增加延时时间，配置有效Cookie

3. **IP格式错误**
   - 症状：`error`字段包含"IP 格式无效"
   - 解决：检查IP地址格式是否正确

4. **查询结果为空**
   - 症状：`domains`字段为空数组
   - 说明：正常情况，表示该IP没有解析域名

## 注意事项

1. **法律合规**：仅用于合法的安全研究和SEO分析
2. **使用频率**：控制查询频率，避免对爱站网造成过大压力
3. **数据时效性**：IP信息可能发生变化，建议结合其他数据源验证
4. **隐私保护**：不要查询或传播敏感个人信息

## 示例使用

### 基本查询
```python
from scripts.aizhan_ip_query import aizhan_ip_query

# 带Cookie查询
result = aizhan_ip_query("8.8.8.8", "your_cookie_here", delay=3)
print(result)

# 快速查询（无Cookie）
from scripts.aizhan_ip_query import quick_query
result = quick_query("8.8.8.8", delay=2)
print(result)
```

### 批量查询
```python
ips = ["8.8.8.8", "1.1.1.1", "114.114.114.114"]
for ip in ips:
    result = quick_query(ip, delay=3)
    print(f"IP: {ip}, 域名数量: {result.get('domain_count', 'N/A')}")
```

## 限制说明

1. **域名数量限制**：最多返回20个域名
2. **查询延时**：最小延时1秒
3. **IP格式**：仅支持IPv4地址
4. **反爬虫机制**：可能无法查询某些被保护的IP