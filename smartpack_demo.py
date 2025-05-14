import streamlit as st
import pandas as pd
import random
import plotly.express as px

# --- Simulación de base de datos coherente
productos_materiales = {
    "Cápsulas de café": "Aluminio",
    "Botella PET": "PET",
    "Caja de cereal": "Cartón",
    "Lata de bebida": "Aluminio",
    "Botella de vidrio": "Vidrio",
    "Envase de yogurt": "Plástico rígido",
    "Empaque de galletas": "Plástico flexible"
}
ciudades = ["CDMX", "Bogotá", "Santiago", "Buenos Aires", "Madrid"]
productos = list(productos_materiales.keys())

data = {
    "ID Empaque": [f"PACK-{i:04}" for i in range(1, 51)],
    "Producto": random.choices(productos, k=50)
}
df = pd.DataFrame(data)
df["Material"] = df["Producto"].map(productos_materiales)
df["Ciudad"] = random.choices(ciudades, k=50)
df["Reciclado"] = random.choices([True, False], k=50)  # ✅ ESTA columna se mantiene

centros_direcciones = {
    "CDMX": ["Centro Verde - Av. Insurgentes 123", "RecoPlast - Calz. Tlalpan 456"],
    "Bogotá": ["ReciclaYA - Cra 7 #45-67", "EcoAndes - Calle 80 #12-34"],
    "Santiago": ["EcoSantiago - Av. Providencia 890", "Replast - Pajaritos 123"],
    "Buenos Aires": ["Reutil BA - Av. Corrientes 998", "Verde Capital - Palermo 456"],
    "Madrid": ["Madrid Circular - Calle Alcalá 76", "EcoMadrid - Gran Vía 55"]
}

# --- Interfaz Streamlit
st.title("🔄 SmartPack Demo – Plataforma Inteligente de Empaques")
tab1, tab2 = st.tabs(["👤 Vista del Usuario", "🏢 Vista del Administrador"])

# -------------------- VISTA DEL USUARIO --------------------
with tab1:
    st.header("Vista del Usuario")
    codigo_input = st.text_input("🔍 Código del empaque (ID)", placeholder="Ej. 0001 o PACK-0001")
    ciudad = st.selectbox("📍 Ciudad actual", ["Selecciona una ciudad", "CDMX", "Bogotá", "Santiago", "Buenos Aires", "Madrid"])
    confirmar = st.button("Confirmar escaneo")

    if confirmar:
        if ciudad == "Selecciona una ciudad":
            st.warning("⚠️ Por favor selecciona una ciudad válida.")
        else:
            codigo = f"PACK-{codigo_input.zfill(4)}" if codigo_input else ""
            resultado = df[df["ID Empaque"] == codigo]

            if resultado.empty:
                st.error("❌ Código no reconocido.")
            else:
                producto = resultado["Producto"].values[0]
                material = resultado["Material"].values[0]
                reciclable = material in ["Aluminio", "PET"]

                st.success(f"Producto: {producto} | Material: {material}")
                st.balloons()
                st.markdown("### ♻️ Instrucciones de sustentables")

                if reciclable:
                    st.markdown("✅ Este material puede reciclarse fácilmente en tu ciudad.")
                    st.success("🎉 ¡Gracias por tu acción! Has ganado **100 puntos**.")
                    impacto = random.choice([
                        "💡 Equivale a 1 día de luz ahorrada.",
                        "🌳 Si reciclas 7 más como este, ¡estarás salvando un árbol!",
                        "💧 Evitaste el uso de 10 litros de agua.",
                        "🏭 Redujiste CO₂ como evitar 5 km en auto.",
                        "♻️ Ayudaste a mantener limpia tu ciudad."
                    ])
                    st.markdown(f"🌍 Impacto estimado: {impacto}")

                    with st.expander("📍 Consultar centros de reciclaje cercanos"):
                        st.markdown("### 🗺️ Centros de reciclaje en tu ciudad:")
                        for direccion in centros_direcciones.get(ciudad, []):
                            st.markdown(f"- {direccion}")
                else:
                    st.markdown("⚠️ Este material tiene bajo índice de reciclaje. Intenta darle otro uso.")
                    st.markdown("🔁 **¿Sabías que al reutilizar este empaque puedes ayudar a:**")
                    st.markdown("- 🌳 Salvar árboles evitando residuos innecesarios")
                    st.markdown("- 💡 Ahorrar energía de producción")
                    st.markdown("- 💧 Conservar agua usada en empaques nuevos")
                    st.success("👏 Gracias por tu conciencia ambiental. Has ganado **20 puntos** por tu compromiso.")

# -------------------- VISTA DEL ADMINISTRADOR --------------------
with tab2:
    st.header("Vista del Administrador – SmartPack Dashboard")

    total_escaneos = len(df)
    tasa_reciclaje = df["Reciclado"].mean()
    ciudad_top = df["Ciudad"].mode()[0]

    col1, col2, col3 = st.columns(3)
    col1.metric("📦 Total de escaneos", total_escaneos)
    col2.metric("♻️ Tasa de reciclaje", f"{tasa_reciclaje*100:.1f}%")
    col3.metric("📍 Ciudad más activa", ciudad_top)

    st.markdown("---")

    total_reciclados = df["Reciclado"].sum()
    energia_ahorrada_kwh = total_reciclados * 2.3
    agua_ahorrada_litros = total_reciclados * 10
    arboles_salvados = total_reciclados // 7

    st.subheader("🌱 Impacto Ambiental Estimado")
    col4, col5, col6 = st.columns(3)
    col4.metric("⚡ Energía ahorrada", f"{energia_ahorrada_kwh:.1f} kWh")
    col5.metric("💧 Agua conservada", f"{agua_ahorrada_litros} litros")
    col6.metric("🌳 Árboles salvados", f"{arboles_salvados}")

    st.markdown("---")

    precios_material = {"Aluminio": 0.15, "PET": 0.08, "Cartón": 0.03}
    df_reciclado = df[df["Reciclado"] == True].copy()
    df_reciclado["Ahorro USD"] = df_reciclado["Material"].map(precios_material)
    ahorro_material = df_reciclado["Ahorro USD"].sum()
    ahorro_logistico = len(df_reciclado) * 0.02
    ahorro_total = ahorro_material + ahorro_logistico

    st.subheader("💰 Ahorro Económico Estimado")
    col7, col8 = st.columns(2)
    col7.metric("🔧 Ahorro por reciclaje", f"${ahorro_material:,.2f} USD")
    col8.metric("🚛 Ahorro logístico", f"${ahorro_logistico:,.2f} USD")
    st.success(f"🧾 **Total estimado ahorrado:** ${ahorro_total:,.2f} USD")

    st.markdown("---")

    st.subheader("📍 Escaneos por Ciudad")
    ciudad_count = df["Ciudad"].value_counts().reset_index()
    ciudad_count.columns = ["Ciudad", "Cantidad"]
    fig1 = px.bar(ciudad_count, x="Ciudad", y="Cantidad", text="Cantidad",
                  color="Cantidad", color_continuous_scale="Tealgrn", title="Escaneos por ciudad")
    st.plotly_chart(fig1, use_container_width=True)

    st.subheader("📦 Distribución por Material")
    material_count = df["Material"].value_counts().reset_index()
    material_count.columns = ["Material", "Cantidad"]
    fig2 = px.pie(material_count, names="Material", values="Cantidad", title="Materiales escaneados")
    st.plotly_chart(fig2, use_container_width=True)

    st.subheader("🧃 Escaneos por Tipo de Producto")
    producto_count = df["Producto"].value_counts().reset_index()
    producto_count.columns = ["Producto", "Cantidad"]
    fig3 = px.bar(producto_count, x="Producto", y="Cantidad", text="Cantidad",
                  color="Cantidad", color_continuous_scale="Purples", title="Escaneos por producto")
    st.plotly_chart(fig3, use_container_width=True)

    st.subheader("📋 Detalle de Registros")
    st.dataframe(df, use_container_width=True)

    st.subheader("🤖 Recomendaciones del sistema")
    if tasa_reciclaje < 0.5:
        st.warning("⚠️ La tasa de reciclaje es baja. Se recomienda reforzar campañas educativas y rediseñar empaques con bajo retorno.")
    else:
        st.success("✅ Buen desempeño. Mantener incentivos y continuar expansión regional.")
