# TinkTalker

## Что умеет бот?
Бот готов поговорить с вами на любую тему.

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
  1) Загрузка данных: Наши данные, сохраненные в формате CSV, содержат диалоги из инвесторского чата. Эти диалоги обрабатываются с использованием специальных токенов @@ПЕРВЫЙ@@ и @@ВТОРОЙ@@ и преобразуются в последовательности для дальнейшего дообучения.
  2) Загрузка предобученной модели: Мы используем предобученную модель "tinkoff-ai/ruDialoGPT-medium" как отправную точку. Далее, эта модель дообучается на наших данных.
  3) Дообучение только голов модели: В процессе дообучения мы активируем только головы модели, в то время как остальные слои остаются замороженными. Такой подход позволяет сосредоточить обучение на высокоуровневых абстракциях, сохраняя при этом знания, заложенные в основные слои модели. Это ускоряет процесс обучения и уменьшает риск переобучения.
  4) Специальные токены: Токены @@ПЕРВЫЙ@@ и @@ВТОРОЙ@@ были обнаружены в словаре токенизатора, и дообучение шло с их использованием. Это было сделано для обеспечения совместимости с предобученной моделью, учитывая, что мы обучаем только головы модели.
    
II. Особенности работы в Google Colab
  1) Ограничение времени GPU: Одной из основных особенностей Google Colab является ограничение времени на использование GPU. После определенного периода времени сессия GPU автоматически завершается.
  2) Сохранение промежуточных результатов: Из-за ограничения по времени и возможности неожиданного завершения сессии, мы регулярно сохраняем прогресс модели в Google Drive. Это позволяет нам возобновить процесс дообучения с последнего сохраненного момента, минимизируя потерю прогресса.
  3) Загрузка модели: При каждом новом запуске сессии в Google Colab необходимо загрузить последнюю сохраненную версию модели из Google Drive, чтобы продолжить дообучение.


