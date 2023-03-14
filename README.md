## Lab 3 - Мікросервиси з використанням Hazelcast Distributed Map

### Огляд змін в сервісах
Маємо однакову структуру мікросервісів, 
- facade-service 
- logging-service
- message-service

З першої лабораторної в message-service змін не вносилось.  

Обновлено facade-service, за допомогою python бібліотеки asyncio я настроїв окремий луп для відправки повідомлень. Можна було б використати ThreadPool але враховуючи особливості багатопоточності в python я вирішив покластись на async функції.  
Також я виніс логіку взаємодії з нашими бекендами в FacadeDomain. 
І створив клас AddressHelper щоб відокремити логіку менеджменту каналів бекендів. Зараз цей клас отримує адреси з аргументів сервісу. Він відповідальний за розподіл нагрузки між logging сервісами(звичайний раунд робін).

І звичайно великих змін зазанав сервіс logging-service. Він отримав підтримку Hazelcast. В настройках Hazelcast клієнта має одну ноду яка повинна мати порт як в logging-service + 1000.
Запуск цієї ноди виконується в класі LoggingApp, як і зупинка при сигналах SIGABRT SIGINT SIGKILL.

### Демонстрація роботи

- Разом з запуском logging-service запускається новий екземпляр Hazelcast (або клієнт Hazelcast підключається до своєї ноди кластеру Hazelcast)  

    Запускаємо сервіс  
    ![Alt text](img/1.1.png?raw=true)  

    Бачимо працюючий контейнер  
    ![Alt text](img/1.2.png?raw=true)    

- logging-service використовує Hazelcast Distributed Map для збереження повідомлень замість локальної хеш-таблиці  
    Див. клас LoggingDomain  

- facade-service, з яким взаємодіє клієнт, випадковим чином обирає екземпляр logging-service під час відправки POST/GET запитів
    
    Логіку реалізовано в AddressHelper. 
    Запустимо два logging-service  
    ![Alt text](img/1.3.png?raw=true)    

    Запущено два контейнера Hazelcast на різних портах  
    ![Alt text](img/1.4.png?raw=true)    

    Відправимо два повідомлення   
    ![Alt text](img/1.5.png?raw=true)    

    Як видно перше повідомлення з айді _f8275ba4-c24c-11ed-8e4a-08002704e8bc_ відправлено на _http://127.0.0.1:20000/_  
    А друге _fd5d7392-c24c-11ed-8e4a-08002704e8bc_ на _http://127.0.0.1:20001/_

### Завдання

- Запустити три екземпляра logging-service (локально їх можна запустити на різних портах), відповідно мають запуститись також три екземпляра Hazelcast

    Запустимо 3 logging services на різних портах:
    ![Alt text](img/2.1.png?raw=true)  

- Через HTTP POST записати 10 повідомлень msg1-msg10 через facade-service

    Відправимо повідомлення з текстом від 1 до 10
    ![Alt text](img/2.2.png?raw=true) 

- Показати які повідомлення отримав кожен з екзмеплярів logging-service (це має бути видно у логах сервісу)
    
    Отримані повідомлення в facade-service  
    ![Alt text](img/2.3.png?raw=true) 

    Отримані повідомлення в кожному з logging-service  
    ![Alt text](img/2.4.png?raw=true) 

- Через HTTP GET з facade-service прочитати повідомлення

    Відправимо GET запит
    ![Alt text](img/2.5.png?raw=true) 

- Вимкнути один/два екземпляри logging-service (разом з ним мають вимикатись й ноди Hazelcast) та перевірити чи зможемо прочитати повідомлення 

    Зупинимо сервіс з портом 20002
    ![Alt text](img/2.6.png?raw=true) 

    Перевіримо GET запитом
    ![Alt text](img/2.7.png?raw=true) 

    Зупинимо сервіс з портом 20001
    ![Alt text](img/2.8.png?raw=true) 

    Перевіримо GET запитом(маємо помилку в перші 2 рази round robin вибирає 2 вимкнутих сервіса)
    ![Alt text](img/2.9.png?raw=true) 
    ![Alt text](img/2.10.png?raw=true) 
