import sqlalchemy
from sqlalchemy.orm import sessionmaker
from url_data import connection_driver, login, password, host, port, name_db
import json

from models import create_tables, Publisher, Book, Shop, Stock, Sale

DSN = f'{connection_driver}://{login}:{password}@{host}:{port}/{name_db}'
engine = sqlalchemy.create_engine(DSN)

create_tables(engine)

Session = sessionmaker(bind=engine)
session = Session()

with open('fixtures/tests_data.json', 'r') as fd:
    data = json.load(fd)

for record in data:
    model = {
        'publisher': Publisher,
        'shop': Shop,
        'book': Book,
        'stock': Stock,
        'sale': Sale,
    }[record.get('model')]
    session.add(model(id=record.get('pk'), **record.get('fields')))

session.commit()

request_name = None
request_id = None
request_name_publisher = input('Введите имя или идентификатор издателя (publisher): ')

if request_name_publisher.isdigit():
    request_id = request_name_publisher
else:
    request_name = request_name_publisher

if request_name_publisher.isdigit():
    for request in session.query(Publisher).filter(
            Publisher.id == int(request_id)).all():
        print(request)
else:
    for request in session.query(Publisher).filter(
            Publisher.name.like(f'%{request_name}%')).all():
        print(request)

print('Книги издательства продаются в магазинах:')

for select_shop in session.query(Shop).join(Stock).join(Book).join(Publisher).filter((Publisher.name == request_name) | (Publisher.id == request_id)).all():
    print(select_shop)

session.close()
