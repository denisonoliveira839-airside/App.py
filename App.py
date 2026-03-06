import streamlit as st
import pandas as pd
from database import conectar, criar_tabelas
from calculos import calcular_motor
from materiais import gerar_lista_materiais
from datetime import datetime

criar_tabelas()

st.set_page_config(page_title="AirSide PRO", layout="wide")

st.title("🌀 AirSide PRO - ERP HVAC")

menu = st.sidebar.selectbox(
    "Menu",
    [
        "Dashboard",
        "Projeto",
        "Resultado",
        "Multifilar",
        "Materiais",
        "Simulador",
        "Clientes",
        "Projetos",
        "Orçamento"
    ]
)

# =========================================
# DASHBOARD
# =========================================

if menu == "Dashboard":

    st.header("📊 Dashboard")

    conn = conectar()

    try:
        projetos = pd.read_sql("SELECT * FROM projetos", conn)
        clientes = pd.read_sql("SELECT * FROM clientes", conn)
    except:
        projetos = pd.DataFrame()
        clientes = pd.DataFrame()

    conn.close()

    col1,col2 = st.columns(2)

    col1.metric("Projetos", len(projetos))
    col2.metric("Clientes", len(clientes))

# =========================================
# PROJETO
# =========================================

elif menu == "Projeto":

    st.header("📋 Novo Projeto")

    cliente = st.text_input("Cliente")

    vazao = st.number_input("Vazão m³/h",value=5000)

    tensao = st.selectbox("Tensão",[220,380,440])

    if st.button("Calcular"):

        motor,corrente,disj,cabo = calcular_motor(vazao,tensao)

        st.session_state["resultado"] = {
            "motor":motor,
            "corrente":corrente,
            "disj":disj,
            "cabo":cabo
        }

        st.success("Projeto calculado!")

# =========================================
# RESULTADO
# =========================================

elif menu == "Resultado":

    st.header("📊 Resultado")

    if "resultado" in st.session_state:

        r = st.session_state["resultado"]

        st.write("Motor:",r["motor"],"CV")
        st.write("Corrente:",r["corrente"],"A")
        st.write("Disjuntor:",r["disj"],"A")
        st.write("Cabo:",r["cabo"],"mm²")

    else:

        st.info("Calcule um projeto primeiro")

# =========================================
# MULTIFILAR
# =========================================

elif menu == "Multifilar":

    st.header("📑 Diagrama Multifilar")

    st.write("Rede → Disjuntor → Contator → Relé térmico → Motor")

# =========================================
# MATERIAIS
# =========================================

elif menu == "Materiais":

    st.header("📦 Lista de Materiais")

    if "resultado" in st.session_state:

        lista = gerar_lista_materiais(st.session_state["resultado"])

        df = pd.DataFrame(lista)

        st.dataframe(df)

# =========================================
# SIMULADOR
# =========================================

elif menu == "Simulador":

    st.header("🎛️ Simulador")

    corrente = st.slider("Corrente",0,100,10)

    st.write("Simulação de carga:",corrente)

# =========================================
# CLIENTES
# =========================================

elif menu == "Clientes":

    st.header("👥 Clientes")

    nome = st.text_input("Nome")

    if st.button("Salvar"):

        conn = conectar()
        c = conn.cursor()

        c.execute(
            "INSERT INTO clientes(nome,data) VALUES (?,?)",
            (nome,datetime.now())
        )

        conn.commit()
        conn.close()

        st.success("Cliente salvo")

# =========================================
# PROJETOS
# =========================================

elif menu == "Projetos":

    st.header("📁 Projetos")

    conn = conectar()

    df = pd.read_sql("SELECT * FROM projetos",conn)

    conn.close()

    st.dataframe(df)

# =========================================
# ORÇAMENTO
# =========================================

elif menu == "Orçamento":

    st.header("💰 Orçamento")

    material = st.number_input("Material",value=1000)

    mao = st.number_input("Mão de obra",value=500)

    margem = st.slider("Margem %",0,100,30)

    total = (material+mao)*(1+margem/100)

    st.metric("Total",f"R$ {round(total,2)}")
