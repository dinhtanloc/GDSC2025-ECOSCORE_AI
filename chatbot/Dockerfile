# Sử dụng image Python 3.9
FROM python:3.10

# Tạo và đặt thư mục làm việc
WORKDIR /code

# Sao chép file requirements.txt vào container
COPY ../requirements.txt /code/requirements.txt

# Cài đặt các dependencies
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# Sao chép toàn bộ mã nguồn FastAPI vào container
COPY ./app /code/app

EXPOSE 3000

# Chạy ứng dụng FastAPI bằng Uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "3000"]