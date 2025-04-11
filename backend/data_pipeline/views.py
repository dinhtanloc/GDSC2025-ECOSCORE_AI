from rest_framework import viewsets, status
from rest_framework.response import Response
from .services import FullETLPipeline  # hoặc path tùy bạn tổ chức
from backend.config import PROJECT_CFG


class ETLViewSet(viewsets.ViewSet):
    """
    API để trigger quá trình ETL từ frontend.
    """

    def create(self, request):
        try:
            ticket_collection = request.data.get('tickers', [])
            print(ticket_collection)
            mongo_uri = PROJECT_CFG.mongodb_uri
            db_name = PROJECT_CFG.mongodb_name
            postgres_config = PROJECT_CFG.postgrest_dbms
            html_contents = ticket_collection
            doc_dir = f"{PROJECT_CFG.userdata_docdir}/annual_report"
            print("doc_dir", doc_dir)

            pipeline = FullETLPipeline(ticket_collection, postgres_config, mongo_uri, db_name, html_contents, doc_dir)
            pipeline.run_pipeline()

            return Response({'message': 'ETL pipeline completed successfully.'}, status=status.HTTP_200_OK)
        except Exception as e:
            print(f"Error in ETL pipeline: {e}")
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
