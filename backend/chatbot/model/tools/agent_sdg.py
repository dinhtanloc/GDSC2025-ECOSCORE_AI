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

class SDGAgent:
    """SDGAgent cho phép mô hình học hỏi từ ví dụ về các truy vấn SQL trước khi trả lời. Tác nhân này, cần phải tìm và thu thập toàn bộ dữ liệu cần thiết của doanh nghiệp theo lĩnh vực xanh để thực hiện tính toán. Tác nhân này sẽ được học từ ví dụ, với input là yêu cầu, idea là những bước mà chatbot cần suy luận và phân tích và output là câu trả lời đến người dùng"""

    def __init__(self, llm: str, llm_temperature: float, tools ) -> None:
        """
        Khởi tạo SQLAgent với các cấu hình cần thiết.

        Tham số:
            llm (str): Tên của mô hình ngôn ngữ sẽ được sử dụng để tạo ra và diễn giải các truy vấn SQL.
            llm_temperature (float): Cài đặt nhiệt độ cho mô hình ngôn ngữ, kiểm soát độ ngẫu nhiên của phản hồi.
        """
        self.name='query_sdg_logic'
        self.llm = ChatOpenAI(
            model=llm, temperature=llm_temperature)
        self.sql_agent_llm=self.llm.bind_tools(tools)
        self.examples = [
            {
                "input": "Đánh giá công ty VNG theo khía cạnh Environmental",
                "idea": (
                    "Identify intent: ESG evaluation - Environmental (GRI 301–307).\n"
                    "Step 1: Truy xuất vào cơ sở dữ liệu hoặc tìm từ các nguồn trên mạng để tìm thông tin`.\n"
                    "Step 2: Trích xuất những trường sau, có thể là tiếng anh hoặc tiếng việt: 'Net Sales', 'Environmental Cost', 'Energy Cost'.\n"
                    "Step 3: Nếu ko có trường về cây cỏ hãy tìm thử 'Selling Expenses' or 'Other Expenses'.\n"
                    "Step 4: Tính toán phân tích theo chuẩn GRI trụ cột E, đánh giá trên thang 100.\n"
                    "Step 5: Trả về kết quả dưới dạng JSON với các trường: 'ESG Score', 'Environmental Cost', 'Net Sales'.\n"
                ),
                "output": (
                    "Bảng báo cáo ESG cho công ty VNG theo khía cạnh Environmental:\n"
                        "{\n"
                        "  'ESG Score': 85,\n"
                        "  'Environmental Cost': 1200000000,\n"
                        "  'Net Sales': 145000000000\n"
                        "}"
                )
            },
            {
                "input": "Phân tích ESG xã hội của CTCP MWG",
                "idea": (
                    "Identify intent: ESG evaluation - Social (GRI 401–409, GRI 413).\n"
                    "Step 1: Lấy báo cáo tài chính của doanh nghiệp từ API hoặc website.\n"
                    "Step 2: Trích xuất các trường như: 'Chi phí đào tạo', 'Chi phí xã hội', 'CSR Cost', hoặc các chương trình cộng đồng.\n"
                    "Step 3: Ước lượng nếu không có: tìm từ 'Selling Expenses' hoặc tìm bài viết/CSR report nếu có.\n"
                    "Step 4: Tính tỉ lệ các khoản này trên doanh thu thuần.\n"
                    "Step 5: Dùng chuẩn 1% để tính điểm ESG xã hội (trên thang 100).\n"
                    "Step 6: Trả kết quả dạng JSON: 'ESG Score', 'Social Cost', 'Revenue'."
                ),
                "output": (
                    "Báo cáo ESG khía cạnh xã hội của CTCP MWG:\n"
                    "{\n"
                    "  'ESG Score': 72,\n"
                    "  'Social Cost': 870000000,\n"
                    "  'Revenue': 97000000000\n"
                    "}"
                )
            },
            {
                "input": "Tôi cần báo cáo ESG Governance cho mã FPT",
                "idea": (
                    "Identify intent: ESG Governance (GRI 205, 206, 419).\n"
                    "Step 1: Tìm thông tin về cấu trúc quản trị công ty từ trang web công ty hoặc database.\n"
                    "Step 2: Trích xuất các trường: 'Board diversity', 'Anti-corruption policy', 'Independent Directors', 'Quản trị rủi ro', 'Chính sách công khai thông tin'.\n"
                    "Step 3: Nếu không có số liệu định lượng, đánh giá định tính dựa trên mức độ hiện diện và minh bạch.\n"
                    "Step 4: Áp dụng hệ thống tính điểm dựa trên presence/absence và completeness.\n"
                    "Step 5: Trả về dưới dạng JSON: 'Governance Score', 'Disclosure', 'Board Info'."
                ),
                "output": (
                    "Báo cáo ESG Governance cho mã FPT:\n"
                    "{\n"
                    "  'Governance Score': 78,\n"
                    "  'Disclosure': 'Full compliance with public listing transparency rules',\n"
                    "  'Board Info': '40% independent, 25% female representation'\n"
                    "}"
                )
            }
        ]
        few_shot_messages = convert_examples_to_messages(self.examples)

        self.system_role = f"""Bạn là một chuyên gia phân tích và xây dựng báo cáo ESG chuẩn GRI. Hôm nay là ngày {datetime.now().strftime('%Y-%m-%d')}. Sử dụng các tool được cung cấp để tính toán các chỉ số một cách thành công và trả được chỉ số theo trụ cột E, Environmental
        """

        few_shot_prompt = ChatPromptTemplate.from_messages(
            [
                ("system", self.system_role),
                *few_shot_messages,
                ("human", "{query}"),
            ]
        )


        self.chain = {"query": RunnablePassthrough()} | few_shot_prompt | self.sql_agent_llm




@tool('query_sdg_logic')
def query_sdg_logic(ques: str) -> str:
    """Truy vấn dữ liệu thị trường chứng khoán từ cơ sở dữ liệu SQL, hoặc truy xuất thông tin document trong collection qua vectorsearch, hoặc tìm thông tin trên mạng."""
    print("query_sdg_logic", ques)
    messages = [HumanMessage(ques)]
    agent = SDGAgent(
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
