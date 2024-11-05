# Projeto-Litigants

Para ver os meus comentários sobre os processo de desenvolvimento e as decisões que eu tomei leia [COMMENTS.md](./COMMENTS.md).

# Como executar

## mock-api
Para subir a mock-api, execute:

```bash
cd mock-api
```
```bash
docker-compose up --build
```

## backend-graphql
Para subir o graphql que se comunica com a mock-api, execute:

```bash
cd backend-graphql
```
```bash
pnpm i
```
```bash
pnpm run dev
```

## frontend
Para subir o frontend, execute:

```bash
cd frontend-boilerplate
```
```bash
pnpm i
```
```bash
pnpm run dev
```

Você poderá visualizar a página em:

```bash
http://localhost:3000
```

## Exemplo de consulta

Pesquise pelo CNJ `0001234-56.2023.8.19.0001` do TJAL e por `0001234-56.2023.6.19.0001` do TJCE.
- Se não for selecionado nenhum filtro de tribunal a consulta considerará os dois.
- Esses processos são ficticios e mockados, apenas para visualização (possuem todos os campos necessários).

# Como testar
Fiz testes unitários dos principais compoentes do frontend, para executar siga:

```bash
cd frontend-boilerplate
```
```bash
pnpm test
```

Os testes também estão automatizados no github actions.