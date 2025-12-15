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

        # 支援的台灣城市列表（只限台灣地區）
        self.cities = {
            '台北': 'Taipei,TW',
            '台中': 'Taichung,TW',
            '台南': 'Tainan,TW',
            '高雄': 'Kaohsiung,TW',
            '新北': 'New Taipei City,TW',
            '基隆': 'Keelung,TW',
            '新竹': 'Hsinchu,TW',
            '桃園': 'Taoyuan,TW',
            'taipei': 'Taipei,TW',
            'taichung': 'Taichung,TW',
            'tainan': 'Tainan,TW',
            'kaohsiung': 'Kaohsiung,TW'
        }

        # 台灣允許的城市列表（用於驗證）
        self.taiwan_cities_only = set(self.cities.values())

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
        """
        轉換城市名稱為英文並驗證是否為台灣城市

        Args:
            city: 城市名稱

        Returns:
            英文城市名稱（含國家代碼）

        Raises:
            ValueError: 如果城市不在支援的台灣城市列表中
        """
        city_lower = city.lower()
        city_name = self.cities.get(city, self.cities.get(city_lower, None))

        if city_name is None:
            raise ValueError(
                f"不支援的城市 '{city}'。僅支援台灣地區城市：" +
                "台北、台中、台南、高雄、新北、基隆、新竹、桃園"
            )

        return city_name

    def _fetch_real_weather(self, city: str) -> Dict:
        """從 API 取得真實天氣資料（僅台灣地區）"""
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

            # 取得降雨量資訊（過去1小時，若無降雨則為0）
            rain_1h = 0
            if 'rain' in data and '1h' in data['rain']:
                rain_1h = data['rain']['1h']

            return {
                'city': data['name'],
                'temperature': round(data['main']['temp'], 1),
                'feels_like': round(data['main']['feels_like'], 1),
                'humidity': data['main']['humidity'],
                'description': data['weather'][0]['description'],
                'wind_speed': data['wind']['speed'],
                'rainfall': rain_1h,  # 降雨量 (mm/h)
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'source': 'OpenWeatherMap API'
            }

        except requests.RequestException as e:
            raise ValueError(f"無法取得天氣資料: {e}")

    def _get_mock_weather(self, city: str) -> Dict:
        """
        提供模擬天氣資料（僅台灣地區）
        當沒有 API 金鑰時使用
        """
        import random

        # 移除國家代碼以取得城市名稱
        city_name = city.split(',')[0] if ',' in city else city

        # 模擬不同台灣城市的天氣
        mock_data = {
            'Taipei': {
                'temp_range': (18, 28),
                'conditions': ['多雲', '晴天', '小雨', '陰天'],
                'rain_range': (0, 5)
            },
            'Taichung': {
                'temp_range': (20, 30),
                'conditions': ['晴天', '多雲', '晴朗'],
                'rain_range': (0, 3)
            },
            'Kaohsiung': {
                'temp_range': (22, 32),
                'conditions': ['晴天', '多雲時晴', '炎熱'],
                'rain_range': (0, 2)
            },
            'Tainan': {
                'temp_range': (21, 31),
                'conditions': ['晴天', '多雲', '溫暖'],
                'rain_range': (0, 2)
            },
            'New Taipei City': {
                'temp_range': (18, 28),
                'conditions': ['多雲', '晴天', '小雨'],
                'rain_range': (0, 4)
            },
            'Keelung': {
                'temp_range': (17, 26),
                'conditions': ['多雲', '陰天', '小雨', '毛毛雨'],
                'rain_range': (0, 8)
            },
            'Hsinchu': {
                'temp_range': (19, 29),
                'conditions': ['晴天', '多雲', '有風'],
                'rain_range': (0, 3)
            },
            'Taoyuan': {
                'temp_range': (19, 28),
                'conditions': ['晴天', '多雲', '陰天'],
                'rain_range': (0, 4)
            }
        }

        # 取得城市資料或使用預設值
        city_data = mock_data.get(city_name, mock_data['Taipei'])

        temp = random.randint(*city_data['temp_range'])
        description = random.choice(city_data['conditions'])

        # 根據天氣狀況調整降雨量
        if '雨' in description:
            rainfall = round(random.uniform(1, city_data['rain_range'][1]), 1)
        else:
            rainfall = 0

        return {
            'city': city_name,
            'temperature': temp,
            'feels_like': temp + random.randint(-2, 2),
            'humidity': random.randint(60, 85),
            'description': description,
            'wind_speed': round(random.uniform(1.5, 5.5), 1),
            'rainfall': rainfall,  # 降雨量 (mm/h)
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
        rainfall = weather_data.get('rainfall', 0)
        rain_status = f"{rainfall} mm/h" if rainfall > 0 else "無降雨"

        return f"""
╔════════════════════════════════════════╗
║          🌤️  天氣資訊  🌤️              ║
╠════════════════════════════════════════╣
║  城市: {weather_data['city']:<30} ║
║  溫度: {weather_data['temperature']}°C (體感 {weather_data['feels_like']}°C){' ' * (30 - len(f"{weather_data['temperature']}°C (體感 {weather_data['feels_like']}°C)"))} ║
║  天氣: {weather_data['description']:<30} ║
║  濕度: {weather_data['humidity']}%{' ' * (32 - len(f"{weather_data['humidity']}%"))} ║
║  風速: {weather_data['wind_speed']} m/s{' ' * (28 - len(f"{weather_data['wind_speed']} m/s"))} ║
║  降雨量: {rain_status:<29} ║
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
    print("測試天氣資訊功能 (僅限台灣地區):")
    print(get_daily_weather('台北'))
    print("\n支援的台灣城市: 台北、台中、台南、高雄、新北、基隆、新竹、桃園")
