# S/Key 模拟

## S/Key含义

[S/Key - Wikipedia](https://en.wikipedia.org/wiki/S/KEY)

## 程序描述

编程语言：Python3.8

操作系统: Ubuntu 20.04

分为服务器段和客户端，利用socket进行通信。

通信的过程中模拟了 web api的调用方式，利用json传递数据。

加盐的方式，以用户名为基础种子，然后加上随机的4个字符串，字符串的范围为 字母、数字、标点符号

```python
salt = ''.join(random.sample(string.ascii_letters + string.digits + string.punctuation, 4))
```