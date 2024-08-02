import streamlit as st
import pymysql
from PIL import Image

# Configuração da página
st.set_page_config(page_title="Portal de Autenticação", page_icon="🔒")

# Função para verificar as credenciais do usuário
def check_credentials(username, password):
    connection = pymysql.connect(
        host='your_host',
        user='your_user',
        password='your_password',
        database='your_database'
    )
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM users WHERE username=%s AND password=%s", (username, password))
    user = cursor.fetchone()
    connection.close()
    if user:
        return True
    else:
        return False

# Função para cadastrar um novo usuário
def register_user(username, password, name, address, cpf, birth_date, profession, company):
    connection = pymysql.connect(
        host='your_host',
        user='your_user',
        password='your_password',
        database='your_database'
    )
    cursor = connection.cursor()
    cursor.execute("""
        INSERT INTO users (username, password, name, address, cpf, birth_date, profession, company) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """, (username, password, name, address, cpf, birth_date, profession, company))
    connection.commit()
    connection.close()
    st.success("Usuário cadastrado com sucesso!")

# Carregar e redimensionar o logotipo
logo_path = "logo.png"
logo = Image.open(logo_path)
logo = logo.resize((79, 79))  # Aproximadamente 2x2 cm a 96 DPI

st.image(logo, width=79)

# Título da página
st.title("Portal de Autenticação")

# Tabs para login e cadastro
tab1, tab2 = st.tabs(["Login", "Cadastro"])

# Formulário de login
with tab1:
    st.header("Login")
    with st.form(key='login_form'):
        username = st.text_input("Nome de Usuário")
        password = st.text_input("Senha", type="password")
        login_button = st.form_submit_button("Entrar")

    # Verificação das credenciais
    if login_button:
        if check_credentials(username, password):
            st.success("Login bem-sucedido!")
            # Redirecionar para a página inicial do portal ou mostrar o conteúdo do portal
            st.write("Bem-vindo ao portal!")
        else:
            st.error("Nome de usuário ou senha incorretos. Tente novamente.")

# Formulário de cadastro
with tab2:
    st.header("Cadastro")
    with st.form(key='register_form'):
        new_username = st.text_input("Nome de Usuário")
        new_password = st.text_input("Senha", type="password")
        name = st.text_input("Nome Completo")
        address = st.text_input("Endereço")
        cpf = st.text_input("CPF")
        birth_date = st.date_input("Data de Nascimento")
        profession = st.text_input("Profissão")
        company = st.text_input("Empresa")
        register_button = st.form_submit_button("Cadastrar")

    # Cadastro de novo usuário
    if register_button:
        if new_username and new_password and name and address and cpf and birth_date and profession and company:
            register_user(new_username, new_password, name, address, cpf, birth_date, profession, company)
        else:
            st.error("Por favor, preencha todos os campos para cadastrar.")

# Instruções ou informações adicionais
st.info("Por favor, insira suas credenciais para acessar o portal.")

# Aviso de desenvolvimento (remover em produção)
st.warning("Este é um ambiente de desenvolvimento. Substitua as credenciais do banco de dados e o caminho do logotipo antes de usar em produção.")
