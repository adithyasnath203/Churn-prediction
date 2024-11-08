import os
import pandas as pd
import numpy as np
from django.conf import settings
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction import DictVectorizer
from sklearn.linear_model import LogisticRegression


def sigmoid(z):
    return 1 / (1 + np.exp(-z))


def change_totalcharge_to_int(df):
    df.totalcharges = pd.to_numeric(df.totalcharges, errors="coerce")
    df.totalcharges = df.totalcharges.fillna(0)
    return df


def make_data_uniform(df):
    df.columns = df.columns.str.lower().str.replace(" ", "_")
    categorical_columns = list(df.dtypes[df.dtypes == "object"].index)
    for c in categorical_columns:
        df[c] = df[c].str.lower().str.replace(" ", "_")
    return df


def predict(input):
    df = pd.read_csv(os.path.join(settings.BASE_DIR, "ml/data.csv"))
    df = make_data_uniform(df)
    df = change_totalcharge_to_int(df)
    df.churn = (df.churn == "yes").astype(int)

    # splitting the dataset to train, validation and test
    df_full_train, df_test = train_test_split(df, test_size=0.2, random_state=1)
    df_train, df_val = train_test_split(df_full_train, test_size=0.25, random_state=11)

    # make indices ordered
    df_train = df_train.reset_index(drop=True)
    df_val = df_val.reset_index(drop=True)
    df_test = df_test.reset_index(drop=True)
    df_full_train = df_full_train.reset_index(drop=True)

    y_train = df_train.churn.values
    y_val = df_val.churn.values
    y_test = df_test.churn.values

    del df_train["churn"]
    del df_val["churn"]
    del df_test["churn"]

    global_churn_rate = df_full_train.churn.mean()

    # feature engineering
    numerical = ["tenure", "monthlycharges", "totalcharges"]
    categorical = [
        "gender",
        "seniorcitizen",
        "partner",
        "dependents",
        "phoneservice",
        "multiplelines",
        "internetservice",
        "onlinesecurity",
        "onlinebackup",
        "deviceprotection",
        "techsupport",
        "streamingtv",
        "streamingmovies",
        "contract",
        "paperlessbilling",
        "paymentmethod",
    ]
    # one hot encoding
    dv = DictVectorizer(sparse=False)

    train_dict = df_full_train[categorical + numerical].to_dict(orient="records")
    X_train = dv.fit_transform(train_dict)
    Y_train = df_full_train.churn.values

    model = LogisticRegression().fit(X_train, Y_train)
    value = dv.transform([input])
    return model.predict_proba(value)
