# Justarter - Frontend Template

## Pré-requisitos

- [Node.js](https://nodejs.org/en/)
- [pnpm](https://pnpm.io/)

Você pode usar uma ferramenta como o [asdf](https://asdf-vm.com/) para instalar e gerenciar as versões do Node.js. As versões recomendadas estão no arquivo `.tool-versions`.

## Iniciando

Após clonar o repositório, instale as dependências com o comando:

```bash
pnpm i
```

Atualize a variável de ambiente `GRAPHQL_URL` no arquivo `.env.local` com a URL da API que você irá utilizar.

```bash
cp .env.local.example .env.local
```

Isso deve ser o suficiente para começar a desenvolver com o comando:

```bash
pnpm dev
```

Abra [http://localhost:3000](http://localhost:3000) com o seu navegador para ver o resultado.

## Comandos

| Comando           | Descrição                            |
| ----------------- | ------------------------------------ |
| `pnpm dev`        | Inicia o servidor de desenvolvimento |
| `pnpm lint`       | Roda a ferramenta de lint (ESLint)   |
| `pnpm test`       | Roda os testes                       |
| `pnpm test:watch` | Roda os testes em modo watch         |
| `pnpm test:e2e` | Roda os testes de integração usando o Cypress         |

Outros comandos podem ser encontrados no arquivo `package.json`, mas esses são os principais.

## O que está incluso nesse boilerplate?

Todas as ferramentas já estão configuradas e prontas para uso. Aqui, vocês irão encontrar:

- [Next.js](https://nextjs.org/), um framework React.
- [ESLint](https://eslint.org/), para manter o código limpo e consistente.
- [Prettier](https://prettier.io/), para manter o código formatado.
- [Jest](https://jestjs.io/), para testes unitários.
- [React Testing Library](https://testing-library.com/docs/react-testing-library/intro/), para testes de componentes.
- [TypeScript](https://www.typescriptlang.org/), para adicionar tipagem ao JavaScript.
- [Apollo Client](https://www.apollographql.com/docs/react/), para fazer requisições GraphQL.
- [Radix UI](https://ui.shadcn.com/), para componentes de UI.
- [Cypress](https://www.cypress.io/), para testes de integração.
