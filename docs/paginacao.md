# Documentação sobre paginação

## Parâmetros de rotas paginadas
- **limit:** Quantidade de dados que serão retornados *(default = 20)*;
- **cursor:** Último id retornado na consulta anterior *(default = 0)*.

## Retorno de rotas paginadas
```json
{
    "data": [],
    "paging": {
        "cursor": int,
        "has_more": bool
    }
}
```

- **cursor:** Último id retornado na listagem;
- **has_more:** Valor booleano indicando se existem mais dados após a última listagem.

Caso seja inserido um cursor maior que o último id da tabela será retornado status 200 - OK com o seguinte json:
```json
{
  "data": [],
  "paging": {
    "cursor": null,
    "has_more": false
  }
}
```