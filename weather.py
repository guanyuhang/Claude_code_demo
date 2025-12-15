"""
天氣資訊模組
提供每日天氣查詢功能
"""

import os
from datetime import datetime
from typing import Dict, Optional
import json

try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False


class WeatherService:
    """天氣服務類別"""

    def __init__(self, api_key: Optional[str] = None):
        """
        初始化天氣服務

        Args:
            api_key: OpenWeatherMap API 金鑰（可選）
        """
        self.api_key = api_key or os.getenv('OPENWEATHER_API_KEY')
        self.base_url = "https://api.openweathermap.org/data/2.5/weather"

        # 支援的城市列表
        self.cities = {
            '台北': 'Taipei',
            '台中': 'Taichung',
            '台南': 'Tainan',
            '高雄': 'Kaohsiung',
            '新北': 'New Taipei City',
            'taipei': 'Taipei',
            'taichung': 'Taichung',
            'tainan': 'Tainan',
            'kaohsiung': 'Kaohsiung'
        }

    def get_weather(self, city: str) -> Dict:
        """
        取得指定城市的天氣資訊

        Args:
            city: 城市名稱（支援中文或英文）

        Returns:
            包含天氣資訊的字典
        """
        # 轉換城市名稱
        city_name = self._get_city_name(city)

        # 如果有 API 金鑰且 requests 可用，則使用真實 API
        if self.api_key and REQUESTS_AVAILABLE:
            return self._fetch_real_weather(city_name)
        else:
            # 使用模擬資料
            return self._get_mock_weather(city_name)

    def _get_city_name(self, city: str) -> str:
        """轉換城市名稱為英文"""
        city_lower = city.lower()
        return self.cities.get(city, self.cities.get(city_lower, city))

    def _fetch_real_weather(self, city: str) -> Dict:
        """從 API 取得真實天氣資料"""
        try:
            params = {
                'q': city,
                'appid': self.api_key,
                'units': 'metric',  # 使用攝氏溫度
                'lang': 'zh_tw'      # 中文描述
            }

            response = requests.get(self.base_url, params=params, timeout=10)
            response.raise_for_status()

            data = response.json()

            return {
                'city': data['name'],
                'temperature': round(data['main']['temp'], 1),
                'feels_like': round(data['main']['feels_like'], 1),
                'humidity': data['main']['humidity'],
                'description': data['weather'][0]['description'],
                'wind_speed': data['wind']['speed'],
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'source': 'OpenWeatherMap API'
            }

        except requests.RequestException as e:
            raise ValueError(f"無法取得天氣資料: {e}")

    def _get_mock_weather(self, city: str) -> Dict:
        """
        提供模擬天氣資料
        當沒有 API 金鑰時使用
        """
        import random

        # 模擬不同城市的天氣
        mock_data = {
            'Taipei': {
                'temp_range': (18, 28),
                'conditions': ['多雲', '晴天', '小雨', '陰天']
            },
            'Taichung': {
                'temp_range': (20, 30),
                'conditions': ['晴天', '多雲', '晴朗']
            },
            'Kaohsiung': {
                'temp_range': (22, 32),
                'conditions': ['晴天', '多雲時晴', '炎熱']
            },
            'Tainan': {
                'temp_range': (21, 31),
                'conditions': ['晴天', '多雲', '溫暖']
            }
        }

        # 取得城市資料或使用預設值
        city_data = mock_data.get(city, mock_data['Taipei'])

        temp = random.randint(*city_data['temp_range'])

        return {
            'city': city,
            'temperature': temp,
            'feels_like': temp + random.randint(-2, 2),
            'humidity': random.randint(60, 85),
            'description': random.choice(city_data['conditions']),
            'wind_speed': round(random.uniform(1.5, 5.5), 1),
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'source': '模擬資料 (設定 OPENWEATHER_API_KEY 環境變數以使用真實資料)'
        }

    def format_weather(self, weather_data: Dict) -> str:
        """
        格式化天氣資訊為易讀的字串

        Args:
            weather_data: 天氣資料字典

        Returns:
            格式化的天氣資訊字串
        """
        return f"""
╔════════════════════════════════════════╗
║          🌤️  天氣資訊  🌤️              ║
╠════════════════════════════════════════╣
║  城市: {weather_data['city']:<30} ║
║  溫度: {weather_data['temperature']}°C (體感 {weather_data['feels_like']}°C){' ' * (30 - len(f"{weather_data['temperature']}°C (體感 {weather_data['feels_like']}°C)"))} ║
║  天氣: {weather_data['description']:<30} ║
║  濕度: {weather_data['humidity']}%{' ' * (32 - len(f"{weather_data['humidity']}%"))} ║
║  風速: {weather_data['wind_speed']} m/s{' ' * (28 - len(f"{weather_data['wind_speed']} m/s"))} ║
║                                        ║
║  更新時間: {weather_data['timestamp']:<23} ║
║  資料來源: {weather_data['source']:<23} ║
╚════════════════════════════════════════╝
"""


def get_daily_weather(city: str = '台北') -> str:
    """
    取得每日天氣資訊的便利函數

    Args:
        city: 城市名稱，預設為台北

    Returns:
        格式化的天氣資訊字串
    """
    service = WeatherService()
    try:
        weather = service.get_weather(city)
        return service.format_weather(weather)
    except Exception as e:
        return f"❌ 無法取得天氣資訊: {e}"


if __name__ == "__main__":
    # 測試天氣模組
    print("測試天氣資訊功能:")
    print(get_daily_weather('台北'))
    print("\n支援的城市: 台北、台中、台南、高雄")
