# FLuxo de Processos

Diagramas para o entendimento do fluxo de processos.

## Estrutura do Fluxo

![Estrutura atual do fluxo](./imagens/lawsuit_flow_dc.png)

## Coleta de processos

![Estrutura atual do fluxo](./imagens/collector_flow_da.png)

## Enriquecimento de processos

![Estrutura atual do fluxo](./imagens/er_flow_dc.png)

- **Parser**: Estrutura os processos, atribui id aos envolvidos, padroniza nomes e datas.
- **Classifier**: Identifica temas sensíveis dentro do processo. (Menor infrator, violência doméstica e crime de ódio)
- **db_sync**: Salva os processos em uma base de conhecimento geral. (postgres) 

## Indexação de processos

![Estrutura atual do fluxo](./imagens/indexer_flow_da.png)

