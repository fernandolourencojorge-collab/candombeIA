import streamlit as st
import time
import os

# Configuração da página web
st.set_page_config(page_title="IA II - Portal Candombe", page_icon="", layout="centered")


# ESTILIZAÇÃO CUSTOMIZADA (MATRIX & CYBERPUNK - COMBINANDO COM O ROBÔ)

st.markdown("""
    <style>
    /* Fundo escuro tecnológico baseado no fundo da foto do robô */
    .stApp {
        background-color: #0b131f;
        background-image: radial-gradient(circle at 50% 50%, #112235 0%, #0b131f 100%);
    }
    
    /* Título principal em Ciano/Neon */
    .main-title {
        color: #00f2fe;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        font-weight: 800;
        text-align: center;
        margin-top: 5px;
        margin-bottom: 5px;
        text-shadow: 0 0 10px rgba(0, 242, 254, 0.6);
    }
    
    /* Descrição secundária */
    .sub-title {
        color: #94a3b8;
        text-align: center;
        font-size: 16px;
        margin-bottom: 30px;
    }
    
    /* Contentor para centralizar a foto do robô */
    .robot-image-container {
        display: flex;
        justify-content: center;
        align-items: center;
        margin-bottom: 25px;
    }
    
    /* Fallback do Emoji caso a imagem falhe */
    .robot-emoji {
        font-size: 70px;
        animation: pulse 2s infinite;
    }
    
    /* Balão das respostas da IA (Fundo escuro azulado com borda Ciano brilhante) */
    .bot-bubble {
        background-color: #152538;
        border-left: 5px solid #00f2fe;
        padding: 16px;
        border-radius: 12px;
        box-shadow: 0px 4px 15px rgba(0, 242, 254, 0.1);
        margin-bottom: 18px;
        color: #e2e8f0;
    }
    
    /* Balão das mensagens do Utilizador (Azul Escuro) */
    .user-bubble {
        background-color: #1e293b;
        border-right: 5px solid #3b82f6;
        padding: 14px;
        border-radius: 12px;
        box-shadow: 0px 2px 5px rgba(0,0,0,0.3);
        margin-bottom: 18px;
        color: #93c5fd;
        text-align: left;
    }
    
    /* Customização da barra de input (Texto claro) */
    div[data-baseweb="input"] input {
        color: #ffffff !important;
    }
    
    /* Textos da barra lateral */
    .sidebar-header {
        color: #00f2fe;
        font-weight: 700;
        font-size: 18px;
        margin-top: 10px;
        text-shadow: 0 0 5px rgba(0, 242, 254, 0.3);
    }
    </style>
""", unsafe_allow_html=True)


# 1. MAPEAMENTO SEMÂNTICO DE INTENÇÕES (DADOS REAIS DO RELATÓRIO)

INTENCOES = {
    "seguranca": {
        "conceitos": ["segurança", "seguro", "inseguro", "criminalidade", "crime", "crimes", "roubo", "roubos", "assalto", "assaltos", "gatuno", "gatunos", "ladrão", "ladrao", "ladrões", "droga", "drogas", "tráfico", "violência", "prostituição", "perigo", "noite", "confusão", "deliquencia", "delinquência"],
        "titulo": "Segurança Pública e Criminalidade",
        "texto": " **[DIAGNÓSTICO DE SEGURANÇA PÚBLICA - PROPORÇÃO PARA 1000 INQUIRIDOS]**\n\n"
                 "Com base no relatório, **88%** dos moradores classificam o bairro como inseguro. Numa escala de 1000 pessoas, isto representa **880 indivíduos**.\n\n"
                 "• **Roubo:** 76% das menções (760 pessoas em 1000).\n"
                 "• **Tráfico e consumo de drogas:** 60% das menções (600 pessoas em 1000).\n"
                 "• **Violência física:** 48% das menções (480 pessoas em 1000).\n"
                 "• **Prostituição:** 36% das menções (360 pessoas em 1000)."
    },
    "saude": {
        "conceitos": ["saúde", "saude", "hospital", "hospitais", "posto", "postos", "médico", "médicos", "medico", "doente", "doentes", "doença", "doenças", "malária", "malaria", "paludismo", "tifoide", "febre", "saneamento", "lixo", "clínica"],
        "titulo": "Saúde e Epidemiologia",
        "texto": " **[DIAGNÓSTICO DE SAÚDE - PROPORÇÃO PARA 1000 INQUIRIDOS]**\n\n"
                 "O bairro dispõe de apenas 1 hospital e 2 postos médicos para uma população estimada entre 20.000 a 35.000 habitantes.\n\n"
                 "Num universo de 1000 pessoas:\n"
                 "• **Doenças Crónicas:** Afetam 32% dos inquiridos (**320 pessoas**).\n"
                 "• **Malária (Paludismo):** É a mais frequente, atingindo 56% (**560 pessoas**).\n"
                 "• **Febre Tifoide:** Atinge 32% (**320 pessoas**), estando fortemente ligada à falta de saneamento."
    },
    "infraestrutura": {
        "conceitos": ["infraestrutura", "infraestruturas", "água", "agua", "luz", "energia", "eletricidade", "apagão", "vias", "estrada", "estradas", "asfalto", "lama", "chuva", "chuvas", "buraco", "buracos", "zona 3", "poço", "cacimba", "riacho"],
        "titulo": "Infraestrutura e Serviços Básicos",
        "texto": " **[INFRAESTRUTURA E SERVIÇOS BÁSICOS - PROPORÇÃO PARA 1000 INQUIRIDOS]**\n\n"
                 "• **Energia Elétrica:** 84% (**840 pessoas** em 1000) têm acesso regular à rede pública, enquanto 16% (**160 pessoas**) sofrem com falhas.\n"
                 "• **Água Potável:** 80% (**800 pessoas** em 1000) usam a rede pública. Porém, 20% (**200 pessoas**) dependem de cacimbas, poços e riachos urbanos.\n"
                 "• **Vias de Acesso:** As ruas principais estão asfaltadas, mas as zonas periféricas (como a Zona 3) sofrem com estradas de terra batida, buracos e muita lama nas chuvas."
    },
    "educacao": {
        "conceitos": ["educação", "educacao", "escola", "escolas", "ensino", "estudar", "criança", "crianças", "vagas", "vaga", "abandono", "evasão", "professor", "creche", "parque", "infantil", "aluno", "alunos"],
        "titulo": "Setor Educativo e Infância",
        "texto": " **[ANÁLISE DO SETOR EDUCATIVO - PROPORÇÃO PARA 1000 INQUIRIDOS]**\n\n"
                 "Embora o bairro tenha 6 escolas em funcionamento, estimativas baseadas na taxa de exclusão de 15% indicam que cerca de **480 a 825 crianças** em idade escolar estão fora do sistema de ensino por falta de vagas ou condições financeiras. O bairro apresenta uma ausência total de creches e parques infantis."
    },
    "solucoes": {
        "conceitos": ["solução", "soluções", "solucao", "ajuda", "ajudar", "resolver", "melhorar", "governo", "administração", "recomendações", "recomenda", "proposta", "propostas", "sugestão", "intervenção"],
        "titulo": "Diretrizes e Recomendações",
        "texto": " **[RECOMENDAÇÕES DA IA PARA O DESENVOLVIMENTO]**\n\n"
                 "1. Reforço da segurança pública com policiamento e iluminação pública noturna.\n"
                 "2. Construção de novos postos médicos comunitários descentralizados.\n"
                 "3. Inserção escolar para mitigar os 15% de crianças fora do sistema.\n"
                 "4. Implementação de creches e espaços de lazer infantil.\n"
                 "5. Campanhas de saneamento básico e distribuição de água potável para os 20% afetados.\n"
                 "6. Requalificação e terraplenagem das vias críticas da Zona 3."
    }
}


# 2. MOTOR DE IA POR CONTEXTO LÓGICO

def motor_ia_intencao(pergunta_usuario):
    pergunta = pergunta_usuario.lower().replace("?", "").replace(".", "").replace(",", "").replace("!", "")
    palavras_pergunta = pergunta.split()
    
    pontuacao_intencoes = {"seguranca": 0, "saude": 0, "infraestrutura": 0, "educacao": 0, "solucoes": 0}
    
    for palavra in palavras_pergunta:
        for chave_intencao, dados in INTENCOES.items():
            if palavra in dados["conceitos"]:
                pontuacao_intencoes[chave_intencao] += 1
                
    melhor_intencao = max(pontuacao_intencoes, key=pontuacao_intencoes.get)
    
    if pontuacao_intencoes[melhor_intencao] > 0:
        dados_finais = INTENCOES[melhor_intencao]
        return f" **[Contexto Identificado: {dados_finais['titulo']}]**\n\n{dados_finais['texto']}"
        
    if any(saudacao in pergunta for saudacao in ["olá", "ola", "bom dia", "boa tarde", "tudo bem", "candombe", "bairro", "projeto", "relatório", "amostra", "inquiridos", "divisão"]):
        return (f" **[Dados Gerais e Caracterização da Amostra - Proporção para 1000]**\n\n"
                f"• **Localização:** Bairro Candombe Velho, Uíge, Angola.\n"
                f"• **Equipa de Campo:** Henrique, Fernando, João, Manuel e Teodora.\n"
                f"• **Amostra Proporcional Expandida (1000 Inquiridos):**\n"
                f"  - **Sexo:** 550 Mulheres (55%) e 450 Homens (45%).\n"
                f"  - **Idades:** 18-25 anos (150), 26-35 anos (250), 36-45 anos (280), 46-55 anos (190), 56+ anos (130).\n"
                f"• **Universo Demográfico:** População estimada entre 20.000 a 35.000 habitantes.")

    return (" Compreendo que tens uma dúvida sobre o Candombe Velho. Tenta reestruturar a tua pergunta. "
            "Podes questionar sobre a **segurança**, **saúde/hospitais**, **água/luz/estradas**, ou a situação das **escolas**.")


# 3. INTERFACE INTERATIVA DO SITE (STREAMLIT)


# Configuração da Barra Lateral (Sidebar)
with st.sidebar:
    st.markdown('<center><img src="https://upload.wikimedia.org/wikipedia/commons/e/e1/Logo_Unikivi.png" width="110"></center>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-header">Universidade Kimpa Vita</div>', unsafe_allow_html=True)
    st.caption("Instituto Politécnico • Engenharia Informática")
    st.markdown("---")
    st.markdown("**Cadeira:** Inteligência Artificial II")
    st.markdown("**Docente:** Nganga Pedro")
    st.markdown("---")
    st.markdown("**Grupo de Desenvolvedores (3º Ano):**")
    st.markdown("""
    -  Henrique C. Cassanda
    -  Fernando L. A. Jorge
    -  João F. da Costa
    -  Manuel A. Tolentino
    -  Teodora M. Domingos
    """)

# Renderização Central do Robô (Usa o ficheiro local de forma segura)
nome_imagem = "images (6).jpg"
st.markdown('<div class="robot-image-container">', unsafe_allow_html=True)

if os.path.exists(nome_imagem):
    # Mostra a imagem com os estilos corretos se o ficheiro estiver na pasta
    st.image(nome_imagem, width=180)
else:
    # Caso o ficheiro não esteja na pasta, usa o emoji para não quebrar a interface
    st.markdown('<div class="robot-emoji"></div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<h1 class="main-title">IA II - Portal Candombe Velho</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">Agente de IA treinado para interpretar dados lógicos e estatísticos do relatório comunitário.</p>', unsafe_allow_html=True)

# Inicializar o Histórico do Chat
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Olá! Sou o assistente virtual do Candombe Velho. Podes perguntar-me sobre a criminalidade, o estado dos hospitais, a situação da água/luz, ou o abandono das crianças nas escolas. Como posso ajudar o vosso grupo hoje?"}
    ]

# Renderização das mensagens com os balões de design customizados
for message in st.session_state.messages:
    if message["role"] == "user":
        st.markdown(f'<div class="user-bubble">👤 **Tu:**<br>{message["content"]}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="bot-bubble">{message["content"]}</div>', unsafe_allow_html=True)

# Entrada do Utilizador
if prompt := st.chat_input("Digita a tua pergunta com total liberdade..."):
    st.markdown(f'<div class="user-bubble">👤 **Tu:**<br>{prompt}</div>', unsafe_allow_html=True)
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with st.spinner("A decifrar a intenção da frase..."):
        time.sleep(0.3)
        resposta = motor_ia_intencao(prompt)
        
    st.markdown(f'<div class="bot-bubble">{resposta}</div>', unsafe_allow_html=True)
    st.session_state.messages.append({"role": "assistant", "content": resposta})
