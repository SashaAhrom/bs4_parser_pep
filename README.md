# bs4_parser_pep(educational project)
## Description
```
The project parses data from the resource 'https://peps.python.org/'. and cache them.
Data can be output to logs in the form of a table or in the format .csv
```
## Running a project in dev mode
```
- In the project directory, change to the src directory.
- For information about the program, enter python main.py -h into the console

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
## System requirements
```
Python 3.7
```
