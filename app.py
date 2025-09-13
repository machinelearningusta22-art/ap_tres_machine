import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import geopandas as gpd
import numpy as np
from matplotlib.colors import LinearSegmentedColormap, PowerNorm 

st.set_page_config(
    page_title="Proyecto 3",
)


st.title("Proyecto 3")


data = pd.read_csv("datos3.csv")
gdf  = gpd.read_parquet('datos3.parquet')


departamentos = sorted(data["departamento"].unique().tolist())
departamento = st.selectbox("Seleccione un departamento:", departamentos)

municipios = sorted(data[data["departamento"] == departamento]["municipio"].unique().tolist())
municipio = st.selectbox("Seleccione un municipio:", municipios)



filtro = data[(data["departamento"] == departamento) & (data["municipio"] == municipio)]


tasa_mun = filtro["tasa_homicidios"].values[0]
tasa_dep = data[data["departamento"] == departamento]["tasa_homicidios"].mean()
tasa_nal = data["tasa_homicidios"].mean()


st.metric(
    label=f"Tasa homicidio (x 100.000 habitantes)",
    value=f"{tasa_mun:.2f}"
)


comparativo = pd.DataFrame({
    "Nivel": ["Municipio"],
    "Tasa": [tasa_mun]
})

fig = px.bar(
    comparativo,
    x="Nivel",
    y="Tasa",
    color="Nivel",
    text="Tasa",
    title="Comparación de la tasa de homicidios (x 100.000 hab.)",
    color_discrete_sequence=["#1D2783"]  
)

fig.update_traces(texttemplate='%{text:.2f}', textposition="outside")
st.plotly_chart(fig, use_container_width=True)



st.subheader(" Municipios con más y menos homicidios en 2024")


ordenados = data.sort_values(by="homicidios", ascending=False)

top10_mas = ordenados.head(10)
top10_menos = ordenados.tail(10)


fig_mas = px.bar(
    top10_mas.sort_values("homicidios"),  
    x="homicidios",
    y="municipio",
    orientation="h",
    title="municipios con más homicidios",
    text="homicidios",
    color_discrete_sequence=["#e83807"]  
)
fig_mas.update_traces(textposition="outside")
st.plotly_chart(fig_mas, use_container_width=True)


fig_menos = px.bar(
    top10_menos.sort_values("homicidios"),
    x="homicidios",
    y="municipio",
    orientation="h",
    title="municipios con menos homicidios",
    text="homicidios",
    color_discrete_sequence=["#066C26"]  
)
fig_menos.update_traces(textposition="outside")
st.plotly_chart(fig_menos, use_container_width=True)


st.subheader("Distribución de homicidios en 2024")


# AGREGACIÓN POR DEPARTAMENTO

dep_data = (
    data.groupby("departamento")[["homicidios", "poblacion"]]
    .sum()
    .reset_index()
)

# Calculamos tasa departamental promedio
dep_data["tasa_homicidios"] = (dep_data["homicidios"] / dep_data["poblacion"] * 100000).round(2)

# =====================
# GRÁFICO DE BARRAS - POR DEPARTAMENTO
# =====================
fig_dep = px.bar(
    dep_data.sort_values("homicidios", ascending=False),
    x="homicidios",
    y="departamento",
    orientation="h",
    title="homicidios por departamento ",
    text="homicidios",
    color_discrete_sequence=["#0B606E"]
)
fig_dep.update_traces(textposition="outside")
st.plotly_chart(fig_dep, use_container_width=True)

fig,ax = plt.subplots(1,1, figsize = (10, 8))

gdf.plot(column = 'tasa_homicidios', ax = ax, missing_kwds={
        "color": "lightgrey",
        "edgecolor": "white",
      
    })
ax.set_axis_off()

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

# Paleta: azul frío a naranja cálido
blue_orange = ["#EAF2FA","#CFE3F5","#9BC2E6","#4A90E2","#1F5AA6","#F5C29A","#F09E66","#EB7A3B","#C05A17"]
cmap_bo = LinearSegmentedColormap.from_list("BlueOrange", blue_orange)

vals = gdf["tasa_homicidios"].astype(float).to_numpy()
vmin, vmax = 0, np.nanpercentile(vals, 98)
n_trunc = int(np.sum(vals > vmax))

fig, ax = plt.subplots(1, 1, figsize=(4, 4), dpi=220)
gdf.plot(
    column="tasa_homicidios",
    ax=ax,
    cmap=cmap_bo,
    vmin=vmin, vmax=vmax,
    legend=True,
    edgecolor="#3E3E3E", linewidth=0.15,
    missing_kwds={"color":"#BDBDBD","edgecolor":"#3E3E3E","hatch":"///","label":"Sin datos"}
)
ax.set_facecolor("none"); fig.patch.set_alpha(0); ax.axis("off")
cb = ax.get_figure().axes[-1]; cb.tick_params(colors="#E6E6E6", labelsize=8); cb.set_ylabel("tasa x 100k", color="#E6E6E6")
if n_trunc>0: ax.text(0.01,0.01,f"Escala truncada p98 (↑{n_trunc})",transform=ax.transAxes,color="#CFCFCF",fontsize=7)
st.pyplot(fig)



