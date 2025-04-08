# Sử dụng Node.js 18 Alpine làm image cơ bản
FROM node:18-alpine AS development

# Đặt thư mục làm việc trong container
WORKDIR /app

# Sao chép package.json và package-lock.json
COPY package*.json ./

# Cài đặt dependencies
RUN npm install --legacy-peer-deps

# Sao chép toàn bộ mã nguồn vào container
COPY . .

# Mở cổng 5173 (default port của React/Vite)
EXPOSE 5173

# Chạy ứng dụng trong chế độ phát triển
CMD ["npm", "run", "dev"]