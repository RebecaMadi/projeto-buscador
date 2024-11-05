# Comentários do Projeto

## Introdução
Projeto com a finalidade de desenvolver um produto com o qual um usuário comum possa interagir. Durante o desenvolvimento, foi possível aprofundar o entendimento sobre frontend e desenvolvimento web, explorando diferentes fluxos de interação para personalizar a experiência de acordo com a jornada de cada usuário.

## Diagrama de Sequencia
Fiz um diagrama de sequencia que me ajudou a organizar melhor as ideias, [veja!](./imagens/diagrama_seq_front.png)

## Pastas
- **Frontend**
    - `/src`: Contém o código-fonte principal.
    - `/src/components`: Contém componentes reutilizáveis do frontend.
    - `/src/pages/index.tsx`: Página inicial do projeto que inclui a lógica de busca e exibição.
    - `/src/styles`: Contém a estilização dos componentes.
- **Backend-GraphQL**
    - `/src`: Contém o código-fonte principal.
    - `/src/schema`: Possui o schema geral das queries e mutations aceitas pelo GraphQL.
    - `/src/schema/types`: Possui os as definições dos tipos de estruturas, queries e mutations específicas.
- **mock-api**
    - `/src`: Contém o código-fonte principal.
    - `/src/argos-lock`: Contém as variantes de experimentos.
    - `/src/box-lock`: Contém as informações do modal de ofertas.
    - `/src/data`: Contém dois processos ficticios mockados.

## Decisões de Design
1. **Arquitetura**: A mock API opera como uma API REST que fornece dados para o frontend. O GraphQL atua como um intermediário, comunicando-se com a API REST e oferecendo uma interface unificada para o frontend. O frontend foi desenvolvido como uma SPA (Single Page Application), realizando consultas e alterações por meio do GraphQL.
    - *Observação*: Optei por usar a mock API neste projeto, em vez de minhas próprias APIs desenvolvidas anteriormente, pois estou em uma semana de entrega de trabalhos na faculdade. Assim, decidi implementar apenas o essencial. No entanto, todas as tipagens de dados e estruturas foram padronizadas com base nos projetos anteriores para facilitar uma futura integração.
2. **Frameworks e Bibliotecas**: React, Next.js e Apollo Client

## Variantes de Experimento
### control e variant-a
A variante de controle possui um fluxo em que os usuários podem interagir livremente comos conteúdos do site. A variante variant-a possui um fluxo em que os usuários são bloqueados de veren a ultima movimentação de um processo. Na variant-a os usuários só conseguem visualizar a ultima movimentação se clicarem para visualizar a oferta e a aceitarem.

- `participante`: considerei que inicialmente esse parametro é sempre falso, ele só fica verdadeiro se o usuário estiver na variante variant-a e por acaso clicar para visualizar os detalhes de um processo, ou seja, só fica verdadeiro quando ele visualiza a mudança de fluxo.
- `sorteio`: toda vez que a página é carregada uma variante é sorteado para o usuário. É possível visualizar no log da inspeção.

### Simulação
Tive certa dificuldade para entender como implementar a simulação, minha decisão foi:
- Criar uma variável `simulating` no index.js da página principal, essa variável só pode ser mudada através do código. Fiz assim pois não consegui pensar em uma forma de fazer uma requisição, externa, ao GraphQL mudar diretamente o frontend. Dessa forma, tive duas ideias:
    - Criar três páginas diferents, uma normal e outra para cada simulação;
    - ou, adicionar um componente extra na minha página quando `simulating` fosse verdadeiro. Segui essa ideia.
- Quando `simulating` é definifdo como `true`, na tela principal do site é exibido uma caixa de texto em que é possível escrever o nome da variante e alternar como quisermos entre elas. Acredito que tenha ficado simples de simular.

## Dificulades e comentários
- Como foi minha primeira vez utilizano graphql, e por ser acostumada com APIs REST, tive um pouco de dificuldade de entender como funcionava os conceitos. Olhei bastante os exemplos que foram disponibilizados e tentei reproduzir de acordo com o meu contexto.
- Como decidi fazer um SPA eu precisei utilizar muito o useState, em certos momentos eu me embananei um pouco com a atualização dos estados (Ex: fechar a modal), mas no final deu certo e ficou funcional.
- Também usei os exemplos fornecidos para entender melhor os testes, a ideia de testes em frontend era muito nebulosa na minha cabeça, mas com os exemplos ficou mais fácil de visualizar o que seriam os componentes renderizados e o que seria a parte mockada.

## Melhorias Futuras
1. **Testes Unitários**: Adicionar mais testes unitários. Fiz testes unitários apenas da página de processo, por ser uma das mais importantes e por ter muitas informações. Gostaria de fatorar mais os testes, testando de forma mais modularizada cada componente da página.
2. **Experimentos**: Gostaria de melhorar os meus experimentos, não tenho certeza se fiz da melhor forma, também gostaria de adicionar estatísticas para verificar quantos usuários da variant-a aceitaram ou negaram a oferta.
