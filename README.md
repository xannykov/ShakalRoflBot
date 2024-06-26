<div align="center">
    <h1> ShakalRoflBot
    <br>
    <img src="https://github.com/xannykov/ShakalRoflBot/blob/main/demonstration/ShakalRoflBot.png"/>
</div>

___
## Описание
**ShakalRoflBot** — это Telegram-бот, который сжимает качество изображений и видео. Он позволяет пользователям выбирать уровень сжатия и отправлять файлы для уменьшения их качества. Этот бот идеально подходит для создания забавных и искаженных версий ваших медиафайлов.
___
## Функциональные возможности

* **Выбор уровня сжатия**: Три уровня сжатия — сильный, средний и слабый.
* **Поддержка изображений и видео**: Сжимает как изображения, так и видео файлы.
* **Анимация ожидания**: Отображает анимацию ожидания обработки видео прямо в чате.
* **Автоматическое определение типа файла**: Определяет, является ли загруженный документ изображением или видео.
___
## Демонстрация

### Отправка фотографий
<img src="https://github.com/xannykov/ShakalRoflBot/blob/main/demonstration/demonstration_1.gif"/>

### Отправка видео
<img src="https://github.com/xannykov/ShakalRoflBot/blob/main/demonstration/demonstration_2.gif"/>

___
## Установка

1. Клонируйте репозиторий:

  ```sh
  git clone https://github.com/xannykov/ShakalRoflBot.git
  ```

2. Переход в директорию ShakalRoflBot:

  ```sh
  cd ShakalRoflBot
  ```

3. Создание виртуального окружения:

  ```sh
  py -m venv .venv
  ```

4. Активация:
  ```sh
  .venv\Scripts\activate
  ```
5. Установите зависимости:

  ```sh
  pip install -r requirements.txt
  ```

6. Перейдите в *utils.py* и в строчке ```bot = telebot.TeleBot('TOKEN')``` введите свой TOKEN.

7. Запуск:
   
  ```sh
  py main.py
  ```
___
