from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import numpy as np
from sklearn.preprocessing import MinMaxScaler
import tensorflow as tf
import os

# インスタンスを作成
app = FastAPI()

# h5:モデルのアーキテクチャ、重み、トレーニング設定の全てを保存
MODEL_PATH = "model.h5"

# データの型を定義
class Train(BaseModel):
    data: list
    step: int

# 時系列データ作成
def sequences(data, step):
    X, Y = [], []
    for i in range(len(data) - step):
        X_seq, Y_seq = data[i:i+step], data[i+step]
        X.append(X_seq)
        Y.append(Y_seq)
    return np.array(X), np.array(Y)


@app.post("/train/")
# 非同期関数として定義
async def train_model(request: Train):
    
    data = np.array(request.data).reshape(-1, 1)
    step = request.step

    # 正規化
    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled_data = scaler.fit_transform(data)

    # 説明変数と目的変数に代入
    X, Y = sequences(scaled_data, step)
    
    # モデルが存在するか確認しない場合は作成する
    if os.path.exists(MODEL_PATH):
        model = tf.keras.models.load_model(MODEL_PATH)
    else:
        # モデルが存在しない場合、新しく作成
        model = tf.keras.Sequential()
        model.add(tf.keras.layers.LSTM(50, activation="relu", input_shape=(X.shape[1], X.shape[2]), return_sequences=True))
        model.add(tf.keras.layers.LSTM(100, activation="relu", return_sequences=False))
        model.add(tf.keras.layers.Dense(1, activation="linear"))
        
        model.compile(optimizer="adam", loss="mean_squared_error")
    
    # 学習
    model.fit(X, Y, epochs=50, batch_size=32, verbose=0)

    # モデルの保存
    model.save(MODEL_PATH)

    # 予測
    X_test = scaled_data[-step:].reshape(1, step, 1)
    Y_pred = model.predict(X_test)
    Y_pred_ = scaler.inverse_transform(Y_pred)

    # jsonが「numpy.float32」に対応していないためfloatに変換
    prediction = float(Y_pred_[0][0])

    # return {"prediction": Y_pred_[0][0]}
    return {"prediction": prediction}
