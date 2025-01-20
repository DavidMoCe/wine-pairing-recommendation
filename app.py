import streamlit as st
import pandas as pd
import joblib

# Cargar el modelo de maridaje
@st.cache_resource
def load_model():
    model = joblib.load('modelo_maridaje.pkl')
    return model

model = load_model()

# Cargar los datos de vinos
@st.cache_data
def load_data():
    data = pd.read_csv('data/vivino_clean.csv', encoding='utf-8')
    # Diccionario de mapeo para renombrar las columnas
    column_mapping = {
        'winery': 'bodega',
        'wine_name': 'wine_name',
        'year': 'year',
        'price': 'price',
        'score': 'score',
        'country': 'country',
        'wine_type': 'wine_type',
        'pairing': 'pairing',
        'flavours': 'flavours',
        'picture': 'image',
        'price_quality': 'price_quality',
        'Estilo de vino': 'wine_style',
        'Contenido de alcohol': 'contenido_de_alcohol',
        'country_España': 'country_España',
        'country_Francia': 'country_Francia',
        'country_Italia': 'country_Italia',
        'country_Other': 'country_Other',
        'flavour_cí­trico': 'flavour_citrico',
        'flavour_especias': 'flavour_especias',
        'flavour_floral': 'flavour_floral',
        'flavour_fruta negra': 'flavour_fruta_negra',
        'flavour_fruta seca': 'flavour_fruta_seca',
        'flavour_frutos de árbol': 'flavour_frutos_de_arbol',
        'flavour_frutos rojos': 'flavour_frutos_rojos',
        'flavour_microbio': 'flavour_microbio',
        'flavour_roble': 'flavour_roble',
        'flavour_terroso': 'flavour_terroso',
        'flavour_tropical': 'flavour_tropical',
        'flavour_vegetal': 'flavour_vegetal'
    }

    # Renombrar columnas basándose en el mapeo
    data = data.rename(columns=column_mapping)

    return data

data = load_data()

# Actualizar las URLs en la columna 'image' para que comiencen con 'https:'
data['image'] = data['image'].apply(lambda x: f"https:{x}" if x.startswith('//') else x)

# Diccionario que mapea los números a los nombres de los alimentos
food_mapping = {
    0: 'Ternera',
    1: 'Ternera lechal',
    2: 'Aves',
    3: 'Pasta',
    4: 'Marisco',
    5: 'Aperitivos y tentempiés',
    6: 'Pescado blanco',
    7: 'Carne adobada',
    8: 'Cordero',
    9: 'Carne de caza',
    10: 'Cerdo',
    11: 'Vegetariana',
    12: 'Carne de caza',
    13: 'Queso azul',
    14: 'Pescado azul',
    15: 'Comida picante',
    16: 'Queso tierno y cremoso',
    17: 'Pescado azul',
    18: 'Champiñones',
    19: 'Queso curado',
    20: 'Queso de leche de cabra',
    21: 'Aperitivo'
}

# Diccionario que mapea los números a los nombres de los tipos de vino
wine_type_mapping = {
    1: 'Blanco',
    2: 'Tinto'
}

# Diccionario para mapear los países
country_mapping = {
    'españa': [1, 0, 0, 0],
    'francia': [0, 1, 0, 0],
    'italia': [0, 0, 1, 0],
    'otros': [0, 0, 0, 1]
}

#Diccionario para relacionar la calidad del precio con un número
price_quality_mapping = {
    1: 'Relación calidad-precio no disponible',
    2: 'Mejor relación calidad-precio en otros vinos',
    3: 'Relación calidad-precio razonable',
    4: 'Buena relación calidad-precio',
    5: 'Excelente relación calidad-precio',
    6:'¡Increaíble relación calidad-precio!'
}

# Diccionario para mapear los sabores
flavour_map = {
    'cítrico': [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    'especias': [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    'floral': [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    'fruta negra': [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
    'fruta seca': [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
    'frutos de árbol': [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
    'frutos rojos': [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
    'microbio': [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
    'roble': [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
    'terroso': [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
    'tropical': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
    'vegetal': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
}

# Diccionario con las descripciones de los sabores
flavour_descriptions = {
    'flavour_citrico': 'Sabor fresco y ácido, típico de frutas como naranjas y limones.',
    'flavour_especias': 'Notas especiadas que incluyen pimienta, canela o clavo.',
    'flavour_floral': 'Sabor que recuerda a flores, como jazmín o rosas.',
    'flavour_fruta_negra': 'Notas de frutas oscuras, como moras o ciruelas.',
    'flavour_fruta_seca': 'Sabor a frutas secas, como pasas o albaricoques.',
    'flavour_frutos_de_arbol': 'Sabor a frutos de árbol, como manzanas o peras.',
    'flavour_frutos_rojos': 'Notas de frutas rojas como fresas, cerezas o frambuesas.',
    'flavour_microbio': 'Notas que recuerdan a un sabor fermentado o terroso.',
    'flavour_roble': 'Sabor a madera, especialmente cuando el vino ha sido envejecido en barricas de roble.',
    'flavour_terroso': 'Sabor que recuerda a la tierra o al suelo mojado.',
    'flavour_tropical': 'Sabor a frutas tropicales como piña, mango o maracuyá.',
    'flavour_vegetal': 'Notas vegetales, como hierba fresca o pimientos.'
}

# Función que mapea el país a características One-Hot
def map_country_to_group(country_name):
    country_name = country_name.lower()
    if country_name not in country_mapping:
        country_name = 'Otro'

    # Obtener las características del país según el mapeo
    return country_mapping[country_name]

# Función para obtener las características One-Hot del sabor seleccionado
def get_flavour_features(flavour):
    return flavour_map.get(flavour)


# Función para recomendar maridaje usando el modelo
def recomendar_maridaje(vino, flavour, pais, data=None):
    # Si se pasa el nombre del vino
    if isinstance(vino, str): 
        vino_data = data[data['wine_name'] == vino]
        if vino_data.empty:
            return "No se encontró el vino seleccionado."
    # Si se pasa un DataFrame de datos del vino
    elif isinstance(vino, pd.DataFrame):
        vino_data = vino
    else:
        return "El dataframe del tipo de vino no es correcto"

    # Obtener características del país y del sabor
    country_features = map_country_to_group(pais)
    flavour_features = get_flavour_features(flavour)

    # Usar las características del vino junto con las nuevas características (país y sabor)
    features = vino_data[['year', 'price', 'score', 'wine_type', 'price_quality', 'contenido_de_alcohol']].iloc[0].values.tolist()
    features += country_features + flavour_features  # Concatenamos las características

    # Realizar la predicción de maridaje
    maridaje_predicho = model.predict([features])

    # Convertir los valores predichos a nombres de alimentos
    maridaje_nombres = [food_mapping[i] for i, val in enumerate(maridaje_predicho[0]) if val == 1]

    return maridaje_nombres



# Título de la aplicación
st.title('Recomendación de Maridaje de Vinos')

# Opción para elegir entre buscar un vino o ingresar un vino nuevo
opcion = st.selectbox('Selecciona una opción', ['Buscar vino', 'Ingresar un vino nuevo'])

if opcion == 'Buscar vino':
    # Buscador de vinos
    busqueda_vino = st.text_input('Buscar vino:')

    # Filtrar los vinos según la búsqueda
    vinos_filtrados = data[data['wine_name'].str.contains(busqueda_vino, case=False, na=False)]

    # Ordenar los vinos alfabéticamente
    vinos_ordenados = sorted(vinos_filtrados['wine_name'].unique())

    if vinos_ordenados:
            # Selección del vino
            vino_seleccionado = st.selectbox('Selecciona el vino:', vinos_ordenados)

             # Obtener los datos del vino seleccionado
            vino_data = vinos_filtrados[vinos_filtrados['wine_name'] == vino_seleccionado].iloc[0]

            # Elige el sabor que tiene ese vino
            sabor = vino_data['flavours']

            # Obtener el país del vino a partir de las columnas One-Hot
            if vino_data['country_España'] == 1:
                pais = 'España'
            elif vino_data['country_Francia'] == 1:
                pais = 'Francia'
            elif vino_data['country_Italia'] == 1:
                pais = 'Italia'
            else:
                pais = 'Otro'

            # Llamar a la función de recomendación de maridaje
            if st.button('Recomendar Maridaje'):
                maridaje = recomendar_maridaje(vino_seleccionado, sabor, pais, data)  # Se pasa el nombre del vino y el DataFrame

                st.subheader(f"Maridaje recomendado para el vino: {vino_seleccionado}")
                if maridaje:
                    st.write("Las combinaciones sugeridas son:")
                    # Mostrar el maridaje como una lista tipo viñetas
                    st.markdown("\n".join([f"- {food}" for food in maridaje]))
                else:
                    st.write(f"No se encontró el vino '{vino_seleccionado}' o no se pudo recomendar un maridaje.")

            # Mostrar detalles del vino seleccionado
            vino_data = data[data['wine_name'] == vino_seleccionado]
            if not vino_data.empty:
                st.subheader('Detalles del Vino Seleccionado')
                st.write(f"Bodega: {vino_data.iloc[0]['bodega']}")
                st.write(f"Año: {vino_data.iloc[0]['year']}")
                st.write(f"Precio: {vino_data.iloc[0]['price']}€")
                st.write(f"Grado de alcohol: {vino_data.iloc[0]['contenido_de_alcohol']}%")
                st.write(f"Puntuación: {vino_data.iloc[0]['score']}")
                st.write(f"País: {vino_data.iloc[0]['country']}")
                st.write(f"Tipo de Vino: {wine_type_mapping[vino_data.iloc[0]['wine_type']]}")
                st.write(f"Sabor: {vino_data.iloc[0]['flavours'].capitalize()}")
                st.write(f"Estilo de Vino: {vino_data.iloc[0]['wine_style']}")
                st.write(f"Relación Calidad-Precio: {price_quality_mapping.get(vino_data.iloc[0]['price_quality'])}")
                if vino_data.iloc[0]['image']:
                    st.image(vino_data.iloc[0]['image'], width=80)
    else:
        st.write('No se encontraron vinos que coincidan con tu búsqueda.')

elif opcion == 'Ingresar un vino nuevo':
    # Formulario para ingresar un nuevo vino
    st.subheader("Ingresar datos de un nuevo vino")
    with st.form(key='nuevo_vino_form'):
        bodega = st.text_input('Bodega')
        wine_name = st.text_input('Nombre del vino')
        year = st.number_input('Año', min_value=1700, max_value=2025, step=1, value=2010)
        price = st.number_input('Precio', min_value=0.0, step=0.01, value=12.50)
        alcohol = st.number_input('Grado de alcohol', min_value=0.0, max_value=16.0, step=0.01, value=11.0)
        score = st.number_input('Puntuación', min_value=1.0, max_value=5.0, step=0.1)
        wine_type = st.selectbox('Tipo de vino', options=[2, 1], format_func=lambda x: wine_type_mapping[x])
        price_quality = st.selectbox('Calidad del precio', options=[1, 2, 3, 4, 5, 6], format_func=lambda x: price_quality_mapping[x])  # Ajusta las opciones según sea necesario

        # Elegir el pais del vino
        selected_country = st.selectbox(
            'País',
            options=list(country_mapping.keys()),
            format_func=lambda x: x.capitalize()
        )

        # Elegir el sabor asociado al vino
        selected_flavours = st.selectbox(
            'Sabor del vino',
            options=list(flavour_map.keys()),
            format_func=lambda x: x.capitalize()
        )

        # Botón para enviar el formulario
        submit_button = st.form_submit_button(label='Recomendar Maridaje')

    # Si el formulario fue enviado
    if submit_button:
        # Verificar si los campos están vacíos
        if not bodega and not wine_name:
            st.warning("Por favor, completa todos los campos: 'Bodega' y 'Nombre del vino'.")
        elif not bodega:
            st.warning("Por favor, rellena el campo: 'Bodega'.")
        elif not wine_name:
            st.warning("Por favor, rellena el campo: 'Nombre del vino'.")
        else:
            # Crear un DataFrame con los datos del vino ingresado
            nuevo_vino = pd.DataFrame({
                'year': [year],
                'price': [price],
                'score': [score],
                'wine_type': [wine_type],
                'price_quality': [price_quality],
                'contenido_de_alcohol': [alcohol],
            })
    
            # Obtener el sabor y el país del formulario
            flavour = selected_flavours
            pais = selected_country
    
            # Recomendar maridaje
            maridaje = recomendar_maridaje(nuevo_vino, flavour, pais)
    
            st.subheader(f"Maridaje recomendado para el vino: {wine_name}")
            
            if maridaje:
                st.write("Las combinaciones sugeridas son:")
                # Mostrar el maridaje como una lista tipo viñetas
                st.markdown("\n".join([f"- {food}" for food in maridaje]))
            else:
                st.write(f"No se pudo recomendar un maridaje para el vino '{wine_name}'.")


# Agregar un salto de línea visual
st.markdown('<br>', unsafe_allow_html=True)
# Información de los sabores
st.subheader('Información sobre los sabores')
# Mostrar el selector de sabores
selected_flavour = st.selectbox(
    'Selecciona un sabor del vino',
    options=list(flavour_descriptions.keys()),
    format_func=lambda x: x.replace("flavour_", "").capitalize()  # Formatear para mostrar sin "flavour_"
)

st.write(f"Descripción: {flavour_descriptions[selected_flavour]}")
