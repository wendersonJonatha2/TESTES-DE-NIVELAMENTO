
SELECT uf, COUNT(*) as total
FROM operadoras
GROUP BY uf
ORDER BY total DESC;

SELECT 
    EXTRACT(YEAR FROM competencia) as ano,
    EXTRACT(QUARTER FROM competencia) as trimestre,
    COUNT(*) as registros
FROM demonstracoes
GROUP BY ano, trimestre
ORDER BY ano, trimestre;

SELECT 
    o.razao_social,
    SUM(d.vl_saldo_final) as saldo_total
FROM demonstracoes d
JOIN operadoras o ON d.registro_ans = o.registro_ans
GROUP BY o.razao_social
ORDER BY saldo_total DESC
LIMIT 10;

SELECT 
    o.uf,
    AVG(d.vl_saldo_final) as media_saldo
FROM demonstracoes d
JOIN operadoras o ON d.registro_ans = o.registro_ans
GROUP BY o.uf
ORDER BY media_saldo DESC;

SELECT MAX(competencia) as ultimo_trimestre
FROM demonstracoes;


SELECT 
    (SELECT COUNT(*) FROM operadoras) as total_operadoras,
    (SELECT COUNT(*) FROM demonstracoes) as total_demonstracoes;