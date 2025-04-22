
from flask import Flask, render_template, request
import pandas as pd
from datetime import datetime
import unidecode

app = Flask(__name__)

# Leitura dos arquivos
faturamento = pd.read_excel("data/Faturamento.xlsx")
custo = pd.read_excel("data/Custo.xlsx")
compras = pd.read_excel("data/Compras.xlsx")
aso = pd.read_excel("data/ASO.xlsx")
funcionarios = pd.read_excel("data/Funcionarios.xlsx")
contratos = pd.read_excel("data/Contratos.xlsx")


# Função para extrair mês da pergunta
def extrair_mes(texto):
    meses = [
        "janeiro", "fevereiro", "março", "abril", "maio", "junho",
        "julho", "agosto", "setembro", "outubro", "novembro", "dezembro"
    ]
    texto = unidecode.unidecode(texto.lower())
    for mes in meses:
        if mes in texto:
            return mes.capitalize()
    return None

def responder(pergunta):
    pergunta = pergunta.lower()
    mes = extrair_mes(pergunta)

    if "faturamento" in pergunta:
        if mes:
            linha = faturamento[faturamento["Data"].str.lower().str.contains(mes.lower())]
            if not linha.empty:
                valor = linha["Valor"].sum()
                return f"O faturamento de {mes} foi R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        else:
            total = faturamento["Valor"].sum()
            return f"O faturamento total é R$ {total:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

    elif "compra" in pergunta:
        compras["Data"] = compras["Data"].str.replace("fereveiro", "fevereiro", case=False)
        if mes:
            linha = compras[compras["Data"].str.lower().str.contains(mes.lower())]
            if not linha.empty:
                valor = linha["Valor"].sum()
                return f"O total de compras em {mes} foi R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        else:
            total = compras["Valor"].sum()
            return f"O total de compras é R$ {total:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

    elif "aso" in pergunta:
        aso["Data de Vencimento"] = pd.to_datetime(aso["Data de Vencimento"])
        hoje = pd.to_datetime("today")
        vencendo = aso[aso["Data de Vencimento"] < hoje]
        return f"Quantidade de ASOs vencidos: {len(vencendo)}."

    elif "contrato" in pergunta:
        if "Valor Contrato" in contratos.columns:
            total = contratos["Valor Contrato"].sum()
            return f"O valor total dos contratos é R$ {total:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        else:
            return f"O total de contratos é {len(contratos)}."

    else:
        return "Desculpe, não entendi. Tente perguntar sobre faturamento, compras, ASOs ou contratos."

@app.route("/", methods=["GET", "POST"])
def index():
    resposta = ""
    pergunta = ""
    if request.method == "POST":
        pergunta = request.form["pergunta"]
        resposta = responder(pergunta)
    return render_template("index.html", pergunta=pergunta, resposta=resposta)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
