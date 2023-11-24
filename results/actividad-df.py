
# Import necessary libraries
import streamlit as st
from pymongo import MongoClient
import matplotlib.pyplot as plt
import pandas as pd

client = MongoClient("mongodb+srv://leonardo:datatest@cluster0.rfrxhhg.mongodb.net/?retryWrites=true&w=majority")
db = client.test
collection1 = db.DB1

data = pd.DataFrame(list(collection1.find()))

st.title("GBS MX HC List")
st.text('Leonardo')

st.write("## Headcount List:")
st.write(data.head())

st.write("## Number of employees by department")
property_type_counts = data['Department'].value_counts().sort_values(ascending=False)

st.bar_chart(property_type_counts)

