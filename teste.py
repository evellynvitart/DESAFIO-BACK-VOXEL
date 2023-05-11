import requests
import json
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.orm import declarative_base, sessionmaker


Base = declarative_base()

class Produto(Base):
    __tablename__ = 'produtos'
    id = Column(Integer, primary_key=True)
    title = Column(String)
    category = Column(String)
    price = Column(Float)


response = requests.get('https://dummyjson.com/products')


if response.ok:
    try:
        produtos = [json.loads(produto.replace("'", '"')) for produto in response.json()]
    except json.decoder.JSONDecodeError:
        print("Erro ao carregar os dados da API.")
        produtos = []
else:
    print("Erro ao acessar a API.")
    produtos = []


precos_smartphones = [produto['price'] for produto in produtos if produto['category'] == 'smartphones']
if len(precos_smartphones) > 0:
    media_precos_smartphones = sum(precos_smartphones) / len(precos_smartphones)
else:
    media_precos_smartphones = 0


print("## Resultado da coleta de dados ##")
print(f"Preço médio dos smartphones: $ {media_precos_smartphones:.2f}.")


engine = create_engine('sqlite:///produtos.db')
Base.metadata.create_all(engine)


Session = sessionmaker(bind=engine)
session = Session()

for produto in produtos:
    p = Produto(title=produto['title'], category=produto['category'], price=produto['price'])
    session.add(p)


session.commit()
session.close()


response = requests.get('https://api.chucknorris.io/jokes/random')
piada = response.json()['value']


print("\nAqui vai uma piada do Chuck Norris para descontrair:\n", piada)






