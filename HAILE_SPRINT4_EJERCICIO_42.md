# Proyecto: Modelo para crear clasificaciones según los perfiles de cliente usando Clustering
## 1. Fuentes

**Identificación de Fuentes:**
- Base de datos interna del CRM de un Banco de Portugal

**Descripción de las Fuentes:**
- La base de datos CRM contiene registros integrales de una campaña telefónica de la Institución que contiene datos de diversas categorías que han sido capturadas a través de una API, dentro de ellos se pueden encontrar: Datos Demográficos, Datos Financieros y Datos sobre la Campaña de Llamadas.
  
## 2. Métodos de recolección de datos

**Procedimientos y Herramientas:**
- Los Datos provienen de una exportació programada en formato CSV por el Departamento de Ingeniería de Datos, quienes se encargan de que los datos se obtengan de la manera más integral y buscando garantizar que sean enviados sin errores. El CSV se encuentra alojado en los servidores locales de la entidad.

**Frecuencia de Recolección:**
- Diaria
  
**Scripts de Descarga:**

```python

import pandas as pd

archivo_csv = "ruta_de_acceso/bank_dataset.csv"

df = pd.read_csv(archivo_csv)

print(df.head())

```

## 3. Formato y Estructura de les Datos

**Tipos de Datos:**
- Numéricos: `age`, `balance`, `duration`, `campaign`, `pdays`, `previous`
- Categóricos: `job`, `marital`, `education`, `contact`, `poutcome`
- Binarios: `default`, `housing`, `loan`, `y`
- Fecha: `month`, `day`

**Formato de Almacenamiento:**
- Datos tabulares almacenados en un fichero csv.

## 4. Limitaciones de los datos

- Captura de los datos: Se realiza de manera manual por los empleados del banco, por lo que pueden existir omisiones o errores al momento de introducirlos.

- Tiempos de Actualización: Los datos pueden ser recolectados y actualizados al CRM en momentos diferentes y pueden influir en los plazos de entrega de informes.

## 5. Consideraciones sobre Datos Sensibles

**Tipos de Datos Sensibles:**
- Información Personal Identificable (PII): `education`, `age`, `marital`, `job`
- Información Financera Sensible: `default`, `housing`, `loan`, `balance`
- Datos de Comportamiento Sensibles:`contact`, `day`, `month`, `poutcome`

**Medidas de Protección:**
- **Anonimización y Pseudonimización:**
  - Se solicitará su aplicación en el momento que los datos sean exportados a los archivos CSV de las actualizaciones, modificaciones e incorporaciones que hubieran durante el proyecto.
- **Acceso Restringido:**
  - El acceso a los datos sensibles será restringido solo al personal autorizado y que necesite conocerlos para fines exclusivos al proyecto.
- **Complimiento de las Regulaciones:**
  - Cumplimento de la GDRP vigente.
