# 如何使用Tushare作为OpenBB的数据源

**OpenBB** 作为**开源金融数据平台**，致力于为投资者、分析师与开发者提供免费透明的金融数据接口。关于OpenBB的介绍以及如何使用，请参阅[OpenBB的介绍以及如何使用OpenBB助力A股港股的金融数据分析](https://blog.csdn.net/qq_29953771/article/details/148971007?fromshare=blogdetail&sharetype=blogdetail&sharerId=148971007&sharerefer=PC&sharesource=qq_29953771&sharefrom=from_link)。

OpenBB虽支持多个数据源，但中国区（含香港）金融数据获取主要依赖Yahoo Finance。该平台作为免费基础数据源虽能满足基本需求，但对中港市场的覆盖深度仍显不足。更关键的是，中国内地用户需借助VPN方可访问此服务，形成显著使用门槛。

要查询A股和港股数据，OpenBB亟待完善本地化金融数据源的接入。A股和港股数据，付费的主流方案包括Wind、东方财富Choice和同花顺iFind（主要面向机构客户）；开源数据源则以Tushare或AKShare为主要替代方案。

Tushare 与 AKShare 作为两款重要的金融数据工具，具备各自鲜明的特点。为清晰展示其差异，下表对二者进行了系统性的比较和总结。

| 特性     | Tushare         | AKShare       |
| ------ | --------------- | ------------- |
| 是否免费   | 免费版功能受限，高级功能需积分 | 完全免费          |
| 数据质量   | 高，标准化           | 中等，依赖源站，需清洗   |
| 数据覆盖范围 | 广，偏重A股和宏观       | 非常广，含加密货币、外盘等 |
| 接口稳定性  | 高（Pro API）      | 中等（受源站影响）     |
| 文档完整性  | 高，详细            | 中等，部分需看源码     |
| 社区活跃度  | 高，成熟            | 高，更新快         |
| 学习成本   | 低               | 低到中           |
| 适合用户   | 企业、专业研究者        | 学生、个人开发者、初学者  |
| 实时数据支持 | 支持（需高级权限）       | 部分支持，依赖源站     |
| 维护模式   | 个人主导            | 社区驱动          |

当前已有两个独立项目，分别开发了针对 Tushare 和 AKShare 的 OpenBB 数据源扩展。

- Tushare: https://github.com/finanalyzer/openbb_tushare

- AKShare: https://github.com/finanalyzer/openbb_akshare

`openbb_tushare`项目作为 OpenBB 的数据源扩展，可实现 Tushare 数据在 OpenBB 平台的无缝接入。以下为详细使用指南：

## 💻 环境搭建与安装流程

作为开发者，我们主要通过Python API接口和OpenBB Platform CLI与平台交互。要集成Tushare数据源，需按以下步骤配置开发环境：

1. 创建Python虚拟环境

   可以使用uv或者poetry来创建虚拟环境。在这里，我使用Python自带的组件venv来搭建虚拟环境。

   ```bash
   python3 -m venv .venv
   ```

   创建了虚拟环境后，可以用下面的命令使用这个虚拟环境。

   ```bash
   source .venv/bin/activate
   ```

   注：Windows系统执行`.venv\Scripts\activate`

2. 安装OpenBB Platform CLI

   在上面的虚拟环境中，我们需要先安装`openbb-cli`来使用OpenBB Platform CLI。

   ```bash
   pip install openbb-cli
   ```

   如果你在中国大陆，可以先设置下面的环境变量。这样可以使用阿里的镜像来加速安装过程。

   ```powershell
   set PIP_INDEX_URL=https://mirrors.aliyun.com/pypi/simple
   ```

3. 安装openbb_tushare

   接下来，我们需要安装`openbb_tushare`来使用Tushare数据源。

   ```bash
   pip install openbb_tushare
   ```

   安装`openbb_tushare`后，需要重新构建资源让安装生效。

   ```bash
   python -c "import openbb; openbb.build()"
   ```

## Tushare token的配置

由于 Tushare 要求使用 token 访问数据源，使用前需完成 token 配置。数据源的 token 支持以下两种配置方式：

1.  通过OpenBB Hub配置

2.  本地环境配置

具体操作流程请参阅官方文档：https://docs.openbb.co/platform/settings/user_settings/api_keys

本文简要说明在本地环境配置 Tushare token 的方法：OpenBB 的用户偏好设置及 token 均存储于本地路径 ~/.openbb_platform/，并以 JSON 格式保存于 user_settings.json 文件，示例如下：

```JSON
{
  "credentials": {
    "fmp_api_key": "REPLACE",
    "tushare_api_key": "REPLACE"
  }
}
```

## 🚀 使用 Tushare 数据源

### 案例 1：查询 A 股公司动态（以万科为例）

**Jupyter Notebook 代码示例**：

```Python
from openbb import obb
messages = obb.news.company("000002", provider="tushare")
for result in messages.results:
    print(f"{result.title}")
```

执行结果：

```plaintext
开源证券发布万科A研报，公司信息更新报告：销售均价有所提升，股东持续借款提供支持
万科A出售2086万股库存股，金额1.36亿元
万科A：已完成所有A股库存股出售 所得资金4.79亿元
...
```

**命令行查询方式**：

```bash
openbb
2025 Jun 26, 03:11 (🦋) /news/ $ company --symbol 000002 --provider tushare
```

输入上述命令，我们可以看到下面的结果。OpenBB CLI的结果会显示在一个WebView里，如下图所示：

![openbb04](docs/images/openbb04.png)

### 案例 2：获取港股历史股价（以香港电讯为例）

**命令行查询**:

Tushare也提供港股数据，我们可以使用下面的命令来查询"香港电讯"的股价历史。

```
2025 Jun 26, 03:28 (🦋) /equity/price/ $ historical --symbol 06823 --provider tushare
```

我们可以看到下面的WebView输出：![openbb05](docs/images/openbb05.png)

**Jupyter Notebook 代码示例**：

同样的，我们也可以用代码来查询"香港电讯"的股价，如下：

```Python
from openbb import obb
prices = obb.equity.price.historical(symbol='06823', start_date="2025-06-01", end_date="2025-06-10", provider="tushare")
prices.results[0].date, prices.results[0].open, prices.results[0].close, prices.results[0].high, prices.results[0].low, prices.results[0].volume
```

输出示例：

```
(datetime.date(2025, 6, 2), 11.28, 11.3, 11.3, 11.14, 10308375)
```

## 🌟 openbb_tushare 项目生态

目前`openbb_tushare`项目正处于活跃开发阶段，欢迎开源社区贡献力量：

**代码仓库**：

- GitHub：https://github.com/finanalyzer/openbb_tushare

- GitCode（国内镜像）：https://gitcode.com/finanalyzer/openbb_tushare

**参与方式**：

1. 提交 Issue 反馈数据需求或 Bug

2. 贡献 PR 优化数据源接口

3. 完善文档帮助更多用户

通过 Tushare 与 OpenBB 的集成，中国区用户可更便捷地获取 A 股、港股等市场的实时与历史数据，为量化分析、投资研究提供强有力的数据支撑。