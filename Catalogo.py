
from abc import ABC, abstractmethod


# Clase base y subclases
class Product:
    def __init__(self, name: str, price: float, category: str):
        self.name = name
        self.price = price
        self.category = category

    def get_info(self):
        return f"{self.name} - ${self.price} - {self.category}"

class Electronics(Product):
    def __init__(self, name: str, price: float):
        super().__init__(name, price, "Electronics")

class Clothing(Product):
    def __init__(self, name: str, price: float):
        super().__init__(name, price, "Clothing")

class Food(Product):
    def __init__(self, name: str, price: float):
        super().__init__(name, price, "Food")



# Factory Method
class ProductFactory:
    @staticmethod
    def create_product(category: str, name: str, price: float) -> Product:
        if category == "Electronics":
            return Electronics(name, price)
        elif category == "Clothing":
            return Clothing(name, price)
        elif category == "Food":
            return Food(name, price)
        else:
            return Product(name, price, category)



# Singleton
class ProductCatalog:
    _instance = None

    def __init__(self):
        if ProductCatalog._instance is not None:
            raise Exception("Este catálogo ya existe (Singleton)")
        self.products = []

    @staticmethod
    def get_instance():
        if ProductCatalog._instance is None:
            ProductCatalog._instance = ProductCatalog()
        return ProductCatalog._instance

    def add_product(self, product: Product):
        self.products.append(product)

    def get_products(self):
        return self.products

    def filter(self, strategy):
        return strategy.filter(self.products)


# Strategy
class FilterStrategy(ABC):
    @abstractmethod
    def filter(self, products: list[Product]) -> list[Product]:
        pass

class CategoryFilter(FilterStrategy):
    def __init__(self, category: str):
        self.category = category

    def filter(self, products: list[Product]):
        return [p for p in products if p.category == self.category]

class PriceFilter(FilterStrategy):
    def __init__(self, min_price: float, max_price: float):
        self.min_price = min_price
        self.max_price = max_price

    def filter(self, products: list[Product]):
        return [p for p in products if self.min_price <= p.price <= self.max_price]



# Ejemplo de uso
if __name__ == "__main__":
    catalog = ProductCatalog.get_instance()

    p1 = ProductFactory.create_product("Electronics", "Laptop", 1200)
    p2 = ProductFactory.create_product("Clothing", "T-Shirt", 25)
    p3 = ProductFactory.create_product("Food", "Pizza", 15)
    p4 = ProductFactory.create_product("Electronics", "Smartphone", 800)

    catalog.add_product(p1)
    catalog.add_product(p2)
    catalog.add_product(p3)
    catalog.add_product(p4)

    print("\n📦 Todos los productos:")
    for prod in catalog.get_products():
        print(prod.get_info())

    print("\n📂 Filtrar por categoría 'Electronics':")
    electronics_filter = CategoryFilter("Electronics")
    for prod in catalog.filter(electronics_filter):
        print(prod.get_info())

    print("\n💰 Filtrar por precio entre $20 y $1000:")
    price_filter = PriceFilter(20, 1000)
    for prod in catalog.filter(price_filter):
        print(prod.get_info())
