import joblib
import pandas as pd
import numpy as np
from app.core.config import settings

def load_model():
    return joblib.load(settings.MODEL_PATH)


def precess_data():
    data = pd.read_csv(settings.DATASET_PATH)  # Ensure this is the correct path to your dataset
    data.drop(columns=['Address', 'Type', 'Method', 'Seller', 'Regionname', 'Propertycount', 'CouncilArea'], inplace=True)
    data['Year'] = pd.to_datetime(data['Date']).dt.year
    data.drop(columns=['Date'], inplace=True)
    numeric_columns = data.select_dtypes(include=['float64', 'int64']).columns
    data[numeric_columns] = data[numeric_columns].fillna(data[numeric_columns].median())
    data = pd.get_dummies(data, columns=['Suburb', 'Postcode'], drop_first=True)
    X_columns = data.drop(columns=['Price']).columns.tolist()  # Store the feature columns for later use

    return X_columns

def return_sample_input():
    df = pd.read_csv(settings.DATASET_PATH)
    # Extract unique suburbs and their corresponding postal codes
    suburb_data = df[['Suburb', 'Postcode']].drop_duplicates()

    # Create the JSON structure as specified
    suburb_json = []
    for suburb, group in suburb_data.groupby('Suburb'):
        postal_codes = [{"code": int(pc), "value": int(pc)} for pc in group['Postcode'].unique()]
        suburb_json.append({
            "name": suburb,
            "value": suburb,
            "postalCodes": postal_codes
        })

    return suburb_json


