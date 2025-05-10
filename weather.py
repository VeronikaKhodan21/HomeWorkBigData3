import requests
import json
import pandas as pd
from datetime import datetime as dt
import matplotlib.pyplot as plt
from hdfs import InsecureClient
import seaborn as sns
import matplotlib.pyplot as plt

api_key = '1262f42ec5784eee84a2c0b591963a44'


# Список городов для запроса данных о погоде
cities = ['Moscow', 'New York', 'Paris', 'Tokyo', 'Bangkok']
num =[1,2,3,4,5]
tempCity = [] #список для постороения графика температуры и городов
humCity = [] #список городов и влажности в них
# Словарь для хранения данных о погоде в каждом городе
weather_data = {}

# Запрос данных о погоде для каждого города
for city in cities:
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric'                   
    weather_data[city] = requests.get(url).json()

# запись данных в файл
with open('homework3\\img\\weather_data.json', 'w') as f:
    json.dump(weather_data, f)
#чтение из файла
with open('homework3\\img\\weather_data.json', 'r') as file:
   weather_data = json.load(file)

# запись в список температуры в городах
for city, data in weather_data.items():
    temp = data["main"]['temp']
    tempCity.append((city,temp))

for city, data in weather_data.items():
    humidity = data["main"]['humidity']
    humCity.append((city,humidity))

df = pd.DataFrame(tempCity, columns=['City', 'Temperature'])    

# создание графика температура от города
plt.figure(figsize=(12, 7))
sns.barplot(data=df, x='City', y='Temperature',  color="violet")
plt.xlabel('City')
plt.ylabel('Temperature(°C)')
plt.title('Cities and Temperatures '+dt.now().strftime('%x'))
plt.grid(True)
plt.savefig('homework3\\img\\tempCity.png')
plt.show()

dfe = pd.DataFrame(tempCity, columns=['City', 'Humidity'])
# Создание граффика влажномть от города
plt.plot( dfe["City"],dfe['Humidity'] , color="blue") 
plt.xlabel('City')
plt.ylabel('Humidity')
plt.title('Cities and Humidity '+dt.now().strftime('%x'))
plt.grid(True)
plt.savefig('homework3\\img\\humCity.png')
plt.show()

client = InsecureClient('http://localhost:9000')
with client.write('homework3\\img\\tempCity.png', encoding='utf-8') as writer:
    plt.figure(figsize=(12, 7))
    sns.barplot(data=df, x='City', y='Temperature',  color="violet")
    plt.xlabel('City')
    plt.ylabel('Temperature(°C)')
    plt.title('Cities and Temperatures '+dt.now().strftime('%x'))
    plt.grid(True)
    plt.savefig(writer)

with client.write('homework3\\img\\humCity.png', encoding='utf-8') as writer:
    plt.plot(data=df, x= "City", y="Humidity", color="blue") 
    plt.xlabel('City')
    plt.ylabel('Humidity')
    plt.title('Cities and Humidity '+dt.now().strftime('%x'))
    plt.grid(True)
    plt.savefig('homework3\\humCity.png')
    plt.show()

client.download('homework3\\img\\tempCity.png', 'tempCity.png', overwrite=True)
client.download('homework3\\img\\humCity.png', 'humCity.png', overwrite=True)
print("Данные о погоде сохранены в файлы")