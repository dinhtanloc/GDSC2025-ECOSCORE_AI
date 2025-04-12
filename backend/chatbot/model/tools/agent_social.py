from langchain_core.tools import tool
from langchain_community.utilities import SQLDatabase
from langchain.chains import create_sql_query_chain
from langchain_community.tools.sql_database.tool import QuerySQLDataBaseTool
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from operator import itemgetter
from langchain_openai import ChatOpenAI
from langchain_core.messages import AIMessage, ToolMessage, HumanMessage
from datetime import datetime
from langchain_core.prompts import ChatPromptTemplate
from chatbot.model.tools.tools_finance_calculation import tool_mapping, tools
from chatbot.model.config.load_tools_config import TOOLS_CFG
import json
from chatbot.model.utils.agent_utils import convert_examples_to_messages

class SocialAgent:
    """SocialAgent cho phép mô hình học hỏi từ ví dụ về các truy vấn SQL trước khi trả lời. Tác nhân này, cần phải tìm và thu thập toàn bộ dữ liệu cần thiết của doanh nghiệp theo khía cạnh social, tác nhân này sẽ đánh giá dựa trên độ tích cực, tiêu cực về các bài viết, hoạt động hoặc các bình luận đại chúng. Tác nhân này sẽ được học từ ví dụ, với input là yêu cầu, idea là những bước mà chatbot cần suy luận và phân tích và output là câu trả lời đến người dùng"""

    def __init__(self, llm: str, llm_temperature: float, tools ) -> None:
        """
        Khởi tạo SQLAgent với các cấu hình cần thiết.

        Tham số:
            llm (str): Tên của mô hình ngôn ngữ sẽ được sử dụng để tạo ra và diễn giải các truy vấn SQL.
            llm_temperature (float): Cài đặt nhiệt độ cho mô hình ngôn ngữ, kiểm soát độ ngẫu nhiên của phản hồi.
        """
        self.name='query_social_logic'
        self.llm = ChatOpenAI(
            model=llm, temperature=llm_temperature)
        self.sql_agent_llm=self.llm.bind_tools(tools)
        self.examples = [
            {
                "input": "Đánh giá khía cạnh Social của công ty VNG theo chuẩn quốc tế GRI",
                "idea": (
                    "Step 1: Nhận diện mục tiêu là đánh giá ESG - Khía cạnh Social (GRI 401–409, GRI 413).\n"
                    "Step 2: Tìm kiếm thông tin về hoạt động xã hội, từ thiện, trách nhiệm cộng đồng của VNG.\n"
                    "Step 3: Nếu không có báo cáo chính thức, tìm trên nguồn báo chí (cafef, vnexpress) hoặc các diễn đàn người dùng (tinhte.vn, facebook).\n"
                    "Step 4: Nếu có công cụ phân tích văn bản, áp dụng sentiment analysis để đánh giá độ tích cực của nội dung.\n"
                    "Step 5: Trả về báo cáo có điểm ESG Social ước lượng dựa trên mức độ hoạt động xã hội của doanh nghiệp. Bao gồm các trường: 'ESG Social Score', 'Hoạt động nổi bật', 'Nguồn trích dẫn nếu có'."
                ),
                "output": (
                    "Đánh giá khía cạnh Social của VNG:\n"
                    "{\n"
                    "  'ESG Social Score': 88,\n"
                    "  'Hoạt động nổi bật': 'VNG tài trợ học bổng cho học sinh vùng sâu, tổ chức hội thảo kỹ năng nghề nghiệp cho sinh viên',\n"
                    "  'Nguồn': 'vnexpress.net, tinhte.vn'\n"
                    "}"
                )
            },
            {
                "input": "Công ty MWG có đóng góp gì cho cộng đồng không?",
                "idea": (
                    "Step 1: Tìm kiếm bài viết, tin tức, hoặc phát biểu từ đại diện MWG liên quan đến từ thiện, trách nhiệm cộng đồng.\n"
                    "Step 2: Tổng hợp thông tin từ các nguồn tin tức (cafef, laodong, vnexpress).\n"
                    "Step 3: Trích dẫn những hoạt động tiêu biểu nếu có: hỗ trợ thiên tai, chương trình giáo dục, v.v.\n"
                    "Step 4: Chấm điểm ESG xã hội ước lượng theo thang điểm 100."
                ),
                "output": (
                    "MWG thường xuyên tổ chức các hoạt động thiện nguyện như tặng thiết bị học tập cho học sinh vùng cao. ESG Social Score: 92/100."
                )
            }
        ]
        few_shot_messages = convert_examples_to_messages(self.examples)
        self.system_role = f"""Bạn là một chuyên gia chơi chứng khoán trong lĩnh vực kinh tế đầu tư tại thị trường chứng khoán Việt Nam. Hôm nay là ngày {datetime.now().strftime('%Y-%m-%d')}. Sử dụng các tool được cung cấp như một ví dụ để đưa ra những lời khuyên hữu ích để người chơi mới tại Việt Nam lựa chọn và tối ưu hóa danh mục đầu tư, đầu tư chứng khoán thành công
        """

        few_shot_prompt = ChatPromptTemplate.from_messages(
            [
                ("system", self.system_role),
                *few_shot_messages,
                ("human", "{query}"),
            ]
        )


        self.chain = {"query": RunnablePassthrough()} | few_shot_prompt | self.sql_agent_llm




@tool('query_social_logic')
def query_social_logic(ques: str) -> str:
    """Truy vấn dữ liệu thị trường chứng khoán từ cơ sở dữ liệu SQL, hoặc truy xuất thông tin document trong collection qua vectorsearch, hoặc tìm thông tin trên mạng."""
    messages = [HumanMessage(ques)]
    print("query_social_logic", ques)
    agent = SocialAgent(
        llm=TOOLS_CFG.funcagent_llm,
        llm_temperature=TOOLS_CFG.funcagent_llm_temperature,
        tools=tools
    )
    ai_msg = agent.chain.invoke({"query": ques})
    messages.append(ai_msg)
    for tool_call in ai_msg.tool_calls:
        print(tool_call)
        selected_tool = tool_mapping[tool_call["name"].lower()]
        print(tool_call["args"])
        tool_output = selected_tool.invoke(dict(tool_call["args"]))
        # if isinstance(tool_output, (dict, list)):
        #     tool_output = json.dumps(tool_output)
        messages.append(ToolMessage(tool_output, tool_call_id=tool_call["id"]))
    res =agent.chain.invoke(messages)
    response=str(res.content)
    return response
