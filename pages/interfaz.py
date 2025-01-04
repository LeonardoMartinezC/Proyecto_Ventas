import streamlit as st
# En esta pagina se establece el flujo de las paginas que existiran en el documento

# Se llama a navigation para la navegacion entre las paginas que se definen
pg = st.navigation([

    st.Page("page1.py", title="Exploración"),
    st.Page("page2.py", title="Visualización", icon=":material/favorite:"),
    st.Page("page3.py", title="Recomendaciones", icon = "")
],expanded=True)


# Se corre la navegacion y despues se verifica que se haya establecido de manera correcta la barra de opciones de paginas

pg.run()
st.sidebar.success("Escoge una de tus paginas")







