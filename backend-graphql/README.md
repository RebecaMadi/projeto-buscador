# Justarter - Backend Template

## Pré-requisitos

- [Node.js](https://nodejs.org/en/)
- [pnpm](https://pnpm.io/)

Você pode usar uma ferramenta como o [asdf](https://asdf-vm.com/) para instalar e gerenciar as versões do Node.js. As versões recomendadas estão no arquivo `.tool-versions`.

## Iniciando

Após clonar o repositório, instale as dependências com o comando:

```bash
pnpm i
```

Isso deve ser o suficiente para começar a desenvolver com o comando:

```bash
pnpm dev
```

Abra [http://localhost:4000](http://localhost:4000) com o seu navegador para ver o playground do graphql.

## Comandos

| Comando           | Descrição                            |
| ----------------- | ------------------------------------ |
| `pnpm dev`        | Inicia o servidor de desenvolvimento |
| `pnpm build`      | Realiza o build da aplicação (não necessário para ambiente de desenvolvimento) |
| `pnpm start`      | Inicia o servidor com o build gerado |
| `pnpm lint`       | Roda a ferramenta de lint (ESLint)   |
| `pnpm test`       | Roda os testes                       |
| `pnpm test:watch` | Roda os testes em modo watch         |

Outros comandos podem ser encontrados no arquivo `package.json`, mas esses são os principais.


## Estrutura do projeto
#### `src/index.js`
Esse arquivo contém as configurações necessários para iniciar o servidor graphql.

#### `apis/`
Este diretório é responsável pela comunicação com APIs externas e serviços mock. Os arquivos dentro deste diretório implementam interfaces para APIs externas.

- **Exemplo de Arquivos:**
  - `httpClient.js`: Implementa um cliente HTTP genérico, usando Axios, para gerenciar requisições a endpoints externos.
  - `mockAPI.js`: implementar os métodos disponíveis pela API de mock para facilitar o desenvolvimento sem dependência de um backend real.
  - `tests/`: Contém testes unitários para validar a funcionalidade dos clientes HTTP e APIs.

#### Adicionando Novas APIs
Para incluir um novo cliente de API:
1. Crie um novo arquivo no diretório `apis/` com um nome descritivo, por exemplo, `newApi.js`.
2. Implemente a lógica de requisição usando o `httpClient.js` como base.
3. Se for incluir testes, adicione um arquivo no subdiretório `tests/`.

#### `schema/`
Este diretório contém as definições de schema GraphQL para a aplicação, organizando a estrutura dos dados que serão manipulados e expostos.

- **Arquivo Principal:**
  - `index.js`: Serve como ponto de entrada que consolida e exporta todos os schemas definidos, definindo os types de `Query` e `Mutation` agregando campos a partir dos types incluídos.

#### Atualizando o `schema/index.js`
Ao adicionar um novo "type" no projeto, ele vai ser importado automaticamente no schema do graphql. No entanto, para funcionar corretamente, você precisar exportar no `index.js` de cada type o seguinte formato:
```
export default {
  mutations,
  queries,
  typeDefs,
};
```

#### `types/`
O diretório `types/` armazena definições de types e funcionalidades relacionadas a diferentes entidades do projeto. Ele está subdividido em módulos específicos.

##### Estrutura dos Subdiretórios
Os types `Address` e `User` são apenas exemplos e não vão ser necessários para o desafio final. Você pode remover esses types quando fizer o fork do repositório.

- **`address/`**
  - `index.js`: Ponto de entrada para types relacionados a endereços.
  - `typeDefs.js`: Contém as definições de types GraphQL específicas para endereços.

- **`user/`**
  - `index.js`: Ponto de entrada para os types relacionados a usuários.
  - `mutations/`: Implementa as mutations relacionadas a usuários.
    - `createUser.js`: Contém a lógica para a mutation que cria um novo usuário.
    - `index.js`: Consolida e exporta todas as mutations de usuário.
  - `queries/`: Implementa as queries relacionadas a usuários.
    - `getUser.js`: Contém a lógica para a query que obtém informações de um usuário.
    - `index.js`: Consolida e exporta todas as queries de usuário.
  - `typeDefs.js`: Define os types e estruturas de dados GraphQL para usuários.
  - `usersMock.js`: Fornece mocks de dados de usuários para testes e desenvolvimento.

#### Adicionando novos Types
1. Crie um subdiretório dentro de `types/` para a nova entidade.
2. Dentro do subdiretório, implemente os arquivos necessários, como `index.js`, `typeDefs.js`, e pastas para `queries/` e `mutations`.
3. Lembre-se de exportar o novo type corretamente.

---

## O que está incluso nesse boilerplate?

Todas as ferramentas já estão configuradas e prontas para uso. Aqui, vocês irão encontrar:

- [Apollo Server](https://www.apollographql.com/docs/apollo-server), uma biblioteca para GraphQL no lado servidor. 
- [Axios](https://axios-http.com), um cliente para requisições HTTP.
- [ESLint](https://eslint.org/), para manter o código limpo e consistente.
- [Prettier](https://prettier.io/), para manter o código formatado.
- [Jest](https://jestjs.io/), para testes unitários.

