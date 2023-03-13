### 1. Встановити і налаштувати Hazelcast

Я встановив hazelcast за інструкцією. Cкачав докер контейнери самого hazelcast та management-center

### 2. Сконфігурувати і запустити 3 ноди

Запустив 3 ноди, одного кластеру(командами з файлу hints) і management-center. Для всіх них створив віртуальну мережу
![Alt text](img/2.1.png?raw=true)  

Перевірка в management-center, всі три ноди працюють в кластері:
![Alt text](img/2.3.png?raw=true) 
(В процесі айпі адреси мінялись, бо я перезапускав віртуальну машину, контейнери, тощо...)
### 3.Продемонструйте роботу Distributed Map 

Запишемо дані в map функцією set_data
![Alt text](img/3.1.png?raw=true) 

Перевіримо в management-center
![Alt text](img/3.2.png?raw=true) 

### 4.Подивитись як зміниться розподіл якщо відключити:
### Одну ноду
![Alt text](img/4.1.png?raw=true) 

Перевіримо чи всі дані в порядку функцією check_data
![Alt text](img/4.2.png?raw=true)   

### Дві ноди
![Alt text](img/4.3.png?raw=true) 

Перевіримо чи всі дані в порядку
![Alt text](img/4.4.png?raw=true) 

чи буде втрата даних? -- __Ні!__

### 5.Змініть backup-count 
### на 0
Змінемо параметр в hazelcast-backup0.xml  
Перезапустимо кластер з новим конфігом(команда в hints), настройка в дії:
![Alt text](img/5.1.png?raw=true) 

Перевіримо розподіл
![Alt text](img/5.2.png?raw=true) 

### на 2
Змінемо параметр в hazelcast-backup2.xml
Перезапустимо кластер з новим конфігом, настройка в дії:
![Alt text](img/5.3.png?raw=true) 

Перевіримо розподіл
![Alt text](img/5.4.png?raw=true) 

### 6.Продемонструйте роботу Distributed Map with locks
одночансо запустіть приклади за посиланням з документації з підрахунку значень в циклі: a) без блокування; б) з песимістичним; в) з оптимістичним блокуванням
	http://docs.hazelcast.org/docs/latest/manual/html-single/index.html#locking-maps 
порівняйте результати кожного з запусків

а) Одночасно запустимо функцію write_no_lock з 3х потоків. Очікувано останній результат не 3000(3 потоки * 1000 операцій ++)
![Alt text](img/6.1.png?raw=true)   
Видно що результати різні, однозначно виникає data race  

б) Одночасно запустимо функцію write_pessimistic_lock з 3х потоків.
![Alt text](img/6.2.png?raw=true)   
Бачимо стабільний результат 3000  

в) Одночасно запустимо функцію write_optimistic_lock з 3х потоків.
![Alt text](img/6.3.png?raw=true)   
Бачимо стабільний результат 300(код на 1000 ітерацій працював дуже довго і я зробив на 100) 

### 7.Налаштуйте Bounded queue
на основі Distributed Queue (http://docs.hazelcast.org/docs/latest/manual/html-single/index.html#queue) налаштуйте Bounded queue (http://docs.hazelcast.org/docs/latest/manual/html-single/index.html#setting-a-bounded-queue) 
з однієї ноди (клієнта) йде запис, а на двох інших читання 
перевірте яка буде поведінка на запис якщо відсутнє читання, і черга заповнена
як будуть вичитуватись значення з черги якщо є декілька читачів 

Установимо ліміт для queue на рівні 15  
![Alt text](img/7.1.png?raw=true)   

За допомогою функції start_only_writer запустимо запис в чергу. Видно що після 15 елементу черга не приймає нові значення.   
![Alt text](img/7.2.png?raw=true)   
Якщо запустити тільки чатача, одразу отримаємо всі 15 повідомлень:  
![Alt text](img/7.3.png?raw=true)  

Запустимо одного продьюсера і 2 читача в окремих потоках:  
Читачі почергово отримують об'єкти з черги  
![Alt text](img/7.4.png?raw=true)   

Якщо зменшити інтервал між додаванням елементів в чергу, то можна побачити що вони успішно зберігаються там поки не запустяться читачі:  
![Alt text](img/7.5.png?raw=true)   