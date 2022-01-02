# -*- coding: utf-8 -*-
"""5_Sheets_Stock_Prediction.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1TyxHELQ6mNHfttFafJte5URQsPUc6TNN

# Importación
"""

!pip install yfinance

import pandas as pd
import yfinance as yf
from datetime import datetime
from dateutil.relativedelta import relativedelta

from google.colab import auth
auth.authenticate_user()

import gspread
from oauth2client.client import GoogleCredentials

# Importar el fichero import_data_stock_prediction.py, el cual se conecta a Yahoo Finance e importa los datos
from google.colab import drive
drive.mount('/content/drive')

execfile('/content/drive/MyDrive/StockPrediction/import_data_stock_prediction.py')

# Importar el ficher lstm_stock_prediction.py, el cual contiene el modelo predictivo LSTM
drive.mount('/content/drive', force_remount=True)
execfile('/content/drive/MyDrive/StockPrediction/lstm_stock_prediction.py')

# Se comprueba que se tiene activado la aceleración con GPU
print("GPU available: ", tf.config.list_physical_devices('GPU'))

"""# Leer de Google Sheets"""

def OpenSheet(sheetName):
    gc = gspread.authorize(GoogleCredentials.get_application_default())

    worksheet = gc.open('Cartera StockPrediction').worksheet(sheetName)

    # get_all_values gives a list of rows.
    rows = worksheet.get_all_values()

    # Convert to a DataFrame and render.
    stock_wallet = pd.DataFrame.from_records(rows)
    stock_wallet.columns = stock_wallet.iloc[0]
    stock_wallet = stock_wallet.iloc[1: , :]
    return worksheet, stock_wallet

worksheet, stock_wallet = OpenSheet('Prediccion 27122021')
stock_wallet.iloc[0:]['Ticker'].head(5)

"""# Analizar una compañía"""

tickerSymbol = 'AAPL'

# Obtenemos los datos desde el día actual hasta hace 5 años
one_year_ago = datetime.now() - relativedelta(years=5)
start_date = one_year_ago.strftime('%Y-%m-%d')

#one_year_ago = datetime.now() - relativedelta(years=1)
end_date = datetime.now().strftime('%Y-%m-%d')

# Se obtiene el datafram de la empresa seleccionada y en el rango de fechas
tickerDf = GetStockDataByTicker(tickerSymbol, start_date, end_date)

GetStockInformationByTicker(tickerSymbol, start_date, end_date)

Graph_StockEvolutionByTime(tickerSymbol, tickerDf, 180)

x_train, y_train, dataset, training_data_len, scaler, scaled_data = TransformData(tickerDf, split_data)
LSTM_model = LSTM_Model(x_train, model_dropout, model_neuron, model_learning_rate)
LSTM_history = LSTM_fit(LSTM_model, x_train, y_train, model_epochs, model_batch_size)

predictions, y_test = LSTM_Predictions(LSTM_model, training_data_len, scaled_data, scaler, dataset)
LSTM_PlotPredictions(tickerDf.filter(['Adj Close']), training_data_len, predictions)
print("RSME = ", LSTM_RMSE(predictions, y_test))

"""# Predicción en Bucle

Parámetros de predicción
"""

train_last_days = 60
split_data = 0.8 #80% train, 20% test

model_neuron = 50
model_epochs = 25 
model_batch_size = 32 
model_learning_rate = 1e-4
model_dropout = 0.2

from random import randint
from time import sleep

# last_company = Ult numeración del excel - 2 casillas
def PredictWeek_SP500(sheet_name,
                        last_company,
                        train_last_days = 60,
                        split_data = 0.8,
                        model_neuron = 50,
                        model_epochs = 25,
                        model_batch_size = 32,
                        model_learning_rate = 1e-4,
                        model_dropout = 0.2):
    # Se abre la hoja de cálculo
    worksheet, stock_wallet = OpenSheet(sheet_name)

    # Obtenemos los datos desde el día actual hasta hace 5 años
    five_year_ago = datetime.now() - relativedelta(years=5)
    start_date = five_year_ago.strftime('%Y-%m-%d')
    end_date = datetime.now().strftime('%Y-%m-%d')

    row = last_company + 2
    for tickerSymbol in stock_wallet.iloc[last_company:]['Ticker']:
        tickerSymbol = tickerSymbol.replace(".", "-")
        # Temporizador aleatorio de parada para evitar que Google Colab aborte la sesión
        #sleep(randint(10,100))

        # Se obtiene el datafram de la empresa seleccionada y en el rango de fechas
        tickerDf = GetStockDataByTicker(tickerSymbol, start_date, end_date)

        # Tratamiento de datos
        x_train, y_train, dataset, training_data_len, scaler, scaled_data = TransformData(tickerDf, split_data)

        # Entrenamiento
        LSTM_model = LSTM_Model(x_train, model_dropout, model_neuron, model_learning_rate)
        LSTM_history = LSTM_fit(LSTM_model, x_train, y_train, model_epochs, model_batch_size)

        # Testeo
        predictions, y_test = LSTM_Predictions(LSTM_model, training_data_len, scaled_data, scaler, dataset)
        rsme = LSTM_RMSE(predictions, y_test)

        # Actualizar lista de valores del Excel
        worksheet.update_cell(row, 5, str(rsme).replace('.', ','))                                   # RMSE
        
        # Predicción de la última semana
        column = 0
        for predicted_day in reversed(range(1,6)):
            day, real, predicted = LSTM_PredictNextDay(tickerDf, scaler, LSTM_model, train_last_days, predicted_day)
            if predicted_day != 0:
                worksheet.update_cell(row, 7+column, str(real).replace('.', ','))                  # Real
                worksheet.update_cell(row, 8+column, str(predicted).replace('.', ','))             # Predecido
            else:
                worksheet.update_cell(row, 8+column, str(predicted).replace('.', ','))             # Predecido  
            column += 3

        row += 1

sheet_name = 'Prediccion 27122021'
last_company = 476 - 2
PredictWeek_SP500(sheet_name, last_company) #train_last_days, split_data, model_neuron, model_epochs, model_batch_size, model_learning_rate, model_dropout

"""# Actualizar Estudio Cartera o SP_500

"""

def UpdateExcelByCompany(sheetName, company, row):
    # Fechas de Inicio y Fin para obtener los datos.
    five_years_ago = datetime.now() - relativedelta(years=5)
    start_date = five_years_ago.strftime('%Y-%m-%d')
    end_date = datetime.now().strftime('%Y-%m-%d')

    # Obtenemos los datos por companía y fechas
    newCompany = GetStockInformationByTicker(company, start_date, end_date)

    # Se accede al Excel
    gc = gspread.authorize(GoogleCredentials.get_application_default())
    worksheet = gc.open('Cartera StockPrediction').worksheet(sheetName)

    # Se actualizan los valores del Excel
    worksheet.update_cell(row, 2, str(newCompany['Short Name'][0]))                                 # Short Name
    worksheet.update_cell(row, 3, str(newCompany['Sector'][0]))                                     # Sector
    worksheet.update_cell(row, 4, str(newCompany['Industry'][0]))                                   # Industry
    worksheet.update_cell(row, 5, str(newCompany['Recommendation'][0]))                             # Recommendation
    worksheet.update_cell(row, 6, str(newCompany['Recommendation Mean'][0]).replace('.', ','))      # Recommendation Mean
    worksheet.update_cell(row, 8, str(newCompany['Target Low Price'][0]).replace('.', ','))         # Target Low Price
    worksheet.update_cell(row, 9, str(newCompany['Target High Price'][0]).replace('.', ','))        # Target High Price
    worksheet.update_cell(row, 10, str(newCompany['Target Mean Price'][0]).replace('.', ','))       # Target Mean Price
    worksheet.update_cell(row, 11, str(newCompany['52 Week Change'][0]).replace('.', ','))          # 52 Week Change
    worksheet.update_cell(row, 14, str(newCompany['EMA10'][0]).replace('.', ','))                   # EMA10
    worksheet.update_cell(row, 15, str(newCompany['SMA20'][0]).replace('.', ','))                   # SMA20
    worksheet.update_cell(row, 16, str(newCompany['SMA50'][0]).replace('.', ','))                   # SMA50
    worksheet.update_cell(row, 17, str(newCompany['SMA100'][0]).replace('.', ','))                  # SMA100
    worksheet.update_cell(row, 18, str(newCompany['SMA200'][0]).replace('.', ','))                  # SMA200
    worksheet.update_cell(row, 25, str(newCompany['EBITDA'][0]).replace('.', ','))                  # EBITDA
    worksheet.update_cell(row, 26, str(newCompany['EBITDA Margins'][0]).replace('.', ','))          # EBITDA Margins
    worksheet.update_cell(row, 27, str(newCompany['Fecha Actualización'][0]))                       # Fecha Actualización

from random import randint
from time import sleep

# Nombre de la hoja donde escribir los datos
# sheetName = 'Estudio Cartera'
sheetName = 'SP_500'

worksheet, stock_wallet = OpenSheet(sheetName)
last_company = 191
row = last_company + 2
for company in stock_wallet.iloc[last_company:]['Ticker']:
    wait_time = randint(7,30)
    print(wait_time)
    sleep(wait_time)
    company = company.replace(".", "-")
    
    UpdateExcelByCompany(sheetName, company, row)
    row += 1