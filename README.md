# TinkTalker

## Что умеет бот?
Бот готов поговорить с вами на любую тему, но его любимая тема - инвестиции и все что с ними связано.

## Запуск приложения

`git clone https://github.com/alimaskina/TinkTalker.git`  
`cd TinkTalker`  
`docker build --env TG_TOKEN=<токен вашего телеграм бота> tt_bot .`  
`docker run -d tt_bot`

## Использование приложения
Осталось запустить вашего бота в телеграм. Моего бота зовут так: `@tink_talker_bot`. 

## Описание решения

### Телеграм бот

I. Глобально использован паттерн MVC, который разделил приложение на 3 части:
1) Model - вся логика использования дообученной модели;
2) View - часть, отвечающая за то, что видит пользователь;
3) TelegramController - связывает Model и View и знает о сценарии работы.

Это было сделано, потому что эти части интуитивно довольно независимы и, значит, их хочется разрабатывать и тестировать отдельно. Это даст гибкость и позволит в будущем при необходимости менять части независимо.

II. Для работы приложению требуются настройки, которые лежат в config.yml. Чтобы не читать их во всех классах, есть специальных класс Config, который создается в единственном экземпляре (Singleton) и читает config.yml при создании. 
В классе Config есть геттеры для всех настроек, чтобы информация о том, как устроен config.yml хранилась в одном месте, а именно в Config. Все остальные классы создают себе приватное поле config и пользуются этими геттерами. 

III. Так как на будущее хочется оставить свободу для выбора пользовательского представления, то есть абстрактный класс View, который и является интерфейсом, доступным Контроллеру. От него могут наследоваться разные виды представлений, например, сейчас это только TelegramView. 
Чтобы создать наследника определнного типа, используется фабричный метод.

IV. Главная часть Модели - это класс Model. В нем реализуется логика использования дообученной модели.

V. TelegramController осуществляет общее руководство процессом, храня в себе View и Model. 

### Дообучение модели на основе данных из инвесторского чата

Мы дообучаем модель в среде Google Colab c GPU T4 на данных из инвесторского чата с целью улучшения её способности отвечать на вопросы, связанные с инвестициями и финансами.

I. Процесс дообучения в Google Colab
  1) Препроцессинг данных: данные, представленные в формате CSV, содержат диалоги, характерные для инвесторского чата. В ходе препроцессинга диалоги конвертируются в соответствующие последовательности с использованием маркеров @@ПЕРВЫЙ@@ и @@ВТОРОЙ@@.
  3) Загрузка предобученной модели: мы используем предобученную модель "tinkoff-ai/ruDialoGPT-medium" как отправную точку. Далее, эта модель дообучается на наших данных.
  4) Дообучение только голов модели: в процессе дообучения мы активируем только головы модели, в то время как остальные слои остаются замороженными. Такой подход позволяет сосредоточить обучение на высокоуровневых абстракциях, сохраняя при этом знания, заложенные в основные слои модели. Это ускоряет процесс обучения и уменьшает риск переобучения.
  5) Использование специальных маркеров: маркеры @@ПЕРВЫЙ@@ и @@ВТОРОЙ@@ присутствуют в словаре токенизатора. Их использование обеспечивает совместимость с предобученной архитектурой модели.
    
II. Особенности работы в Google Colab
  1) Ограничение времени GPU: одной из основных особенностей Google Colab является ограничение времени на использование GPU. После определенного периода времени сессия GPU автоматически завершается.
  2) Сохранение промежуточных результатов: из-за ограничения по времени и возможности неожиданного завершения сессии, мы регулярно сохраняем прогресс модели в Google Drive. Это позволяет нам возобновить процесс дообучения с последнего сохраненного момента, минимизируя потерю прогресса.
  3) Загрузка модели: при каждом новом запуске сессии в Google Colab необходимо загрузить последнюю сохраненную версию модели из Google Drive, чтобы продолжить дообучение.

Важно: в ноутбуке отражен один из последних запусков - это значит, что модель уже обучалась до этого несколько эпох (это объясняет такие низкие потери на старте).

III. Параметризация оптимизатора

Оптимизатор AdamW инициализирован со скоростью обучения 5×10−5. Это значение было выбрано на основе аналитического изучения динамики функции потерь на предварительных этапах обучения. Для дополнительной стабилизации процесса и автоматической коррекции скорости обучения применяется планировщик ReduceLROnPlateau.


### Инференс дообученной модели
I. Обзор

В связи с ограничениями на размер файлов, предоставляемыми большинством бесплатных хостинг-платформ Python, и учитывая, что рекомендованная модель имеет объем 1,3 Гб, решено было вынести инференс модели на отдельный сервер.

II. Архитектура веб-сервера

Для реализации веб-сервера, обеспечивающего доступ к модели, применяются библиотеки fastapi и uvicorn.

III. Интерфейс доступа

Доступ к инференсу модели осуществляется посредством HTTP-запроса к серверу. Клиент передает контекст из трех последних сообщений, в ответ получает сгенерированный моделью текст.

IV. Подготовка к инференсу

Для развертывания инференса модели служит директория inference. Внутри этой директории созданы две пустые папки: model и tokenizer. Перед сборкой Docker-образа необходимо разместить в этих папках файлы дообученной модели GPT-2 и соответствующего токенайзера.

V. Сборка и запуск

В директории inference представлен Dockerfile, который служит для создания Docker-образа. При запуске контейнера на основе этого образа рекомендуется пробросить 8000 порт на 5000.

VI. Конфигурация

URL удаленного сервера указан в файле config.yaml.
