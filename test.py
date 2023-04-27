class SellItem:
    def __init__(self, name: str, price: int or float) -> None:
        self.name = name
        self.price = price


class House(SellItem):
    def __init__(self, name: str, price: int or float, material, square) -> None:
        super().__init__(name, price)
        self.material = material
        self.square = square


class Flat(SellItem):
    def __init__(self, name: str, price: int or float, size, rooms) -> None:
        super().__init__(name, price)
        self.size = size
        self.rooms = rooms


class Land(SellItem):
    def __init__(self, name: str, price: int or float, square) -> None:
        super().__init__(name, price)
        self.square = square


class Agency:
    lst = []

    def __init__(self, name: str) -> None:
        self.name = name

    def add_object(self, obj):  # добавление нового объекта недвижимости для продажи (один из объектов классов: House, Flat, Land);
        self.obj = obj
        self.lst.append(self.obj)

    def remove_object(self, obj):  # удаление объекта obj из списка объектов для продажи;
        self.obj = obj
        self.lst.pop(self.obj)
    
    def get_objects(self):  # возвращает список из всех объектов для продажи.
        return self.lst


ag = Agency("Рога и копыта")
ag.add_object(Flat("квартира, 3к", 10000000, 121.5, 3))
ag.add_object(Flat("квартира, 2к", 8000000, 74.5, 2))
ag.add_object(Flat("квартира, 1к", 4000000, 54, 1))
ag.add_object(House("дом, крипичный", price=35000000, material="кирпич", square=186.5))
ag.add_object(Land("участок под застройку", 3000000, 6.74))
for obj in ag.get_objects():
    print(obj.name)

lst_houses = [x for x in ag.get_objects() if isinstance(x, House)] # выделение списка домов