---
title: Move语言：Sui与Aptos合约开发
date: 2026-07-10 16:44:23
categories:
  - 多链生态
tags:
  - 多链生态
  - 多链生态
description: Move是Facebook（现Meta）为Diem（原Libra）区块链开发的智能合约语言。Diem虽然没有成功，但Move语言被Sui和Aptos继承并发展，成为新一代高性能区块链的核心语言。
cover: false
---

## Move语言


## Sui与Aptos合约开发


## Move语言是什么？


Move是Facebook（现Meta）为Diem（原Libra）区块链开发的智能合约语言。Diem虽然没有成功，但Move语言被Sui和Aptos继承并发展，成为新一代高性能区块链的核心语言。

Move的核心设计理念：

* 资源作为一等公民：代币不能被复制或删除
* 形式化验证支持：可以用Move Prover证明代码正确性
* 静态类型系统：编译时捕获大部分错误
* 模块化设计：代码可复用，安全性高


## Move vs Solidity


Move和Solidity最核心的区别在于"资源"的处理方式。Solidity中，代币只是数字，可以随意复制。Move中，资源有严格的所有权规则——不能复制，不能凭空消失。

Move vs Solidity：

* Solidity的代币只是uint256，可以无限复制
* Move的代币是资源类型，有所有权语义
* Move的"资源"类似Rust的Box<T>，移动语义严格
* Move可以形式化验证，Solidity难以验证


## Sui和Aptos的区别


Sui和Aptos都使用Move语言，但它们对Move做了不同的扩展。

Sui的创新：

* 对象模型：一切都是对象
* 独立对象：每个对象有独立ID
* 并行执行：对象可以并行处理
* Move Sui扩展：增加了Object类型

Aptos的创新：

* 保留原版Move语言特性
* Block-STM并行执行
* 更接近Diem原始设计
* Move语言标准化方向


## Move基本语法


Move使用模块（Module）和脚本（Script）的结构。模块定义类型和函数，脚本是执行入口。

Move基本结构：

* module：定义类型和函数，类似合约
* struct：定义类型，包括资源类型
* fun：定义函数
* script：程序入口，一次性执行


## Sui合约开发


Sui的合约用Sui Move编写，基于对象模型。每个资产都是Sui Object（对象），有全局唯一ID。

Sui对象的特点：

* 每个对象有全局唯一ID
* 对象可以被拥有（owned）或共享（shared）
* 所有者可以转移对象
* 共享对象可以被任何人修改


## Sui合约示例


counter.move


```plaintext
module example::counter {
use sui::object::{UID, ID};
use sui::tx_context::TxContext;
public struct Counter has key, store {
id: UID,
value: u64,
}
public fun new(ctx: &mut TxContext): Counter {
Counter {
id: object::new(ctx),
value: 0,
}
}
public fun increment(c: &mut Counter) {
c.value = c.value + 1;
}
}
```


## 部署与交互


deploy.sh


```javascript
# 安装Sui CLI
curl -fsSL https://docs.sui.io/install | sh
# 初始化开发环境
sui client
# 发布合约
sui client publish --path my_project
# 创建计数器对象
sui client call --package PACKAGE_ID --module counter --function new
```


**8. 总结**

①  Move语言由Facebook开发，被Sui和Aptos继承

②  资源作为一等公民，代币不能被复制或删除

③  Sui使用对象模型，一切都是对象

④  Move支持形式化验证，安全性高

⑤  Sui并行执行性能优秀

Stacks智能合约、闪电网络支付、RGB协议

━━━━━━━━━━━━━━━━━━━━━

未经授权，禁止转载

如有转载需求，请联系作者

关注我，解锁更多可能