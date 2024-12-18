from models import Car, CarFullInfo, CarStatus, Model, ModelSaleStats, Sale
from datetime import datetime
from decimal import Decimal


class CarService:
    def __init__(self, root_directory_path: str) -> None:
        self.root_directory_path = root_directory_path

    # Задание 1. Сохранение автомобилей и моделей
    def add_model(self, model: Model) -> Model:
        # Запишем модель в файл(в конец)
        with open(self.root_directory_path + 'models.txt', 'a') as f:
            f.write(
                ';'.join([str(value) for value in model.model_dump().values()]).ljust(500) + '\n')
        # запишем модель в индекс
        with open(self.root_directory_path + 'models_index.txt', 'a+') as f:
            f.seek(0)
            entries = f.readlines()            # список из всех записей
            # последняя запись(если записей нет, то None)
            last_entry = None if not entries else entries[-1]
            next_entry_id = 1 if not last_entry else int(           # id следующей записи
                last_entry[:last_entry.find(';')]) + 1
            f.seek(0, 2)        # курсор в конец файла
            f.write(f'{next_entry_id};{model.index()}'.ljust(
                500) + '\n')   # новая запись в индексе
        return model
    # Задание 1. Сохранение автомобилей и моделей

    def add_car(self, car: Car) -> Car:
        # Запишем машину в файл(в конец)
        with open(self.root_directory_path + 'cars.txt', 'a') as f:
            f.write(
                ';'.join([str(value) for value in car.model_dump().values()]).ljust(500) + '\n')
        # запишем машину в индекс
        with open(self.root_directory_path + 'cars_index.txt', 'a+') as f:
            f.seek(0)
            entries = f.readlines()     # список из всех записей
            # последняя запись(если записей нет, то None)
            last_entry = None if not entries else entries[-1]
            next_entry_id = 1 if not last_entry else int(last_entry[:last_entry.find(
                ';')]) + 1
            f.seek(0, 2)        # курсор в конец файла
            f.write(f'{next_entry_id};{car.index()}'.ljust(
                500) + '\n')         # новая запись в индексе
        return Car
    # Задание 2. Сохранение продаж.

    def sell_car(self, sale: Sale) -> Car:
        # Запишем продажу в файл(в конец)
        with open(self.root_directory_path + 'sales.txt', 'a') as f:
            f.write(';'.join(
                [str(value) for value in sale.model_dump().values()]).ljust(500) + '\n')
        # Запишем продажу в индекс
        with open(self.root_directory_path + 'sales_index.txt', 'a+') as f:
            f.seek(0)
            entries = f.readlines()
            last_entry = None if not entries else entries[-1]
            next_entry_id = 1 if not last_entry else int(last_entry[:last_entry.find(
                ';')]) + 1
            f.seek(0, 2)
            f.write(f'{next_entry_id};{sale.index()}'.ljust(500) + '\n')
        # поменяем статус купленной машины(для начала ее нужно найти в индексе)
        line_number = None
        with open(self.root_directory_path + 'cars_index.txt', 'r') as f:
            entries = f.readlines()         # считаем все записи
            # убрем в конце переносы строк
            entries = list(map(str.strip, entries))
            for entry in entries:
                car_vin = entry[entry.find(';') + 1:]
                if car_vin == sale.car_vin:
                    line_number = int(entry[:entry.find(';')])
                    break
            # зная, номер записи в cars, обновим стасус на "sold"
            if line_number:
                with open(self.root_directory_path + 'cars.txt', 'r+') as f:
                    f.seek((line_number - 1) * (502))
                    # уберем в конце перенос строк и пробелы
                    entry_to_update = f.readline().strip()
                    lst = entry_to_update.split(';')
                    lst[-1] = 'sold'
                    entry_to_update = ';'.join(lst).ljust(
                        500) + '\n'   # 'собираем' строку обратно
                    # ставим курсор в нужно позицию
                    f.seek((line_number - 1) * (502))
                    # записываем измененную строку
                    f.write(entry_to_update)
    # Задание 3. Доступные к продаже

    def get_cars(self, status: CarStatus) -> list[Car]:
        with open(self.root_directory_path + 'cars.txt', 'r') as f:
            result = []
            entries = f.readlines()
            # убрем в конце переносы строк
            entries = list(map(str.strip, entries))
            for entry in entries:
                lst = entry.split(';')
                if lst[-1] == 'available':
                    result.append(
                        Car(vin=lst[0], model=lst[1], price=lst[2], date_start=lst[3], status=lst[4]))
        return result

    # Задание 4. Детальная информация
    def get_car_info(self, vin: str) -> CarFullInfo | None:
        line_number_car = None
        # найдем номер строки cars в индексе
        with open(self.root_directory_path + 'cars_index.txt', 'r') as f:
            entries = f.readlines()         # считаем все записи
            # убрем в конце переносы строк
            entries = list(map(str.strip, entries))
            for entry in entries:
                car_vin = entry[entry.find(';') + 1:]
                if car_vin == vin:
                    line_number_car = int(entry[:entry.find(';')])
                    break
        if line_number_car:
            with open(self.root_directory_path + 'cars.txt', 'r+') as f:
                f.seek((line_number_car - 1) * (502))
                lst_car = f.readline().strip().split(';')      # список с информацией о машине
                model = lst_car[1]                  # модель авто
                status = lst_car[-1]
            with open(self.root_directory_path + 'models_index.txt', 'r') as f:
                entries = f.readlines()         # считаем все записи
                # убрем в конце переносы строк
                entries = list(map(str.strip, entries))
                for entry in entries:
                    model_index = entry[entry.find(';') + 1:]
                    if model == model_index:
                        line_number_model = int(entry[:entry.find(';')])
                        break
            with open(self.root_directory_path + 'models.txt', 'r+') as f:
                f.seek((line_number_model - 1) * (502))
                lst_model = f.readline().strip().split(';')      # список с информацией о машине
            if status == 'sold':
                with open(self.root_directory_path + 'sales.txt', 'r') as f:
                    entries = f.readlines()
                    for entry in entries:
                        entry = entry.strip()
                        entry = entry.split(';')
                        if vin == entry[1]:
                            sales_date = entry[2]
                            cost = entry[-1]
            else:
                sales_date = cost = None
        else:
            return None     # если такого vin в БД нет, возвращаме None
        return CarFullInfo(vin=vin, car_model_name=lst_model[1], car_model_brand=lst_model[2], price=lst_car[2],
                           date_start=lst_car[-2], status=lst_car[-1], sales_date=sales_date, sales_cost=cost)

    # Задание 5. Обновление ключевого поля

    def update_vin(self, vin: str, new_vin: str) -> Car:
        line_number = None
        # найдем номер строки cars в индексе и изменим vin в самом индексе
        with open(self.root_directory_path + 'cars_index.txt', 'r+') as f:
            entries = f.readlines()         # считаем все записи
            # убрем в конце переносы строк
            entries = list(map(str.strip, entries))
            for entry in entries:
                car_vin = entry[entry.find(';') + 1:]
                if car_vin == vin:
                    line_number = int(entry[:entry.find(';')])
                    # поставим курсор на нужную позицию
                    f.seek((line_number - 1) * (502))
                    f.write(f'{line_number};{new_vin}'.ljust(
                        500) + '\n')         # перепишем строку новым vin
                    break
        # если такой vin есть в БД, то изменим его и в cars
        if line_number:
            with open(self.root_directory_path + 'cars.txt', 'r+') as f:
                f.seek((line_number - 1) * (502))
                lst_car = f.readline().strip().split(';')      # список с информацией о машине
                lst_car[0] = new_vin            # запишем в список new_vin
                # поставим курсор на правильнцю позицию
                f.seek((line_number - 1) * (502))
                # запишем в файл новую строку
                f.write(';'.join(lst_car).ljust(500) + '\n')
        else:
            return None
        return Car

    # Задание 6. Удаление продажи

    def revert_sale(self, sales_number: str) -> Car:
        vin = sales_number[sales_number.find('#')+1:]       # получим vin авто
        line_number_car_index = None            # номер строк в car
        # найдем номер строки cars в индексе
        with open(self.root_directory_path + 'cars_index.txt', 'r') as f:
            entries = f.readlines()         # считаем все записи
            # убрем в конце переносы строк
            entries = list(map(str.strip, entries))
            for entry in entries:
                car_vin = entry[entry.find(';') + 1:]
                if car_vin == vin:
                    line_number_car_index = int(entry[:entry.find(';')])
                    break
        # если такой vin есть в БД
        if line_number_car_index:
            # откроем файл cars и изменим статус авто
            with open(self.root_directory_path + 'cars.txt', 'r+') as f:
                f.seek((line_number_car_index - 1) * (502))
                lst_car = f.readline().strip().split(';')      # список с информацией о машине
                lst_car[-1] = "available"           # меняем статус
                # поставим курсор на правильнцю позицию
                f.seek((line_number_car_index - 1) * (502))
                # запишем измененную строку
                f.write(';'.join(lst_car).ljust(500) + '\n')
        # номер строки с нужной записью и временны номер записи
        line_number_sale = cur_line_number_sale = None
        # переменная флаг(надо сместить строки выше данной или нет)
        to_shift = False
        # изменяем индекс sales
        with open(self.root_directory_path + 'sales_index.txt', 'r+') as f:
            entries = f.readlines()         # считаем все записи
            # убрем в конце переносы строк
            entries = list(map(str.strip, entries))
            for entry in entries:
                car_vin = entry[entry.find(';') + 1:]
                if car_vin == vin:
                    line_number_sale = cur_line_number_sale = int(
                        entry[:entry.find(';')])
                    # ставим курсор в позицию, куда будет записана новая строка
                    f.seek((cur_line_number_sale - 1) * (502))
                    to_shift = True
                elif to_shift:
                    # нужная строка найдена, теперь надо сместить строки, которые находятся ниже, вверх на 1 позицию
                    lst = entry.split(';')
                    # меняем номер строки на 1 меньше, чем был(т.е cur_line_number_sale)
                    lst[0] = cur_line_number_sale
                    f.write(';'.join(lst))              # записываем из
                    cur_line_number_sale += 1           # берем следующую строку
                    # перемещаем курсор выше на 1 строку
                    f.seek((cur_line_number_sale - 1) * (502))
        # изменим sales
        with open(self.root_directory_path + 'sales.txt', 'r+') as f:
            num_entries_to_move = cur_line_number_sale - line_number_sale - \
                1           # количество записей, которые нужно сместить
            while num_entries_to_move > 0:
                f.seek(line_number_sale * (502))        # следующая строка
                line = f.readline()             # считаем ее
                # запишем ее на место старой
                f.seek((line_number_sale - 1) * (502))
                f.write(line)                   # запишем ее
                line_number_sale += 1           # берем следующую строку
                num_entries_to_move -= 1        # количество строк, которые надо переместить
        return Car

    # Задание 7. Самые продаваемые модели
    def top_models_by_sales(self) -> list[ModelSaleStats]:
        sales_lst: list[dict] = []         # список продаж
        line_number_car_index = model_number = line_number_model_index = None
        model_in_sales_lst = False      # есть модель в списке продаж или нет
        # откроем индекс и пройлемся циклом по всем записям
        with open(self.root_directory_path + 'sales_index.txt', 'r') as f1:
            entries = f1.readlines()
            for entry in entries:
                entry = entry.strip()
                vin = entry[entry.find(';') + 1:]       # запомним vin
                # найдем номер записи cars в индексе
                with open(self.root_directory_path + 'cars_index.txt', 'r') as f:
                    lines = f.readlines()         # считаем все записи
                    # уберем в конце переносы строк и пробелы
                    lines = list(map(str.strip, lines))
                    for line in lines:
                        car_vin = line[line.find(';') + 1:]
                        if car_vin == vin:
                            line_number_car_index = int(line[:line.find(';')])
                            break
                # найдем запись в cars, зная номер строки
                with open(self.root_directory_path + 'cars.txt', 'r') as f:
                    f.seek((line_number_car_index - 1) * (502))
                    line = f.readline().strip()
                    lst = line.split(';')
                    model_number = lst[1]          
                    price = lst[2]
                # найдем в индексе запись по переменной model_number
                with open(self.root_directory_path + 'models_index.txt', 'r') as f:
                    lines = f.readlines()         # считаем все записи
                    # убрем в конце переносы строк
                    lines = list(map(str.strip, lines))
                    for line in lines:
                        model = line[line.find(';') + 1:]
                        if model_number == model:
                            line_number_model_index = int(
                                line[:line.find(';')])
                            break
                # зная line_number_model_index, найдем записб
                with open(self.root_directory_path + 'models.txt', 'r') as f:
                    f.seek((line_number_model_index - 1) * (502))
                    line = f.readline().strip()
                    lst = line.split(';')
                    name = lst[1]       # запишем names, brand
                    brand = lst[2]
                # проверим, есть ли наша модель в списке sales_lst
                for element in sales_lst:       
                    if element['car_model_name'] == name:
                        element['sales_count'] += 1     # модель есть - инкрементируем
                        model_in_sales_lst = True       # такая модель уже покупалась
                        break
                if not model_in_sales_lst:              # если модель не была найдена, то запишем новую запись в sales_lst
                    sales_lst.append(
                        {'vin': vin, 'price': price, 'car_model_name': name, 'brand': brand, 'sales_count': 1})
                model_in_sales_lst = False          # возвращаем флаг в исходное состояние
        sales_lst.sort(key=lambda sale: (
            sale['sales_count'], sale['price']), reverse=True)      # отсортируем список по 2 параметра
        sales_lst = sales_lst[:3]       # берем первые три элемента списка
        result: list[ModelSaleStats] = []       # результирующий список
        for sale in sales_lst:          # запишем модели в результирующий список
            result.append(ModelSaleStats(
                car_model_name=sale['car_model_name'], brand=sale['brand'], sales_number=sale['sales_count']))
        return result
