import streamlit as st
import sklearn
from sklearn import model_selection, svm
import pickle
import pandas as pd


# Cargo el modelo y el escalador desde los archivos
with open('kmeans.pkl', 'rb') as model_file:
    model = pickle.load(model_file)

with open('scaler.pkl', 'rb') as scaler_file:
    scaler = pickle.load(scaler_file)

# Título de la aplicación

st.title('Identificador de Grupo de Cliente')

# Datos demográficos del cliente

st.header('Datos Demográficos del Cliente')

edad = st.number_input('Edad:', min_value=18, max_value=100)

trabajo = st.selectbox('Tipo de Trabajo:',
                        ('Administración', 'Tecnico', 'Gerencia', 'Emprendedor',
                         'Autonomo', 'Obrero', 'Servicios', 'Hogar', 'Desempleado',
                         'Estudiante', 'Desconocido' ))

estado_civil = st.radio('Estado Civil:', ['soltero', 'casado', 'divorciado'])

educacion = st.radio('Educación:', ['primaria', 'media', 'superior'])

# Datos financieros del usuario

st.header('Datos Financieros del Cliente')

saldo = st.number_input('Cuál es el Saldo del cliente:')

hipoteca = st.radio('Tiene Hipoteca', ['no', 'si'])

prestamos = st.radio('Tiene contratado prestamos:', ['no', 'si'])

deposito = st.radio('Ha contratado depósito:', ['no', 'si'])

# Creo un dataframe con los datos ingresados

user_data = pd.DataFrame({
        'edad':[edad],
        'trabajo':[trabajo],
        'estado_civil':[estado_civil],
        'educacion':[educacion],
        'saldo':[saldo],
        'hipoteca':[hipoteca],
        'prestamos':[prestamos],
        'deposito': [deposito]
})

# Realizo Mapeo para las características hipoteca, prestamos, deposito

user_data['hipoteca'] = user_data['hipoteca'].map({'no':0, 'si':1}).astype(int)
user_data['prestamos'] = user_data['prestamos'].map({'no':0, 'si':1}).astype(int)
user_data['deposito'] = user_data['deposito'].map({'no':0, 'si':1}).astype(int)
user_data['educacion'] = user_data['educacion'].map({'primaria':1, 'media':2, 'superior': 3}).astype(int)

# Realizo Label Encoding para las características trabajo y estado civil, agrupando primero las categorías

trabajos = {'Administración': 'profesional',
            'Tecnico': 'profesional',
            'Gerencia': 'profesional',
            'Autonomo': 'profesional',
            'Obrero': 'manual',
            'Servicios':'manual',
            'Hogar': 'manual',
            'Desempleado': 'otro',
            'Estudiante': 'otro',
            'Desconocido': 'otro'}

user_data['trabajo'] = user_data['trabajo'].map(trabajos)

categorical_features = ["trabajo", "estado_civil"]

label_encoders = {}

for feature in categorical_features:
    label_encoders[feature] = LabelEncoder()
    
    user_data[feature + "_encoded"] = label_encoders[feature].fit_transform(user_data[feature])

user_data = user_data.drop(columns=categorical_features, axis=1)

required_columns = [
    'edad', 'educacion', 'saldo', 'hipoteca', 'prestamos', 'deposito',
    'trabajo_encoded', 'estado_civil_encoded'
]

# Agregar columnas faltantes con valor 0
for col in required_columns:
    if col not in user_data.columns:
        user_data[col] = 0

# Reordenar las columnas
user_data = user_data[required_columns]

# Estandarizar las entradas de edad y saldo
scale_variable = ['edad', 'saldo']
user_data[scale_variable] = scaler.transform(user_data[scale_variable])

# Se realiza la predicción
perfil_map = {
    0: "1: Profesionales Estables",
    1: "2: Jóvenes Profesionales",
    2: "3: Profesionales Altos Ingresos",
    3: "4: Trabajadores Bajos Ingresos ",
}

prediction = model.predict(user_data)

# Resultados de la predicción
st.header('Clasificación del cliente')

# Accediendo al valor del diccionario usando la predicción como clave
perfil = perfil_map.get(prediction, "Perfil no encontrado")

st.success(f'El cliente pertenece al perfil: {perfil}')
