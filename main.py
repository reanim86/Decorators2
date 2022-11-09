import os
import time

def logger(path):

    def __logger(old_function):

        def new_function(*args, **kwargs):
            start_time = time.ctime(time.time())
            result = old_function(*args, **kwargs)
            name = old_function.__name__
            arg = f'{args}{kwargs} '
            res = f'{result} '
            log = [f'{start_time} ', f'{name} ', arg, res, '\n']
            with open(path, 'a+', encoding='utf-8') as f:
                f.writelines(log)
            return result

        return new_function

    return __logger

def test_2():
    paths = ('log_1.log', 'log_2.log', 'log_3.log')

    for path in paths:
        if os.path.exists(path):
            os.remove(path)

        @logger(path)
        def summator(a, b=0):
            return a + b

        @logger(path)
        def div(a, b):
            return a / b

        result = summator(2, 2)
        assert isinstance(result, int), 'Должно вернуться целое число'
        assert result == 4, '2 + 2 = 4'
        div(4, 2)
        summator(4.3, b=2.2)

    for path in paths:

        assert os.path.exists(path), f'файл {path} должен существовать'

        with open(path) as log_file:
            log_file_content = log_file.read()

        assert 'summator' in log_file_content, 'должно записаться имя функции'

        for item in (4.3, 2.2, 6.5):
            assert str(item) in log_file_content, f'{item} должен быть записан в файл'


if __name__ == '__main__':
    test_2()