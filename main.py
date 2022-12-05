import uuid
from fastapi import FastAPI, Body, status
from fastapi.responses import JSONResponse, FileResponse

#шаблон хранения объекта, 2 из которых будут заполняться через конструктор
class Product:
    def __init__(self, name, quantity):
        self.name = name
        self.quantity = quantity
        self.id = str(uuid.uuid4())


# условная база данных - набор объектов Product
item = [Product("Ручка", 38), Product("Карандаш", 42), Product("Тетрадь", 28)]


# для поиска продукта в списке item
def find_product(id):
    for product in item:
        if product.id == id:
            return product
    return None


app = FastAPI()

#получение шаблона html(разворачивание объекта JSON)
@app.get("/")
async def main():
    return FileResponse("public/index.html")

#получение условной базы
@app.get("/api/users")
def get_item():
    return item

#получение и вывод данных из базы
@app.get("/api/users/{id}")
def get_product(id):
    # получаем товары по id
    product = find_product(id)
    print(product)
    # если не найден, отправляем статусный код и сообщение об ошибке
    if product == None:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"message": "Пользователь не найден"}
        )
    # если продукт найден, отправляем его
    return product

#запись в условную базу
@app.post("/api/users")
def create_product(data=Body()):
    product = Product(data["name"], data["quantity"])
    # добавляем объект в список item
    item.append(product)
    return product


@app.put("/api/users")
def edit_product(data=Body()):
    # получаем товар по id
    product = find_product(data["id"])
    # если не найден, отправляем статусный код и сообщение об ошибке
    if product == None:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"message": "Пользователь не найден"}
        )
    # если товар найден, изменяем его данные и отправляем обратно клиенту
    product.quantity = data["quantity"]
    product.name = data["name"]
    return product


@app.delete("/api/users/{id}")
def delete_product(id):
    # получаем товар по id
    product = find_product(id)

    # если не найден, отправляем статусный код и сообщение об ошибке
    if product == None:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"message": "Пользователь не найден"}
        )

    # если товар найден, удаляем его
    item.remove(product)
    return product