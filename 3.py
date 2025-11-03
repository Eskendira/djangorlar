# file3.py - Inventory Management System
class Product:
    def __init__(self, product_id, name, price, quantity):
        self.product_id = product_id
        self.name = name
        self.price = price
        self.quantity = quantity
        self.category = "Uncategorized"
    
    def update_price(self, new_price):
        if new_price >= 0:
            old_price = self.price
            self.price = new_price
            return f"Price updated from ${old_price:.2f} to ${new_price:.2f}"
        return "Price cannot be negative"
    
    def update_quantity(self, new_quantity):
        if new_quantity >= 0:
            old_quantity = self.quantity
            self.quantity = new_quantity
            return f"Quantity updated from {old_quantity} to {new_quantity}"
        return "Quantity cannot be negative"
    
    def add_stock(self, amount):
        if amount > 0:
            self.quantity += amount
            return f"Added {amount} units. New quantity: {self.quantity}"
        return "Amount must be positive"
    
    def remove_stock(self, amount):
        if amount > 0:
            if self.quantity >= amount:
                self.quantity -= amount
                return f"Removed {amount} units. New quantity: {self.quantity}"
            return f"Insufficient stock. Available: {self.quantity}"
        return "Amount must be positive"
    
    def set_category(self, category):
        self.category = category
        return f"Category set to {category}"
    
    def get_total_value(self):
        return self.price * self.quantity
    
    def get_product_info(self):
        return (f"ID: {self.product_id}, Name: {self.name}, "
                f"Price: ${self.price:.2f}, Quantity: {self.quantity}, "
                f"Category: {self.category}, Total Value: ${self.get_total_value():.2f}")


class Inventory:
    def __init__(self):
        self.products = {}
        self.next_id = 1
        self.categories = set()
    
    def add_product(self, name, price, quantity, category="Uncategorized"):
        product_id = f"P{self.next_id:03d}"
        product = Product(product_id, name, price, quantity)
        product.set_category(category)
        self.products[product_id] = product
        self.next_id += 1
        self.categories.add(category)
        return product_id
    
    def remove_product(self, product_id):
        if product_id in self.products:
            category = self.products[product_id].category
            del self.products[product_id]
            # Check if category is still used
            self._update_categories()
            return f"Removed product {product_id}"
        return f"Product {product_id} not found"
    
    def _update_categories(self):
        current_categories = set(product.category for product in self.products.values())
        self.categories = current_categories
    
    def get_product(self, product_id):
        return self.products.get(product_id)
    
    def get_all_products(self):
        return list(self.products.values())
    
    def search_products(self, name=None, category=None):
        results = []
        for product in self.products.values():
            if name and name.lower() not in product.name.lower():
                continue
            if category and category.lower() != product.category.lower():
                continue
            results.append(product)
        return results
    
    def get_low_stock_products(self, threshold=5):
        low_stock = []
        for product in self.products.values():
            if product.quantity <= threshold:
                low_stock.append(product)
        return low_stock
    
    def get_total_inventory_value(self):
        total_value = 0
        for product in self.products.values():
            total_value += product.get_total_value()
        return total_value
    
    def get_category_summary(self):
        summary = {}
        for product in self.products.values():
            category = product.category
            if category not in summary:
                summary[category] = {
                    'count': 0,
                    'total_value': 0,
                    'total_quantity': 0
                }
            summary[category]['count'] += 1
            summary[category]['total_value'] += product.get_total_value()
            summary[category]['total_quantity'] += product.quantity
        return summary
    
    def restock_product(self, product_id, amount):
        product = self.get_product(product_id)
        if product:
            return product.add_stock(amount)
        return f"Product {product_id} not found"
    
    def sell_product(self, product_id, amount):
        product = self.get_product(product_id)
        if product:
            return product.remove_stock(amount)
        return f"Product {product_id} not found"

# Example usage
if __name__ == "__main__":
    inventory = Inventory()
    
    # Add products
    p1 = inventory.add_product("Laptop", 999.99, 10, "Electronics")
    p2 = inventory.add_product("Mouse", 25.50, 50, "Electronics")
    p3 = inventory.add_product("Notebook", 5.99, 100, "Stationery")
    p4 = inventory.add_product("Pen", 1.99, 200, "Stationery")
    
    # Perform operations
    inventory.restock_product(p1, 5)
    inventory.sell_product(p2, 10)
    inventory.sell_product(p3, 25)
    
    # Update price
    laptop = inventory.get_product(p1)
    if laptop:
        laptop.update_price(899.99)
    
    # Display information
    print("All Products-V5:")
    for product in inventory.get_all_products():
        print(product.get_product_info())
    
    print(f"\nTotal Inventory Value: ${inventory.get_total_inventory_value():.2f}")
    
    print("\nLow Stock Products (threshold: 5):")
    for product in inventory.get_low_stock_products():
        print(f"  {product.name} - {product.quantity} units")
    
    print("\nCategory Summary:")
    summary = inventory.get_category_summary()
    for category, data in summary.items():
        print(f"  {category}: {data['count']} products, "
              f"{data['total_quantity']} units, "
              f"${data['total_value']:.2f} total value")