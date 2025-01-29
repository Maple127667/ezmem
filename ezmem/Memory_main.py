from .deepseek import get_chat_messages
from .Prompt import prompt
import sqlite3
from openai import OpenAI

DATABASE_PATH = 'memory.db'

def initialize_db():
    """
    初始化数据库，确保内存表存在。
    """
    with sqlite3.connect(DATABASE_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS memories (
                user_id TEXT PRIMARY KEY,
                memory TEXT NOT NULL
            )
        ''')
        conn.commit()

# 调用一次以确保数据库和表已创建


class EasyMemory():
    """
    用于管理和操作用户记忆的类。
    """
    client : OpenAI
    def __init__(self, client:OpenAI):
        """
        初始化EasyMemory类。
        client : OpenAI
        """
        self.client = client
        initialize_db()

    def abstraction(self, text_input: str) -> str:
        """
        简化输入的聊天内容。

        :param text_input: 输入的聊天内容。
        :type text_input: str
        :return: 简化后的内容，如果不需要记忆则返回"None"。
        :rtype: str
        """
        ans = get_chat_messages(text_input, rule=prompt.abstraction, client=self.client)
        ans = ans.choices[0].message.content
        return ans

    def GetUpdate(self, new_mem: str, old_mem: str) -> str:
        """
        合并新旧记忆信息。

        :param new_mem: 新的记忆信息。
        :type new_mem: str
        :param old_mem: 旧的记忆信息。
        :type old_mem: str
        :return: 合并后的记忆信息。
        :rtype: str
        """
        ans = get_chat_messages(
            f"old_memory: {old_mem}\nnew_memory: {new_mem}", 
            rule=prompt.optimized_instruction,
            client=self.client
        )
        ans = ans.choices[0].message.content
        return str(ans)

    @staticmethod
    def query(user_id: str) -> str:
        """
        查询指定用户的记忆信息。

        :param user_id: 用户的唯一标识符。
        :type user_id: str
        :return: 用户的记忆信息，如果不存在则返回None。
        :rtype: str
        """
        with sqlite3.connect(DATABASE_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT memory FROM memories WHERE user_id = ?', (user_id,))
            result = cursor.fetchone()
            if result is not None:
                return result[0]  # 返回 memory 字段的内容
            else:
                return None  # 如果没有找到对应的记录，则返回 None

    @staticmethod
    def update(user_id: str, memory: str):
        """
        更新或插入用户的记忆信息。

        :param user_id: 用户的唯一标识符。
        :type user_id: str
        :param memory: 新的记忆信息。
        :type memory: str
        """
        with sqlite3.connect(DATABASE_PATH) as conn:
            cursor = conn.cursor()
            try:
                cursor.execute('INSERT INTO memories (user_id, memory) VALUES (?, ?)', (user_id, memory))
                conn.commit()
            except sqlite3.IntegrityError:
                # 如果 user_id 已经存在，则更新现有的记录
                cursor.execute('UPDATE memories SET memory = ? WHERE user_id = ?', (memory, user_id))
                conn.commit()

    def add(self, text: str, user_id: int) -> str:
        """
        添加新的记忆信息，并更新用户的记忆。

        :param text: 输入的聊天内容。
        :type text: str
        :param user_id: 用户的唯一标识符。
        :type user_id: int
        :return: 简化后的文本、旧记忆和新记忆的组合信息。
        :rtype: str
        """
        # 调用 AI 简化聊天信息
        simplified_text = self.abstraction(text)

        # 检查简化结果
        if simplified_text == "None":
            return '记忆无效'
        
        # 查询用户当前的 profile
        profile = self.query(user_id)

        # 如果 profile 不为空，调用 GetUpdate 结合新旧 profile
        if profile is not None:
            new_profile = self.GetUpdate(new_mem=simplified_text, old_mem=profile)
        else:
            # 如果用户不存在或当前 profile 为空，直接使用 simplified_text
            new_profile = simplified_text

        self.update(user_id=user_id, memory=new_profile)

        return f'simplified_text:{simplified_text}\nold_mem:{profile}\nnew_mem:{new_profile}'

    @staticmethod
    def delete_all(user_id: str) -> str:
        """
        删除指定用户的所有记忆信息。

        :param user_id: 用户的唯一标识符。
        :type user_id: str
        :return: 删除操作的确认信息。
        :rtype: str
        """
        with sqlite3.connect(DATABASE_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM memories WHERE user_id = ?', (user_id,))
            conn.commit()
        
        # 确认删除操作
        if cursor.rowcount > 0:
            return f"Deleted all records for user_id: {user_id}"
        else:
            return f"No records found for user_id: {user_id}"
        
    def chat(self, text: str, rule: str) -> str:
        """
        与AI进行聊天交互。

        :param prompt: 聊天提示信息。
        :type prompt: str
        :param rule: 聊天规则。
        :type rule: str
        """
        return get_chat_messages(prompt_text=text, rule=rule,client=self.client).choices[0].message.content