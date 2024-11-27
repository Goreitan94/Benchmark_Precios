import streamlit as st
import pandas as pd

# Contraseña para acceder a la app
PASSWORD = "Eitangor1994"  # Cambia esta contraseña por la que prefieras

# Función para verificar la contraseña
def login():
    """Pantalla de login para ingresar la contraseña."""
    st.title("Inicio de Sesión")
    st.sidebar.header("Acceso a la aplicación")
    password = st.sidebar.text_input("Introduce la contraseña:", type="password")
    if password == PASSWORD:
        st.session_state.logged_in = True
        st.sidebar.success("Acceso concedido. Recarga la página para salir.")
    elif password:
        st.sidebar.error("Contraseña incorrecta.")
    else:
        st.sidebar.info("Introduce la contraseña para continuar.")

# Verificar si ya se inició sesión
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if st.session_state.logged_in:
    # Cargar los datos
    @st.cache
    def load_data():
        file_path = 'benchmark_precios.xlsx'  # Asegúrate de que este archivo esté en el mismo directorio que la app.
        data = pd.ExcelFile(file_path).parse('Sheet1')
        # Normalize column names
        data.columns = data.columns.str.strip().str.lower()
        # Remove empty columns
        data = data.drop(columns=[col for col in data.columns if "unnamed" in col])
        return data

    df = load_data()

    # Título de la app
    st.title("Benchmark de Precios por Barrio")

    # Filtrar por barrio
    st.sidebar.header("Búsqueda por Barrio")
    barrios_disponibles = df['barrio'].unique()
    barrio_seleccionado = st.sidebar.selectbox("Selecciona un barrio:", barrios_disponibles)

    # Mostrar información del barrio seleccionado
    st.subheader(f"Datos para el barrio: {barrio_seleccionado}")
    filtro_barrio = df[df['barrio'] == barrio_seleccionado]
    st.write(filtro_barrio)

    # Entrada de precio y m²
    st.sidebar.header("Cálculo del Precio por m²")
    precio_total = st.sidebar.number_input("Introduce el precio total (€):", min_value=0.0, step=1000.0)
    metros_cuadrados = st.sidebar.number_input("Introduce los m²:", min_value=1.0, step=1.0)
    precio_por_m2 = precio_total / metros_cuadrados
    if precio_total > 0 and metros_cuadrados > 0:
        precio_por_m2 = precio_total / metros_cuadrados
        st.sidebar.write(f"Precio por m² calculado: €{precio_por_m2:.2f}")

    # Comparar con los datos del barrio
    if 'venta' in filtro_barrio.columns and 'compra' in filtro_barrio.columns and 'margen 15%' in filtro_barrio.columns:
        precio_venta = filtro_barrio['venta'].values[0]
        precio_compra = filtro_barrio['compra'].values[0]
        margen = filtro_barrio['margen 15%'].values[0]

        # Mostrar resultados
        st.subheader("Resultados del Cálculo")
        st.write(f"Precio de Venta: €{precio_venta:.2f}")
        st.write(f"Precio de Compra: €{precio_compra:.2f}")
        st.write(f"Margen del 15%: €{margen:.2f}")

        # Calcular porcentajes
        porcentaje_margen = ((precio_por_m2 - margen) / margen) * 100
        porcentaje_compra = ((precio_por_m2 - precio_compra) / precio_compra) * 100

        # Mostrar porcentajes
        #st.write(f"Porcentaje respecto al margen: {porcentaje_margen:.2f}%")
        st.write(f"Porcentaje respecto a la compra: {porcentaje_compra:.2f}%")

        # Identificar oportunidad
        if precio_por_m2 < margen:
            st.markdown(f"### :green[¡Oportunidad!]")
        else:
            st.markdown(f"### No es una oportunidad.")
    else:
        st.error("Faltan columnas en los datos para calcular los resultados.")
else:
    login()
