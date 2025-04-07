from typing import List, Tuple
import uuid
from chatbot.configs.config import LoadToolsConfig
from chatbot.models.agent_graph.build_full_graph import build_graph
from chatbot.models.utils.app_utils import create_directory
from chatbot.models.utils.memory import Memory
from datetime import datetime
import pytesseract
from PIL import Image


TOOLS_CFG = LoadToolsConfig()

graph = build_graph()


class ChatBot:
    """
    Lớp này chịu trách nhiệm xử lý các tương tác với chatbot bằng cách sử dụng một đồ thị tác nhân đã được định nghĩa trước.
    Chatbot tiếp nhận tin nhắn từ người dùng, sinh ra phản hồi thích hợp và lưu trữ lịch sử hội thoại vào thư mục bộ nhớ đã chỉ định.

    Thuộc tính:
        config (dict): Một từ điển cấu hình lưu trữ các thiết lập cụ thể như `thread_id`.

    Phương thức:
        respond(chatbot: List, message: str, userid: int) -> Tuple:
            Xử lý tin nhắn người dùng thông qua đồ thị tác nhân, sinh ra phản hồi,
            thêm phản hồi vào lịch sử hội thoại và lưu lịch sử hội thoại vào một tệp bộ nhớ.
    """
    def __init__(self, user_id, thread_id=None):
        self.thread_id = thread_id or str(uuid.uuid4())
        self.user_id = user_id

    def respond(self, chatbot: List, message: str) -> Tuple:
        """
        Xử lý một tin nhắn từ người dùng bằng cách sử dụng đồ thị tác nhân, sinh ra phản hồi và thêm phản hồi vào lịch sử hội thoại.
        Lịch sử hội thoại cũng được lưu vào một tệp bộ nhớ để tham khảo trong tương lai.

        Tham số:
            chatbot (List): Danh sách đại diện cho lịch sử hội thoại của chatbot.
                            Mỗi mục là một tuple gồm tin nhắn của người dùng và phản hồi của bot.
            message (str): Tin nhắn của người dùng để xử lý.

        Trả về:
            Tuple: Trả về một chuỗi rỗng (đại diện cho placeholder cho đầu vào mới của người dùng)
                   và lịch sử hội thoại đã được cập nhật.
        """
        events = graph.stream(
            {"messages": [("user", message)]}, 
            {"configurable": {"thread_id": self.thread_id}}, 
            stream_mode="values"
        )
        for event in events:
            event["messages"][-1].pretty_print()

        chatbot.append(
            (message, event["messages"][-1].content))
        response_content = event["messages"][-1].content
        Memory.save_chat_interaction(user=self.user_id, thread_id=self.thread_id, user_query=message, response=response_content)
        return "", chatbot
