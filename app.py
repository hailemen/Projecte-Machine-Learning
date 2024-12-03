import streamlit as st
import pandas as pd
import pickle
from sklearn.preprocessing import LabelEncoder 

# Cargo el modelo y el escalador desde los archivos
with open('kmeans.pkl', 'rb') as model_file:
    model = pickle.load(model_file)

with open('scaler.pkl', 'rb') as scaler_file:
    scaler = pickle.load(scaler_file)

with open('label_encoders.pkl', 'rb') as f:
    loaded_label_encoders = pickle.load(f)

# Título de la aplicación
st.title('Joonie, Luna & Doria Banking Group. Identificador de Clientes')

# Datos demográficos del cliente
st.header('Ingrese los datos demográficos del Cliente')
edad = st.number_input('Edad:', min_value=18, max_value=100)
trabajo = st.selectbox('Tipo de Trabajo:',
                        ('Administración', 'Tecnico', 'Gerencia', 'Emprendedor',
                         'Autonomo', 'Obrero', 'Servicios', 'Hogar', 'Desempleado',
                         'Estudiante', 'Jubilado'))
estado_civil = st.radio('Estado Civil:', ['soltero', 'casado', 'divorciado'])
educacion = st.radio('Educación:', ['primaria', 'media', 'superior'])

# Datos financieros del usuario
st.header('Ingrese los datos financieros del Cliente')
saldo = st.number_input('Cuál es el Saldo del cliente:')
hipoteca = st.radio('Tiene Hipoteca', ['no', 'si'])
prestamos = st.radio('Tiene contratado prestamos:', ['no', 'si'])
deposito = st.radio('Ha contratado depósito:', ['no', 'si'])

# Creo un dataframe con los datos ingresados
user_data = pd.DataFrame({
    'edad': [edad],
    'educacion': [educacion],
    'saldo': [saldo],
    'hipoteca': [hipoteca],
    'prestamos': [prestamos],
    'deposito': [deposito],
    'trabajo': [trabajo],
    'estado_civil': [estado_civil]
})

# Mapeo de valores categóricos
user_data['hipoteca'] = user_data['hipoteca'].map({'no': 0, 'si': 1}).astype(int)
user_data['prestamos'] = user_data['prestamos'].map({'no': 0, 'si': 1}).astype(int)
user_data['deposito'] = user_data['deposito'].map({'no': 0, 'si': 1}).astype(int)
user_data['educacion'] = user_data['educacion'].map({'primaria': 1, 'media': 2, 'superior': 3}).astype(int)

trabajos = {'Administración': 'profesional', 'Tecnico': 'profesional',
            'Gerencia': 'profesional', 'Autonomo': 'profesional',
            'Obrero': 'manual', 'Servicios': 'manual', 'Hogar': 'manual',
            'Desempleado': 'otro', 'Estudiante': 'otro', 'Jubilado': 'retirado'}
user_data['trabajo'] = user_data['trabajo'].map(trabajos).fillna('otro')

categorical_features = ["trabajo", "estado_civil"]
for feature in categorical_features:
    try:
        user_data[feature + "_encoded"] = loaded_label_encoders[feature].transform(user_data[feature])
    except KeyError:
        print(f"Error al codificar la característica '{feature}'. ¿El codificador está guardado correctamente?")

user_data = user_data.drop(columns=categorical_features, axis=1)


# Estandarización
scale_variable = ['edad', 'saldo']
user_data[scale_variable] = scaler.transform(user_data[scale_variable])

required_columns = [
    'edad', 'educacion', 'saldo', 'hipoteca', 'prestamos', 'deposito',
    'trabajo_encoded', 'estado_civil_encoded'
]

for col in required_columns:
    if col not in user_data.columns:
        user_data[col] = 0
user_data = user_data[required_columns]

# Predicción
perfil_map = {
    0: "1: Línea Access: Cuentas de ahorro saldos altos, Planes de pensiones individuales, Seguros de vida o de protección familiar y Productos bancarios vinculados a la vivienda",
    1: "2: Línea Joven Flex: Cuentas de ahorro con beneficios, Depósitos a corto plazo con flexibilidad, Préstamos personales con tasas bajas y Productos Bancarios Digitales",
    2: "3: Línea Platinum: Fondos de inversión diversificados, Cuenta Premium con servicios exclusivos, Seguros de vida y salud de alta gama y Planes de inversión a largo plazo o jubilación privada",
    3: "4: Línea Starter: Cuentas de ahorro con beneficios por lealtad, Microcréditos específicos, Reestructuración de deuda (hipotecas y préstamos) y Planes de ahorro para metas específicas (ejemplo: educación de hijos)",
}
prediction = model.predict(user_data)
perfil = perfil_map.get(int(prediction[0]), "Perfil no encontrado")
st.header('Clasificación del cliente')
st.success(f'El cliente pertenece al perfil: {perfil}')

