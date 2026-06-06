import streamlit as st

# 1. Configuración de la página
st.title("Tarea 3 — Clasificando Patrones con una Máquina Simple")
st.write("Estudiante: Daniela Quiceno | Materia: Autómatas, Gramáticas y Lenguaje")
st.markdown("---")

# 2. Definición de los Patrones (Imágenes 3x3 representadas como listas de 9 números)
# 1 = Píxel encendido, 0 = Píxel apagado
patrones = {
    "T Clásica (Positivo)":     [1, 1, 1,  0, 1, 0,  0, 1, 0],
    "T Normal (Positivo)":      [1, 1, 1,  0, 1, 0,  0, 1, 1],
    "T Estándar (Positivo)":    [1, 1, 1,  0, 1, 0,  1, 1, 0],
    "Cruz '+' (Negativo)":      [0, 1, 0,  1, 1, 1,  0, 1, 0],
    "Diagonal (Negativo)":      [1, 0, 0,  0, 1, 0,  0, 0, 1],
    "Letra L (Negativo)":       [1, 0, 0,  1, 0, 0,  1, 1, 1],
}

# 3. PARTE INTERACTIVA: Controles para el usuario
st.sidebar.header("🎛️ Panel de Control")
st.sidebar.write("Modifica los pesos y el threshold aquí:")

# Slider para el Threshold (Umbral)
threshold = st.sidebar.slider("Threshold (Umbral de decisión)", min_value=-10.0, max_value=10.0, value=7.0, step=0.5)

# Creación de los 9 sliders para los pesos (organizados en una cuadrícula 3x3 visual)
st.sidebar.subheader("Pesos de la cuadrícula (w)")
w = []
for fila in range(3):
    cols_sidebar = st.sidebar.columns(3)
    for columna in range(3):
        idx = fila * 3 + columna
        # Inicializamos con valores sugeridos de la Tarea 2 para que sea fácil ganar
        valor_inicial = 5.0 if idx in [0, 1, 2, 4, 7] else -2.0
        peso_calc = cols_sidebar.number_input(f"w({fila+1},{columna+1})", min_value=-10.0, max_value=10.0, value=valor_inicial, step=0.5)
        w.append(peso_calc)

# 4. EVALUACIÓN DE EJEMPLOS
st.header("🔎 Evaluación Automática de Patrones")

correctas = 0
total_ejemplos = len(patrones)

# Vamos a procesar cada patrón uno por uno
for nombre, pixeles in patrones.items():
    st.subheader(f"🔷 {nombre}")
    
    # Dibujar la matriz de forma visual para cumplir con la interactividad
    cols_matriz = st.columns(3)
    for i in range(9):
        con_col = cols_matriz[i % 3]
        if pixeles[i] == 1:
            con_col.markdown("<div style='background-color: #FF4B4B; width:30px; height:30px; border-radius:5px; margin:auto;'></div>", unsafe_allow_html=True)
        else:
            con_col.markdown("<div style='background-color: #F0F2F6; width:30px; height:30px; border-radius:5px; margin:auto;'></div>", unsafe_allow_html=True)
            
    # --- LA LÓGICA MATEMÁTICA MANUAL (Sin librerías) ---
    # Multiplicar cada píxel por su peso correspondiente y sumar todo
    score = 0.0
    for i in range(9):
        score += pixeles[i] * w[i]
        
    # --- REGLA DE CLASIFICACIÓN (La condición obligatoria) ---
    if score >= threshold:
        decision = "Es una T"
    else:
        decision = "No es una T"
        
    # Verificar si la máquina acertó
    es_positivo_real = "Positivo" in nombre
    deberia_ser_T = es_positivo_real
    
    acerto = (decision == "Es una T" and deberia_ser_T) or (decision == "No es una T" and not deberia_ser_T)
    
    if acerto:
        correctas += 1
        color_resultado = "green"
        emoji = "✅ ¡Correcto!"
    else:
        color_resultado = "red"
        emoji = "❌ Error de clasificación"
        
    # Mostrar resultados del patrón en pantalla
    st.write(f"**Puntaje calculado (Score):** {score} | **Threshold:** {threshold}")
    st.markdown(f"**Decisión final:** <span style='color:{color_resultado}; font-weight:bold;'>{decision}</span> ({emoji})", unsafe_allow_html=True)
    st.markdown("---")

# 5. MARCADOR FINAL
st.header("🏆 Marcador Global")
porcentaje = (correctas / total_ejemplos) * 100
st.metric(label="Precisión del clasificador", value=f"{correctas} / {total_ejemplos}", delta=f"{porcentaje:.1f}%")

if correctas == total_ejemplos:
    st.success("🎉 ¡Perfecto! Encontraste la configuración ideal. Todas las imágenes fueron clasificadas correctamente.")
else:
    st.warning("⚠️ Sigue ajustando los pesos o el threshold en el panel izquierdo para corregir los errores.")
