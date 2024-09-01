# Análise de Dados de Vendas da Amazon

Este projeto pessoal de análise de dados utiliza um dataset de vendas da Amazon, obtido da plataforma Kaggle. O objetivo deste projeto é explorar, limpar, modelar e visualizar dados de vendas da Amazon utilizando diversas ferramentas e tecnologias, como AWS, SQL, e Power BI.

## Sumário

- [Visão Geral](#visão-geral)
- [Tecnologias Utilizadas](#tecnologias-utilizadas)
- [Arquitetura do Projeto](#arquitetura-do-projeto)
- [Aprendizados](#aprendizados)
- [Etapas do Projeto](#etapas-do-projeto)
- [Resultados](#resultados)
- [Como Executar o Projeto](#como-executar-o-projeto)
- [Referências](#referências)

## Visão Geral

Este projeto faz uma análise dos detalhes de vendas da Amazon, incluindo informações sobre reviews de produtos, preços e outras métricas importantes. O objetivo principal é aplicar técnicas de análise de dados para obter insights valiosos que possam ajudar a entender melhor o desempenho dos produtos no marketplace da Amazon.

## Tecnologias Utilizadas

- **Kaggle**: Fonte do dataset.
- **AWS S3**: Armazenamento dos dados.
- **AWS Glue (Crawler e DataCatalog)**: Criação e gerenciamento de metadados.
- **AWS Athena**: Análise exploratória de dados (EDA) utilizando SQL.
- **Power BI**: Limpeza, modelagem e visualização de dados.
- **Snowflake Schema**: Estrutura de dados adotada para modelagem.
- **Power Query**: Ferramenta utilizada para transformação de dados no Power BI.
- **SQL**: Linguagem utilizada para manipulação de dados e consultas no Athena.

## Arquitetura do Projeto

O fluxo de trabalho do projeto segue a seguinte arquitetura:

1. **Kaggle (Fonte dos Dados)**: O dataset foi obtido na plataforma Kaggle e contém detalhes sobre vendas, reviews, produtos e preços da Amazon.
2. **AWS S3**: Os dados foram carregados para um bucket S3 para armazenamento seguro e escalável.
3. **AWS Glue Crawler e DataCatalog**: Um Crawler foi configurado para catalogar o dataset e criar uma tabela no Glue DataCatalog.
4. **AWS Athena**: SQL foi utilizado para a exploração inicial dos dados e análise exploratória de dados (EDA) no Athena.
5. **Power BI**: O Power BI foi utilizado para a limpeza, modelagem, e criação de visualizações de dados, permitindo insights mais profundos.

![GITHUB ARQUITETURA](https://github.com/user-attachments/assets/778f082d-c646-4652-a7e0-e460608b26f9)

## Aprendizados

Durante o desenvolvimento deste projeto, aprofundei meus conhecimentos nas seguintes áreas:

- **Snowflake Schema**: Estrutura de modelagem de dados em estrela e floco de neve para análise de dados.
- **Power Query**: Manipulação e transformação de dados no Power BI.
- **SQL**: Consultas SQL para análise exploratória no AWS Athena.
- **AWS Services**: Utilização de serviços AWS, como S3, Glue e Athena, para processamento de dados.
- **Análise de Dados**: Técnicas de análise exploratória de dados e visualização no Power BI.

## Etapas do Projeto

### 1. Obtenção dos Dados

- Dataset baixado da plataforma Kaggle, contendo informações detalhadas sobre vendas da Amazon.

### 2. Armazenamento no AWS S3

- Os dados foram armazenados em um bucket S3 para fácil acesso e manipulação.

### 3. Criação de Tabelas no Glue DataCatalog

- Um Crawler foi configurado para detectar automaticamente o esquema dos dados e catalogá-los.

### 4. Análise Exploratória no AWS Athena

- Utilização de SQL no Athena para realizar a análise exploratória dos dados, incluindo limpeza e identificação de padrões.
- As consultas SQL a seguir foram usadas para responder a perguntas chave de negócios:

#### Maiores Porcentagens de Descontos?

```sql
SELECT product_id,
       discount_percentage
FROM data_set_aws
WHERE product_id IN (
    SELECT product_id
    FROM data_set_aws
    GROUP BY product_id
    HAVING COUNT(*) = 3
);
```

#### Qual Categoria mais teve indício de venda?

```sql
SELECT
    category,
    COUNT(*) as vendas_totais
FROM data_set_aws
GROUP BY
    category
ORDER BY
    vendas_totais DESC;
```

#### Produtos com maiores indícios de avaliações?

```sql
SELECT
    DISTINCT product_name,
    TRIM(rating) AS rating,
    TRIM(rating_count) AS rating_count
FROM data_set_aws
WHERE rating_count <> ''
    OR TRIM(rating) <> '|'
ORDER BY
    rating DESC,
    rating_count DESC;
```

#### Quais foram as maiores vendas?

```sql
SELECT
    product_name,
    COUNT(*)
FROM sales.data_set_aws
GROUP BY
    product_name;
```

### 5. Limpeza e Modelagem no Power BI

- Os dados foram carregados no Power BI, onde foram realizadas transformações e limpezas utilizando o Power Query.
- A modelagem dos dados seguiu o esquema Snowflake (floco de neve), organizando as tabelas de fatos e dimensões de forma otimizada para a análise.

![image](https://github.com/user-attachments/assets/6b6a069f-ca1f-403a-b5d0-77c3dc6a6498)


### 6. Visualização e Geração de Insights no Power BI

- Foram criados dashboards interativos no Power BI para visualização dos dados.
- As visualizações forneceram insights sobre os padrões de vendas, produtos mais vendidos, impacto das avaliações e variações de preços ao longo do tempo.

## Resultados

![power bi github](https://github.com/user-attachments/assets/dc2388e3-6647-42c4-9255-64f6e753339f)


## Como Executar o Projeto

Se você deseja reproduzir este projeto, siga os passos abaixo:

1. **Baixe ou clone os arquivos neste repositório:** 
    - amazon.csv 
    - Amazon-sales-dashboard.pbix

## Referências

- [Kaggle - Fonte do Dataset](https://www.kaggle.com/datasets/karkavelrajaj/amazon-sales-dataset)

## Licença

Este projeto está licenciado sob a licença MIT - veja o arquivo [LICENSE](LICENSE) para mais detalhes.
