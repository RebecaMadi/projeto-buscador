FROM node:18

WORKDIR /app-frontend

COPY . .

EXPOSE 3003

RUN npm install -g pnpm && pnpm install

CMD ["pnpm", "run", "dev"]