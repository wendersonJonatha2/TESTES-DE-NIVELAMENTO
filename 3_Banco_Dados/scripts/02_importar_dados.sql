
\copy operadoras FROM 'data/operadoras.csv' WITH CSV HEADER DELIMITER ';';


\copy demonstracoes FROM 'data/demonstracoes/2023/1T2023.csv' WITH CSV HEADER DELIMITER ';';
\copy demonstracoes FROM 'data/demonstracoes/2023/2T2023.csv' WITH CSV HEADER DELIMITER ';';
\copy demonstracoes FROM 'data/demonstracoes/2023/3T2023.csv' WITH CSV HEADER DELIMITER ';';
\copy demonstracoes FROM 'data/demonstracoes/2023/4T2023.csv' WITH CSV HEADER DELIMITER ';';


\copy demonstracoes FROM 'data/demonstracoes/2024/1T2024.csv' WITH CSV HEADER DELIMITER ';';
\copy demonstracoes FROM 'data/demonstracoes/2024/2T2024.csv' WITH CSV HEADER DELIMITER ';';
\copy demonstracoes FROM 'data/demonstracoes/2024/3T2024.csv' WITH CSV HEADER DELIMITER ';';
\copy demonstracoes FROM 'data/demonstracoes/2024/4T2024.csv' WITH CSV HEADER DELIMITER ';';


SELECT 
    'Operadoras' AS tabela, 
    COUNT(*) AS registros 
FROM operadoras
UNION ALL
SELECT 
    'Demonstrações' AS tabela, 
    COUNT(*) AS registros 
FROM demonstracoes;


SELECT 
    EXTRACT(YEAR FROM competencia) AS ano,
    EXTRACT(QUARTER FROM competencia) AS trimestre,
    COUNT(*) AS registros
FROM demonstracoes
GROUP BY ano, trimestre
ORDER BY ano, trimestre;