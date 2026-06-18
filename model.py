import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from utils.preprocess import load_and_preprocess, encode_user_symptoms

# Load and preprocess data once
X, y, all_symptoms = load_and_preprocess()

# Split into training and testing sets
# 80% training, 20% testing
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# ── Train all three models ──────────────────────────────

# 1. Random Forest — Deep Analysis
rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
rf_model.fit(X_train, y_train)

# 2. KNN — Balanced Analysis
knn_model = KNeighborsClassifier(n_neighbors=5)
knn_model.fit(X_train, y_train)

# 3. Naive Bayes — Quick Check
nb_model = GaussianNB()
nb_model.fit(X_train, y_train)

# ── Calculate accuracy for each model ──────────────────

rf_accuracy = round(accuracy_score(y_test, rf_model.predict(X_test)) * 100, 2)
knn_accuracy = round(accuracy_score(y_test, knn_model.predict(X_test)) * 100, 2)
nb_accuracy = round(accuracy_score(y_test, nb_model.predict(X_test)) * 100, 2)

# ── Prediction function ─────────────────────────────────

def predict_disease(user_symptoms, mode):
    # Encode user symptoms into binary format
    input_vector = encode_user_symptoms(user_symptoms, all_symptoms)
    input_vector = np.array(input_vector).reshape(1, -1)

    # Select model based on mode
    if mode == "Quick Check":
        model = nb_model
    elif mode == "Balanced Analysis":
        model = knn_model
    else:
        model = rf_model

    # Get prediction
    prediction = model.predict(input_vector)[0]

    # Get probability scores for all diseases
    proba = model.predict_proba(input_vector)[0]
    classes = model.classes_

    # Build a sorted dictionary of disease → probability
    disease_proba = dict(zip(classes, proba))
    disease_proba = dict(
        sorted(disease_proba.items(), key=lambda x: x[1], reverse=True)
    )

    # Top 3 diseases
    top_3 = list(disease_proba.items())[:3]

    return prediction, top_3


def get_symptom_importance(user_symptoms):
    # Uses Random Forest feature importance to find which
    # of the user's symptoms influenced the prediction most
    input_vector = encode_user_symptoms(user_symptoms, all_symptoms)
    importances = rf_model.feature_importances_

    symptom_scores = {}
    for i, symptom in enumerate(all_symptoms):
        if input_vector[i] == 1:
            symptom_scores[symptom] = round(importances[i] * 100, 4)

    # Sort by importance descending
    symptom_scores = dict(
        sorted(symptom_scores.items(), key=lambda x: x[1], reverse=True)
    )
    return symptom_scores


def get_model_accuracies():
    return {
        "Quick Check (Naive Bayes)": nb_accuracy,
        "Balanced Analysis (KNN)": knn_accuracy,
        "Deep Analysis (Random Forest)": rf_accuracy
    }