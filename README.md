[Задачи]
- [вып]Вывод в консоль весь ответ в удобном виде при успешном запросе к API
- [вып]При удачно запросе к OpenGeData необходимо произвести выборку по наличию элементов для вывода, после вывести все что имеются (отличаются исходя из местоположения)
- Log_file (Запись ошибок в log)
- Уменьшение ссылки (использование API?) на просмотр карты
- Ф-ция на удаление комнаты (ведь есть на создание, а нету на удаление)

[Основные возможности]
-Хранит все нужные данные (токены авторизации, ссылки) в файле конфига и парсит их оттуда (дял безопасности, удобства);

-Спрашивает пользователя будет ли он использовать текущий токен из файла или введет новый.
Перезаписывает в файл конфиг новый Токен при необходимости (добавление нового токена взамен старого);

-С помощью API webex получает список комнат пользователя, выводит в консоль, предоставляет выбор комнаты, есть возможность создание новой комнаты из консоли;

-Просит пользователя выбрать одной из комнат скрипт будет "прослушивать" чат;

-С помощью API webex скрипт подключается к комнате и каждую секунду получает последнее сообщение чата, ищет совпадения по ключевым словам (/Help, /ISS, /ISS_crew).
	При нахождении совпадения по ключевым словам :
    - /Help - использует API(webex) отправляет сообщения в чат с текстом справки.
    - /ISS - использует API (open-notify) для нахождения текущего местоположения ISS (координат), после получения координат использует API (OpencaGeData) для геодекодирования, по координатам вычисляя страну, город, улицу над которой пролетает ISS в данный момент (отправляет полученные данные в чат).
    - /ISS_crew - использует API (open-notify) для получения текущего списка экипажа ISS, отправляет в чат сообщение о экипаже.


