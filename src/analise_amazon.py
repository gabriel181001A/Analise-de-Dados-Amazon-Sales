# -*- coding: utf-8 -*-
"""
Análise dos produtos da Amazon (Índia): preços, descontos e avaliações.

Lê o amazon.csv (dataset do Kaggle), limpa os campos de texto (₹, %, vírgulas),
calcula métricas e gera os gráficos usados no README.

Uso:
    python src/analise_amazon.py
"""
from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

BASE = Path(__file__).resolve().parents[1]
CSV = BASE / "amazon.csv"
FIG = BASE / "imagens"
FIG.mkdir(exist_ok=True)

sns.set_theme(style="whitegrid")
plt.rcParams["figure.figsize"] = (10, 5)

# Tradução das categorias principais (inglês -> português)
CAT_PT = {
    "Electronics": "Eletrônicos",
    "Computers&Accessories": "Computadores & Acessórios",
    "Home&Kitchen": "Casa & Cozinha",
    "OfficeProducts": "Produtos de Escritório",
    "MusicalInstruments": "Instrumentos Musicais",
    "HomeImprovement": "Reforma & Construção",
    "Health&PersonalCare": "Saúde & Cuidado Pessoal",
    "Toys&Games": "Brinquedos & Jogos",
    "Car&Motorbike": "Carro & Moto",
}


def limpar(df: pd.DataFrame) -> pd.DataFrame:
    """Converte os campos de texto (₹, %, vírgulas) em números e cria colunas úteis."""
    def num(col):
        return pd.to_numeric(
            col.astype(str).str.replace("₹", "", regex=False)
               .str.replace(",", "", regex=False).str.replace("%", "", regex=False).str.strip(),
            errors="coerce",
        )

    df = df.copy()
    df["preco"] = num(df["discounted_price"])
    df["preco_original"] = num(df["actual_price"])
    df["desconto_pct"] = num(df["discount_percentage"])
    df["nota"] = pd.to_numeric(df["rating"].astype(str).str.strip(), errors="coerce")
    df["qtd_avaliacoes"] = num(df["rating_count"])
    cat = df["category"].astype(str).str.split("|").str[0]
    df["categoria_principal"] = cat.map(lambda c: CAT_PT.get(c, c))
    return df


def grafico_categorias(df):
    top = df["categoria_principal"].value_counts().head(6).sort_values()
    ax = top.plot(kind="barh", color=sns.color_palette("viridis", len(top)))
    ax.set_title("Produtos por categoria (top 6)")
    ax.set_xlabel(""); ax.set_ylabel("")
    for i, v in enumerate(top):
        ax.text(v + top.max() * 0.01, i, f"{v}", va="center", fontsize=9)
    ax.set_xticks([]); ax.set_xlim(0, top.max() * 1.12)
    sns.despine(left=True, bottom=True)
    plt.tight_layout()
    plt.savefig(FIG / "categorias.png", dpi=120)
    plt.close()


def grafico_desconto_nota(df):
    df = df.copy()
    df["faixa"] = pd.cut(df["desconto_pct"], [0, 25, 50, 75, 100],
                         labels=["0-25%", "25-50%", "50-75%", "75-100%"], include_lowest=True)
    m = df.groupby("faixa", observed=True)["nota"].mean()
    ax = m.plot(kind="bar", color=sns.color_palette("viridis", len(m)))
    ax.set_title("Nota média por faixa de desconto")
    ax.set_xlabel("Faixa de desconto"); ax.set_ylabel("Nota média (1-5)")
    ax.set_ylim(3.5, 4.3)
    for i, v in enumerate(m):
        ax.text(i, v + 0.01, f"{v:.2f}".replace(".", ","), ha="center", fontsize=10)
    plt.xticks(rotation=0)
    sns.despine()
    plt.tight_layout()
    plt.savefig(FIG / "desconto_vs_nota.png", dpi=120)
    plt.close()


def grafico_distribuicao_desconto(df):
    ax = sns.histplot(df["desconto_pct"].dropna(), bins=20, color="#2E86C1")
    ax.axvline(df["desconto_pct"].mean(), color="#E74C3C", linestyle="--",
               label=f"média {df['desconto_pct'].mean():.0f}%")
    ax.set_title("Distribuição do desconto oferecido")
    ax.set_xlabel("Desconto (%)"); ax.set_ylabel("Nº de produtos")
    ax.legend()
    sns.despine()
    plt.tight_layout()
    plt.savefig(FIG / "distribuicao_desconto.png", dpi=120)
    plt.close()


def main():
    df = limpar(pd.read_csv(CSV))
    grafico_categorias(df)
    grafico_desconto_nota(df)
    grafico_distribuicao_desconto(df)
    print(f"Gráficos salvos em: {FIG}")
    print(f"Produtos: {len(df)} | nota média: {df['nota'].mean():.2f} | "
          f"desconto médio: {df['desconto_pct'].mean():.0f}% | "
          f"correlação desconto x nota: {df['desconto_pct'].corr(df['nota']):.3f}")


if __name__ == "__main__":
    main()
