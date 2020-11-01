# Task manager by Roman Sergeichuk
Веб-приложение, реализующее систему управления задачами.

### Hexlet tests and linter status:
![Actions Status](/workflows/hexlet-check/badge.svg)

[![Maintainability](https://api.codeclimate.com/v1/badges/ab78a17e98fa320e4257/maintainability)](https://codeclimate.com/github/Roman-Sergeichuk/python-project-lvl4/maintainability)
[![Test Coverage](https://api.codeclimate.com/v1/badges/ab78a17e98fa320e4257/test_coverage)](https://codeclimate.com/github/Roman-Sergeichuk/python-project-lvl4/test_coverage)
[![Build Status](https://travis-ci.com/Roman-Sergeichuk/python-project-lvl4.svg?branch=main)](https://travis-ci.com/Roman-Sergeichuk/python-project-lvl4)


Приложение развернуто на Heroku:
https://taskmanager-rs.herokuapp.com/

## Функциональные возможности
- приложение настроено на работу с базой данных PostgreSQL;
- реализована авторизация пользователей;
- в системе может быть зарегистрировано множество пользователей;
- пользователь после авторизации может создавать себе задачу, указав для этого ее название, описание, статус, назначить 
исполнителя из списка зарегистрированных пользователей и при необходимости выбрать один или несколко тегов из списка;
- пользователь может редактировать содержимое любой своей или чужой задачи;
- пользователь может удалить любую из ранее созданных задач;
- пользователь может вывести список задач с возможностью фильтрации по статусу, автору, исполнителю, а также по тегам;
- пользователь может может добавлять, редактировать и изменять статусы, а также добавлять теги.

## Запуск приложения
Для запуска приложения склонируйте репозиторий:

    https://github.com/Roman-Sergeichuk/python-project-lvl4.git
    
Активируйте виртуальное окружение и установите необходимые зависимости, выполнив команду:
    
    poetry install
    
Замениете название файла .env.example на .env и задайте свои значения переменных внутри этого файла.

После этого сделайте и примените миграции командой:

    make migrations
    
Запустите сервер командой:

    make deploy
    
## Запуск тестов
Для запуска тестов воспользуйтесь командой:

    make check
