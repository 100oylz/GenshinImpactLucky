# GenshinImpact 抽卡模拟工具

## 使用工具

1. requests获取卡池信息
2. json加载json数据，获取对应字典和列表
3. random实现抽卡的流程

## 实现思路

1. 进入原神游戏，进入卡池详情，断网刷新获取url
2. 进入web页面，利用开发者工具获取jsonURL
3. 利用requests截取其中数据
4. 利用json加载数据，得到字典和列表数据类型
5. 切片得到对应的up，普通，武器，人物等属性所对应的物品字典数据类型
6. 将抽卡分成两部分，先判断保底，利用if的先后顺序，先判断5星保底，再利用elif判断4星保底，再进行else，利用random正常概率抽奖（概率为基础概率，非保底概率）

## 优点

1. 概率接近真实抽卡
2. 代码可读性较好，有一定python基础的人能够通过阅读来理解内容（命名较为简洁明了，注释只有部分，且有复制粘贴前面代码，注释的内容可能不准确）

## 缺陷

1. 无法自动获取卡池信息，需要手动设置，且只考虑了2.6版本下半的卡池，卡池数量只有3个

2. 武器池没有定轨（懒得设置了）

   