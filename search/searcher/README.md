# Buscador de processos com Elasticsearch

Buscador utilizando elasticsearch para fazer consultas por processos.

## Execução

O [README inicial](../../README.md) mostra instruções de como executar o buscador.

## Comentários
- Comcei fazendo a query com multi_match, mas depois que estava funcional mudei para query_string pois achei que iria diminuir o tamanho da query.
- Adicionei uma feature para filter de numero de processso em consultas textuais que continham um CNJ.
- Tentei modularizar a query.

## Dificuldades
- Deixar a query flexível.

## Melhorias
- Adicionar busca nas descrições, tem bastante texto.
