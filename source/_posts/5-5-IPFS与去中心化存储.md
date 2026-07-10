---
title: IPFS与去中心化存储：NFT元数据与文件存储
date: 2026-04-21 10:00:00
categories:
  - 开发工具
tags:
  - 开发工具
  - 开发工具与前端
description: 现在的互联网数据几乎都存在几大云服务商（AWS、Google Cloud、阿里云）的服务器上。一旦这些服务商出问题，或者遭遇审查，数据可能永久消失。
cover: false
---

## IPFS与去中心化存储


## NFT元数据与文件存储


## 中心化存储的问题


现在的互联网数据几乎都存在几大云服务商（AWS、Google Cloud、阿里云）的服务器上。一旦这些服务商出问题，或者遭遇审查，数据可能永久消失。

更现实的问题是：你上传的文件，平台可以随时删除。微博删帖、公众号被封、云盘文件消失——这类事情我们见得太多了。

中心化存储的问题：

• 单点故障：一个服务器挂了，服务就没了
• 审查风险：平台可以随时删除内容
• 数据主权：你存的文件，平台可以随意处置
• 隐私问题：服务商可以看到你所有的数据


## IPFS是什么？


IPFS（InterPlanetary File System，星际文件系统）是一个点对点的去中心化存储协议。和传统Web不同，IPFS用内容寻址而不是地址寻址。

打个比方：传统Web像是按门牌号找房子（地址变了就找不到），IPFS像是按房子内容生成的指纹找房子（内容不变，指纹就不变）。

IPFS的核心特点：

• 内容寻址：文件用哈希指纹（CID）标识，内容不变CID不变
• 去中心化：文件分散存储在全球无数节点上
• 防篡改：修改文件内容，CID立刻变化
• 抗审查：没有单一控制者


## CID是什么？


CID（Content Identifier，内容标识符）是IPFS中文件的唯一标识。它基于文件内容生成，内容相同则CID相同。

CID示例.txt


```bash
# CID示例
QmXoypizjW3WknFiJnKLwHCnL72vedxjQkDDP1mXWo6uco
# 这是一个IPFS哈希/CID，指向一个具体文件
# 类比：文件的指纹，内容相同则指纹相同
```


## IPFS Gateway


IPFS Gateway（网关）让普通浏览器可以访问IPFS上的文件。直接用IPFS协议访问需要本地运行节点，但通过Gateway就可以通过HTTP访问。

Gateway访问.sh


```bash
# 通过公共网关访问IPFS文件
https://ipfs.io/ipfs/QmXoypizjW3WknFiJnKLwHCnL72vedxjQkDDP1mXWo6uco
https://cloudflare-ipfs.com/ipfs/QmXoypizjW3WknFiJnKLwHCnL72vedxjQkDDP1mXWo6uco
https://dweb.link/ipfs/QmXoypizjW3WknFiJnKLwHCnL72vedxjQkDDP1mXWo6uco
```


## Pinata（最流行的IPFS服务）


虽然任何人都可以运行IPFS节点自己存储，但普通用户更常用Pinata这样的IPFS上传服务。Pinata提供API，让你方便地上传文件、管理CID、设置元数据。

为什么需要Pinata？因为自己运行IPFS节点需要24小时在线，否则文件会被"垃圾回收"。Pinata帮你"固定"（Pin）文件，确保它们永久可访问。


## 注册Pinata


访问 pinata.cloud 注册账号，获取API Key（JWT Token）。免费账号每月有1GB上传额度，足够开发测试用。


## Node.js上传文件


upload.js


```javascript
npm install @pinata/sdk axios FormData
const pinataSDK = require('@pinata/sdk');
const pinata = new pinataSDK({ pinataJWTKey: 'YOUR_JWT_TOKEN' });
```


```javascript
async function uploadFile(filePath, fileName) {
const readableStreamForFile = fs.createReadStream(filePath);
const options = {
pinataMetadata: {
name: fileName,
},
};
const result = await pinata.pinFileToIPFS(readableStreamForFile, options);
console.log('CID:', result.IpfsHash);
console.log('Gateway: https://gateway.pinata.cloud/ipfs/' + result.IpfsHash);
return result.IpfsHash;
}
```


```plaintext
uploadFile('./image.png', 'MyImage');
```


## 上传JSON数据


上传JSON特别重要，因为NFT的元数据就是JSON格式。

uploadMetadata.js


```javascript
async function uploadMetadata(metadata) {
const result = await pinata.pinJSONToIPFS(metadata, {
pinataMetadata: { name: metadata.name || 'metadata' }
});
console.log('Metadata CID:', result.IpfsHash);
return result.IpfsHash;
}
```


```javascript
const metadata = {
name: 'My NFT #1',
description: 'This is my first NFT on the blockchain',
image: 'ipfs://Qm...',  // 图片的IPFS地址
};
await uploadMetadata(metadata);
```


## NFT元数据标准


NFT的核心价值在于元数据。元数据定义了NFT长什么样、叫什么、有什么属性。没有元数据，NFT就只是一个链上编号。

ERC721标准定义了NFT的tokenURI字段，这个字段指向一个JSON文件的URL。NFT图片和属性都存在这个JSON里。


## ERC721元数据格式


metadata.json


```plaintext
{
"name": "CryptoPunk #888",
"description": "One of 10,000 unique characters from the Larva Labs CryptoPunks.",
"image": "ipfs://QmTCcVTLmrCMj3mS6MKLvT5VoFdyS6Q5jb4BkJnooKBFz/888.png",
"attributes": [
{ "trait_type": "Accessory", "value": "Shades" },
{ "trait_type": "Hair", "value": "Mohawk" },
{ "trait_type": "Skin", "value": "Dark" }
]
}
```


## 图片和元数据分离的好处


把图片存在IPFS上，把元数据也存IPFS上，只在链上存元数据的CID。这样链上数据量最小，元数据可以包含丰富信息，而且不怕图片链接失效。


## 完整的NFT铸造流程


mintNft.js


```javascript
// 1. 上传图片到IPFS
const imageCid = await uploadFile('./nft.png', 'MyNFT');
const imageUrl = 'ipfs://' + imageCid;
```


```javascript
// 2. 创建元数据JSON
const metadata = {
name: 'My NFT #1',
description: 'My first NFT artwork',
image: imageUrl,
attributes: [
{ trait_type: 'Artist', value: 'BlockchainCoder' },
{ trait_type: 'Rarity', value: 'Rare' }
]
};
```


```javascript
// 3. 上传元数据到IPFS
const metadataCid = await uploadMetadata(metadata);
const tokenUri = 'ipfs://' + metadataCid;
```


```plaintext
// 4. 铸造NFT（链上只存tokenUri）
await nftContract.mint(account, tokenUri);
```


## Pinata SDK完整示例


pinata-upload.js


```javascript
// pinata-upload.js
const pinataSDK = require('@pinata/sdk');
const fs = require('fs');
const pinata = pinataSDK(process.env.PINATA_JWT);
```


```javascript
async function main() {
// 方式1：上传单个文件
const fileStream = fs.createReadStream('./artwork.png');
const fileResult = await pinata.pinFileToIPFS(fileStream, {
pinataMetadata: { name: 'Artwork-PNG' },
pinataOptions: { cidVersion: 1 }
});
console.log('图片CID:', fileResult.IpfsHash);
```


```javascript
// 方式2：上传JSON
const jsonData = {
name: 'My NFT',
image: 'ipfs://' + fileResult.IpfsHash,
description: 'Generated with Pinata SDK'
};
const jsonResult = await pinata.pinJSONToIPFS(jsonData, {
pinataMetadata: { name: 'NFT-Metadata' }
});
console.log('元数据CID:', jsonResult.IpfsHash);
console.log('NFT URI: ipfs://' + jsonResult.IpfsHash);
}
```


```plaintext
main().catch(console.error);
```


## 其他去中心化存储方案


Filecoin：IPFS的激励层，用代币激励存储提供商

Arweave：一次付费，永久存储，适合NFT数据

Sia：去中心化云存储，主打隐私


## Arweave永久存储


Arweave的宣传语是"Store now, save forever"。一次付费，永久存储——这对NFT来说很有吸引力，因为NFT需要永久保存。


## IPFS的实际应用场景


NFT图片和元数据存储（最常见）

去中心化网站（托管HTML/CSS/JS）

数字凭证和证书

法律文档存证（防篡改）

游戏资产存储

**9. 总结**


## ①  中心化存储有单点故障和审查风险


## ②  IPFS用内容寻址（CID），内容不变地址不变


## ③  Pinata是最流行的IPFS上传服务，提供SDK和API


## ④  ERC721元数据是JSON格式，包含名称、图片、属性


## ⑤  完整铸造流程：上传图片→上传元数据→mintNFT


## ⑥  Filecoin和Arweave是其他去中心化存储方案


━━━━━━━━━━━━━━━━━━━━━

未经授权，禁止转载

如有转载需求，请联系作者

关注我，解锁更多可能