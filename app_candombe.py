import streamlit as st
import time

# Configuração da página web
st.set_page_config(page_title="IA II - Portal Candombe", page_icon="🤖", layout="centered")

# =====================================================================
# 1. MAPEAMENTO SEMÂNTICO DE INTENÇÕES (DADOS REAIS DO RELATÓRIO)
# =====================================================================
INTENCOES = {
    "seguranca": {
        "conceitos": ["segurança", "seguro", "inseguro", "criminalidade", "crime", "crimes", "roubo", "roubos", "assalto", "assaltos", "gatuno", "gatunos", "ladrão", "ladrao", "ladrões", "droga", "drogas", "tráfico", "violência", "prostituição", "perigo", "noite", "confusão"],
        "titulo": "Segurança Pública e Criminalidade",
        "texto": "🚨 **[DIAGNÓSTICO DE SEGURANÇA PÚBLICA - PROPORÇÃO PARA 1000 INQUIRIDOS]**\n\n"
                 "Com base no relatório, **88%** dos moradores classificam o bairro como inseguro. Numa escala de 1000 pessoas, isto representa **880 indivíduos**.\n"
                 "• **Roubo:** 76% das menções (760 pessoas em 1000).\n"
                 "• **Tráfico e consumo de drogas:** 60% das menções (600 pessoas em 1000).\n"
                 "• **Violência física:** 48% das menções (480 pessoas em 1000).\n"
                 "• **Prostituição:** 36% das menções (360 pessoas em 1000)."
    },
    "saude": {
        "conceitos": ["saúde", "saude", "hospital", "hospitais", "posto", "postos", "médico", "médicos", "medico", "doente", "doentes", "doença", "doenças", "malária", "malaria", "paludismo", "tifoide", "febre", "saneamento", "lixo", "clínica"],
        "titulo": "Saúde e Epidemiologia",
        "texto": "🏥 **[DIAGNÓSTICO DE SAÚDE - PROPORÇÃO PARA 1000 INQUIRIDOS]**\n\n"
                 "O bairro dispõe de apenas 1 hospital e 2 postos médicos para uma população estimada entre 20.000 a 35.000 habitantes.\n"
                 "Num universo de 1000 pessoas:\n"
                 "• **Doenças Crónicas:** Afetam 32% dos inquiridos (**320 pessoas**).\n"
                 "• **Malária (Paludismo):** É a mais frequente, atingindo 56% (**560 pessoas**).\n"
                 "• **Febre Tifoide:** Atinge 32% (**320 pessoas**), estando fortemente ligada à falta de saneamento."
    },
    "infraestrutura": {
        "conceitos": ["infraestrutura", "infraestruturas", "água", "agua", "luz", "energia", "eletricidade", "apagão", "vias", "estrada", "estradas", "asfalto", "lama", "chuva", "chuvas", "buraco", "buracos", "zona 3", "poço", "cacimba", "riacho"],
        "titulo": "Infraestrutura e Serviços Básicos",
        "texto": "⚡ **[INFRAESTRUTURA E SERVIÇOS BÁSICOS - PROPORÇÃO PARA 1000 INQUIRIDOS]**\n\n"
                 "• **Energia Elétrica:** 84% (**840 pessoas** em 1000) têm acesso regular à rede pública, enquanto 16% (**160 pessoas**) sofrem com falhas.\n"
                 "• **Água Potável:** 80% (**800 pessoas** em 1000) usam a rede pública. Porém, 20% (**200 pessoas**) dependem de cacimbas, poços e riachos urbanos.\n"
                 "• **Vias de Acesso:** As ruas principais estão asfaltadas, mas as zonas periféricas (como a Zona 3) sofrem com estradas de terra batida, buracos e muita lama nas chuvas."
    },
    "educacao": {
        "conceitos": ["educação", "educacao", "escola", "escolas", "ensino", "estudar", "criança", "crianças", "vagas", "vaga", "abandono", "evasão", "professor", "creche", "parque", "infantil", "aluno", "alunos"],
        "titulo": "Setor Educativo e Infância",
        "texto": "📚 **[ANÁLISE DO SETOR EDUCATIVO - PROPORÇÃO PARA 1000 INQUIRIDOS]**\n\n"
                 "Embora o bairro tenha 6 escolas em funcionamento, estimativas baseadas na taxa de exclusão de 15% indicam que cerca de **480 a 825 crianças** em idade escolar estão fora do sistema de ensino por falta de vagas ou condições financeiras. O bairro apresenta uma ausência total de creches e parques infantis."
    },
    "solucoes": {
        "conceitos": ["solução", "soluções", "solucao", "ajuda", "ajudar", "resolver", "melhorar", "governo", "administração", "recomendações", "recomenda", "proposta", "propostas", "sugestão", "intervenção"],
        "titulo": "Diretrizes e Recomendações",
        "texto": "💡 **[RECOMENDAÇÕES DA IA PARA O DESENVOLVIMENTO]**\n\n"
                 "1. Reforço da segurança pública com policiamento e iluminação pública noturna.\n"
                 "2. Construção de novos postos médicos comunitários descentralizados.\n"
                 "3. Inserção escolar para mitigar os 15% de crianças fora do sistema.\n"
                 "4. Implementação de creches e espaços de lazer infantil.\n"
                 "5. Campanhas de saneamento básico e distribuição de água potável para os 20% afetados.\n"
                 "6. Requalificação e terraplenagem das vias críticas da Zona 3."
    }
}

# =====================================================================
# 2. MOTOR DE IA POR CONTEXTO LÓGICO
# =====================================================================
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
        return f"📋 **[Contexto Identificado: {dados_finais['titulo']}]**\n\n{dados_finais['texto']}"
        
    if any(saudacao in pergunta for saudacao in ["olá", "ola", "bom dia", "boa tarde", "tudo bem", "candombe", "bairro", "projeto", "relatório", "amostra", "inquiridos", "divisão"]):
        return (f"📊 **[Dados Gerais e Caracterização da Amostra - Proporção para 1000]**\n\n"
                f"• **Localização:** Bairro Candombe Velho, Município e Província do Uíge, Angola.\n"
                f"• **Equipa de Campo:** Henrique, Fernando, João, Manuel e Teodora (09/04/2026).\n"
                f"• **Amostra Proporcional Expandida (1000 Inquiridos):**\n"
                f"  - **Sexo:** 550 Mulheres (55%) e 450 Homens (45%).\n"
                f"  - **Idades:** 18-25 anos (150), 26-35 anos (250), 36-45 anos (280), 46-55 anos (190), 56+ anos (130).\n"
                f"• **Universo Demográfico:** População total estimada entre 20.000 a 35.000 habitantes.")

    return ("🤖 Compreendo que tens uma dúvida sobre o Candombe Velho. Tenta reestruturar a tua pergunta. "
            "Podes questionar sobre a **segurança**, **saúde/hospitais**, **água/luz/estradas**, ou a situação das **escolas**.")

# =====================================================================
# 3. INTERFACE INTERATIVA DO SITE (STREAMLIT)
# =====================================================================

with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/e/e1/Logo_Unikivi.png", width=100)
    st.title("Universidade Kimpa Vita")
    st.subheader("Instituto Politécnico")
    st.caption("Curso de Engenharia Informática")
    st.markdown("---")
    st.markdown("**Cadeira:** Inteligência Artificial II")
    st.markdown("**Trabalho:** Portal de Dados de Angola")
    st.markdown("**Docente:** Nganga Pedro")
    st.markdown("---")
    st.markdown("**Desenvolvedores (3º Ano):**")
    st.write("- Henrique Calenda Cassanda\n- Fernando Lourenço A. Jorge\n- João Fernando da Costa\n- Manuel António Tolentino\n- Teodora Miguel Domingos")

st.title("🧠 Inteligência Artificial II - Candombe Velho")
st.write("Este agente de IA interpreta o contexto lógico da tua frase e aplica as proporções matemáticas exatas do teu relatório técnico.")

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Olá! Estou pronto. Podes perguntar-me sobre a criminalidade, o estado dos hospitais, a situação da água e luz, ou o abandono das crianças nas escolas. O que queres saber?"}
    ]

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

if prompt := st.chat_input("Digita a tua pergunta com total liberdade..."):
    with st.chat_message("user"):
        st.write(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        message_placeholder.markdown("*A decifrar a intenção da frase...*")
        time.sleep(0.4)
        
        resposta = motor_ia_intencao(prompt)
        message_placeholder.markdown(resposta)
        
    st.session_state.messages.append({"role": "assistant", "content": resposta})