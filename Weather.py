import requests
from datetime import datetime
import json
import os


class WeatherParser:
    def __init__(self, api_key):
        self.api_key = api_key
        self.history = []
        self.history_file = "weather_history.json"
        self._load_history()

    def _load_history(self):
        """Загрузка истории из файла"""
        if os.path.exists(self.history_file):
            try:
                with open(self.history_file, 'r', encoding='utf-8') as f:
                    self.history = json.load(f)
            except (json.JSONDecodeError, FileNotFoundError):
                self.history = []

    def _save_history(self):
        """Сохранение истории в файл"""
        try:
            with open(self.history_file, 'w', encoding='utf-8') as f:
                json.dump(self.history[-10:], f, ensure_ascii=False, indent=2)  # Сохраняем последние 10 записей
        except IOError:
            print("Ошибка при сохранении истории")

    def get_weather(self, city_name):
        """Получение текущей погоды"""
        current_url = "http://api.openweathermap.org/data/2.5/weather"

        params = {
            'q': city_name,
            'appid': self.api_key,
            'units': 'metric',
            'lang': 'ru'
        }

        try:
            response = requests.get(current_url, params=params)
            response.raise_for_status()

            data = response.json()

            if data['cod'] != 200:
                print(f"Ошибка: {data.get('message', 'Неизвестная ошибка')}")
                return None

            return self._parse_current_data(data, city_name)

        except requests.exceptions.RequestException as e:
            print(f"Ошибка при запросе к API: {e}")
            return None

    def _parse_current_data(self, data, city_name):
        """Парсинг данных текущей погоды"""
        try:
            weather_data = {
                'город': city_name,
                'время': datetime.now().strftime('%d.%m.%Y %H:%M'),
                'температура': round(data['main']['temp'], 1),
                'ощущается_как': round(data['main']['feels_like'], 1),
                'влажность': data['main']['humidity'],
                'давление': data['main']['pressure'],
                'скорость_ветра': round(data['wind']['speed'], 1),
                'описание': data['weather'][0]['description'].capitalize(),
                'видимость': data.get('visibility', 'N/A')
            }
            return weather_data
        except KeyError as e:
            print(f"Ошибка формата данных: {e}")
            return None

    def display_weather(self, weather_data):
        """Отображение текущей погоды"""
        if not weather_data:
            return

        print(f"\n🌤 ПОГОДА В {weather_data['город'].upper()}")
        print("=" * 50)
        print(f"📅 {weather_data['время']}")
        print(f"🌡 Температура: {weather_data['температура']}°C")
        print(f"🤔 Ощущается как: {weather_data['ощущается_как']}°C")
        print(f"💧 Влажность: {weather_data['влажность']}%")
        print(f"📊 Давление: {weather_data['давление']} гПа")
        print(f"🌬 Ветер: {weather_data['скорость_ветра']} м/с")
        print(f"☁️ {weather_data['описание']}")
        if weather_data['видимость'] != 'N/A':
            print(f"👁 Видимость: {weather_data['видимость']} м")

    def save_to_history(self, weather_data):
        """Сохранение в историю"""
        self.history.append(weather_data)
        # Сохраняем только последние 10 записей
        if len(self.history) > 10:
            self.history = self.history[-10:]
        self._save_history()

    def show_history(self):
        """Показать историю запросов"""
        if not self.history:
            print("История запросов пуста")
            return

        print("\n📋 ИСТОРИЯ ЗАПРОСОВ")
        print("=" * 50)
        for i, record in enumerate(reversed(self.history), 1):
            print(f"{i}. {record['город']} - {record['время']}")
            print(f"   {record['температура']}°C, {record['описание']}")
            print("-" * 30)

    # Остальные методы остаются без изменений
    def get_forecast(self, city_name, days=5):
        """Получение прогноза погоды на несколько дней"""
        forecast_url = "http://api.openweathermap.org/data/2.5/forecast"

        params = {
            'q': city_name,
            'appid': self.api_key,
            'units': 'metric',
            'lang': 'ru'
        }

        try:
            response = requests.get(forecast_url, params=params)
            response.raise_for_status()

            data = response.json()

            if data['cod'] != '200':
                print(f"Ошибка: {data.get('message', 'Неизвестная ошибка')}")
                return None

            return self._parse_forecast_data(data, days)

        except requests.exceptions.RequestException as e:
            print(f"Ошибка при запросе к API: {e}")
            return None
        except KeyError as e:
            print(f"Ошибка формата данных: {e}")
            return None

    def _parse_forecast_data(self, data, days):
        """Парсинг данных прогноза"""
        forecasts = []
        processed_dates = set()

        for item in data['list']:
            try:
                forecast_time = datetime.fromtimestamp(item['dt'])
                forecast_date = forecast_time.date()

                # Берем только один прогноз на день (ближайший к 12:00)
                if forecast_date not in processed_dates and len(forecasts) < days:
                    # Ищем лучшее время для отображения (ближе к полудню)
                    if abs(forecast_time.hour - 12) <= 3 or len(forecasts) == 0:
                        forecast = {
                            'дата': forecast_time.strftime('%d.%m.%Y'),
                            'день_недели': self._get_weekday(forecast_time),
                            'температура': round(item['main']['temp'], 1),
                            'ощущается_как': round(item['main']['feels_like'], 1),
                            'влажность': item['main']['humidity'],
                            'описание': item['weather'][0]['description'].capitalize(),
                            'скорость_ветра': round(item['wind']['speed'], 1),
                            'давление': item['main']['pressure'],
                            'время': forecast_time.strftime('%H:%M')
                        }
                        forecasts.append(forecast)
                        processed_dates.add(forecast_date)

            except (KeyError, TypeError) as e:
                print(f"Ошибка при обработке данных прогноза: {e}")
                continue

        return forecasts[:days]

    def _get_weekday(self, date_obj):
        """Получение названия дня недели на русском"""
        weekdays = [
            'Понедельник', 'Вторник', 'Среда', 'Четверг',
            'Пятница', 'Суббота', 'Воскресенье'
        ]
        return weekdays[date_obj.weekday()]

    def display_forecast(self, forecasts, city_name):
        """Вывод прогноза погоды"""
        if not forecasts:
            print("Нет данных для отображения прогноза")
            return

        print(f"\n📅 ПРОГНОЗ ПОГОДЫ В {city_name.upper()}")
        print("=" * 70)

        for forecast in forecasts:
            print(f"{forecast['дата']} ({forecast['день_недели']}, {forecast['время']}):")
            print(f"  🌡 {forecast['температура']}°C (ощущается как {forecast['ощущается_как']}°C)")
            print(f"  💧 Влажность: {forecast['влажность']}%")
            print(f"  🌬 Ветер: {forecast['скорость_ветра']} м/с")
            print(f"  📊 Давление: {forecast['давление']} гПа")
            print(f"  ☁️ {forecast['описание']}")
            print("-" * 70)


def main():
    API_KEY = "ваш_api_ключ_здесь"  # Замените на ваш реальный API ключ
    weather_parser = WeatherParser(API_KEY)

    print("🌤 Парсер погоды")
    print("Команды:")
    print("  город - текущая погода")
    print("  прогноз город [дни] - прогноз на N дней (по умолчанию 5)")
    print("  история - показать историю запросов")
    print("  выход - завершить программу")

    while True:
        try:
            command = input("\nВведите команду: ").strip().lower()

            if command in ['выход', 'exit', 'quit']:
                print("До свидания!")
                break
            elif command == 'история':
                weather_parser.show_history()
            elif command.startswith('прогноз '):
                parts = command.split()
                if len(parts) >= 2:
                    city = ' '.join(parts[1:-1]) if len(parts) > 2 and parts[-1].isdigit() else ' '.join(parts[1:])
                    days = int(parts[-1]) if len(parts) > 2 and parts[-1].isdigit() else 5

                    if 1 <= days <= 10:
                        forecasts = weather_parser.get_forecast(city, days)
                        if forecasts:
                            weather_parser.display_forecast(forecasts, city)
                    else:
                        print("Количество дней должно быть от 1 до 10")
                else:
                    print("Укажите город после 'прогноз'")
            elif command:
                weather_data = weather_parser.get_weather(command)
                if weather_data:
                    weather_parser.display_weather(weather_data)
                    weather_parser.save_to_history(weather_data)

        except KeyboardInterrupt:
            print("\n\nПрограмма завершена пользователем")
            break
        except Exception as e:
            print(f"Произошла ошибка: {e}")


if __name__ == "__main__":
    main()