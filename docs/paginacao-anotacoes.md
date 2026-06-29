# y = limit
# z = ultimo id retornado na consulta anterior

# z = 0 por padrão na api (primeira consulta)
SELECT * FROM usuario WHERE id > z ORDER BY id LIMIT y;

SELECT count(*) FROM usuario; # c
# c = quantidade de registros
# limite de paginas = c / limit (arredondado para cima)