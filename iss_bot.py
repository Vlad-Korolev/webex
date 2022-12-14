# Запросы
import requests
# Преобразование
import json
# Работа со временем
import time
# Использования файла для хранения параметров
from configparser import ConfigParser 
# Получение даты и времени
import datetime


# Объявляем переменную, необходимую для работы ConfigParser
config = ConfigParser() 
# Считываем данные с файла конфигурации
config.read('config.ini')
# Объявляем переменную для подсчета номера сообщения в логе
log_count = 0


##############     Функции     ##############
def webexCreateMessage(message):
    '''
    Функция "webexCreateMessage()" отправляет сообщения в чат комнаты Webex
        Ф-ция ожидает в качестве аргумента сообщения webexCreateMessage(message), необходимое для отправки
    '''

    # Заголовок запроса
    HTTPHeaders = { 
          "Authorization": AccessTokenWebex,
          "Content-Type": "application/json"
    }
    # Параметры запроса
    PostData = {
          "roomId": roomIdToGetMessages,
          "text": message
    }
    # Запрос (post)
    r = requests.post(
                       config.get('WEBEX', 'webexUrlMessagesPost'), 
                       data = json.dumps(PostData), 
                       headers = HTTPHeaders
                     )

def webexCreateRoom(title):
    '''
    Функция "webexCreateRoom(title)" создает новую комнату Webex
        Ф-ция ожидает в качетстве аргумента имя новой комнаты
    '''

    # Параметры для запроса на создание новой комнаты
    GetParameters = {
                      "title": title
                    }
    # Заголовок запроса на создание новой комнаты
    GetHeaders =    {
                      "Authorization": AccessTokenWebex,
                      "Content-Type": "application/json"
                    }
    # Запрос(post) создание новой комнаты Webex
    r = requests.post( 
                       config.get('WEBEX', 'webexurlcreateroom'), 
                       headers = GetHeaders,
                       json = GetParameters
                     )
    
    # При возвращении кода отличного от "200" скрипт в консоль выводит сообщения об ошибке
    if not r.status_code == 200:
        raise Exception("Некорректный запрос к Webex Teams API (Создание комнаты). Статус код: {}. : {}".format(r.status_code, r.text))
    

def webexShowRooms():
    '''
    Функция "webexShowRooms()" проверят комнаты текущего пользователя, выводит их список, ждет выбора одной из комнат
        Ф-ция возвращает "return(roomIdToGetMessages)" ID выбранной комнаты.
    '''

    # Запрос к API Webex для получения списка комнат
    r = requests.get(   config.get('WEBEX', 'webexUrlRooms'),
                        headers = {"Authorization": AccessTokenWebex}
                    )

    # При возвращении кода отличного от "200" скрипт в консоль выводит сообщения об ошибке
    if not r.status_code == 200:
        raise Exception("Некорректный запрос к Webex Teams API (Просмотр и выбор комнаты). Статус код: {}. Сообщение: {}".format(r.status_code, r.text))

    # Выводим в консоль список комнат пользователя
    print("\nКомнаты:")
    rooms = r.json()["items"]

    for i in range(len(rooms)):
        print(i, '-', rooms[i]['title'])
    else:
        print('Всего комнат: ' + str(len(rooms)))
        print('Для создания комнаты выберите номер:', len(rooms))

    # Возвращаем список комнат
    return(rooms)
    

def consoleMessage(titel, data):
    '''
    Функция "consoleMessage(titel, data)" печатае в консоле сообщение.
        Ф-ция ожидает в качестве аргумента "title" - название и "data" - данные для вывода
    '''
    # Шаблон для вывода сообщений в консоль
    s1 = '**********************************************************'
    s2 = titel
    s3 = '**********************************************************'
    s4 = json.dumps(data, indent=4)
    s5 = '=========================================================='
    s_cancat = f'\n{s1}\n{s2}\n{s3}\n{s4}\n{s5}'
    print(s_cancat)

    


##############     Часть 1      ##############
# Webex авторизация
# Токен авторизации по умолчанию берется из файла конфигурации (действует 12 часов)
AccessTokenWebex = config.get('WEBEX', 'AccessTokenWebex')

print ('Используется Токен Авторизации по умолчанию')

# Возможность ввести новый Токен
choice = input("Ввести новый Токен Авторизации (y/n) ")
if choice == "Y" or choice == "y":
    # После ввода нового токена добавляем его в файл конфигурации
    AccessTokenWebex = input("Новый Токен Авторизации: ")
    config.set('WEBEX', 'AccessTokenWebex',  AccessTokenWebex)
    config.write(open('config.ini', "w"))

AccessTokenWebex = "Bearer " + AccessTokenWebex



##############     Часть 2      ##############
# Webex просмотр комнат пользователя
# Вызываем ф-цию для просмотра комнат webex (выбора или удаления) 
# Пользователь выбирает комнату из списка (в которой чат будет "прослушиваться")

rooms = webexShowRooms()

while True:
    roomNumberToSearch = input("\nВыберите номер комнаты для работы скрипта: ") 

    # Обработчик исключений, првоеряем правильность ввода ЦИФРЫ номера комнаты
    try:
        roomNumberToSearch = int(roomNumberToSearch)

        # Проверяем на парвильность выбора комнаты (существует такой номер комнаты или нет)
        if  roomNumberToSearch >= 0 and roomNumberToSearch < len(rooms):
            # Сохраняем в переменную id выбранной команты (id нужен для запросов)
            roomIdToGetMessages = rooms[roomNumberToSearch]["id"]
            roomTitleToGetMessages = rooms[roomNumberToSearch]["title"]
            print("Выбрана комната : " + roomTitleToGetMessages)
            print("Id комнаты : " + roomIdToGetMessages + '\n')
            break

        # Создание новой комнаты
        elif roomNumberToSearch == len(rooms):
            print('Вы выбрали создание новой комнаты')
            webexCreateRoom(input('Введите имя новой комнаты: '))
            # Вызываем ф-цию для вывода нового списка комнат (после создания очередной комнаты)
            rooms = webexShowRooms()

        # Вариант с несуществующим номером комнаты
        else:
            print("Ошибка, нету такого номера комнаты")
            print("Введите номер команты повторно...")

    # Обрабатываем исключение с неверным воодом (например: буквы)        
    except ValueError:
        print("Введено недопустимое значение.")
        print("Необходимо ввести цифру номера комнаты.") 




##############     Часть 3     ##############
# Скрипт "прсолушивает" чат выбранной комнаты Webex
while True:
    # выполнятсья каждую секунду
    time.sleep(1)

    # Параметры для запроса на наличие сообщений в чате комнаты
    GetParameters = {
                            "roomId": roomIdToGetMessages,
                            "max": 1 # Макисмальное число сообщений
                    }
                    
    # Запрос (GET) в комнату Webex для получения списка сообщений
    r = requests.get(config.get('WEBEX', 'webexUrlMessages'), 
                         params = GetParameters, 
                         headers = {"Authorization": AccessTokenWebex}
                    )

    # При возвращении кода отличного от "200" скрипт в консоль выводит сообщения об ошибке
    if not r.status_code == 200:
        raise Exception("Некорректный запрос к Webex Teams API. Статус код: {}. : {}".format(r.status_code, r.text))
    
    # Преобразуем полученный ответ к удробному отображению
    json_data = r.json()

    # Условие, вернул ли запрос сообщение (или их нет)
    if len(json_data["items"]) == 0:
        raise Exception("В комнате нету ни одного сообщения")
    
    # Переменная для хранения всего ответа
    messages = json_data["items"]
    # Текст сообщения
    message = messages[0]["text"]
    # ID пользователя оставившего сообщение
    personID = messages[0]["personId"] 

    # Параметры для запроса (описание пользователя оставившего последнее сообщение)
    GetParameters = {
                            "id": personID,
                            "max": 1 
                    }
                    
    # Запрос (GET) для получения информации о пользователе по его Id (полученному из последнего сообщения)
    r = requests.get(config.get('WEBEX', 'webexurlpeople'), 
                         params = GetParameters, 
                         headers = {"Authorization": AccessTokenWebex}
                    )

    # При возвращении кода отличного от "200" скрипт в консоль выводит сообщения об ошибке
    if not r.status_code == 200:
        raise Exception("Некорректный запрос к Webex Teams API. Статус код: {}. Сообщение: {}".format(r.status_code, r.text))
    
    # Преобразуем полученный ответ к удобному отображению
    json_data = r.json()
    # Переменная для хранения всего ответа
    people = json_data['items'] 
    # Переменная для хранения имени пользователя
    people_name = people[0]['displayName']

    # Выводим в консоль последнее сообщение в чате комнаты
    
    # Переменная для хранения текущей даты (времени)
    now = datetime.datetime.now()
    # Увеличиваем номер сообщений в логе
    log_count += 1
    # Строка с сообщением пользователя (выводим в консоль)
    last_message  = f'[{log_count}][{now.strftime("%d-%m-%Y %H:%M:%S")}] от [{people_name}][сообщение] : \n{message}'
    print(last_message)



    ##############     Часть 4     ##############
    # Скрипт "прсолушивает" чат и находит совпадения сообщений
    
    if (message.lower()).find("/help") == 0:

        s1 = '***************************************'
        s2 = '/ISS -  Просмотр местоположения МКС'
        s3 = '/ISS_crew - Просмотр экипажа на МКС'

        responseMessage = f'{s1}\n{s2}\n{s3}\n'
        # Ф-ция для запроса (post) на печать сообщения в чат
        webexCreateMessage(responseMessage)

    elif (message.lower()).find("/iss_crew") == 0:

        # Выполняем запрос к "open-notify" для получения списка экпижа на МКС
        r = requests.get(config.get('ISS', 'issUrlCrew'))
        json_data = r.json()['people']

        # Выводим в консоль ответ на запрос в удобном для чтения виде
        # Вызываем ф-цию для вывода сообщений в консоль
        consoleMessage('Запрос /ISS_crew (список астронавтов)', json_data)

        # Проходим циклом по полученным сведениям и записываем всех членов экипажа в строку
        crew = ''
        for crew_numb in range(len(json_data)):
            crew = crew + json_data[crew_numb]['name'] + '\n'

        # Ф-ция для запроса (post) на печать сообщения в чат
        webexCreateMessage('\nСколько людей сейчас находится в космосе?\n')
        webexCreateMessage(crew)

    elif (message.lower()).find("/iss") == 0:

        # Ф-ция для запроса (post) на печать сообщения в чат
        webexCreateMessage('\nМКС движется со скоростью, близкой к 28 000 км / ч, поэтому ее местоположение меняется очень быстро! Где он находится прямо сейчас?')

        # Выполняем запрос к "open-notify" для получения координат местоположения МКС в текущий момент
        r = requests.get(config.get('ISS', 'issUrl'))

        # Преобразуем полученный ответ к удобному отображению
        json_data = r.json()['iss_position']

        # Выводим в консоль ответ на запрос в удобном для чтения виде
        # Вызываем ф-цию для вывода сообщений в консоль
        consoleMessage('Запрос /ISS (получение координат)', json_data)

        # Записываем в переменную полученные координаты МКС
        coordinates_iss = f"{json_data['latitude']},{json_data['longitude']}"

        # Выполняем запрос к "OPENCAGEDATA" по полученным координатам МКС, вычисляем над какой она страной, городом, улицей (геокодинг)
        GetParameters = {
                              "key": config.get('OPENCAGEDATA', 'accesstokenopencagedata'), # Токен доступа
                                "q": coordinates_iss, # Координаты МКС
                         "language": 'ru' # Язык ответа
                        }
                                
        r = requests.get(config.get('OPENCAGEDATA', 'opencagedataurl'), 
                         params = GetParameters, 
                        )

        # Преобразуем полученный ответ к удобному отображению
        json_data = r.json()

        # Выводим в консоль ответ на запрос в удобном для чтения виде
        # Вызываем ф-цию для вывода сообщений в консоль
        consoleMessage('Запрос /ISS (получение расположения на местности)', json_data)

        # Записываем в переменную полученный ответ
        result = json_data['results'][0]
        # Записываем в переменную категорию (от нее зависят возвращаемые данные)
        opencagedata_category = result['components']['_category']
        opencagedata_osm   = result['annotations']['OSM']['url']

        # Выстраиваем сообщения ответа в зависимости от категории "opencagedata_category"
        if opencagedata_category != 'natural/water':
            # Словарь для хранения элементов необходимых для вывода (инф. о стране, городе, области и т.п.)
            showInf = dict() 

            # В цикле перебираем весь полученный ответ (ветка 'components')
            for key, value in result['components'].items():            

                # Проходим по заранее известным словам, если в ответе API (ветка 'components') есть такие, то формируем из них слвоарь
                if key == 'continent':
                    showInf['Континент'] = value 
                elif key == 'country':
                    showInf['Страна'] = value 
                elif key == 'county':
                    showInf['Округ'] = value                 
                elif key ==  'county':
                    showInf['Округ'] = value                                 
                elif key == 'state':
                    showInf['Область'] = value                                 
                elif key == 'city':
                    showInf['Город'] = value                                                 
                elif key == 'region':
                    showInf['Регион'] = value

            # Случай, когда в ответе API не нашлось ни одного совпадения с ключевыми словами (словарь "showInf" пуст)  
            if len(showInf) == 0:
                showInf['Ошибка'] ='Словарь с элементами для вывода не сформирован, не нашлось ни одного совпадения.'

            # Подгатавливаем сообщения для отправки в чат комнаты
            s1 = f'Координаты МКС: {coordinates_iss}'
            s2 = '***************************************'
            responseMessage = f'\n{s1}\n{s2}'

            # В цикле проходим по составленному словарю "showInf" добавляем все элементы из него в сообщения для отправки в чат комнаты
            for key, value in showInf.items():
                string = f'\n{key}: {value}'
                responseMessage = responseMessage + string
            
            # Добавляем к сообщению последнюю строку с выводом ссылки на карту (по полученным координатам)
            sFinal = f'\n\nПросмотр на карте: \n{opencagedata_osm}'
            responseMessage += sFinal

            # Ф-ция для запроса (post) на печать сообщения в чат
            webexCreateMessage(responseMessage)
            

        elif opencagedata_category == 'natural/water':

            # Записываем в переменные нужные нам значения
            opencagedata_water = result['components']['body_of_water']
           

            # Подгатавливаем сообщения для отправки в чат комнаты
            s1 = f'Координаты МКС: {coordinates_iss}'
            s2 = '***************************************'
            s3 = f'Нейтралные территории (вода)'
            s4 = f'Местоположение: { opencagedata_water}'
            s5 = f'\nПросмотр на карте: \n{opencagedata_osm}'

            responseMessage = f'\n{s1}\n{s2}\n{s3}\n{s4}\n{s5}\n'
            # Ф-ция для запроса (post) на печать сообщения в чат
            webexCreateMessage(responseMessage)
            
        else:
            # Заглушка (проработать вариант с ошибкой)
            pass



            












        



    


