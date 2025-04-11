from typing import List, Tuple
import uuid
from chatbot.model.config.load_tools_config import LoadToolsConfig
from chatbot.model.agent_graph.build_full_graph import build_graph
from chatbot.model.utils.app_utils import create_directory
from chatbot.model.utils.memory import Memory
# from model.utils.langsmith_metrics import log_event
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

    # @staticmethod
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
            {"messages": [
                ("system", 
                 """
                 Bạn là một AI chuyên gia tư vấn báo cáo phát triển bền vững, có nhiệm vụ trích xuất, phân tích và đánh giá các chỉ số ESG của doanh nghiệp theo tiêu chuẩn GRI (Global Reporting Initiative). Bạn cần sử dụng các công cụ, truy xuất các dữ liệu cần thiết ở các database, truy cập dữ liệu mạng, tìm kiếm thêm thông tin để đưa ra bảng báo cáo ESG. Hãy sử dụng các tools được làm sẵn để trả lời, nếu ko được thì mới tìm trên mạng
                 """
                ),
                ("user", message)
                ]}, 
            {"configurable": {"thread_id": self.thread_id}}, 
            stream_mode="values"
        )
        for event in events:
            event["messages"][-1].pretty_print()

        chatbot.append(
            (message, event["messages"][-1].content))
        response_content = event["messages"][-1].content
        # user_id = userid
        # log_event({
        #         "user_id": user_id,
        #         "user_query": message,
        #         "bot_response": response_content,
        #         "timestamp": datetime.now()
        #     })
        # Memory.write_chat_history_to_cache(
        #     gradio_chatbot=chatbot, thread_id=TOOLS_CFG.thread_id, user=userid
        # )
        Memory.save_chat_interaction(user=self.user_id, thread_id=self.thread_id, user_query=message, response=response_content)
        return "", chatbot
    
    def ESG_score(self, chatbot: List, message: str) -> Tuple:
        """
        Xây dựng một bản báo cáo ESG cho một công ty cụ thể theo chuẩn GRI (Global Reporting Initiative).
        Bản báo cáo này sẽ bao gồm các chỉ số về môi trường, xã hội và quản trị của công ty đó.
        Các thông tin này sẽ được lấy từ một cơ sở dữ liệu SQL hoặc sẽ được lấy từ một tệp PDF được lưu ở MongoDB.
        Nếu không có thông tin nào trong cơ sở dữ liệu, chatbot sẽ tìm kiếm trên mạng.
        Bằng kiến trúc agent_graph, hãy xây dựng một báo cáo ESG cho một công ty cụ thể theo chuẩn GRI (Global Reporting Initiative).

        Tham số:
            chatbot (List): Danh sách đại diện cho lịch sử hội thoại của chatbot.
                            Mỗi mục là một tuple gồm tin nhắn của người dùng và phản hồi của bot.
            message (str): Tin nhắn của người dùng để xử lý.

        Trả về:
            Tuple: Trả về một chuỗi rỗng (đại diện cho placeholder cho đầu vào mới của người dùng)
                   và lịch sử hội thoại đã được cập nhật.
        """
        events = graph.stream(
            {"messages": [
                ("system", 
                 """
                 ###Context###
                    Bạn là một AI chuyên gia tư vấn báo cáo phát triển bền vững, có nhiệm vụ trích xuất, phân tích và đánh giá các chỉ số ESG của doanh nghiệp theo tiêu chuẩn GRI (Global Reporting Initiative). Bạn cần sử dụng các công cụ, truy xuất các dữ liệu cần thiết ở các database, truy cập dữ liệu mạng, tìm kiếm thêm thông tin để đưa ra bảng báo cáo ESG
                ###Input###
                    Mã công ty (str): Thường là mã chứng khoán niêm yết, giúp cho bạn có thể nhận diện chính xác công ty trên sàn chứng khoán Việt Nam
                ###Output###
                    ESG_report: {
                        E (int): Environmental score
                        S (int):  Social score
                        G (int): Governance score
                    }
                    ESG_report là output duy nhất cần gửi về, không trả lời hoặc giải thích gì thêm. Trong trường họp không tính được, mỗi chỉ số hãy chọn một giá trị từ khoảng 0-100 để tính tương đối!
                ### GRI Criteria ###
                    Mục tiêu: Tự động nhận diện, phân loại và chuẩn hóa thông tin theo từng chỉ số GRI từ GRI 301 đến GRI 413 (phiên bản GRI 2016 hoặc mới nhất).
                    Nhóm chỉ số GRI theo 3 trụ cột ESG:
                    E Environmental: GRI 301 → 307
                    S Social: GRI 401 → 409, GRI 413
                    G Governance: GRI 205, GRI 206, GRI 207, GRI 419 (Nếu dùng phiên bản GRI 2021, cập nhật GRI 102 thành GRI 2)
                    Yêu cầu chuẩn hóa thông tin theo cấu trúc:
                    Chỉ số GRI
                    Nội dung đầu vào
                    Giá trị định lượng
                    Đơn vị
                    Năm báo cáo
                    Thiếu sót / Ghi chú
                    Cho phép AI chuyển đổi đơn vị đo lường về hệ SI (ví dụ: kg, tấn, kWh, m³, %).
                    Nếu dữ liệu không có định lượng, AI cần gợi ý người dùng bổ sung hoặc truy vấn thêm từ chuỗi cung ứng hoặc bộ phận liên quan.
                    Những thông tin này, bạn thường có thể dễ dàng tìm kiếm trong các bản báo cáo tài chính thường niên, hoặc thường được công bố công khai trên nền tảng mạng
                ###Note###
                    Trường hợp không thể tính toán chính xác, do thiếu hụt dữ liệu, hãy cho tôi bảng báo cáo ESG giả định, mỗi trường tuân thủ từ 0-100 (chỉ số trung bình thường khoảng các chỉ số random từ 65-90, các chỉ số trong báo cáo không được phép bằng nhau), có định dạng như sau. Lưu ý, câu trả lời của bạn không có giải thích gì thêm, ngoài bảng báo cáo
                    ESG_report{
                    E: ,
                    S:,
                    G: 
                    }
                 """
                ),
                ("user", message)
                ]}, 
            {"configurable": {"thread_id": self.thread_id}}, 
            stream_mode="values"
        )
        for event in events:
            event["messages"][-1].pretty_print()

        chatbot.append(
            (message, event["messages"][-1].content))
        response_content = event["messages"][-1].content
        # user_id = userid
        # log_event({
        #         "user_id": user_id,
        #         "user_query": message,
        #         "bot_response": response_content,
        #         "timestamp": datetime.now()
        #     })
        # Memory.write_chat_history_to_cache(
        #     gradio_chatbot=chatbot, thread_id=TOOLS_CFG.thread_id, user=userid
        # )
        # Memory.save_chat_interaction(user=self.user_id, thread_id=self.thread_id, user_query=message, response=response_content)
        return "", chatbot
