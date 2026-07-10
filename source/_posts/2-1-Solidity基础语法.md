---
title: Solidity基础语法：数据类型、变量与函数
date: 2026-07-10 16:44:23
categories:
  - Solidity开发
tags:
  - Solidity开发
  - Solidity 智能合约
description: Solidity是静态类型语言，每个变量都需要声明类型。
cover: false
---

## Solidity基础语法


## 数据类型、变量与函数


## 基础数据类型


Solidity是静态类型语言，每个变量都需要声明类型。


## 整型（Integer）


uint8 到 uint256：无符号整数（默认uint256）

int8 到 int256：有符号整数

常用：uint256（最大值 2^256-1）

BasicTypes.sol


```solidity
uint256 public positiveNumber = 100;
int256 public negativeNumber = -50;
uint8 public smallNumber = 255;  // 最大255
```


## 布尔型（Boolean）


BasicTypes.sol


```plaintext
bool public isActive = true;
bool public hasPermission = false;
```


## 地址类型（Address）


address：以太坊地址（20字节）

• address：普通地址
• address payable：可接收ETH的地址
• 内置成员：balance、transfer、call

BasicTypes.sol


```solidity
address public owner;
address payable public recipient;
```


```solidity
// 查询余额
uint256 balance = owner.balance;
```


```plaintext
// 转账
recipient.transfer(1 ether);
```


## 字节类型（Bytes）


定长：bytes1 到 bytes32

不定长：bytes（类似byte[]）

string：UTF-8编码，不定长

BasicTypes.sol


```plaintext
bytes32 public hash;
string public name = "Hello";
bytes public data;
```


## 复杂数据类型


## 数组（Array）


定长数组：uint[5] fixedArray

动态数组：uint[] dynamicArray

内存数组：new uint[](10)

BasicTypes.sol


```plaintext
uint[] public numbers;  // 动态数组
```


```javascript
function addNumber(uint n) public {
numbers.push(n);
}
```


```javascript
function getLength() public view returns (uint) {
return numbers.length;
}
```


```javascript
function removeLast() public {
numbers.pop();
}
```


## 结构体（Struct）


BasicTypes.sol


```solidity
struct User {
string name;
uint256 age;
address wallet;
}
```


```plaintext
User public user;
```


```javascript
function setUser(string memory _name, uint256 _age) public {
user = User(_name, _age, msg.sender);
}
```


## 映射（Mapping）


mapping(keyType => valueType)

• 类似哈希表，键值对存储
• 所有可能的键都存在，默认值为0/false
• 无法遍历（需要额外维护键数组）

BasicTypes.sol


```solidity
// 地址到余额的映射
mapping(address => uint256) public balances;
```


```solidity
// 地址到用户的映射
mapping(address => User) public users;
```


```javascript
function deposit() public payable {
balances[msg.sender] += msg.value;
}
```


```javascript
function getBalance() public view returns (uint256) {
return balances[msg.sender];
}
```


## 枚举（Enum）


BasicTypes.sol


```plaintext
enum Status { Pending, Active, Inactive }
```


```plaintext
Status public status;
```


```javascript
function activate() public {
status = Status.Active;
}
```


## 函数定义


Solidity函数的基本结构：

BasicTypes.sol


```javascript
function functionName(<参数>) <可见性> <状态可变性> <修饰符> returns (<返回类型>) {
// 函数体
}
```


## 可见性修饰符


## public  任何人可调用    自动生成getter


## private  仅合约内部    不生成getter


## internal  合约内部+继承合约    类似protected


## external  仅外部调用    gas更省


**状态可变性**


## view  读取状态    不消耗gas（外部调用）


## pure  不读不写状态    纯计算


## payable  可接收ETH    msg.value可用


## 默认  修改状态    消耗gas


BasicTypes.sol


```solidity
contract FunctionExamples {
uint256 public value;
// 修改状态
function setValue(uint256 _value) public {
value = _value;
}
// 只读
function getValue() public view returns (uint256) {
return value;
}
// 纯计算
function add(uint256 a, uint256 b) public pure returns (uint256) {
return a + b;
}
// 接收ETH
function deposit() public payable {
value += msg.value;
}
}
```


## 常用全局变量


Solidity提供了一些内置全局变量：


## 区块和交易信息


BasicTypes.sol


```solidity
block.number      // 当前区块号
block.timestamp   // 当前区块时间戳（uint256）
block.difficulty  // 区块难度
block.gaslimit    // 区块gas上限
```


```plaintext
msg.sender        // 调用者地址
msg.value         // 随交易发送的ETH（wei）
msg.data          // 完整的调用数据
```


```plaintext
tx.origin         // 交易发起者（注意安全问题）
tx.gasprice       // 交易的gas价格
```


## 错误处理


Solidity提供了三种错误处理方式：


## require


条件为false时回滚交易

退还剩余gas

用于验证输入条件

BasicTypes.sol


```javascript
function withdraw(uint256 amount) public {
require(balances[msg.sender] >= amount, "余额不足");
require(amount > 0, "金额必须大于0");
balances[msg.sender] -= amount;
payable(msg.sender).transfer(amount);
}
```


## assert


用于检查内部错误

不应该失败的条件

消耗所有gas（0.8.0后改变）

BasicTypes.sol


```plaintext
// 检查不变量
assert(totalSupply == sumOfAllBalances);
```


## revert


直接回滚交易

可以带错误信息

用于复杂条件判断

BasicTypes.sol


```javascript
function transfer(address to, uint256 amount) public {
if (to == address(0)) {
revert("不能转账到零地址");
}
// ...
}
```


## 完整示例：简单的银行合约


BasicTypes.sol


```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;
```


```solidity
contract SimpleBank {
mapping(address => uint256) private balances;
address public owner;
event Deposit(address indexed user, uint256 amount);
event Withdrawal(address indexed user, uint256 amount);
constructor() {
owner = msg.sender;
}
function deposit() public payable {
require(msg.value > 0, "必须存入正数");
balances[msg.sender] += msg.value;
emit Deposit(msg.sender, msg.value);
}
function withdraw(uint256 amount) public {
require(amount > 0, "金额必须大于0");
require(balances[msg.sender] >= amount, "余额不足");
balances[msg.sender] -= amount;
payable(msg.sender).transfer(amount);
emit Withdrawal(msg.sender, amount);
}
function getBalance() public view returns (uint256) {
return balances[msg.sender];
}
}
```


**7. 总结**


## ①  Solidity是静态类型语言，支持丰富的数据类型


## ②  基础类型：uint/int、bool、address、bytes/string


## ③  复杂类型：array、struct、mapping、enum


## ④  函数可见性：public/private/internal/external


## ⑤  状态可变性：view/pure/payable


## ⑥  错误处理：require/assert/revert


合约定义、继承、接口、库的使用

━━━━━━━━━━━━━━━━━━━━━

未经授权，禁止转载

如有转载需求，请联系作者

关注我，解锁更多可能