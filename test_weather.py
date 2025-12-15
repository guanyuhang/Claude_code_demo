"""
天氣模組測試
"""

import unittest
from weather import WeatherService, get_daily_weather


class TestWeatherService(unittest.TestCase):
    """測試天氣服務類別"""

    def setUp(self):
        """設置測試環境"""
        self.service = WeatherService()

    def test_city_name_conversion_chinese(self):
        """測試中文城市名稱轉換"""
        self.assertEqual(self.service._get_city_name('台北'), 'Taipei,TW')
        self.assertEqual(self.service._get_city_name('台中'), 'Taichung,TW')
        self.assertEqual(self.service._get_city_name('高雄'), 'Kaohsiung,TW')

    def test_city_name_conversion_english(self):
        """測試英文城市名稱轉換"""
        self.assertEqual(self.service._get_city_name('taipei'), 'Taipei,TW')
        self.assertEqual(self.service._get_city_name('kaohsiung'), 'Kaohsiung,TW')

    def test_unsupported_city_rejected(self):
        """測試非台灣城市會被拒絕"""
        with self.assertRaises(ValueError) as context:
            self.service._get_city_name('Tokyo')
        self.assertIn('不支援的城市', str(context.exception))

        with self.assertRaises(ValueError) as context:
            self.service._get_city_name('New York')
        self.assertIn('僅支援台灣地區城市', str(context.exception))

    def test_get_mock_weather(self):
        """測試模擬天氣資料"""
        weather = self.service._get_mock_weather('Taipei,TW')

        # 檢查必要欄位
        self.assertIn('city', weather)
        self.assertIn('temperature', weather)
        self.assertIn('humidity', weather)
        self.assertIn('description', weather)
        self.assertIn('wind_speed', weather)
        self.assertIn('rainfall', weather)  # 新增降雨量檢查
        self.assertIn('timestamp', weather)

        # 檢查資料類型
        self.assertIsInstance(weather['temperature'], int)
        self.assertIsInstance(weather['humidity'], int)
        self.assertIsInstance(weather['description'], str)
        self.assertIsInstance(weather['rainfall'], (int, float))

        # 檢查合理範圍
        self.assertGreater(weather['temperature'], 0)
        self.assertLess(weather['temperature'], 50)
        self.assertGreaterEqual(weather['humidity'], 0)
        self.assertLessEqual(weather['humidity'], 100)
        self.assertGreaterEqual(weather['rainfall'], 0)  # 降雨量不應為負

    def test_get_weather_without_api_key(self):
        """測試無 API 金鑰時的天氣查詢"""
        weather = self.service.get_weather('台北')
        self.assertIsNotNone(weather)
        self.assertEqual(weather['city'], 'Taipei')

    def test_format_weather(self):
        """測試天氣格式化輸出"""
        weather_data = {
            'city': 'Taipei',
            'temperature': 25,
            'feels_like': 26,
            'humidity': 70,
            'description': '晴天',
            'wind_speed': 3.5,
            'rainfall': 0,  # 新增降雨量
            'timestamp': '2025-12-15 12:00:00',
            'source': '測試資料'
        }

        formatted = self.service.format_weather(weather_data)
        self.assertIsInstance(formatted, str)
        self.assertIn('Taipei', formatted)
        self.assertIn('25', formatted)
        self.assertIn('晴天', formatted)
        self.assertIn('降雨量', formatted)  # 檢查降雨量欄位

    def test_format_weather_with_rain(self):
        """測試有降雨時的天氣格式化輸出"""
        weather_data = {
            'city': 'Taipei',
            'temperature': 22,
            'feels_like': 23,
            'humidity': 85,
            'description': '小雨',
            'wind_speed': 2.5,
            'rainfall': 3.5,  # 有降雨
            'timestamp': '2025-12-15 12:00:00',
            'source': '測試資料'
        }

        formatted = self.service.format_weather(weather_data)
        self.assertIsInstance(formatted, str)
        self.assertIn('3.5 mm/h', formatted)  # 檢查降雨量顯示

    def test_get_daily_weather_function(self):
        """測試便利函數"""
        result = get_daily_weather('台北')
        self.assertIsInstance(result, str)
        self.assertIn('天氣資訊', result)

    def test_multiple_cities(self):
        """測試多個城市的天氣查詢"""
        cities = ['台北', '台中', '台南', '高雄']
        for city in cities:
            weather = self.service.get_weather(city)
            self.assertIsNotNone(weather)
            self.assertIn('temperature', weather)


if __name__ == '__main__':
    print("執行天氣模組測試...\n")
    unittest.main(verbosity=2)
