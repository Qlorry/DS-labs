## Lab 5 - Мікросервиси з використанням Service Discovery та Config Server на базі Consul

### Огляд змін в сервісах

Для спрощення запуску всієї системи я зробив докерфайл для кожного з сервісів і compose.yaml.

Сервіси Hazelcast я додав в дефолтну конфігурацію(consul-services.json).

В усі сервіси я додав клас ConsulRepo, в ньому логіка з реєстрації сервісу та отримання імен структур hazelcast(де потрібно)

З попередньої версії я трохи переглянув логи та додав більше інформації в message service, інші покращив.

Додав логіку для health checks.

### Демонстрація роботи

- Всі мікросервіси мають реєструватись при старті у Consul, кожного з сервісів може бути запущено декілька екземплярів:  

    Клас ConsulRepo в кожному з сервісів відповідає за реєстрацію сервіса в Consul. Кожен сервіс реєструється з настроєним health check, перевірка за допомогою http GET.   
    При закритті сервіса запис видаляється, у випадку падіння сервіса за таймаутом сервіс видаляється з consul.  

    ![Alt text](img/0.1.png?raw=true)  
    ![Alt text](img/0.2.png?raw=true)  
    ![Alt text](img/0.3.png?raw=true)  

- При звертанні facade-service до logging-service та messages-service, IP-адреси (і порти) мають зчитуватись facade-service з Consul. Немає бути задано в коді чи конфігураціях статичних значень адрес.  

    Логіка додана в AddressHelper.  
    отримання адрес прим POST
    ![Alt text](img/0.5.png?raw=true)  
    отримання адрес прим GET  
    ![Alt text](img/0.6.png?raw=true)  

- Налаштування для клієнтів Hazelcast мають зберігатись як key/value у Consul і зчитуватись logging-service

    В Consul додано стандартні записи сервісів hazelcast(файл consul-services.json що передається в якості docker volume в compose.yaml)  
    Назва distrebuted-map задана в Consul як KV. Збережено в consul-volume.  
    ![Alt text](img/0.4.png?raw=true)  

- Налаштування для Message Queue (адреса, назва черги, …) мають зберігатись як key/value у Consul і зчитуватись facade-service та messages-service

    Назва distrebuted-queue задана в Consul як KV. Збережено в consul-volume.  
    

### Завдання

### 1. Запустимо compose.yaml. Маємо:
- facade-service
- два екземпляра message-service
- три екземпляра logging-service
- три екземпляра hazelcast
- Consul

![Alt text](img/1.1.png?raw=true)  

Всі контейнери запущені в одній мережі.  

![Alt text](img/1.2.png?raw=true)

### 2. Дочекаємось запуску і ініціалізації всіх контейнерів. 
Перевіримо зареєстровані сервіси в Consul:  

![Alt text](img/1.3.png?raw=true)

Значення в KV:

![Alt text](img/1.4.1.png?raw=true)  
![Alt text](img/1.4.2.png?raw=true)![Alt text](img/1.4.3.png?raw=true)

### 3. Відправимо повідомлення  
![Alt text](img/1.5.png?raw=true)

Логи з facade  
![Alt text](img/1.6.png?raw=true)

Логи одного з message   
![Alt text](img/1.7.png?raw=true)

Логи одного з logging   
![Alt text](img/1.8.png?raw=true)

Повторимо 10 разів. 
    
### 4. Відправимо GET
повідомлення з сервіса message i logging відділені "---------"
![Alt text](img/1.9.png?raw=true)
![Alt text](img/1.10.png?raw=true)

### 5. Зупинимо кілька сервісів

Для початку зупинимо logging, втрати даних не очікується:  
![Alt text](img/2.1.png?raw=true)  
Перевірка в Consul:  
![Alt text](img/2.2.png?raw=true)  
GET запит видає ті самі результати
![Alt text](img/2.3.png?raw=true)  

Зупинимо message сервіс
![Alt text](img/2.4.png?raw=true)  
Перевірка в Consul:   
![Alt text](img/2.7.png?raw=true)  
2 запити GET підряд видають однакові результати кожен раз(інформація з зупиненого сервіса втрачена):  
![Alt text](img/2.5.png?raw=true)  
![Alt text](img/2.6.png?raw=true)  

### 6. Запустимо сервіс
В систему можна додати повністю новий сервіс, але перезапуск контейнера буде сприйнято системою як новий сервіс(і це простіше зробити).  
Тому перезапустимо для наочності message і відправимо 2 GET запити:  
![Alt text](img/2.8.png?raw=true)   
![Alt text](img/2.9.png?raw=true)  
Перший запит надійшов до ноди що працювала до того, а другий до нової -- тому повідомлення від неї пусте.