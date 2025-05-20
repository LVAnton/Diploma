#Чтоб приложение работало
from fastapi import FastAPI, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import csv
import io
from typing import List, Dict

# Ml библиотеки
import pandas as pd
import numpy as np
import catboost
from catboost import CatBoostRegressor, CatBoostClassifier, Pool


app = FastAPI()

origins = [
    "http://localhost:8000",
    "http://127.0.0.1:8000",
    "http://localhost",
    "http://127.0.0.1",
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
model1 = CatBoostClassifier()
model1.load_model("models/1.cbm")
model2 = CatBoostClassifier()
model2.load_model("models/2.cbm")
model3 = CatBoostClassifier()
model3.load_model("models/3.cbm")
model4 = CatBoostClassifier()
model4.load_model("models/4.cbm")
model5 = CatBoostClassifier()
model5.load_model("models/5.cbm")
model6 = CatBoostClassifier()
model6.load_model("models/6.cbm")
model7 = CatBoostClassifier()
model7.load_model("models/7.cbm")
model8 = CatBoostClassifier()
model8.load_model("models/8.cbm")
model9 = CatBoostClassifier()
model9.load_model("models/9.cbm")

loaded_model = CatBoostRegressor()
loaded_model.load_model("models/MAE_model.cbm")


@app.post("/process_csv")
async def process_csv(file: UploadFile = File(...), prediction_type: str = Form(...)):
    contents = await file.read()
    decoded_contents = contents.decode("utf-8")
    csv_data = io.StringIO(decoded_contents)
    df = pd.read_csv(csv_data)

    if prediction_type == 'first':

        X = df.drop('rate', axis=1)
        X = X.drop('id', axis=1)

        predictions = loaded_model.predict(X)
        averege_tasks = predictions.mean()

        new_df = pd.DataFrame()
        new_df['id'] = df['id']
        new_df['predictions'] = predictions
        json_data = new_df.to_json(orient="records", force_ascii=False)
        filik = json_data
        return JSONResponse(
            content={"message": "Successful!", "file": filik , "type": "first", "avg": averege_tasks},
            status_code=200,
        )
    else:
        if 'Unnamed: 0' in df.columns:
            df = df.drop('Unnamed: 0', axis=1)

        new_df = pd.DataFrame()
        new_df['id'] = df['id']

        data = df
        df = df.reset_index()
        df['rate'] = (df['index'] + 1) / len(df)
        df = df.drop('index', axis=1)
        df = df.drop('id', axis=1)
        res1 = model1.predict(df)
        res2 = model2.predict(df)
        res3 = model3.predict(df)

        df = data

        def floatize_rate(rate):
            try:
                rate = int(rate)
            except:
                k = 0
                while (rate[k] != '-'):
                    k += 1
                rate = int(rate[:k])
            return rate

        df['rate'] = df['rate'].apply(floatize_rate)
        df = df.drop('id', axis=1)
        res4 = model4.predict(df)
        res5 = model5.predict(df)
        res6 = model6.predict(df)

        df = data
        df = df.drop('rate', axis=1)
        df = df.drop('id', axis=1)
        res7 = model7.predict(df)
        res8 = model8.predict(df)
        res9 = model9.predict(df)

        summ = []
        print("Кол-во участников курса: ", len(df))
        all_people = len(df)
        good_people = res1.sum()
        bad_people = all_people - good_people
        print("отток в людях: ", bad_people, "  В процентах", bad_people * 100 / all_people)
        summ.append(bad_people)
        good_people = res2.sum()
        bad_people = all_people - good_people
        print("отток в людях: ", bad_people, "  В процентах", bad_people * 100 / all_people)
        summ.append(bad_people)
        good_people = res3.sum()
        bad_people = all_people - good_people
        print("отток в людях: ", bad_people, "  В процентах", bad_people * 100 / all_people)
        summ.append(bad_people)
        good_people = res4.sum()
        bad_people = all_people - good_people
        print("отток в людях: ", bad_people, "  В процентах", bad_people * 100 / all_people)
        summ.append(bad_people)
        good_people = res5.sum()
        bad_people = all_people - good_people
        print("отток в людях: ", bad_people, "  В процентах", bad_people * 100 / all_people)
        summ.append(bad_people)
        good_people = res6.sum()
        bad_people = all_people - good_people
        print("отток в людях: ", bad_people, "  В процентах", bad_people * 100 / all_people)
        summ.append(bad_people)
        good_people = res7.sum()
        bad_people = all_people - good_people
        print("отток в людях: ", bad_people, "  В процентах", bad_people * 100 / all_people)
        summ.append(bad_people)
        good_people = res8.sum()
        bad_people = all_people - good_people
        print("отток в людях: ", bad_people, "  В процентах", bad_people * 100 / all_people)
        summ.append(bad_people)
        good_people = res9.sum()
        bad_people = all_people - good_people
        print("отток в людях: ", bad_people, "  В процентах", bad_people * 100 / all_people)
        summ.append(bad_people)
        summ.sort()

        print("Среднее предсказание оттока учеников", round(sum(summ) / 9))
        print("Средний процент оттока учеников", round(sum(summ) / 9) * 100 / all_people)
        averege_tasks = round(sum(summ) / 9) * 100 / all_people

        new_df['predictions1_model'] = res1
        new_df['predictions2_model'] = res2
        new_df['predictions3_model'] = res3
        new_df['predictions4_model'] = res4
        new_df['predictions5_model'] = res5
        new_df['predictions6_model'] = res6
        new_df['predictions7_model'] = res7
        new_df['predictions8_model'] = res8
        new_df['predictions9_model'] = res9

        json_data = new_df.to_json(orient="records", force_ascii=False)
        filik = json_data
        return JSONResponse(
            content={"message": "Successful", "file": filik,"type": "second", "avg": averege_tasks, 'all_people': len(df), 'away_people': round(averege_tasks * all_people / 100) },
            status_code=200,
        )

