# Сборка
FROM node:18 as builder

WORKDIR /app

COPY . .
RUN npm install
RUN npm run build

# Продакшн-сервер (nginx)
FROM nginx:alpine

COPY --from=builder /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf
