# Hong Kong financial Mihomo rule-sets

面向香港银行与券商服务的 [Mihomo](https://github.com/MetaCubeX/mihomo) `domain` 规则集。目录结构仿照 [meta-rules-dat](https://github.com/MetaCubeX/meta-rules-dat/tree/meta)：规则源文件与构建产物统一放在 `geo/geosite/` 下，YAML 源文件可审阅，`.list` 与 `.mrs` 由 GitHub Actions 自动生成。

## 目录结构

```
geo/geosite/
├── hk-banks.yaml      # 源文件：可审阅，带机构注释
├── hk-banks.list      # 生成：纯域名列表
├── hk-banks.mrs       # 生成：mihomo 二进制规则集
├── hk-brokers.yaml    # 源文件：可审阅，带机构注释
├── hk-brokers.list    # 生成：纯域名列表
└── hk-brokers.mrs     # 生成：mihomo 二进制规则集
```

## 规则集

| 规则集 | 覆盖范围 | YAML 源文件 | 构建产物 |
| --- | --- | --- | --- |
| `hk-banks` | 香港零售、虚拟及商业银行的第一方客户域名 | [`geo/geosite/hk-banks.yaml`](geo/geosite/hk-banks.yaml) | `geo/geosite/hk-banks.list`、`geo/geosite/hk-banks.mrs` |
| `hk-brokers` | 服务香港客户的券商和交易平台第一方域名 | [`geo/geosite/hk-brokers.yaml`](geo/geosite/hk-brokers.yaml) | `geo/geosite/hk-brokers.list`、`geo/geosite/hk-brokers.mrs` |

`hk-banks` 的机构范围以 [HKMA 授权机构名录](https://vpr.hkma.gov.hk/eng/regulatory-resources/registers/register-of-ais-and-lros/) 为核对依据。每条规则只匹配机构的第一方域名；不会收录 CDN、分析、云服务或通用身份提供商，以避免误分流。

## 在 Mihomo 中使用

将下列 `<owner>/<repo>` 替换为你的 GitHub 用户或组织与仓库名：

```yaml
rule-providers:
  hk-banks:
    type: http
    behavior: domain
    format: mrs
    url: https://raw.githubusercontent.com/<owner>/<repo>/main/geo/geosite/hk-banks.mrs
    path: ./ruleset/hk-banks.mrs
    interval: 86400
  hk-brokers:
    type: http
    behavior: domain
    format: mrs
    url: https://raw.githubusercontent.com/<owner>/<repo>/main/geo/geosite/hk-brokers.mrs
    path: ./ruleset/hk-brokers.mrs
    interval: 86400

rules:
  - RULE-SET,hk-banks,DIRECT
  - RULE-SET,hk-brokers,DIRECT
```

`.mrs` 仅支持 `domain` 和 `ipcidr` 行为；本仓库全部规则都是 `domain`。语法与转换命令见 [Mihomo 官方文档](https://wiki.metacubex.one/en/config/rule-providers/)。

## 维护与构建

1. 在 `geo/geosite/*.yaml` 中增删域名；每条新增域名都应附上所属机构注释。
2. 提交或发起 PR 后，工作流会用标准库脚本检查格式和重复项。
3. 工作流下载最新稳定版 Mihomo，将每个 YAML 编译为同目录下的 `*.list` 与 `*.mrs`。
4. `main` 分支和每周一 UTC 03:17 的定时构建会自动提交更新后的产物；PR 只验证，不会写回分支。

本地构建（已安装 Mihomo 时）：

```bash
python3 scripts/validate_rulesets.py
mihomo convert-ruleset domain yaml geo/geosite/hk-banks.yaml geo/geosite/hk-banks.mrs
mihomo convert-ruleset domain mrs geo/geosite/hk-banks.mrs geo/geosite/hk-banks.list
mihomo convert-ruleset domain yaml geo/geosite/hk-brokers.yaml geo/geosite/hk-brokers.mrs
mihomo convert-ruleset domain mrs geo/geosite/hk-brokers.mrs geo/geosite/hk-brokers.list
```

## 收录标准

- 仅香港银行／面向香港客户的券商和交易平台的**官方第一方域名**。
- 不以 IP、ASN、CDN 或第三方登录域名匹配。
- 合并前应在机构官网、App 链接或可验证的官方文档中确认域名归属。
- 域名按机构分组；同一机构多个域名可保留，避免业务迁移造成失效。

这不是金融建议，也不代表机构的官方认可。

