FROM node:18

WORKDIR /app-backend

COPY . .

EXPOSE 4000

RUN npm install -g pnpm && pnpm install

CMD ["pnpm", "run", "dev"]