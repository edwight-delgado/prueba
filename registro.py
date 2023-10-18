import streamlit as st
import pandas as pd
import numpy as np
from st_aggrid import AgGrid, GridUpdateMode
from st_aggrid.grid_options_builder import GridOptionsBuilder

#lectura de variables y database
df = pd.read_csv('database/data.csv',sep=";")
gd = GridOptionsBuilder.from_dataframe(df)
gd.configure_selection(selection_mode='single', use_checkbox=True)
gridoptions =gd.build()

#@st.cache_data
def registro():    
    excel_file = pd.read_csv('database/casagrande.csv', encoding="UTF-8")
    return excel_file
 
def catalogo(text_search):
    
    # Filter the dataframe using masks
    m1 = df["precio"].str.contains(text_search)
    m2 = df["titulo"].str.lower()
    m2 = m2.str.contains(text_search)
    df_search = df[m1 | m2]

        # Show the results, if you have a text_search
    if text_search:
        #st.write(df_search)
        grid_table =AgGrid(df_search, height=250, gridOptions=gridoptions, update_mode=GridUpdateMode.SELECTION_CHANGED)

    else:

        grid_table =AgGrid(df, height=250, gridOptions=gridoptions, update_mode=GridUpdateMode.SELECTION_CHANGED)

    seleted_row = grid_table['selected_rows']

    #new_data = st.dataframe(seleted_row)
    d = pd.DataFrame(seleted_row)

    return d

def reporte(search, fecha_search):
    excel_file = registro()
    if search:
        fecha_search = pd.to_datetime(fecha_search, format='%Y-%m-%d')
        #fecha_search = datetime.date(fecha_search.year,fecha_search.month,fecha_search.day)
        excel_file['fecha'] = pd.to_datetime(excel_file['fecha'], format='%Y-%m-%d')
        fecha_df = excel_file['fecha']
        filterd_df = excel_file.loc[(fecha_df >= fecha_search) & (fecha_df <= fecha_search)]
    
        #data = filterd_df[['precio','neto']].apply(np.sum)
        #st.bar_chart(data=filterd_df,y="venta")
        #st.write(filterd_df)

        #df_fecha = filterd_df.groupby('fecha').sum()
        df_metodo = filterd_df.groupby('metodo_pago')['venta'].sum()
        df_direccion = filterd_df.groupby('direccion')['venta'].sum()
        df_titulo = filterd_df.groupby('titulo')['venta'].sum()
        st.bar_chart(
            data=df_metodo,
            y="venta",
            )
        st.write(df_metodo)

        st.bar_chart(
            data=df_direccion,
            y="venta",
            )
        st.bar_chart(
            data=df_titulo,
            y="venta",
            )
        st.write(df_direccion)
        #st.write(filterd_df.groupby('metodo_pago')['venta'].sum())
    else:

        #data  = excel_file[['precio','neto']].apply(np.sum)
        df_fecha = excel_file.groupby('fecha').sum()
        st.bar_chart(data=df_fecha,y="venta")
        st.write(df_fecha)
        #st.write(excel_file.groupby(['fecha','direccion']).sum())

    #st.markdown(f"## Total ventas: **{data['precio']}**")
    #st.markdown(f"## Total neto: **{data['neto']}**")
    #st.area_chart(data,x=['precio','neto'])
    #st.write(fecha_df, fecha_search)
    #st.write(filterd_df.groupby('direccion').sum())
    #st.write(filterd_df.groupby('metodo_pago')['cantidad'].count())
    #st.write(filterd_df.groupby('metodo_pago')['precio'].sum())