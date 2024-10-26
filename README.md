<div align="center">
  <h1>Парсер "Четыре Лапы"</h1>
  <h3>Описание</h3>
  <p>Парсер магазина <b>"Четыре Лапы"</b> через <code>API</code> мобильного приложения.</p>
  <hr>
  <h3>Фукционал</h3>
  <ul>
    <li>Парсинг выбранной категории Москвы и Санкт-Петербурга с учётом вариантов упаковки товара.</li>
    <li>Выбор категории и сортировки товаров через аргументы командной строки.</li>
    <li>Сохранение спаршенных товаров в <code>JSON</code>-файл.</li>
    <li>Асинхронность.</li>
  </ul>
  <hr>
  <h3>Примечания</h3>
</div>
  <p align="center">Файлы с товарами сохраняются по пути <code>корневая папка проекта <b>/</b> slug города <b>/</b> slug категории.json</code>.</p>
  <p align="center">Парсятся не только <b>регулярная цена</b> и <b>промо цена</b>, а все разновидности цен для учёта скидок от количества и т.д., так же товар парсится сразу со всеми вариантами упаковок.</p>
    <p align="center">Аргументы: <code>id</code> категории <i>(не обязательный)</i> - <code>-c (--category) int</code>, сортировка категории <i>(не обязательный)</i> - <code>-s (--sort) popular | "up-price" | "down-price" | novinki</code>.</p>
  <p align="center">Все команды выполнять из корневой папки проекта.</p>
<hr>

<h3 align="center">Как запустить</h3>
<details>
  <p align="center"><summary align="center"><ins>Через консоль</ins></summary></p>
  <ul>
    <li align="center"><b>1.</b> Создать и активировать виртуальное окружение при помощи <code>Poetry</code>:
       <ul>
          <li><b>a)</b> Установить <code>Poetry</code>: <code>pip install poetry</code></li>
          <li><b>б)</b> Активировать виртуальное окружение: <code>poetry shell</code> (если <code>Poetry</code> не находит <code>Python ^3.12</code>, воспользоваться <a href="https://python-poetry.org/docs/managing-environments/">инструкцией</a>)</li>
          <li><b>в)</b> Установить зависимости: <code>poetry install</code></li>
       </ul>
    </li>
    <li align="center">
       <p><b>2.</b> Инициализировать <code>pre-commit</code>: <code>pre-commit install</code></p>
    </li>
    <li align="center">
      <p><b>3.</b> Выполнить команду <code>python main.py</code></p>
    </li>
  </ul>
  <ul>
    <hr>
    <li align="center"><b>1.</b> Создать и активировать виртуальное окружение стандартным способом:
       <ul>
          <li><b>a)</b> Создать виртуальное окружение: <code>python -m venv venv</code></li>
          <li><b>б)</b> Активировать виртуальное окружение: <b>Linux/macOS -</b> <code>source venv/bin/activate</code>, <b>Windows -</b> <code>source venv/scripts/activate</code></li>
          <li><b>в)</b> Установить зависимости из файла <code>requirements.txt</code>: <code>python -m pip install --upgrade pip</code> <code>pip install -r requirements.txt</code></li>
       </ul>
    </li>
    <li align="center">
       <p><b>2.</b> Инициализировать <code>pre-commit</code>: <code>pre-commit install</code></p>
    </li>
    <li align="center">
      <p><b>3.</b> Выполнить команду <code>python main.py</code></p>
    </li>
  </ul>
</details>

<hr>

<h3 align="center">Стек</h3>
<p align="center">
  <img src="https://img.shields.io/badge/Python-3.12-red?style=flat&logo=python&logoColor=white">
  <img src="https://img.shields.io/badge/aiohttp-3.10.10-red?style=flat&logo=aiohttp&logoColor=white">
  <img src="https://img.shields.io/badge/Poetry-Latest-red?style=flat&logo=poetry&logoColor=white">
  <img src="https://img.shields.io/badge/Pre commit-Latest-red?style=flat&logo=Precommit&logoColor=white">
</p>
<hr>
