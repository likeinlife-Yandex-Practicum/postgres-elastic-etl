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
    id: string,
    imdb_rating: float,
    genre: [string],
    title: string,
    description: string,
    directors: [
        {
            id: string,
            name: string
        }
    ],
    actors: [
        {
            id: string,
            name: string
        }
    ],
    writers: [
        {
            id: string,
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
    id: string,
    name: string,
    description: string,
    movies: [
        {
            id: string,
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
    id: string,
    name: string,
    movies: [
        {
            id: string,
            title: string,
            roles: [string]
        }
    ]
}
```
</details>
