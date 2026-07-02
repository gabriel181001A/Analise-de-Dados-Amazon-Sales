-- ============================================================
-- Amazon (Índia) — Consultas de análise exploratória (AWS Athena / Presto)
-- Tabela: data_set_aws  (dados brutos como texto: preços com "₹", desconto com "%")
-- Observação: o dataset é de PRODUTOS (preço, desconto, avaliação) — não há
-- volume de vendas; por isso as métricas giram em torno de preço/nota/popularidade.
-- ============================================================


-- ------------------------------------------------------------
-- 1) Categorias com mais produtos (usa o 1º nível da categoria)
-- ------------------------------------------------------------
SELECT
    split_part(category, '|', 1)  AS categoria_principal,
    COUNT(*)                       AS qtd_produtos
FROM data_set_aws
GROUP BY split_part(category, '|', 1)
ORDER BY qtd_produtos DESC;


-- ------------------------------------------------------------
-- 2) Produtos com os MAIORES descontos (corrigido)
--    (a versão antiga filtrava produtos que apareciam 3x — não media desconto)
-- ------------------------------------------------------------
SELECT
    product_name,
    TRY_CAST(REPLACE(discount_percentage, '%', '') AS DOUBLE) AS desconto_pct,
    actual_price,
    discounted_price
FROM data_set_aws
ORDER BY desconto_pct DESC
LIMIT 10;


-- ------------------------------------------------------------
-- 3) Desconto médio por categoria
-- ------------------------------------------------------------
SELECT
    split_part(category, '|', 1)                                        AS categoria,
    ROUND(AVG(TRY_CAST(REPLACE(discount_percentage, '%', '') AS DOUBLE)), 1) AS desconto_medio_pct,
    COUNT(*)                                                            AS qtd_produtos
FROM data_set_aws
GROUP BY split_part(category, '|', 1)
ORDER BY desconto_medio_pct DESC;


-- ------------------------------------------------------------
-- 4) Desconto x avaliação: nota média por faixa de desconto
--    Hipótese: desconto agressivo NÃO significa produto melhor avaliado.
-- ------------------------------------------------------------
WITH base AS (
    SELECT
        TRY_CAST(REPLACE(discount_percentage, '%', '') AS DOUBLE) AS desconto,
        TRY_CAST(rating AS DOUBLE)                                AS nota
    FROM data_set_aws
)
SELECT
    CASE
        WHEN desconto <= 25 THEN '0-25%'
        WHEN desconto <= 50 THEN '25-50%'
        WHEN desconto <= 75 THEN '50-75%'
        ELSE '75-100%'
    END                        AS faixa_desconto,
    ROUND(AVG(nota), 2)        AS nota_media,
    COUNT(*)                   AS qtd_produtos
FROM base
WHERE nota IS NOT NULL
GROUP BY 1
ORDER BY 1;


-- ------------------------------------------------------------
-- 5) Produtos mais populares (maior número de avaliações)
-- ------------------------------------------------------------
SELECT
    product_name,
    TRY_CAST(REPLACE(rating_count, ',', '') AS BIGINT) AS avaliacoes,
    TRY_CAST(rating AS DOUBLE)                         AS nota
FROM data_set_aws
WHERE rating_count <> ''
ORDER BY avaliacoes DESC
LIMIT 10;
