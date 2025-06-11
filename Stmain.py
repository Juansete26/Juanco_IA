	
import streamlit as st
import groq as gr

st.set_page_config(page_title="JUANCO IA - La mejor en su rubro")

MODELOS = ['llama3-8b-8192', 'llama3-70b-8192']

# configuración de página  
def Configurar_pagina():
    st.title("Bienvenido a JUANCO-IA")

# crear un cliente groq
def crear_cliente_groq():
    groq_api_key = st.secrets["GROQ_API_KEY"]
    return gr.Groq(api_key=groq_api_key)

# inicializar el estado del chat
def Inicializar_estado_chat():
    if "mensajes" not in st.session_state:
        st.session_state.mensajes = []

# mostrar mensajes previos
def obtener_mensajes_previos():
    for mensaje in st.session_state.mensajes:
        with st.chat_message(mensaje['role']):
            st.markdown(mensaje["content"])

# obtener indicaciones del usuario
def obtener_mensaje_usuario():
    return st.chat_input("Enviá tu mensaje")

# guardar mensajes
def agregar_mensaje(role, content):
    st.session_state.mensajes.append({"role": role , "content": content})

# mostrar mensajes en pantalla
def mostrar_mensaje(role, content):
    with st.chat_message(role):
        st.markdown(content)

# mostrar barra lateral
def Mostrar_Sidebar():
    st.sidebar.title("Modelos de IA")
    modelo = st.sidebar.selectbox('Elegí tu modelo', MODELOS, index=0)
    st.write(f'**Elegiste el modelo:** {modelo}')
    return modelo

#llamar modelo groq
def Obtener_respuesta_modelo(Cliente, modelo, mensaje):
   Respuesta = Cliente.chat.completions.create(
        model = modelo,
        messages = mensaje,
        stream = False
    )
   return Respuesta.choices[0].message.content


# ejecutar la app principal
def ejecutar_chat():
    Configurar_pagina()
    cliente = crear_cliente_groq()
    modelo = Mostrar_Sidebar()

    Inicializar_estado_chat()
    Mensaje_usuario = obtener_mensaje_usuario()
    obtener_mensajes_previos()

    if Mensaje_usuario:
        agregar_mensaje("user",Mensaje_usuario)
        mostrar_mensaje("user",Mensaje_usuario)

        respuesta_contenido = Obtener_respuesta_modelo(cliente, modelo, st.session_state.mensajes)

        agregar_mensaje("assistant",respuesta_contenido)
        mostrar_mensaje("assistant",respuesta_contenido)



# ejecutar la app
if __name__ == '__main__':
    ejecutar_chat()
