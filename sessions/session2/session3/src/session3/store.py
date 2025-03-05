class Product:
    def __init__(self, name, price, quantity):
        self.name = name
        self.price = price
        self.quantity = quantity

    def __str__(self):
        return f"Product: {self.name}, Price: ${self.price:.2f}, Quantity: {self.quantity}"

    def add_stock(self, quantity):
        self.quantity += quantity


class User:
    def __init__(self, name, email):
        self.name = name
        self.email = email

    def __str__(self):
        return f"User: {self.name}, Email: {self.email}"

    def register(self):
        print(
            f"User {self.name} has been registered with the email {self.email}.")


class Store:
    def __init__(self):
        self.products = []
        self.users = []

    def add_product(self, product):
        self.products.append(product)
        print(f"Product {product.name} added to the store.")

    def register_user(self, user):
        self.users.append(user)
        user.register()

store = Store()

# auto testing
store.add_product(Product("test1", 5, 10))
store.add_product(Product("teste2", 0.50, 20))

# manual testing
choiceAdd = input("Would you like to add a product? Y or N")
if choiceAdd == "y" or choiceAdd == "Y":
    productTestName = input("Input a product name: ")
    productTestPrice = float(input("Input the price of the product: "))
    productTestQuantity = int(input("Input the quantity of the product: "))
    store.add_product(Product(productTestName, productTestPrice, productTestQuantity))
else:
    pass

store.register_user(User("lucas", "lucas@example.com"))

print("\nProducts in Store:")
for product in store.products:
    print(product)

print("\nRegistered users:")
for user in store.users:
    print(user)
