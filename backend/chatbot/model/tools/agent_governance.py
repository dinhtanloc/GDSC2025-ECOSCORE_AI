from langchain_core.tools import tool
from langchain_community.utilities import SQLDatabase
from langchain.chains import create_sql_query_chain
from langchain_community.tools import QuerySQLDatabaseTool

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

class GovernanceAgent:
    """FinanceAgent cho phép mô hình học hỏi từ ví dụ về các truy vấn SQL trước khi trả lời. Cho phép đánh giá xem, dựa vào tình hình kinh tế của VNindex nói chung và tình hình của mã công ty nói riêng, đánh giá sức khỏe của doanh nghiệp"""

    def __init__(self, llm: str, llm_temperature: float, tools ) -> None:
        """
        Khởi tạo FinanceAgent với các cấu hình cần thiết.

        Tham số:
            llm (str): Tên của mô hình ngôn ngữ sẽ được sử dụng để tạo ra và diễn giải các truy vấn SQL.
            llm_temperature (float): Cài đặt nhiệt độ cho mô hình ngôn ngữ, kiểm soát độ ngẫu nhiên của phản hồi.
        """
        self.name='query_governance_logic'
        self.llm = ChatOpenAI(
            model=llm, temperature=llm_temperature)
        self.sql_agent_llm=self.llm.bind_tools(tools)
        self.examples = [
            HumanMessage(content="Bạn hãy đánh giá công ty VNG theo khía cạnh Governance theo chuẩn quốc tế?"),
            AIMessage(content=(
                "Bảng đánh giá ESG - Governance cho công ty VNG:\n"
                "{\n"
                "  \"ESG Governance Score\": 80,\n"
                "  \"Tax Transparency\": \"Đóng thuế đầy đủ, không có khiếu kiện tài chính\",\n"
                "  \"Training Investment\": \"Đầu tư 3 tỷ vào đào tạo nội bộ năm 2023\",\n"
                "  \"Net Profit\": \"Lợi nhuận sau thuế năm 2023 đạt 120 tỷ VND\"\n"
                "}"
            )),

            HumanMessage(content="MWG có đảm bảo quản trị tốt không?"),
            AIMessage(content=(
                "MWG có hệ thống quản trị minh bạch, đóng thuế đúng hạn, không có khiếu kiện lớn.\n"
                "Điểm ESG Governance: 92/100"
            )),
        ]
        
        # self  = convert_examples_to_messages(self.examples)
        self.system_role = f"""Bạn là một chuyên gia phân tích và xây dựng báo cáo ESG chuẩn GRI. Hôm nay là ngày {datetime.now().strftime('%Y-%m-%d')}. Sử dụng các tool được cung cấp để tính toán các chỉ số một cách thành công và trả được chỉ số theo trụ cột G, Governance.
        """

        few_shot_prompt = ChatPromptTemplate.from_messages(
            [
                ("system", self.system_role),
                # *self.examples,
                ("human", "{query}"),
            ]
        )


        self.chain = {"query": RunnablePassthrough()} | few_shot_prompt | self.sql_agent_llm




@tool('query_governance_logic')
def query_governance_logic(ques: str) -> str:
    """Truy vấn dữ liệu thị trường chứng khoán từ cơ sở dữ liệu SQL, hoặc truy xuất thông tin document trong collection qua vectorsearch, hoặc tìm thông tin trên mạng."""
    print("query_governance_logic", ques)
    messages = [HumanMessage(ques)]
    agent = GovernanceAgent(
        llm=TOOLS_CFG.funcagent_llm,
        llm_temperature=TOOLS_CFG.funcagent_llm_temperature,
        tools=tools
    )
    ai_msg = agent.chain.invoke(ques)
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
