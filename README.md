# 简介
相比于那些更繁杂的ai本地化记忆agent，ezmem提供了一个超轻量级，无需额外挂载数据库，上手即用的简单记忆逻辑  
## 使用 pip 安装
```bash
pip install ezmem
```
## 功能示例  
### 搭建示例
<img src="./images/pic1.jpg" alt="Example 1" width="800" />  

### 效果展示
<div style="display: flex; justify-content: space-around; align-items: center;">
  <img src="./images/example1.jpg" alt="Example 1" width="300"/>
  <img src="./images/example2.jpg" alt="Example 2" width="300"/>
</div>

## 简易上手
```python
from ezmem import EasyMemory #导入包

config = OpenAI(
    api_key="填入您自己的api",
    base_url="填入您自己的url",
)#api_key 以及 base_url配置

m = EasyMemory(config) #创建memory实例

m.add(text,user_id)#将记忆信息记录进user_id中

memory = m.query(user_id)#根据user_id查询记忆内容

answer = m.chat(text,rule)#text：用户聊天信息，rule：ai遵循规则

m.delete_all(user_id)#删除user_id的所有记忆信息
```
