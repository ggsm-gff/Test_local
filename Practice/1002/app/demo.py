import streamlit as st
import pandas as pd
import numpy as np
import pickle  # to load a saved modelimport base64  # to handle gif encoding

@st.cache_data
def get_fvalue(val):    
    feature_dict = {"No": 1, "Yes": 2}    
    return feature_dict[val]
    
def get_value(val, my_dict):    
    return my_dict[val]

#if app_mode == 'Home':    
st.title('Loan Prediction')    
#st.image('loan_image.jpg')    
st.markdown('Dataset:')    
#data = pd.read_csv('loan_dataset.csv')    
#st.write(data.head())    
st.bar_chart(data[['ApplicantIncome', 'LoanAmount']].head(20))


data1={    
    'Gender':Gender,    
    'Married':Married,    
    'Dependents':[class_0,class_1,class_2,class_3],    
    'Education':Education,    
    'ApplicantIncome':ApplicantIncome,    
    'CoapplicantIncome':CoapplicantIncome,    
    'Self Employed':Self_Employed,    
    'LoanAmount':LoanAmount,    
    'Loan_Amount_Term':Loan_Amount_Term,    
    'Credit_History':Credit_History,    
    'Property_Area':[Rural,Urban,Semiurban],    
    }    
    feature_list=[ApplicantIncome,
        CoapplicantIncome,
        LoanAmount,
        Loan_Amount_Term,
        Credit_History,
        get_value(Gender,gender_dict),
        get_fvalue(Married),
        data1['Dependents'][0],
        data1['Dependents'][1],
        data1['Dependents'][2],
        data1['Dependents'][3],
        get_value(Education,edu),
        get_fvalue(Self_Employed),
        data1['Property_Area'][0],
        data1['Property_Area'][1],
        data1['Property_Area'][2]]    
single_sample = np.array(feature_list).reshape(1,-1)