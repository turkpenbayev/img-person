# Сервис фотографии

[![Build Status](https://github.com/turkpenbayev/img-person/actions/workflows/django.yml/badge.svg?branch=master)](https://github.com/turkpenbayev/img-person/actions/workflows/django.yml)

```sh
docker-compose up -d --build
```
## выполныние задачи

-  организовать тестирование написанного кода 
-  обеспечить автоматическую сборку/тестирование с помощью GitLab CI 
-  подготовить docker-compose для запуска всех сервисов проекта одной командой
-  по адресу /docs/ открывалась страница со Swagger UI и в нём отображалось описание разработанного API. Пример: [http://0.0.0.0:9000/docs/](http://0.0.0.0:9000/docs/)
-  доп задача: сделать апи автодополнение по поиску возможных имен людей присутствующих на фотографиях [http://0.0.0.0:9000/person/names/](http://0.0.0.0:9000/person/names/) token 'Token 1c092ea9d1f0cc7735a073c06111685b31880fca'
-  обеспечить подробное логирование на всех этапах обработки запросов, чтобы при эксплуатации была возможность найти в логах всю информацию по