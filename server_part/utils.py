from datetime import datetime, timedelta
import requests

from weather import Weather

"""                  OPENWEATHER
Обратите внимание, что запросы API по названию города ,
почтовому индексу и идентификатору города устарели.
Хотя они по-прежнему доступны для использования, исправления ошибок и обновления для этой
функции больше не доступны.
                 COPIFT(Sergeev Daniil)
Так как методы устарели, лучше будет искать погоду только по координатам,
а  у городов уточнять координаты и  по ним искать
Более того по координатам выдается больше информации о погоде
(для примера по координатам Иркутска выдается 5 геостанций которые его охватывают)
В то время как по запросу города выдается всего одна общая сводка о погоде
"""


def sr(
        list : list
) -> float:
    """
        Получение среднего значения массива.

    Args:
                  list : массив значений
    Returns:
                 среднее значение
              """

    sum = 0
    count = 0
    for element in list:
        sum = element + sum
        count += 1
    return sum // count


def getDayFromForecast(
        listWeather: list,
        shift: int = 1
) -> Weather:
    """Получение погоды на день на основе по-трех-часовых прогнозов.

            Args:
                listWeather : List из obj:Weather по-трех-часовых прогнозов
                shift : отклонение от текущего дня(max 4)
            Returns:
               obj:Weather
            """
    day = []
    # находим все подходящие данные на день
    for station in listWeather:
        if station.time.day == (datetime.now() + timedelta(days=shift)).day:
            day.append(station)

    # находим значения  для середины дня
    desc = day[(len(day) - 1) // 2].description
    dir = day[(len(day) - 1) // 2].wind_deg
    unit = day[(len(day) - 1) // 2].unit
    time = day[(len(day) - 1) // 2].dt
    temps = [time.temp for time in day]
    max_temp = max(temps)
    min_temp = min(temps)

    # находим средние значения
    sr_temp = sr(temps)
    feel_like = sr([time.feels_like for time in day])
    sr_scloud = sr([time.clouds for time in day])
    sr_pression = sr([time.pression for time in day])
    sr_speed = sr([time.wind_speed for time in day])
    # возвращаем обьект класса Weather
    return Weather(name=day[0].name,
                   id=day[0].id,
                   max_temp=max_temp,
                   min_temp=min_temp,
                   temp=sr_temp,
                   feels_like=feel_like,
                   wind_speed=sr_speed,
                   wind_deg=dir,
                   pressure=sr_pression,
                   clouds=sr_scloud,
                   description=desc,
                   unit=unit,
                   time=time)
def deSerlJsonToWeather(
        jsonWeather,
        units: str,
        fl=True
) -> list:
    """Дессериализация json ответа в лист обьектов класса Weather.

    Args:
                    jsonWeather : json ответа  содержащий в себе список данных
                    units : система счисления
                    fl : флаг для различных json(Fasle для Forecast)
    Returns:
                    list Weather
                """
    if jsonWeather['cod'] == '200':
        stations = jsonWeather['list']
        i = 2
        names = []
        alr = []
        for station in stations:
            # обработка различных json, передаваемых на вход(Да некрасиво, можно  лучше, но что поделать)
            if fl:  # по умолчанию
                name = station['name']
                id = station['id']
                if name in alr:  # проверка на одинаковые имена, чтобы убрать зацикливание у бота
                    name = f"{name} - {i}"
                    i += 1
                rain = station['rain']
                snow = station['snow']
            else:  # для FORECAST
                name = jsonWeather['city']['name']
                id = jsonWeather['city']['id']
                rain = None
                snow = None
            alr.append(name)
            # десериализация
            names.append(Weather(name=name,
                                 id=id,
                                 max_temp=station['main']['temp_max'],
                                 min_temp=station['main']['temp_min'],
                                 temp=station['main']['temp'],
                                 pressure=station['main']['pressure'],
                                 feels_like=station['main']['feels_like'],
                                 wind_speed=station['wind']['speed'],
                                 wind_deg=station['wind']['deg'],
                                 clouds=station['clouds']['all'],
                                 rain=rain,
                                 snow=snow,
                                 description=station['weather'][0]['description'],
                                 icon=station['weather'][0]['icon'],
                                 unit=units,
                                 time=station['dt']))

        return (names)
    else:
        return ([Weather(name="NOT FOUND")])



def getWeatherByCoordinates(lat : float,
                            lon : float,
                            units="metric",
                            exclude="current"
                            ) -> list:
    """Метод для запроса на openweather, получает погоду по координатам

    Args:
         lat:долгота
         lon:широта
         units: система счисления
         exclude: тип запроса

    Returns:
        list of Weather

    """
    answer = requests.get("http://api.openweathermap.org/data/2.5/find",
                          params={"lat": lat,
                                  "lon": lon,
                                  "units": units,
                                  "lang": "ru",
                                  "exclude": exclude,
                                  "appid": "3f1eaf8a73edf5dcc0e9fce32ff24372"}).json()
    return deSerlJsonToWeather(answer, units)


# метод запроса по координатам FORECAST, сnt-количество шагов
def getWeatherByCoordinatesForecast(lat, lon, cnt=40, units="metric") -> list:
    """Метод для запроса на openweather, получает погоду по координатам на будущее,  в cnt требуется передать количетсво по-трехчасовых шагов вперед

     Args:
          lat:долгота
          lon:широта
          cnt: количество получаемых шагов
          units: система счисления

     Returns:
         list of Weather

     """
    answer = requests.get("http://api.openweathermap.org/data/2.5/forecast?",
                          params={"lat": lat,
                                  "lon": lon,
                                  "units": units,
                                  "lang": "ru",
                                  "cnt": cnt,
                                  "appid": "3f1eaf8a73edf5dcc0e9fce32ff24372"}).json()
    return deSerlJsonToWeather(answer, units, False)


# уточнение координат города, возвращает словарь координат места по названию
def getCityCoordinates(city: str) -> dict:
    """Метод для запроса на openweather, получает координаты города по названию

     Args:
        city: название города

     Returns:
         dict:  { ' lat ' , ' lon ' }

     """
    answer = requests.get("http://api.openweathermap.org/geo/1.0/direct", params={"q": city,
                                                                                  "appid": "3f1eaf8a73edf5dcc0e9fce32ff24372"}).json()
    return {'lat': answer[0]['lat'], 'lon': answer[0]['lon']}
