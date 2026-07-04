## Explicações
No comando existem parâmetros com nomes de tabelas seguidos de números, estes representando a quantidade de dados que serão inseridos.

Há também o parâmetro **--batch** que aumenta a quantidade de dados inseridos por lote *(padrão = 1000)*. Aumentar o batch aumenta a velocidade porém também o consumo de RAM e CPU. **NÃO RECOMENDADO USAR BATCH MAIOR QUE 5000**

## Como executar
Apenas execute o script "seed.py" localizado no diretório do backend. Modifique os parâmetros se necessário.

```bash
python backend/seed.py --usuarios 1000000 --conteudos 1000000 --avaliacoes 1000000 --favoritos 1000000 --assistidos 1000000
```