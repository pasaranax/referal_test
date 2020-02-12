# Описание
Тестовое задание. Разбор логов на предмет покупок от партнеров.

# Использование
Создаем парсер и передаем ему лог
Конструктор `Parser` принимает на вход dict-like объект с полями: client_id, date, document.referer, document.location, 
а также параметр `sort` (bool) для применения сортировки по дате. 
```python
log = json.load(open("log.json"))
parser = Parser(log, sort=True)
```
Метод `records` возвращает итератор по найденным записям. Возвращает объект `Customer`. Имеет следующие параметры:
- `only_purchases` - bool, возвращать только покупки, по умолчанию False
- `partner` - str, возвращать только клиентов указанного партнера, по умолчанию None
Найдем покупки партнера "referal.ours.com"
```python
for customer in parser.records(partner="referal.ours.com", only_purchases=True):
    print(customer)
```
Вывод:
```
Customer(client_id=user17, partner=referal.ours.com, purchase=True)
Customer(client_id=user7, partner=referal.ours.com, purchase=True)
Customer(client_id=user101, partner=referal.ours.com, purchase=True)
Customer(client_id=user101, partner=referal.ours.com, purchase=True)
```

# Тесты
`pytest -v test.py`

# Пути оптимизации
- на вход Parser может принимать итерируемый объект, что позволит не хратить весь лог в памяти (если не использовать параметр sort)
- модель Customer можно хранить в key-value хранилище, чтобы не занимать память в питоне
- с помощью блокировок на отдельных Customer можно реализовать многопоточную обработку логов, создав несколько Parser и скармливая им различные фрагменты логов
