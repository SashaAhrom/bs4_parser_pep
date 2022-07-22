# Проект парсинга pep
### Описание
```
Проект парсит данные с ресурса 'https://peps.python.org/'.
```
### Запуск программы
```
- В дериктории проекта перейдите в каталог src.
- Для получения информации о программе введите в консоль python main.py -h
```
```
main.py [-h] [-c] [-p] [-o {pretty,file}] {whats-new,latest-versions,download,pep}

Парсер документации Python

positional arguments:
  {whats-new,latest-versions,download,pep}
                        Режимы работы парсера

optional arguments:
  -h, --help            show this help message and exit
  -c, --clear-cache     Очистка кеша
  -p, --pretty          Вывод в формате PrettyTable
  -o {pretty,file}, --output {pretty,file}
                        Дополнительные способы вывода данных
```