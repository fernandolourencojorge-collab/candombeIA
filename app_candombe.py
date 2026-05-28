import streamlit as st
import time
import os
from datetime import datetime

# Configuração da página web
st.set_page_config(page_title="IA II - Portal Candombe", page_icon="", layout="centered")


#  ESTILIZAÇÃO CUSTOMIZADA (MATRIX & CYBERPUNK)

st.markdown("""
    <style>
    .stApp {
        background-color: #0b131f;
        background-image: radial-gradient(circle at 50% 50%, #112235 0%, #0b131f 100%);
    }
    .main-title {
        color: #00f2fe;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        font-weight: 800;
        text-align: center;
        margin-top: 5px;
        margin-bottom: 5px;
        text-shadow: 0 0 10px rgba(0, 242, 254, 0.6);
    }
    .sub-title {
        color: #94a3b8;
        text-align: center;
        font-size: 16px;
        margin-bottom: 30px;
    }
    .robot-image-container {
        display: flex;
        justify-content: center;
        align-items: center;
        margin-bottom: 25px;
    }
    .robot-emoji {
        font-size: 70px;
    }
    .bot-bubble {
        background-color: #152538;
        border-left: 5px solid #00f2fe;
        padding: 16px;
        border-radius: 12px;
        box-shadow: 0px 4px 15px rgba(0, 242, 254, 0.1);
        margin-bottom: 18px;
        color: #e2e8f0;
    }
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
    div[data-baseweb="input"] input {
        color: #ffffff !important;
    }
    .sidebar-header {
        color: #00f2fe;
        font-weight: 700;
        font-size: 18px;
        margin-top: 10px;
        text-shadow: 0 0 5px rgba(0, 242, 254, 0.3);
    }
    </style>
""", unsafe_allow_html=True)


#  MAPEAMENTO DE INTENÇÕES (DADOS DO RELATÓRIO)

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
                 "• **Água Potável:** 80% (**800 pessoas** em 1000)修 usam a rede pública. Porém, 20% (**200 pessoas**) dependem de cacimbas, poços e riachos urbanos.\n"
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


#  FUNÇÃO PARA DETETAR O PERÍODO DO DIA (FUSO HORÁRIO)

def obter_saudacao_fuso_horario():
    hora_atual = datetime.now().hour
    if 5 <= hora_atual < 12:
        return "Bom dia"
    elif 12 <= hora_atual < 18:
        return "Boa tarde"
    else:
        return "Boa noite"


# 2. MOTOR DE IA POR CONTEXTO LÓGICO (COM DETEÇÃO DE SAUDAÇÕES)

def motor_ia_intencao(pergunta_usuario):
    pergunta = pergunta_usuario.lower().strip().replace("?", "").replace(".", "").replace(",", "").replace("!", "")
    palavras_pergunta = pergunta.split()
    
    # 1. Verificação de Saudações (inclui gírias e erros comuns como 'olla' ou 'tade')
    gatilhos_saudacao = [
        "olá", "ola", "olla", "oi", "bom dia", "bondia", 
        "boa tarde", "boatarde", "tade", "boa noite", "boanoite", "salute"
    ]
    
    # Se a entrada for apenas uma saudação ou contiver uma das palavras gatilho
    if pergunta in gatilhos_saudacao or any(saudacao in pergunta for saudacao in ["olá", "ola", "olla", "oi", "bom dia", "boa tarde", "boa noite"]):
        saudacao_dinamica = obter_saudacao_fuso_horario()
        return (f" **{saudacao_dinamica}!** Sou o assistente virtual do Candombe Velho.\n\n"
                f"Estou pronto para ajudar o vosso grupo com os dados estatísticos. "
                f"Podes perguntar-me sobre a **segurança**, **saúde (hospitais)**, **infraestrutura (água e luz)**, ou sobre as **escolas** do bairro. O que desejas analisar?")

    # 2. Processamento das intenções normais do relatório
    pontuacao_intencoes = {"seguranca": 0, "saude": 0, "infraestrutura": 0, "educacao": 0, "solucoes": 0}
    
    for palavra in palavras_pergunta:
        for chave_intencao, dados in INTENCOES.items():
            if palavra in dados["conceitos"]:
                pontuacao_intencoes[chave_intencao] += 1
                
    melhor_intencao = max(pontuacao_intencoes, key=pontuacao_intencoes.get)
    
    if pontuacao_intencoes[melhor_intencao] > 0:
        dados_finais = INTENCOES[melhor_intencao]
        return f" **[Contexto Identificado: {dados_finais['titulo']}]**\n\n{dados_finais['texto']}"
        
    # 3. Informações gerais do projeto
    if any(termo in pergunta for termo in ["candombe", "bairro", "projeto", "relatório", "amostra", "inquiridos"]):
        return (f" **[Dados Gerais da Amostra - Proporção para 1000]**\n\n"
                f"• **Localização:** Bairro Candombe Velho, Uíge, Angola.\n"
                f"• **Amostra:** 1000 Inquiridos (55% Mulheres / 45% Homens).\n"
                f"• **Universo Demográfico:** População estimada entre 20.000 a 35.000 habitantes.")

    return ("🤖 Compreendo a tua questão, mas preciso que sejas mais específico para buscar no relatório. "
            "Tenta usar palavras como **segurança**, **hospital**, **vagas na escola**, **água** ou **luz**.")


# 3. INTERFACE INTERATIVA DO SITE (STREAMLIT)


with st.sidebar:
    st.markdown('<center><img src="https://upload.wikimedia.org/wikipedia/commons/e/e1/Logo_Unikivi.png" width="110"></center>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-header">Universidade Kimpa Vita</div>', unsafe_allow_html=True)
    st.caption("Instituto Politécnico • Engenharia Informática")
    st.markdown("---")
    st.markdown("**Cadeira:** Inteligência Artificial II")
    st.markdown("**Docente:** Nganga Pedro")
    st.markdown("---")
    st.markdown("**Grupo de Desenvolvedores (3º Ano):**")
    st.markdown("- 👨‍💻 Henrique C. Cassanda\n- 👨‍💻 Fernando L. A. Jorge\n- 👨‍💻 João F. da Costa\n- 👨‍💻 Manuel A. Tolentino\n- 👩‍💻 Teodora M. Domingos")

# Renderização Central do Robô
nome_imagem = "images (6).jpg"
st.markdown('<div class="robot-image-container">', unsafe_allow_html=True)

if os.path.exists(nome_imagem):
    st.image(nome_imagem, width=180)
else:
    st.markdown('<div class="robot-emoji"></div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<h1 class="main-title">IA II - Portal Candombe Velho</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">Agente de IA treinado para interpretar dados lógicos e estatísticos do relatório comunitário.</p>', unsafe_allow_html=True)

# Mensagem inicial com saudação dinâmica inteligente
if "messages" not in st.session_state:
    saudacao_inicial = obter_saudacao_fuso_horario()
    st.session_state.messages = [
        {"role": "assistant", "content": f"Olá, {saudacao_inicial.lower()}! Sou o assistente virtual do Candombe Velho. Podes perguntar-me sobre a criminalidade, o estado dos hospitais, a situação da água/luz ou o abandono escolar. Como posso ajudar o vosso grupo hoje?"}
    ]

# Exibição do histórico de mensagens
for message in st.session_state.messages:
    if message["role"] == "user":
        st.markdown(f'<div class="user-bubble">👤 **Tu:**<br>{message["content"]}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="bot-bubble">{message["content"]}</div>', unsafe_allow_html=True)

# Entrada do utilizador
if prompt := st.chat_input("Digita a tua mensagem ou saudação..."):
    st.markdown(f'<div class="user-bubble">👤 **Tu:**<br>{prompt}</div>', unsafe_allow_html=True)
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with st.spinner("A processar resposta..."):
        time.sleep(0.2)
        resposta = motor_ia_intencao(prompt)
        
    st.markdown(f'<div class="bot-bubble">{resposta}</div>', unsafe_allow_html=True)
    st.session_state.messages.append({"role": "assistant", "content": resposta})
