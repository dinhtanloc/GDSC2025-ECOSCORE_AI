from langchain_core.tools import tool
import sys,os
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
# os.environ['DJANGO_SETTINGS_MODULE'] = 'backend.settings'
from langchain_community.utilities import SQLDatabase
from langchain.chains import create_sql_query_chain
from langchain_community.tools import QuerySQLDatabaseTool

from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from operator import itemgetter
from langchain_openai import ChatOpenAI
from chatbot.model.config.load_tools_config import TOOLS_CFG



class SQLAgent:
    """
    Lớp này đại diện cho một tác nhân SQL, sử dụng mô hình ngôn ngữ để tạo và thực thi các truy vấn SQL trên cơ sở dữ liệu. Đây là nơi để lấy toàn bộ thông tin về hoạt động của doanh nghiệp, tình hình tài chính trong những năm gần đây, thực hiện các chỉ số ESG của doanh nghiệp, từ đó đưa ra những phân tích và dự đoán về tình hình hoạt động của doanh nghiệp trong tương lai. Chúng ta sẽ đánh giá theo chuẩn GRI, tác nhân này có nhiệm vụ chính phải đánh giá được tình hình công ty thông qua khía cạnh kinh doanh, hoạt động tài chính, và đánh giá những hoạt động của công ty đến với môi trường, xã hội và quản trị. 
    Nó sử dụng một mô hình ngôn ngữ để tạo ra các truy vấn SQL và sau đó thực thi chúng trên cơ sở dữ liệu SQL. Kết quả từ cơ sở dữ liệu sẽ được sử dụng để trả lời các câu hỏi của người dùng.

    Các thuộc tính:
        sql_agent_llm (ChatOpenAI): Một phiên bản của mô hình ngôn ngữ ChatOpenAI được sử dụng để tạo và xử lý các truy vấn SQL.
        system_role (str): Một mẫu nhắc hệ thống hướng dẫn mô hình ngôn ngữ trong việc trả lời các câu hỏi của người dùng dựa trên kết quả truy vấn SQL.
        db (SQLDatabase): Một phiên bản của cơ sở dữ liệu SQL được sử dụng để thực thi các truy vấn.
        chain (RunnablePassthrough): Một chuỗi các thao tác tạo ra các truy vấn SQL, thực thi chúng và tạo ra một phản hồi.

    Các phương thức:
        __init__: Khởi tạo SQLAgent bằng cách thiết lập mô hình ngôn ngữ, cơ sở dữ liệu SQL và quy trình trả lời truy vấn.

    """

    def __init__(self, llm: str, llm_temerature: float) -> None:
        """
        Khởi tạo SQLAgent với các cấu hình cần thiết.

        Tham số:
            llm (str): Tên của mô hình ngôn ngữ sẽ được sử dụng để tạo ra và diễn giải các truy vấn SQL.
            llm_temperature (float): Cài đặt nhiệt độ cho mô hình ngôn ngữ, kiểm soát độ ngẫu nhiên của phản hồi.
        """
        self.name='query_stock_sqldb'
        self.sql_agent_llm = ChatOpenAI(
            model=llm, temperature=llm_temerature)
        self.system_role = """Given the following user question, corresponding SQL query, and SQL result, answer the user question.\n
            Question: {question}\n
            SQL Query: {query}\n
            SQL Result: {result}\n
            Answer:
            """
        self.db = SQLDatabase.from_uri(
            TOOLS_CFG.stock_db)
        print(self.db.get_usable_table_names())

        execute_query = QuerySQLDatabaseTool(db=self.db)
        write_query = create_sql_query_chain(
            self.sql_agent_llm, self.db)
        answer_prompt = PromptTemplate.from_template(
            self.system_role)

        answer = answer_prompt | self.sql_agent_llm | StrOutputParser()
        self.chain = (
            RunnablePassthrough.assign(query=write_query).assign(
                result=itemgetter("query") | execute_query
            )
            | answer
        )


@tool('query_stock_sqldb')
def query_stock_sqldb(query: str) -> str:
    """Truy vấn dữ liệu thị trường chứng khoán Việt Nam từ cơ sở dữ liệu SQL Vnstock và truy cập toàn bộ thông tin công ty, sự kiện. Đầu vào nên là một truy vấn tìm kiếm."""
    agent = SQLAgent(
        llm=TOOLS_CFG.sqlagent_llm,
        llm_temerature=TOOLS_CFG.sqlagent_llm_temperature
    )
    response = agent.chain.invoke({"question": query})
    return response

