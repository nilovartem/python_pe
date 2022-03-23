import csv
import copy
import operator
import os
from dataclasses import dataclass
from tabulate import tabulate

@dataclass
class Building:
    microdistrict: str
    street: str
    number: int
    year: int

    def print(self):
      print('Улица -', self.street, 'Номер дома -', self.number, 'Год постройки =', self.year)
    def values(self):
      return self.microdistrict, self.street, self.number, self.year

def is_file_empty(file_path):
    #если размер файла = 0 байт, то функция вернет 0
    return os.path.exists(file_path) and os.stat(file_path).st_size == 0

def read(buildings):
    with open('data.csv', encoding="cp1251", errors='ignore', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            building = Building(row['microdistrict'], row['street'], int(row['number']), int(row['year']))
            buildings.append(building)
        return buildings

def write(building):
  with open('pe/data.csv', encoding="cp1251", errors='ignore', newline='', mode="a") as csvfile:
        print(building[0].keys())
        writer = csv.DictWriter(csvfile, fieldnames=building[0].keys());
        if is_file_empty('pe/data.csv'):
          print('Файл был пустой')
          writer.writeheader()
        writer.writerows(building)

def myFunc(e):
  return int(e[3])#год

def print_table(table, headers, temp_microdisctrict):
    print('\033[1mМикрорайон:\033[0m', temp_microdisctrict)
    if table.__len__() == 0:
      print('Таких домов нет')
    else:
      print('Таблица домов')
      table.sort(key=myFunc)
      print(tabulate(table, headers, tablefmt="grid"))

def print_out(buildings, year):
    buildings.sort(key=operator.attrgetter('microdistrict'))
    iterator = 0
    temp_microdisctrict = buildings[0].microdistrict
    table = []
    headers = ['Номер дома', 'Микрорайон', 'Улица','Год постройки']
    print('Сортировка списка домов по микрорайонам:')
    for building in buildings:
        if temp_microdisctrict != building.microdistrict:
          print_table(table, headers,temp_microdisctrict)
          table = []
          temp_microdisctrict = building.microdistrict
        if(building.year <= year) | (year == -1):
          table.append([building.number, building.microdistrict, building.street, building.year])
    #обход для конца цикла
    print_table(table, headers,temp_microdisctrict)
    
print('1 - Показать список домов')
print('2 - Добавить новый дом')
print('3 - Вывести список домов по микрорайонам и отсортировать')
buildings = []
buildings = read(buildings)
choice = int(input('Ваш выбор - '))
if choice == 1:
  print_out(buildings, -1)
elif choice == 2:
  try:
    print('\033[1mДобавление дома:\033[0m')
    microdistrict = (str) (input('Введите название микрорайона: '))
    number = (int) (input('Введите номер дома: '))
    street = (str) (input('Введите улицу: '))
    year = (int) (input('Введите год постройки: '))
    building = [{
      'microdistrict': microdistrict,
      'street':street,
      'number':number,
      'year':year
    }]
    write(building)
    print('Сведения о доме успешно сохранены в файле')
  except:
    print('Произошла непредвиденная ошибка')
elif choice == 3:
  year = int(input('Введите год. Будут показаны все дома, построенные раньше этого года или в этом году: '))
  print_out(buildings, year)