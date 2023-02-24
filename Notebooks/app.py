
import numpy as np
from flask import Flask, request, jsonify, render_template
from sklearn.preprocessing import StandardScaler, MinMaxScaler, OneHotEncoder
from sklearn.linear_model import LogisticRegression
import xgboost as xgb
from xgboost import XGBClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.pipeline import make_pipeline
import pandas as pd
import os
import streamlit as st

# Load the data
df = pd.read_csv('/home/ashioyajotham/Downloads/PMTCT-Data-Behavior-Identification-and-Clean-Up-Automation/Data/data.csv')

# Preprocess the data
target = "PMTCT"
features = ['facility', 'ward', 'sub_county', 'county', 'indicators', 
            'khis_data', 'datim_value', 'period', 'Month']

X = df1[features]
y = df1[target]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=.2, random_state=42)

lr_model = make_pipeline(
    OneHotEncoder(handle_unknown = "ignore"),
    LogisticRegression()
)
lr_model.fit(X_train, y_train)


# Encode the data
encoder = OneHotEncoder(handle_unknown = "ignore")
X_train_encoded = encoder.fit_transform(X_train)
X_test_encoded = encoder.transform(X_test)

# Fit the RF model
rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
rf_model.fit(X_train_encoded, y_train)


st.set_page_config (page_title="PMTCT Reporting", page_icon=":heart:", layout="centered", initial_sidebar_state="expanded")

st.title("HIV Testing")

st.write("This is a simple HIV Testing prediction web app to predict whether a facility reports PMTCT or not.")

st.write("Please fill in the required details.")

st.balloons() # Adds a balloon animation

# style 
st.markdown(""" <style> .reportview-container { background: #F5F5F5; } </style> """, unsafe_allow_html=True)



# Create a text element and let the reader know the data is loading.
data_load_state = st.text('Loading data...')
# Load 10,000 rows of data into the dataframe.
data = pd.read_csv('/home/ashioyajotham/Downloads/PMTCT-Data-Behavior-Identification-and-Clean-Up-Automation/Data/data.csv')
# Notify the reader that the data was successfully loaded.
data_load_state.text("Loading data...done!")

# Classify the data
st.subheader('Classify the data')

# Create a selectbox for the classification model
classifier = st.selectbox('Select the classifier', ('Logistic Regression', 'Random Forest'))

def user_input_features():
    
    facility = st.text_input("Facility", "Facility")
    period = st.text_input("Period", "Period")

    data = {'facility': facility,
            'period': period}

    features = pd.DataFrame(data, index=[0])
    return features

df = user_input_features()

st.subheader('User Input parameters')
st.write(df)

if classifier == 'Logistic Regression':
    prediction = lr_model.predict(df)
    prediction_proba = lr_model.predict_proba(df)

elif classifier == 'Random Forest':
    prediction = rf_model.predict(df)
    prediction_proba = rf_model.predict_proba(df)

st.subheader('Prediction')
st.write(prediction)

st.subheader('Prediction Probability')
st.write(prediction_proba)

st.subheader('Data')
st.write(data)
    
if st.button("Predict"):
    st.write(prediction)

st.write("This is a simple HIV Testing prediction web app to predict whether a facility reports PMTCT or not.")
