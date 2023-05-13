import numpy as np
from keras.models import Sequential
from keras.layers import Dense, LSTM


def training_model_and_predict_incidents_ai(clear_data):
    predicted_data = []
    events_fit_data = []
    events_real_data = []
    fit_data = []
    real_data = []
    for item in range(len(clear_data)):
        for hour in range(0, 25):
            hour_array_fit = [hour, 0]
            events_fit_data.append(hour_array_fit)
        for hour in range(0, 25):
            hour_array_real = [hour, 0]
            events_real_data.append(hour_array_real)
        for _ in clear_data[item]:
            print(_)
            """ место для указания даты инцидента"""
            if int(_[3][8:10]) == 2:
                for hour_array in events_real_data:
                    if int(hour_array[0]) == int(_[3][10:13]):
                        hour_array[1] += 1
            else:
                for hour_array in events_fit_data:
                    if int(hour_array[0]) == int(_[3][10:13]):
                        hour_array[1] += 1

        for events_fit_data_item in events_fit_data:
            fit_data.append(events_fit_data_item[1])
        for events_real_data_item in events_real_data:
            real_data.append(events_real_data_item[1])
        # Определяем параметры модели
        n_steps = 3
        n_features = 1

        # Создаем функцию для подготовки данных
        def prepare_data(data, n_steps):
            X, y = [], []
            for i in range(len(data)):
                end_ix = i + n_steps
                if end_ix > len(data) - 1:
                    break
                seq_x, seq_y = data[i:end_ix], data[end_ix]
                X.append(seq_x)
                y.append(seq_y)
            return np.array(X), np.array(y)

        # Подготавливаем данные для обучения модели
        X, y = prepare_data(data=fit_data, n_steps=n_steps)
        X = np.reshape(X, (X.shape[0], X.shape[1], n_features))

        # Создаем модель RNN
        model = Sequential()
        model.add(LSTM(50, activation='relu', input_shape=(n_steps, n_features)))
        model.add(Dense(1))
        model.compile(optimizer='adam', loss='mse')

        # Обучаем модель(на тестовых значениях(fit_data))
        model.fit(X, y, epochs=620, verbose=0)

        # Предсказываем количество происшествий на следующий месяц(реальные значения(real_data))
        last_months_incidents = np.array(real_data[-n_steps:])
        last_months_incidents = np.reshape(last_months_incidents, (1, n_steps, n_features))
        next_month_incidents = model.predict(last_months_incidents)
        print(f"Возможность {clear_data[item][0][4]} на улице {clear_data[item][0][2]}:",
              float(next_month_incidents[0][0]))
        predicted_data.append([clear_data[item][0],
                              float(next_month_incidents[0][0])])
        events_fit_data.clear()
        events_real_data.clear()
        fit_data.clear()
        real_data.clear()

    return predicted_data
