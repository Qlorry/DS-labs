## Вступ

Маємо три сервіса:

1. facade-service
1. logging-service
1. message-service

Всі три сервіса написано на Пайтон.  
Настроєно логування в консоль та файл. Вони мають типову архітектуру клас App для application level логіки та Impl для сервісної логіки  
Для першої лаби я не виншосив доменну логіку в окремий клас...

Взаємодія на основі HTTP протоколу згідно завдання

facade-service працює на порті 10000  
logging-service працює на порті 20000
message-service працює на порті 30000

## Приклад роботи

Перше повідомлення
![Alt text](screenshots/a.png?raw=true)

Друге повідомлення
![Alt text](screenshots/b.png?raw=true)

Запит GET
![Alt text](screenshots/c.png?raw=true)

__Логи сервіса__ logging-service

>  [logging-service][App][2023-02-17 19:38:35,373]: Initialized logging for logging-service  
>  [logging-service][App][2023-02-17 19:38:35,377]: Starting httpd at ('', 20000)  
>  [logging-service][Domain][2023-02-17 19:38:39,788]: POST request, message "This is first message!" logged with ID "ea2d548e-aee9-11ed-a869-08002704e8bc"  
>  127.0.0.1 - - [17/Feb/2023 19:38:39] "POST / HTTP/1.1" 200 -  
>  [logging-service][Domain][2023-02-17 19:38:39,824]: POST request, message "This is second message!" logged with ID "ea33a186-aee9-11ed-a869-08002704e8bc"  
>  127.0.0.1 - - [17/Feb/2023 19:38:39] "POST / HTTP/1.1" 200 -  
>  [logging-service][Domain][2023-02-17 19:38:39,854]: POST request 2 messages sent  
>  127.0.0.1 - - [17/Feb/2023 19:38:39] "GET / HTTP/1.1" 200 -  

__Логи сервіса__ facade-service

>  [facade-service][App][2023-02-17 19:38:32,523]: Initialized logging for facade-service  
>  [facade-service][App][2023-02-17 19:38:32,528]: Starting httpd at ('', 10000)  
>  [facade-service][Domain][2023-02-17 19:38:39,780]: POST request! With new message: This is first message!  
>  127.0.0.1 - - [17/Feb/2023 19:38:39] "POST / HTTP/1.1" 200 -  
>  [facade-service][Domain][2023-02-17 19:38:39,796]: Message writen with {'ID': 'ea2d548e-aee9-11ed-a869-08002704e8bc'}  
>  [facade-service][Domain][2023-02-17 19:38:39,821]: POST request! With new message: This is second message!  
>  127.0.0.1 - - [17/Feb/2023 19:38:39] "POST / HTTP/1.1" 200 -  
>  [facade-service][Domain][2023-02-17 19:38:39,831]: Message writen with {'ID': 'ea33a186-aee9-11ed-a869-08002704e8bc'}  
>  [facade-service][Domain][2023-02-17 19:38:39,850]: GET request!  
>  127.0.0.1 - - [17/Feb/2023 19:38:39] "GET / HTTP/1.1" 200 -  

__Логи сервіса__ message-service
> [message-service][App][2023-02-17 19:38:29,700]: Initialized logging for > message-service  
> [message-service][App][2023-02-17 19:38:29,703]: Starting httpd at ('', 30000)  
> [message-service][Domain][2023-02-17 19:38:39,794]: POST request  
> 127.0.0.1 - - [17/Feb/2023 19:38:39] "POST / HTTP/1.1" 200 -  
> [message-service][Domain][2023-02-17 19:38:39,829]: POST request  
> 127.0.0.1 - - [17/Feb/2023 19:38:39] "POST / HTTP/1.1" 200 -  
> [message-service][Domain][2023-02-17 19:38:39,859]: GET request  
> 127.0.0.1 - - [17/Feb/2023 19:38:39] "GET / HTTP/1.1" 200 -  
