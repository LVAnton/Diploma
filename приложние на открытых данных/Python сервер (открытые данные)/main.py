from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from catboost import CatBoostClassifier, Pool
import pandas as pd

app = FastAPI()

origins = [
    "http://localhost",  # Разрешить localhost
    "http://localhost:8080",  # Разрешить, если вы открываете HTML на другом порту
    "http://127.0.0.1",  # Разрешить 127.0.0.1
    "http://127.0.0.1:8080",  # Разрешить, если вы открываете HTML на другом порту
    "*",  # Только для разработки!  В production так делать НЕЛЬЗЯ!
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # Разрешить все методы
    allow_headers=["*"],  # Разрешить все заголовки
)


class CourseData(BaseModel):
    course_name: str
    hours_spent: float
    videos_watched: int
    tests_completed: int
    average_score: float
    completion_percentage: float
    device_type: str


@app.post("/process_form")
async def process_form(data: CourseData):
    """
    Эндпоинт для обработки данных из формы.
    """
    print("Полученные данные:", data)  # Выводим данные в консоль сервера
    loaded_model = CatBoostClassifier()
    loaded_model.load_model("model.cbm")
    if data.device_type == 'computer':
        data.device_type = 0
    else:
        data.device_type = 1
    new_data = pd.DataFrame({
        'CourseCategory': [data.course_name],
        'TimeSpentOnCourse': [data.hours_spent],
        'NumberOfVideosWatched': [data.videos_watched],
        'NumberOfQuizzesTaken': [data.tests_completed],
        'QuizScores': [data.average_score],
        'CompletionRate': [data.completion_percentage],
        'DeviceType': [data.device_type]
    })
    categorical_features = ['CourseCategory']
    new_data_pool = Pool(data=new_data, cat_features=categorical_features)
    probabilities = loaded_model.predict_proba(new_data_pool)
    # Вероятность того, что CourseCompletion = 1
    positive = probabilities[0, 1]  # Первая строка, второй столбец (класс 1)
    print(f"Вероятность завершения курса: {positive}")

    return {"probability": round(positive, 2)}