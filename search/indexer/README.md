# Indexando processos com Elasticsearch

Criação de um pipeline de indexação de processos. O indexador faz os seguintes passos:
- Seleciona todos os documentos da base de dados.
- Faz transformações na estrutura dos dados para um esquema específico.
- Indexa os documentos fazendo relação com os ids do banco de dados.

## Execução

O [README inicial](../../README.md) mostra instruções de como rodar e testar o pipeline.

## Dificulades
 - Garantir que quem fosse testar tivesse o banco de dados populado.

## Melhorias
 - Automatização do pipeline com um DAG.
