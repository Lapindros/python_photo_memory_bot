import requests


def get_quotes_today(valute):
    data = requests.get('https://www.cbr-xml-daily.ru/daily_json.js').json()
    valute_name = data['Valute'][valute]['Name']
    valute_value = data['Valute'][valute]['Value']
    return f'{valute_name} - {valute_value}'
