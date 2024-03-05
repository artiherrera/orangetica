import streamlit as st
from streamlit_option_menu import option_menu
import resumen, info_operadores, info_distrito
import os

current_dir = os.path.dirname(__file__)


icon_path = os.path.join(current_dir, "assets", "orange.ico")
logo_path = os.path.join(current_dir, "assets", "orange.png")

st.set_page_config(page_title="Orangética", page_icon=icon_path)

# Simulación de una base de datos de usuarios
usuarios = {"orange": "Naranja123", "apple": "Manzana123", "banana": "Plátano123"}

# Función para mostrar el formulario de inicio de sesión centrado
def mostrar_login_centro():
    st.title("Login")
    with st.form("form_login"):
        usuario = st.text_input("Nombre de usuario", key="usuario_centro")
        contraseña = st.text_input("Contraseña", type="password", key="contraseña_centro")
        submit_button = st.form_submit_button("Iniciar sesión")
        
        if submit_button:
            if usuario in usuarios and usuarios[usuario] == contraseña:
                st.session_state['autenticado'] = True
                st.rerun()
            else:
                st.error("El nombre de usuario o la contraseña son incorrectos.")

# Inicializar el estado de autenticación si no existe
if 'autenticado' not in st.session_state:
    st.session_state['autenticado'] = False

def mostrar_login_centro():
    """Muestra el formulario de inicio de sesión en el centro de la página."""
    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:  # Usar la columna central
        st.title("Login")

        usuario = st.text_input("Nombre de usuario")
        contraseña = st.text_input("Contraseña", type="password")

        if st.button("Iniciar sesión"):
            if usuario in usuarios and usuarios[usuario] == contraseña:
                st.session_state['autenticado'] = True
                st.rerun()
            else:
                st.error("El nombre de usuario o la contraseña son incorrectos.")

if not st.session_state['autenticado']:
    mostrar_login_centro()
else:
    
    # Configuración de la página (opcional)
    # Logo cnetrado en la barra lateral
    st.sidebar.image(logo_path, width=100, output_format='PNG', use_column_width=True)
    st.sidebar.title("Orangética")


    # Barra lateral con menú de navegación
    with st.sidebar:
        selected = option_menu("Menú", ["Resumen Ejecutivo", "Información por operador", "Información por distrito"],
            icons=['journal-text', 'person-lines-fill', 'map-fill'], menu_icon="house", default_index=0)

    # Cargar las páginas basadas en la selección
    if selected == "Resumen Ejecutivo":
        resumen.run()
    elif selected == "Información por operador":
        info_operadores.run()
    elif selected == "Información por distrito":
        info_distrito.run()


