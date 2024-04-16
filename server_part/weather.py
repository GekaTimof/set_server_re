import datetime


class Weather:
    """ Класс описывающий погоды со станции в определнное время


    :param name: имя станиции погоды
    :param id: id станции
    :param max_temp: максимальная темература
    :param min_temp: минимальнная температура
    :param pressure: давление
    :param feels_like: ощущается как
    :param temp:температура
    :param wind_speed: скорость ветра
    :param wind_deg: направление
    :param rain:состояние дождя
    :param snow:состояние снега
    :param clouds:облачноть
    :param description: описание погоды
    :param icon: значок погоды
    :param unit: система счисления
    :param time: штамп времени погоды
    """
    def getWindDirect(self):
        """
        получение направления ветра в символах

        :return: напрвление ветра в str
        """
        deg=self.wind_deg
        if deg==None:
            return "None"
        if deg>345 or deg<15:
            return "N"
        if deg > 75 and deg < 105:
            return "E"
        if deg>165 and deg<195:
            return "S"
        if deg>255 and deg<285:
            return "W"
        if deg>15 and deg<75:
            return "N-E"
        if deg>105 and deg<165:
            return "S-E"
        if deg > 195 and deg < 255:
            return "S-W"
        if deg > 255and deg < 345:
            return "N-W"

    def __init__(self, name='', id=0,max_temp=None,min_temp=None,pressure=None,feels_like=None,temp=None,
                 wind_speed=None,wind_deg=None,  rain=None, snow=None, clouds=None, description=None, icon=None,
                 unit=None,time=datetime.datetime.timestamp(datetime.datetime.now())) :

        self.time = datetime.datetime.fromtimestamp(time)
        self.dt=time
        self.unit=unit
        self.clouds = clouds
        self.snow = snow
        self.rain = rain
        self.wind_deg=wind_deg
        self.description = description
        self.id = id
        self.wind_dir = self.getWindDirect()
        self.wind_speed=wind_speed
        self.temp=temp
        self.max_temp = max_temp
        self.min_temp = min_temp
        self.pression = pressure
        self.feels_like = feels_like
        self.name = name
        self.deg_wind=wind_deg
        self.icon = icon # к сожалению в консольной версии невозможно использование icon( формат png) link https://openweathermap.org/img/w/{self.icon}.png
        self.units={'metric':{'speed':'m/s','temp':'°C'},
                    'imperial':{'speed':'miles/s','temp':'°F'},
                    'standart':{'speed':'m/s','temp':'°K'}}
        if self.unit!=None:
            self.sign_temp=self.units[self.unit]['temp']
            self.sign_speed = self.units[self.unit]['speed']
        else:
            self.sign_temp = None
            self.sign_speed = None


    def __str__(self) -> str:
        return f"{self.name}:\n " \
               f"{self.description} {self.temp}{self.sign_temp}\n" \
               f"ощущается как: {self.feels_like}{self.sign_temp}\n" \
               f"мин:{self.min_temp}{self.sign_temp}  макс:{self.max_temp}{self.sign_temp}\n" \
               f"давление:      {self.pression}\n" \
               f"ветер:         {self.wind_speed}{self.sign_speed} {self.getWindDirect()}\n" \
               f"дождь:         {self.rain}\n" \
               f"снег:          {self.snow}\n" \
               f"облачность:    {self.clouds}\n" \
               f"данные на {self.time.strftime('%H:%M %d/%m ')}\n"






