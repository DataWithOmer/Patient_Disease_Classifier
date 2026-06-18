import pandas as pd
import numpy as np

def load_and_preprocess():
    # Load the dataset
    df = pd.read_csv("data/dataset.csv")

    # Strip extra spaces from column names and values
    df.columns = df.columns.str.strip()
    df = df.apply(lambda col: col.str.strip() if col.dtype == "object" else col)

    # Fill empty symptom cells with "none"
    df = df.fillna("none")

    # Get all unique symptoms from the dataset (excluding "none")
    all_symptoms = set()
    symptom_cols = [col for col in df.columns if col.startswith("Symptom")]
    for col in symptom_cols:
        all_symptoms.update(df[col].unique())
    all_symptoms.discard("none")
    all_symptoms = sorted(list(all_symptoms))

    # Convert each row into binary format
    # For each symptom, 1 = patient has it, 0 = patient does not have it
    def encode_row(row):
        patient_symptoms = set(row[symptom_cols].values)
        return [1 if symptom in patient_symptoms else 0 for symptom in all_symptoms]

    X = pd.DataFrame(
        [encode_row(row) for _, row in df.iterrows()],
        columns=all_symptoms
    )
    y = df["Disease"]

    return X, y, all_symptoms


def encode_user_symptoms(user_symptoms, all_symptoms):
    # Convert user selected symptoms into binary format
    # Same format as training data so model can understand it
    return [1 if symptom in user_symptoms else 0 for symptom in all_symptoms]


def load_precautions():
    df = pd.read_csv("data/symptom_precaution.csv")
    df.columns = df.columns.str.strip()
    df = df.apply(lambda col: col.str.strip() if col.dtype == "object" else col)

    precautions = {}
    for _, row in df.iterrows():
        disease = row["Disease"]
        precs = [row[col] for col in df.columns if col.startswith("Precaution") and pd.notna(row[col])]
        precautions[disease] = precs

    return precautions