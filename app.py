import streamlit as st
import google.generativeai as genai
import matplotlib.pyplot as plt

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="Davo Math Academy ⚽", layout="wide")

# Instrucciones de Davo (El "Cerebro")
SYSTEM_PROMPT = """
Actúa como Davo Xeneize nivel 10 (Termo total). Tu misión es enseñar fracciones.
REGLAS:
1. Hablá como streamer argentino: "boludo", "fiera", "una locura", "pará un poco".
2. Si el usuario entiende, poné [ESTADO: GOL]. Si falla, [ESTADO: ERROR].
3. Siempre que expliques una fracción, escribila así: [F: numerador/denominador].
4. Todo se explica con fútbol: el numerador son los goles, el denominador los partidos.
"""

# --- CONECTAR CON GEMINI ---
# Aquí deberás poner tu API Key en los secretos de Streamlit más tarde
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    model = genai.GenerativeModel('gemini-1.5-flash')
except:
    st.error("Che, falta la API Key en los secretos. ¡Ponete las pilas!")

# --- FUNCIÓN PARA DIBUJAR ---
def dibujar_fraccion(n, d):
    fig, ax = plt.subplots(figsize=(3, 3))
    data = [1] * d
    colors = ['#3b4252'] * d
    for i in range(min(n, d)):
        colors[i] = '#fbbf24' # Color Oro
    ax.pie(data, colors=colors, startangle=90, wedgeprops={"edgecolor":"white"})
    ax.set_title(f"Táctica: {n}/{d}", color="white", fontsize=15)
    fig.patch.set_facecolor('#0e1117')
    return fig

# --- INTERFAZ DE LA APP ---
st.title("⚽ DAVO XENEIZE: CLASE DE FRACCIONES")

if "chat" not in st.session_state:
    st.session_state.chat = []

col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📺 Streaming Educativo")
    # GIF dinámico según el último mensaje
    imagen_davo = "https://media.tenor.com/uR1kS1v-NfQAAAAC/davo-xeneize-davo.gif"
    if st.session_state.chat:
        last_res = st.session_state.chat[-1]["content"]
        if "[ESTADO: GOL]" in last_res:
            imagen_davo = "https://media.tenor.com/9O0Z-oV_H0AAAAAd/davo-boca.gif"
        elif "[ESTADO: ERROR]" in last_res:
            imagen_davo = "https://media.tenor.com/F_V9p6fP8m8AAAAC/davo-davo-xeneize.gif"
    
    st.image(imagen_davo, use_container_width=True)
    
    # Mostrar el gráfico de la fracción
    st.subheader("📋 Pizarra de Román")
    if st.session_state.chat:
        last_res = st.session_state.chat[-1]["content"]
        if "[F:" in last_res:
            frac = last_res.split("[F:")[1].split("]")[0].strip()
            n, d = map(int, frac.split("/"))
            st.pyplot(dibujar_fraccion(n, d))

with col2:
    st.subheader("💬 Chat con el Davo")
    for m in st.session_state.chat:
        with st.chat_message(m["role"]):
            st.write(m["content"])

    if prompt := st.chat_input("Escribí acá tu duda..."):
        st.session_state.chat.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)
        
        response = model.generate_content(SYSTEM_PROMPT + "\nAlumno dice: " + prompt)
        st.session_state.chat.append({"role": "assistant", "content": response.text})
        st.rerun()