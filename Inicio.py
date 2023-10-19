#from tkinter.messagebox import NO
import streamlit as st
from registro import registro, catalogo, reporte
import pandas as pd
import numpy as np
import datetime

st.set_page_config(layout="wide")
#aside area
cantidad = 0
peso = 0
precio_venta = 0
p_venta = 0
precio_neto = 0
precio = 0
precio_costo = 0


tab1, tab2, tab3 = st.tabs(["Catalogo", "Registro", "Reporte"])

with tab1:
    st.header("Catalogo")
    
    text_search = st.text_input("buscar", value="")
    text_search = text_search.lower()

    d = catalogo(text_search)

try:
    titulo = d.get('titulo')
    precio_a = d.get('precio')
    precio_costo = float(precio_a[0])
    precio_venta_a = d.get('pventa')
    precio_venta = float(precio_venta_a[0])

    st.sidebar.markdown(f"nombre: **{titulo[0]}**")
    st.sidebar.markdown(f"precio:  ** {precio_a[0]}** ")
    st.sidebar.markdown(f"precio costo:  ** {precio_venta_a[0]}** ")
    img = d.get('img')
    if img[0] is not None:
        st.sidebar.image('./images/'+ img[0])

except:
    st.sidebar.markdown(f"nombre: ")
    st.sidebar.markdown(f"precio: ")

fecha = st.sidebar.date_input('fecha')
departamento = st.sidebar.text_input('apartamento')

metodo = st.sidebar.radio('metodo de pago:', ['transferencia','efectivo', 'debito'])

peso_select = st.sidebar.radio('se vende por peso:', ['No','Si'])

if peso_select=='No':
    cantidad = int(st.sidebar.number_input('cantidad', 1, 100))
    peso = float(st.sidebar.number_input('peso (gr)', disabled=True, key="peso1"))
    p_venta = cantidad * precio_venta
    precio_neto = cantidad * precio_costo

else:
    cantidad = int(st.sidebar.number_input('cantidad', 1, 100, disabled=True))
    peso = float(st.sidebar.number_input('peso (gr)', disabled=False, key="peso2"))
    p_venta = peso * precio_venta
    precio_neto = peso * precio_costo


# carculo y formula 


utilidad = p_venta - precio_neto


agregar = st.sidebar.button('agregar')


if agregar:

    if (titulo is not None) and (departamento !='') :

        excel_file = pd.read_csv('database/casagrande.csv')
        # Create a new dataframe to be appended to the Excel sheet
        new_data = pd.DataFrame({
            'titulo': titulo, 
            'direccion': departamento, 
            'cantidad':cantidad,
            'precio':precio_venta,
            'venta':p_venta, 
            'neto': precio_neto, 
            'utilidad':utilidad, 
            'metodo_pago':metodo,
            'fecha':fecha
        })

        # Append the new dataframe to the existing dataframe
        appended_data = pd.concat([excel_file, new_data])

        # Optionally, you can reset the index of the appended dataframe
        appended_data = appended_data.reset_index(drop=True)

        # Write the appended data to the Excel file
        appended_data.to_csv('database/casagrande.csv', index=False)
        st.sidebar.success("guardado corretamente")
    
    else:
        excel_file = registro()
        st.sidebar.warning("campo esta vacio")
    

with tab2:
    
    st.header("casagrande registro")
    excel_file = registro()

    #st.download_button('descarga',excel_file)
    sa = excel_file.to_csv().encode('utf-8')
    data_as_csv= excel_file.to_csv(index=False).encode("utf-8")
    st.download_button(
        "Download data as CSV", 
        data_as_csv, 
        "benchmark-tools.csv",
        "text/csv",
        key="download-tools-csv",
    )
    st.empty()
    st.dataframe(excel_file) 

with tab3:
    st.header("Reporte")
    fecha_search = st.date_input('fecha',key='search_fecha')
    search = st.button('buscar')
    r = reporte(search, fecha_search)