import unittest
from datetime import datetime, timedelta

from currency_rates import parser, guide


class TesttDate(unittest.TestCase):
    def test_too_old_date(self):
        date = '--date=1985-05-02'
        code = '--code=USD'
        result = parser(['', code, date])
        self.assertEqual(result, 'Данные за этот период отсутствуют')

    def test_future_date(self):
        cur_date = datetime.today()
        future_date = cur_date + timedelta(days=365)
        date = '--date=' + future_date.strftime('%Y-%m-%d')
        code = '--code=USD'
        result = parser(['', code, date])
        self.assertEqual(result, 'Указанная дата еще не наступила')

    def test_incorrect_date(self):
        date = '--date=2001-02-35'
        code = '--code=USD'
        result = parser(['', code, date])
        self.assertEqual(result, 'Дата указаны в неверном формате, укажите дату в формате YYYY-MM-DD')


class TesttCode(unittest.TestCase):
    def test_incorrect_code(self):
        date = '--date=2001-02-20'
        code = '--code=USDs'
        result = parser(['', code, date])
        self.assertEqual(result, 'Указан неверный код валюты')

    def test_correct_data(self):
        date = '--date=2001-02-20'
        code = '--code=USD'
        result = parser(['', code, date])
        self.assertEqual(result, 'USD (Доллар США): 28,6600')


class TestParams(unittest.TestCase):
    def test_less_params_count(self):
        code = '--code=USDs'
        result = parser(['', code])
        self.assertEqual(result, guide)

    def test_more_params_count(self):
        date = '--date=2001-02-20'
        code = '--code=USD'
        result = parser(['', code, date, 'smth', 18])
        self.assertEqual(result, 'USD (Доллар США): 28,6600')

    def test_incorrect_params_format(self):
        date = '----date=2001-02-20'
        code = 'code=USD'
        result = parser(['', code, date])
        self.assertEqual(result, 'Некорректно указаны параметры\n' + guide)


if __name__ == '__main__':
    unittest.main()