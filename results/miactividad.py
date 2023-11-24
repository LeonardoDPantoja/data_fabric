import pandas as pd
import json
import os
from pymongo.server_api import ServerApi
from datetime import datetime
import streamlit as st
from pymongo import MongoClient
import matplotlib.pyplot as plt

# Conexión a MongoDB
client = MongoClient("mongodb+srv://leonardo:datatest@cluster0.rfrxhhg.mongodb.net/?retryWrites=true&w=majority")
db = client.test
collection1 = db.DB1
collection2 = db.DB2


def save_log(user, action, data_requested=None):
    new_data = {"user": user, "action": action, "timestamp": datetime.now().strftime("%d/%m/%Y %H:%M:%S")}

    if (action == "success_db_check" or action == "unsuccess_db_check") and data_requested is not None:
        new_data["data_accessed"] = data_requested

    # Guardar el log en MongoDB
    db.log.insert_one(new_data)

# Solicitar al usuario que ingrese su nombre
nombre = st.text_input("Por favor, ingresa tu nombre: ")
actions = ['login', 'unsucessful_login', 'success_db_check', 'unsuccess_db_check']

# Verificar si el nombre de usuario está en la base de datos
if db.users.find_one({"user": nombre}) is not None:
    save_log(nombre, actions[0])
    st.write(f"Hola {nombre}!!")

    # Solicitar al usuario que ingrese la columna a consultar
    columna_consulta = st.text_input("¿Qué columna quieres consultar?")

    # Consultar datos en MongoDB
    data_db1 = pd.DataFrame(list(collection1.find()))
    data_db2 = pd.DataFrame(list(collection2.find()))

    if columna_consulta in data_db1.columns:
        save_log(nombre, actions[2], columna_consulta)
        st.write(f'Claro {nombre}, aquí tienes la información de {columna_consulta} \n\n')
        st.write(data_db1[columna_consulta].head())
    elif columna_consulta in data_db2.columns:
        save_log(nombre, actions[2], columna_consulta)
        st.write(f'Claro {nombre}, aquí tienes la información de {columna_consulta} \n\n')
        st.write(data_db2[columna_consulta].head())
    else:
        save_log(nombre, actions[3], columna_consulta)
        st.write(f'Ese dato {columna_consulta} no existe en la base de datos')

else:
    save_log(nombre, actions[1])
    st.write(f"Lo siento {nombre}, no se encontró tu nombre en la base de Usuarios.")
