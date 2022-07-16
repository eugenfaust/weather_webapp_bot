API_TOKEN = 'bot:token'
ERROR_CHANNEL = 123456

POSTGRES_HOST = "localhost"
POSTGRES_PORT = 5432
POSTGRES_USER = 'user'
POSTGRES_PASS = 'password'
POSTGRES_DB = 'weather'
POSTGRES_URI = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASS}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"

WEATHER_URL = 'https://weatherurl.com/'
WEATHER_NOW = WEATHER_URL + 'now?user_id={}'
WEATHER_WEEK = WEATHER_URL + 'week?user_id={}'
OPENWEATHER_APIKEY = 'apikey'
WEATHER_GEOCODING_URL = 'https://api.openweathermap.org/data/2.5/weather?q={}&appid={APIKEY}&lang=ru'
WEATHER_GEODECODING_URL = 'http://api.openweathermap.org/geo/1.0/reverse?lat={}&lon={}&limit=1&appid={APIKEY}'
DONATE_URL = 'https://yoomoney.ru/to/{WALLET}/0'
SOURCE_URL = 'https://github.com/username/repo'
DEVELOPER_USERNAME = '@username'