"""Constants for the Mój Licznik integration."""

DOMAIN = "energa"
DATA_CLIENT = "energa"
DATA_COORDINATOR = "coordinator"

HTTP_API_URL = "https://api-mojlicznik.energa-operator.pl/dp"
HTTP_HEADERS =  {
    'Host': 'api-mojlicznik.energa-operator.pl',
    'Accept': '*/*',
    'Cookie': 'TS015b8f91=01ba031e81a923980736f79040e339445239f3da96e9e683977e25a6e7f0fc1368f11b72cb9611417b760324c5fdba0e9fab685bf6',
    'User-Agent': 'Energa/3.0.1 (pl.energa-operator.mojlicznik; build:25; iOS 15.0.0) Alamofire/4.9.1',
    'Accept-Language': 'en-US;q=1.0',
    'Authorization': 'Basic dGVzdDo5MFlCT20xMg==',
}
