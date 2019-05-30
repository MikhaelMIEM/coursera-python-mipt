import requests


class OpenWeatherMapForecast:

    def get(self, city):
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&APPID=8be8a2954f17ce8a8440b0e9ef4629f9"
        data = requests.get(url).json()
        forecast = {}
        forecast["temperature"] = round(data["main"]["temp"] - 273.15, 1)
        forecast["info"] = data["weather"][0]["main"]
        return forecast


class CityInfo:

    def __init__(self, city, weather_forecast=None):
        self.city = city
        self._weather_forecast = weather_forecast or OpenWeatherMapForecast()

    def weather_forecast(self):
        return self._weather_forecast.get(self.city)


def _main():
    city_info = CityInfo("Chelyabinsk")
    forecast = city_info.weather_forecast()
    print(forecast)


if __name__ == "__main__":
    _main()
