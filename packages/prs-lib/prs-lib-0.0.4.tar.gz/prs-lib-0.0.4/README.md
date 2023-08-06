# PRS Lib

是对 PRS REST API 的封装，开发者可以直接调用与 PRS 服务进行通信。

PRS 目前提供了两个环境供开发者使用：

- 正式环境，域名 https://press.one
- 测试环境，域名 https://beta.press.one
- 开发环境，域名 https://beta.press.one

目前对 DApp 开放的接口有：

- DApp 创建和维护。
- 用户授权。
- 签名。
- 签名文件相关。(签名文件、获取文件)
- 合约相关。（创建合约、绑定合约、查询合约）
- 合约交易相关。（购买合约、合约交易记录）
- 区块信息查询。
- 钱包相关。（查询钱包、查询交易历史、充值、提现）

## 快速开始

### 注册账号

1. 开发者前往 PRS 官网注册账号。(正式环境：https://press.one 测试环境：https://beta.press.one )
2. 登录成功后进入[开发者设置](https://beta.press.one/developer/settings)、[我的 DApp](https://beta.press.one/developer/apps)，完善开发者信息以及创建 DApp。
3. 在项目中安装此 [Lib](https://github.com/Press-One/prs-lib-py)
4. DApp 在合适的时候引导用户进行授权
5. 授权成功后即可进行签名发布文件、创建合约等操作

更多信息，请参考[开发者网站](https://developer.press.one)。

### Python 版本支持

支持 `>= Python 3.6`

### 安装

通过 `pip` 安装:

```bash
pip install prs-lib
```

### 初始化

在代码中 `import prs_lib`，之后创建 client

```python
import prs_lib


# 初始化 client
client = prs_lib.PRS({
  'env': 'dev',
  'private_key': 'private key ..',
  'address': 'address ...',
  'token': 'token ...',
  'debug': True,
})

# 其中，`env` 是必填的，其它都是可选的
```

### 示例代码

以下代码根据块的 id 从链上对块内容进行获取

```python
import prs_lib


client = prs_lib.PRS({
  'env': 'dev',
  'debug': True,
})
res = client.block.get_by_rids([
    'ba03bd584d69b89615ce8db22b4c593342a5ec09b343a7859044a8e4d389c4c2',
    '65163724a98d29506b1031dc68fa62fb5a7a11fe631fb723a723b2a19e9bb65c'
])
print(res.json())
```

## API

prs-lib 暴露一个 PRS 类，开发者通过创建 PRS 实例，来对 REST API 进行交互。

```
$ pydoc prs_lib
```

看某个具体模块的帮助，比如，查看 `block` 的文档：

```
$ pydoc prs_lib.block
```
