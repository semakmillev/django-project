# Кинотеатр

## Список методов:

Формат всех ответов, с корректной обработкой запроса следующий:

```{res:<data>,'error':<текст ошибки>'}```

В случае отсутствия ошибки error - пустой

### ```http://<hostname>/cinema/films```:

**get**: Возвращает список фильмов, зарегистрированных в кинотеатре

Пример ответа: ```[{"id": 1, "film_name": "It", "film_length": 100, "price": 50}]```

### ```http://<hostname>/cinema/films/<int:id>'```:

**get**: Возвращает информацию о фильме 

Пример ответа: ```[{"id": 1, "film_name": "It", "film_length": 100, "price": 50}]```

### ```http://<hostname>/cinema/auth'```:

**post**: Авторизирует пользователя 

Пример запроса:```{"email":"semakmillev@gmail.com", "password":"12345"}```

Пример ответа: ```{
   "name": "semak",
   "token": "bla-bla-bla",
   "user_id": 2
}```
токен - токен JWT

### ```http://<hostname>/cinema/create'```:

**post**: Регистрирует пользователя 

Пример запроса:```{
   "email":"test@test.ru",
   "password": "qwerty",
   "user_name":"my_test"
}```

Пример ответа: ```{
   "res":    {
      "id": 5,
      "email": "test@test.ru",
      "user_name": "my_test"
   },
   "error": ""
}```


### ```http://<hostname>/cinema/film'```:

**[post]**: Создает фильм/изменяет его



Пример запроса:```{
   "film_name": "The Matrix",
   "film_length": "83",
   "price": "10"
}```
для изменения нужно передать поле id

Пример ответа: ```{
   "res":    {
      "id": 3,
      "film_name": "The Matrix",
      "film_length": 83,
      "price": 10
   },
   "error": ""
}```


### ```http://<hostname>/cinema/schedule'```:

**[post]**: Создает расписание фильма/изменяет его



Пример запроса:```{
   "film_id": 3,
   "hall_id": 1,
   "film_start": "2019-12-01T10:00:00Z"
}```
для изменения нужно передать поле id


Пример ответа: ```{
   "res": "",
   "error": "Hall is busy!"
}```
Успешный ответ: ```{
   "res": {"id": 41},
   "error": ""
}```

### ```http://<hostname>/cinema/schedules'```:

**[get]**: Получить список расписаний.

Пример ответа:
{
   "res":    {
      "2":       {
         "hall_name": "Asia",
         "films": [         {
            "film_id": 1,
            "film_name": "It",
            "film_price": 50,
            "film_start": "2019-07-12T12:00:00Z"
         }]
      },
      "1":       {
         "hall_name": "Europe",
         "films":          [
                        {
               "film_id": 3,
               "film_name": "The Matrix",
               "film_price": 10,
               "film_start": "2019-12-01T10:00:00Z"
            },
                        {
               "film_id": 3,
               "film_name": "The Matrix",
               "film_price": 10,
               "film_start": "2019-11-01T10:00:00Z"
            }
         ]
      }
   },
   "error": ""
}

### ```http://<hostname>/cinema/booking```:

**[post]**: Бронирование билета


Пример запроса:```{"schedule_id":37,
"row":1,
"place":2
}```
row - ряд
place - место

Пример ответа:```{
   "res": {"booking_id": 19},
   "error": ""
}```
Пример ошибки:```{
   "res": "",
   "error": "Place is busy!"
}```


### ```http://<hostname>/cinema/pay```:

**[post]**: Оплата билета


Пример запроса:```{"booking_id": 18}```

Пример ответа:```{
   "res": "payed",
   "error": ""}```

### ```http://<hostname>/cinema/places?schedule=<schedule_id>'```:

**[get]**: Получить список мест по сеансу.
    
{"res": [
      {
      "id": 1,
      "places":       [0,1,0,0,0,0,0]
   },
      {
      "id": 2,
      "places":       [0,0,0,0,0,0,0]
   },
      {
      "id": 3,
      "places":       [0,0,0,0,0,0,0]
   }
]}    

0 - свободно, 1 - занято

### ```http://<hostname>/cinema/get_user_bookings?user_id=<user_id>'```:

**[get]**: Получить список мест по сеансу.

если user_id не передан, то возвращаем по текущему пользователю
если роль user - admin - можно смотреть всех, если нет - только себя

Пример ответа:```{
   "res":    [
            {
         "booking_id": 18,
         "place_id": "R1P2",
         "schedule_id": 38,
         "status": "PAID"
      },
            {
         "booking_id": 19,
         "place_id": "R1P5",
         "schedule_id": 38,
         "status": "CREATED"
      }
   ],
   "error": ""
}```
## Запуск

docker_build.sh - для сборки
run.sh - для запуска