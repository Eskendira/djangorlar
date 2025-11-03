
class Calculator:
    def __init__(self):
        self.history = []
        self.memory = 0
    
    def add(self, a, b):
        result = a + b
        self.history.append(f"{a} + {b} = {result}")
        return result
    
    def subtract(self, a, b):
        result = a - b
        self.history.append(f"{a} - {b} = {result}")
        return result
    
    def multiply(self, a, b):
        result = a * b
        self.history.append(f"{a} * {b} = {result}")
        return result
    
    def divide(self, a, b):
        if b == 0:
            raise ValueError("Cannot divide by zero")
        result = a / b
        self.history.append(f"{a} / {b} = {result}")
        return result
    
    def power(self, base, exponent):
        result = base ** exponent
        self.history.append(f"{base}^{exponent} = {result}")
        return result
    
    def square_root(self, number):
        if number < 0:
            raise ValueError("Cannot calculate square root of negative number")
        result = number ** 0.5
        self.history.append(f"√{number} = {result}")
        return result
    
    def factorial(self, n):
        if n < 0:
            raise ValueError("Factorial is not defined for negative numbers")
        if n == 0:
            return 1
        result = 1
        for i in range(1, n + 1):
            result *= i
        self.history.append(f"{n}! = {result}")
        return result
    
    def store_memory(self, value):
        self.memory = value
        self.history.append(f"Stored {value} in memory")
    
    def recall_memory(self):
        self.history.append(f"Recalled {self.memory} from memory")
        return self.memory
    
    def clear_memory(self):
        self.history.append("Cleared memory")
        self.memory = 0
    
    def get_history(self):
        return self.history
    
    def clear_history(self):
        self.history = []
    
    def calculate_expression(self, expression):
        # Simple expression evaluator
        try:
            result = eval(expression)
            self.history.append(f"{expression} = {result}")
            return result
        except Exception as e:
            raise ValueError(f"Invalid expression: {e}")

# Example usage
if __name__ == "__main__":
    calc = Calculator()
    print("Calculator initialized-V2")
    print(f"2 + 3 = {calc.add(2, 3)}")
    print(f"5 * 4 = {calc.multiply(5, 4)}")
    print(f"10 / 2 = {calc.divide(10, 2)}")
    print(f"2^8 = {calc.power(2, 8)}")
    print(f"5! = {calc.factorial(5)}")
    
    calc.store_memory(100)
    print(f"Memory: {calc.recall_memory()}")
    
    print("History:")
    for entry in calc.get_history():
        print(f"  {entry}")