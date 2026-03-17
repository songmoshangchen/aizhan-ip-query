# 爱站网IP查询技能 (aizhan-ip-query)

安全、高效的IP信息查询工具，通过爱站网(dns.aizhan.com)获取IP地址的地理位置、运营商信息和解析域名。

## 🚀 核心特性

- ✅ **必须使用Cookie** - 确保查询质量和数据准确性
- 🔒 **隐私保护** - Cookie不硬编码，用户自行配置
- 📊 **详细信息** - 获取地理位置、域名数量、解析域名详情
- 🔧 **易用设计** - 提供配置向导，5分钟即可完成配置
- 🌍 **批量查询** - 支持批量IP处理，适合网络测绘

## 📋 使用场景

### 🔍 网络安全分析
- IP溯源定位攻击源
- 威胁情报收集
- 网络空间测绘
- 安全事件响应

### 📈 SEO信息收集
- 网站服务器位置分析
- 域名关联关系梳理
- 竞争对手网站架构分析

### 🔧 网络管理
- IP地址归属验证
- CDN节点识别
- 服务器集群分析

## 🛠️ 快速开始

### Step 1: 配置Cookie（必须）

```bash
# 运行配置向导
python3 scripts/setup_cookie.py
```

向导会指导你：
1. 打开爱站网并正常浏览
2. 获取你的Cookie
3. 自动测试配置
4. 保存配置文件

### Step 2: 查询IP信息

```bash
# 基本查询（自动使用配置的Cookie）
python3 scripts/aizhan_ip_query_secure.py 8.8.8.8

# 指定延时
python3 scripts/aizhan_ip_query_secure.py 8.8.8.8 --delay 3

# 直接指定Cookie（覆盖配置文件）
python3 scripts/aizhan_ip_query_secure.py 8.8.8.8 --cookie "your_cookie_here"
```

## 📁 项目结构

```
aizhan-ip-query/
├── scripts/
│   ├── aizhan_ip_query_secure.py    # 核心查询脚本
│   └── setup_cookie.py             # 配置向导
├── config/
│   └── config.env                  # 配置文件
├── SKILL.md                       # 详细使用说明
└── README.md                      # 项目说明
```

## 🔧 API使用

### Python接口

```python
from scripts.aizhan_ip_query_secure import query_ip

# 自动使用配置的Cookie
result = query_ip("8.8.8.8", delay=2)
print(result)

# 指定Cookie
cookie = "your_cookie_here"
result = query_ip("8.8.8.8", delay=2, cookie=cookie)
```

### 返回数据格式

```json
{
  "ip": "8.8.8.8",
  "domain_count": "749",
  "location": "美国",
  "domains": [
    {
      "domain": "example.com",
      "title": "网站标题"
    }
  ],
  "source": "爱站"
}
```

## 🚀 发布指南

### 安全发布原则

1. **隐私保护**
   - Cookie不包含在发布包中
   - 用户需要自行配置
   - 配置文件独立存储

2. **部署清单**
   ```
   必含文件：
   - scripts/aizhan_ip_query_secure.py
   - scripts/setup_cookie.py
   - config/config.env (模板)
   - SKILL.md
   - README.md
   ```

3. **用户使用流程**
   ```bash
   # 1. 解压文件
   # 2. 运行配置向导
   python3 scripts/setup_cookie.py
   # 3. 开始使用
   python3 scripts/aizhan_ip_query_secure.py 目标IP
   ```

### 安全注意事项

⚠️ **用户须知**：
- Cookie包含个人账户信息，请妥善保管
- 不要将配置文件分享给他人
- 定期更新Cookie以保持查询效果

🔒 **发布者责任**：
- 确保不包含任何用户隐私信息
- 提供清晰的配置指导
- 说明Cookie的获取方法和用途

## ⚠️ 重要说明

- **必须使用Cookie** - 这是安全版本的强制要求
- **合法使用** - 仅用于合法的安全研究和SEO分析
- **频率控制** - 避免过于频繁的查询以防被反爬虫
- **数据验证** - 结果仅供参考，建议多源数据交叉验证

## 🔍 故障排除

### 常见问题

1. **Cookie未配置**
   ```bash
   # 解决：运行配置向导
   python3 scripts/setup_cookie.py
   ```

2. **查询失败**
   ```bash
   # 解决：增加延时
   python3 scripts/aizhan_ip_query_secure.py 8.8.8.8 --delay 5
   ```

3. **网络问题**
   - 检查网络连接
   - 确认Cookie是否有效
   - 尝试更新Cookie

## 📄 许可证

本项目仅供学习和合法使用。请遵守爱站网的使用条款和相关法律法规。

## 🤝 贡献

欢迎提交Issue和Pull Request来改进这个项目。

---

**作者**：OpenClaw AI Assistant  
**维护**：安全与隐私优先