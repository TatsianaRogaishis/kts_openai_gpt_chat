## Описание endpoint'ов бекенд сервиса

По [ссылке](http://localhost:8000/docs) можно найти краткое описание и протестировать их

### [Начальная страница](http://localhost:8000/)
Endpoint: /  
GET запрос  
Загрузка начальной страницы для работы с сервисом  
Ответ: файл html  

### [Начальная страница для вебсокета](http://localhost:8000/ws)
Endpoint: /ws  
GET запрос  
Загрузка начальной страницы для работы с сервисом через вебсокет  
Ответ: файл html  

### [Отправка сообщения в ChatGPT](http://localhost:8000/api/v1/ask)
Endpoint: /api/v1/ask  
POST запрос  
Параметры: json {"user": "user_name", "message": "message text"}  
Отправка сообщения в ChatGPT и получение ответа либо ошибки от него. Также происходит запись всех сообщений в БД.  
Ответ: json {"user": "AI", "message": "answer text", "datetime": "08.08.2024 18:18:18", "id": 8}  
Ответ при ошибке: json {"user": "Error", "message": "error details"}  

### [Получение истории сообщений](http://localhost:8000/api/v1/get/history)
Endpoint: /api/v1/get/history  
GET запрос  
Параметры: skip=0 (начальный номер записей, для пагинации), limit=50 (максимальное количество записей)  
Запрос на получение записей истории сообщений из БД. Возвращает список записей либо пустой список.  
Ответ: json [{"user": "AI", "message": "answer text", "datetime": "08.08.2024 18:18:18", "id": 8}, {"user": "user", "message": "text", "datetime": "08.08.2024 15:15:15", "id": 7}]

### [Канал общения с ChatGPT по вебсокету](http://localhost:8000/api/v1/ask/stream)
Endpoint: /api/v1/ask/stream  
Websocket channel  
Параметры: json {"user": "user_name", "message": "message text"}  
Отправка сообщения в ChatGPT по вебсокету и получение ответа либо ошибки от него. Также происходит запись всех сообщений в БД.  
Ответ: json {"user": "AI", "message": "answer text", "datetime": "08.08.2024 18:18:18", "id": 8}  
Ответ при ошибке: json {"user": "Error", "message": "error details"}  