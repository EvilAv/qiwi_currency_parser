import requests
import xml.etree.ElementTree as ET
import sys
from datetime import datetime

guide = 'Утилита запускается в формате:\n'\
        '\tcurrency_rates --code=USD --date=2022-10-08, где\n'\
        '\tcode - код валюты в формате ISO 4217\n'\
        '\tdate - дата в формате YYYY-MM-DD'
url = "https://www.cbr.ru/scripts/XML_daily.asp"
date_format = '%Y-%m-%d'


def parser(args):
    if len(args) >= 3:
        if args[1].startswith('--code=') and args[2].startswith('--date='):

            code = args[1].replace('--code=', ' ').strip()
            date_str = args[2].replace('--date=', ' ').strip()
            date = ''

            try:
                date_obj = datetime.strptime(date_str, date_format)

                if date_obj > datetime.today():
                    return 'Указанная дата еще не наступила'

                date = date_obj.strftime('%d/%m/%Y')

            except ValueError:
                return 'Дата указаны в неверном формате, укажите дату в формате YYYY-MM-DD'

            params = {
                "date_req": date
            }
            res = requests.get(url, params=params)

            if res:
                xml = res.text

                root_node = ET.fromstring(xml)

                if len(root_node) == 0:
                    return 'Данные за этот период отсутствуют'
                else:
                    ans = ''
                    for valute in root_node.findall('Valute'):
                        cur_code = valute.find('CharCode').text
                        if cur_code == code:
                            value = valute.find('Value').text
                            name = valute.find('Name').text
                            ans = f'{code} ({name}): {value}'
                            break
                    if ans == '':
                        ans = 'Указан неверный код валюты'
                    return ans
            else:
                return f'Ошибка сервера: {res.status_code}'
        else:
            return 'Некорректно указаны параметры\n' + guide
    else:
        return guide


if __name__ == '__main__':
    result = parser(sys.argv)
    print(result)
