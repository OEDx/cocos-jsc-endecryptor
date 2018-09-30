# cocos-jsc-endecryptor

## 简介

Cocos Creator 在构建的时候支持对脚本进行加密和压缩。

![](https://ws3.sinaimg.cn/large/0069RVTdgy1fuzxib2j7gj30no04ojrl.jpg)

然而，官方并没有提供一个解压和解密的工具。这给 jsc 的二次修改和重用带来了不便。

本工具弥补了这个不足：提供了与 Cocos Creator 相同的加密、解密、压缩、解压的方法。可以很方便地对构建得到的 jsc 进行解密、解压得到 js ，也可以将 js 压缩、加密回 jsc 。

<img src="https://camo.githubusercontent.com/a958d311700ec37fb2ffb8b943a153ea3a8fd929/687474703a2f2f6f6e6d7737793666342e626b742e636c6f7564646e2e636f6d2f6a73632d656e646563727970742e706e67" alt="" data-canonical-src="http://onmw7y6f4.bkt.clouddn.com/jsc-endecrypt.png" width="283">

> 此 master 分支的脚本适用于 CocosCreator 1.x 编译导出的 jsc文件，如果你使用的 CocosCreator 为 2.0.2 版本，请切换到 v2.0 分支。

## 使用说明

### 命令行使用

1. 如果使用加密功能，第二个参数设置为 `encrypt`；如果使用解密功能，第二个参数设置为 `decrypt`。此参数为必选参数

2. 如需设置加密密钥，添加 `--key` 或 `-k` 参数，并跟上加密密钥字符串。如不设置，会在命令行中提示输入

3. 如需设置为非压缩方案，添加 `--nozip` 或 `-n` 参数，并设置为 true。如不设置，默认为压缩方案

    > 非压缩方案是指Cocos编译时没有勾选“Zip 压缩”选项

4. 找到 CocosCreator 编译出来的 .jsc 文件，一般在工程目录下 `build/jsb-default/src` 文件夹下。你可以在脚本运行时，根据提示输入文件的路径来指定对应文件。也可以添加 `--path` 或 `-p` 参数，设置为文件路径。如不设置，会在命令行中提示输入


5. 运行脚本即可。

    - encrypt：解密后文件路径为 `decryptOutput/decrypt.js`
    - decrypt: 加密后文件路径为 `encryptOutput/projectChanged.jsc`

6. 举例：

    ``` sh
    ./edc.py encrypt --key yourkey --nozip true  # 加密，不压缩
    ./edc.py decrypt --nozip true                # 解密，不需要解压
    ./edc.py decrypt                             # 解密并解压
    ```

### 在其他 Python 脚本中引用

1. 下载edc.py文件放到你的脚本目录下，通过 `import edc` 进行导入
2. 直接调用 `edc.decrypt(is_zip, key, jsc_path)` 或 `edc.encrypt(is_zip, key, js_path)` 即可，可参考 edcExample.py 文件。

> 如果是非交互式脚本，请务必在调用方法时传入有效的参数，并保证其正确性

## 参数说明

| 参数名 | 缩写 | 是否必须 | 默认值 |
| ----- | ----- | ---- | ----- |
| encrypt/decrypt | 无 | 是 | - |
| --key | -k | 否 | - |
| --nozip | -n | 否 | false |
| --path | -p | 否 | - |

## 参考文章

- [jsb_global.cpp](https://github.com/cocos-creator/cocos2d-x-lite/blob/develop/cocos/scripting/js-bindings/manual/jsb_global.cpp)
- [形同虚设的cocos默认加密](http://blog.shuax.com/archives/decryptcocos.html)
- [cocos2dx lua 反编译](https://bbs.pediy.com/thread-216800.htm)
