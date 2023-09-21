# INFO
ETL для курса Яндекс Практикум middle-python-разработчик

Создан для четвертого спринта

# Запуск/остановка
- make up - запуск
- make down - стоп

## Альтернативный метод запуска/остановки
- docker compose up -d
- docker compose down

# Переменные окружения
Смотреть .test.env

# Какие индексы создаются
<details>
<summary>movie</summary>

```
{
    id: uuid,
    imdb_rating: float,
    genre: {
        id: uuid,
        name: str
    },
    title: string,
    description: string,
    directors: [
        {
            id: uuid,
            name: string
        }
    ],
    actors: [
        {
            id: uuid,
            name: string
        }
    ],
    writers: [
        {
            id: uuid,
            name: string
        }
    ]
}
```
</details>

<details>
<summary>genre</summary>

```
{
    id: uuid,
    name: string,
    description: string,
    movies: [
        {
            id: uuid,
            title: string,
            imdb_rating: float
        }
    ]
}
```
</details>

<details>
<summary>person</summary>

```
{
    id: uuid,
    name: string,
    movies: [
        {
            id: uuid,
            title: string,
            imdb_rating: float,
            roles: [string]
        }
    ]
}
```
</details>
