
import streamlit as st
import pandas as pd

st.set_page_config(page_title="Vendas de Carros", layout="wide")

CATALOGO = {
    "Fiat Argo": {"marca": "Fiat", "preco": 85000.00},
    "Chevrolet Onix": {"marca": "Chevrolet", "preco": 95000.00},
    "Hyundai HB20": {"marca": "Hyundai", "preco": 92000.00},
    "Volkswagen Polo": {"marca": "Volkswagen", "preco": 105000.00},
    "Toyota Corolla": {"marca": "Toyota", "preco": 155000.00},
    "Honda Civic": {"marca": "Honda", "preco": 180000.00}
}

if "carrinho" not in st.session_state:
    st.session_state.carrinho = []

if "vendas" not in st.session_state:
    st.session_state.vendas = []

# -----------------------------------------------------------------------------

st.title("Dashboard de Vendas de Carros")
st.markdown("---")

col1, col2 = st.columns([1, 1], gap="large")

with col1:
    st.header("Cadastro de Veiculos")

    with st.form("form_carro"):
        carro = st.selectbox("Escolha o carro", list(CATALOGO.keys()))

        preco = CATALOGO[carro]["preco"]
        st.caption(f"Preco: R$ {preco:.2f}")

        quantidade = st.number_input(
            "Quantidade",
            min_value=1,
            value=1,
            step=1
        )

        adicionar = st.form_submit_button(
            "Adicionar ao Carrinho",
            use_container_width=True
        )

        if adicionar:
            st.session_state.carrinho.append({
                "Veiculo": carro,
                "Marca": CATALOGO[carro]["marca"],
                "Preco (R$)": preco,
                "Quantidade": quantidade,
                "Subtotal (R$)": preco * quantidade
            })
            st.success("Veiculo adicionado com sucesso!")

    st.header("Carrinho")

    if st.session_state.carrinho:
        df_carrinho = pd.DataFrame(st.session_state.carrinho)

        st.dataframe(
            df_carrinho,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Preco (R$)": st.column_config.NumberColumn(
                    "Preco Unitario",
                    format="R$ %.2f"
                ),
                "Subtotal (R$)": st.column_config.NumberColumn(
                    "Subtotal",
                    format="R$ %.2f"
                )
            }
        )

        if st.button("Limpar Carrinho", use_container_width=True):
            st.session_state.carrinho = []
            st.rerun()
    else:
        st.info("Nenhum carro no carrinho.")

with col2:
    st.header("Pagamento")

    total = sum(
        item["Subtotal (R$)"]
        for item in st.session_state.carrinho
    )

    st.metric("Total da Venda", f"R$ {total:.2f}")
    st.divider()

    recebido = st.number_input(
        "Valor recebido (R$)",
        min_value=0.0,
        value=0.0,
        step=1000.0,
        format="%.2f"
    )

    if total == 0:
        st.warning("Adicione um carro antes de realizar o pagamento.")
    elif recebido == 0:
        st.info("Aguardando pagamento.")
    elif recebido < total:
        st.error(f"Valor insuficiente. Faltam R$ {total - recebido:.2f}.")
    else:
        troco = recebido - total
        st.success("Pagamento concluido!")
        st.metric("Troco", f"R$ {troco:.2f}")

        with st.expander("Ver Comprovante"):
            st.write(f"Total da venda: R$ {total:.2f}")
            st.write(f"Valor recebido: R$ {recebido:.2f}")
            st.write(f"Troco: R$ {troco:.2f}")

        if st.button("Finalizar Venda", type="primary",
                     use_container_width=True):
            st.session_state.vendas.append({
                "Veiculos": ", ".join(
                    item["Veiculo"] for item in st.session_state.carrinho
                ),
                "Quantidade": sum(
                    item["Quantidade"] for item in st.session_state.carrinho
                ),
                "Total (R$)": total
            })

            st.session_state.carrinho = []
            st.rerun()

# -----------------------------------------------------------------------------

st.markdown("---")
st.header("Resumo das Vendas")

total_vendido = sum(
    venda["Total (R$)"] for venda in st.session_state.vendas
)

carros_vendidos = sum(
    venda["Quantidade"] for venda in st.session_state.vendas
)

col3, col4, col5 = st.columns(3)

with col3:
    st.metric("Faturamento", f"R$ {total_vendido:.2f}")

with col4:
    st.metric("Carros Vendidos", carros_vendidos)

with col5:
    st.metric("Vendas Realizadas", len(st.session_state.vendas))

st.header("Historico de Vendas")

if st.session_state.vendas:
    df_vendas = pd.DataFrame(st.session_state.vendas)

    st.dataframe(
        df_vendas,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Total (R$)": st.column_config.NumberColumn(
                "Total",
                format="R$ %.2f"
            )
        }
    )
else:
    st.info("Nenhuma venda realizada.")
