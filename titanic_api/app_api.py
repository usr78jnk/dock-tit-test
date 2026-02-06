'''
Задача: создать API с тремя ручками
1. /predict - для предсказания выживаемости
2. /stats - для получения к-ва запросов
3. /health - для проверки работы нашего API

Шаг 1: уснановка зависимостей. `pip install fastapi unicorn pydantic scikit-learn pandas`
нужно расделять создание requiremens для приложения и ноутбука.

Шаг 2: Написанеи прилодения app_api.py
Step 3: Testing API
Sesting will be exploit behevior curl requests or another methods sending HTTP - sequests

Checking what api is work:
curl -X GET http://127.0.0.1/health
curl -X GET http://127.0.0.1/stats
curl -X POST http://127.0.0.1/predict -H "Content-Type: application/json" -d
'''

from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
import pickle
import pandas as pd

app = FastAPI()

# загрузка модели из pickle файла
with open("model.pkl", 'rb') as f:
    model = pickle.load(f)

# счетчик запросов
requests_count = 0

# Создание модели для валидации входных данных
class PredictionInput(BaseModel):
    Pclass: int
    Age: float
    Fare: float

@app.get("/stats")
def stats():
    return {"request_count": requests_count} #Возвращаем даанные типа: словарь

@app.get("/health")
def health():
    return {"status": "OK"} #Максимально простая ручка, для того тчобы понять работает ли модель

# Пробую сам написать ручку, для того что-бы поигратся с простыми заросами типа GET
@app.get("/kkt")
def kokot():
    return f"Michal"

# Попробую сам написать ручку для отображения иконки
# @app.get("/favicon.ico")
# def icon():
#     return("ico/1486506225-item-li-list-list-item-ul_81441.ico")

# хуйня, первый блин комом
icon_path="ico/icon.ico"

@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return FileResponse(icon_path)
# Как оказалось, браузер - пидор, кэшировал состояние без иконки,
# В режиме инкогнито все работает

@app.post("/predict")
def predict(input_data: PredictionInput):
    global requests_count
    requests_count += 1

    # Create DataFrame from data, whitch we got from user
    new_data = pd.DataFrame({
        'Pclass': [input_data.Pclass],
        'Age': [input_data.Age],
        'Fare': [input_data.Fare]
    })

    # получение предсказания
    predictctions = model.predict(new_data)

    # Преобразовнаие результата предсказания в человеческий формат
    result = "Survived" if predictctions == 1 else "Not survived"

    return{"prediction": result}

if __name__ == "__main__":
    import uvicorn
# uvicorn.run(app, host="127.0.0.1", port=5000, reload=True)
    uvicorn.run(
        "app_api:app",
        # host="127.0.0.1",
        host="0.0.0.0",
        port=5000
        # reload=True # for docker image this function doesnt need
    )