"""
COMPREHENSIVE GUIDE TO POLYMORPHISM IN PYTHON
=============================================
Polymorphism means "many forms" - the ability of objects of different types
to respond to the same interface/method call in their own way.
"""


# ============================================================
# 1. BASIC POLYMORPHISM WITH METHODS
# ============================================================

class Animal:
    """Base class demonstrating polymorphism"""

    def __init__(self, name):
        self.name = name

    def speak(self):
        """Base speak method - will be overridden"""
        return f"{self.name} makes a sound"

    def move(self):
        return f"{self.name} moves somehow"

    def eat(self):
        return f"{self.name} eats food"


class Dog(Animal):
    def speak(self):
        return f"{self.name} says: Woof! Woof!"

    def move(self):
        return f"{self.name} runs on four legs"

    def wag_tail(self):
        return f"{self.name} wags tail happily"


class Cat(Animal):
    def speak(self):
        return f"{self.name} says: Meow!"

    def move(self):
        return f"{self.name} walks silently on four legs"

    def purr(self):
        return f"{self.name} purrs contentedly"


class Bird(Animal):
    def speak(self):
        return f"{self.name} says: Chirp! Chirp!"

    def move(self):
        return f"{self.name} flies through the air"

    def lay_eggs(self):
        return f"{self.name} lays eggs"


class Fish(Animal):
    def speak(self):
        return f"{self.name} makes bubble sounds: Blub blub"

    def move(self):
        return f"{self.name} swims in the water"

    def breathe_underwater(self):
        return f"{self.name} breathes through gills"


# ============================================================
# 2. POLYMORPHISM WITH FUNCTIONS
# ============================================================

def animal_sound(animal):
    """Function that works with any animal object"""
    return animal.speak()


def animal_movement(animal):
    """Function that works with any animal object"""
    return animal.move()


def describe_animal(animal):
    """Function that expects any object with speak() and move()"""
    return f"{animal.speak()} | {animal.move()}"


def process_animals(animals):
    """Process a collection of animals polymorphically"""
    results = []
    for animal in animals:
        results.append({
            'name': animal.name,
            'sound': animal.speak(),
            'movement': animal.move(),
            'type': animal.__class__.__name__
        })
    return results


# ============================================================
# 3. POLYMORPHISM WITH DIFFERENT CLASS HIERARCHIES
# ============================================================

class Shape:
    """Shape base class"""

    def __init__(self, name):
        self.name = name

    def area(self):
        raise NotImplementedError("Subclass must implement area()")

    def perimeter(self):
        raise NotImplementedError("Subclass must implement perimeter()")

    def describe(self):
        return f"{self.name}: Area={self.area():.2f}, Perimeter={self.perimeter():.2f}"


class Rectangle(Shape):
    def __init__(self, width, height):
        super().__init__("Rectangle")
        self.width = width
        self.height = height

    def area(self):
        return self.width * self.height

    def perimeter(self):
        return 2 * (self.width + self.height)


class Circle(Shape):
    def __init__(self, radius):
        super().__init__("Circle")
        self.radius = radius

    def area(self):
        import math
        return math.pi * self.radius ** 2

    def perimeter(self):
        import math
        return 2 * math.pi * self.radius


class Triangle(Shape):
    def __init__(self, side_a, side_b, side_c):
        super().__init__("Triangle")
        self.side_a = side_a
        self.side_b = side_b
        self.side_c = side_c

    def area(self):
        # Heron's formula
        import math
        s = self.perimeter() / 2
        return math.sqrt(s * (s - self.side_a) * (s - self.side_b) * (s - self.side_c))

    def perimeter(self):
        return self.side_a + self.side_b + self.side_c


def print_shape_info(shape):
    """Polymorphic function that works with any Shape"""
    print(f"Shape: {shape.name}")
    print(f"Area: {shape.area():.2f}")
    print(f"Perimeter: {shape.perimeter():.2f}")
    print("-" * 30)


# ============================================================
# 4. OPERATOR OVERLOADING (AD-HOC POLYMORPHISM)
# ============================================================

class Vector:
    """Demonstrates operator overloading - another form of polymorphism"""

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        """Overload + operator"""
        if isinstance(other, Vector):
            return Vector(self.x + other.x, self.y + other.y)
        return NotImplemented

    def __sub__(self, other):
        """Overload - operator"""
        if isinstance(other, Vector):
            return Vector(self.x - other.x, self.y - other.y)
        return NotImplemented

    def __mul__(self, scalar):
        """Overload * operator (scalar multiplication)"""
        if isinstance(scalar, (int, float)):
            return Vector(self.x * scalar, self.y * scalar)
        return NotImplemented

    def __rmul__(self, scalar):
        """Reflected multiplication (scalar * vector)"""
        return self.__mul__(scalar)

    def __eq__(self, other):
        """Overload == operator"""
        if isinstance(other, Vector):
            return self.x == other.x and self.y == other.y
        return False

    def __str__(self):
        return f"Vector({self.x}, {self.y})"

    def __repr__(self):
        return f"Vector({self.x}, {self.y})"

    def magnitude(self):
        import math
        return math.sqrt(self.x ** 2 + self.y ** 2)


# ============================================================
# 5. DUCK TYPING (A FORM OF POLYMORPHISM)
# ============================================================

class Duck:
    def quack(self):
        return "Duck quacking"

    def swim(self):
        return "Duck swimming"


class Person:
    def quack(self):
        return "Person imitating a duck"

    def swim(self):
        return "Person swimming"


class Robot:
    def quack(self):
        return "Robot making quack sounds"

    def swim(self):
        return "Robot swimming in water"


def make_it_quack(obj):
    """Duck typing: if it quacks like a duck, it's a duck"""
    return obj.quack()


def make_it_swim(obj):
    """Works with any object that has swim() method"""
    return obj.swim()


# ============================================================
# 6. POLYMORPHISM WITH ABSTRACT BASE CLASSES
# ============================================================

from abc import ABC, abstractmethod


class PaymentProcessor(ABC):
    """Abstract base class for payment processing"""

    @abstractmethod
    def process_payment(self, amount):
        pass

    @abstractmethod
    def refund(self, transaction_id):
        pass

    @abstractmethod
    def get_status(self, transaction_id):
        pass


class CreditCardProcessor(PaymentProcessor):
    def process_payment(self, amount):
        return f"Processing ${amount} via Credit Card"

    def refund(self, transaction_id):
        return f"Refunding transaction {transaction_id} via Credit Card"

    def get_status(self, transaction_id):
        return f"Credit Card transaction {transaction_id}: COMPLETED"


class PayPalProcessor(PaymentProcessor):
    def process_payment(self, amount):
        return f"Processing ${amount} via PayPal"

    def refund(self, transaction_id):
        return f"Refunding transaction {transaction_id} via PayPal"

    def get_status(self, transaction_id):
        return f"PayPal transaction {transaction_id}: PENDING"


class CryptoProcessor(PaymentProcessor):
    def process_payment(self, amount):
        return f"Processing ${amount} via Cryptocurrency"

    def refund(self, transaction_id):
        return f"Refunding transaction {transaction_id} via Cryptocurrency"

    def get_status(self, transaction_id):
        return f"Crypto transaction {transaction_id}: CONFIRMED"


def process_payment(payment_processor, amount):
    """Polymorphic function that works with any PaymentProcessor"""
    return payment_processor.process_payment(amount)


# ============================================================
# 7. POLYMORPHISM IN COLLECTIONS
# ============================================================

class Employee:
    def __init__(self, name, salary):
        self.name = name
        self.salary = salary

    def work(self):
        return f"{self.name} is working"

    def get_payment(self):
        return f"{self.name} receives ${self.salary}"


class Manager(Employee):
    def __init__(self, name, salary, team_size):
        super().__init__(name, salary)
        self.team_size = team_size

    def work(self):
        return f"{self.name} is managing {self.team_size} people"

    def conduct_meeting(self):
        return f"{self.name} is conducting a meeting"


class Developer(Employee):
    def __init__(self, name, salary, programming_language):
        super().__init__(name, salary)
        self.programming_language = programming_language

    def work(self):
        return f"{self.name} is coding in {self.programming_language}"

    def debug(self):
        return f"{self.name} is debugging code"


class Designer(Employee):
    def __init__(self, name, salary, design_tool):
        super().__init__(name, salary)
        self.design_tool = design_tool

    def work(self):
        return f"{self.name} is designing using {self.design_tool}"

    def create_prototype(self):
        return f"{self.name} is creating a prototype"


def manage_team(employees):
    """Polymorphic function that works with any Employee subclass"""
    results = []
    for employee in employees:
        results.append({
            'name': employee.name,
            'work': employee.work(),
            'payment': employee.get_payment(),
            'type': employee.__class__.__name__
        })
    return results


# ============================================================
# 8. POLYMORPHISM WITH BUILT-IN FUNCTIONS
# ============================================================

class MyNumber:
    def __init__(self, value):
        self.value = value

    def __len__(self):
        """Make object work with len()"""
        return self.value

    def __bool__(self):
        """Make object work with bool() and if statements"""
        return self.value != 0

    def __abs__(self):
        """Make object work with abs()"""
        return abs(self.value)


class MyString:
    def __init__(self, text):
        self.text = text

    def __len__(self):
        return len(self.text)

    def __str__(self):
        return self.text

    def __add__(self, other):
        return MyString(self.text + str(other))


def demonstrate_builtin_polymorphism():
    """Show how built-in functions work polymorphically"""
    print("\n" + "=" * 60)
    print("POLYMORPHISM WITH BUILT-IN FUNCTIONS")
    print("=" * 60)

    # len() works with different types
    print(f"len('hello'): {len('hello')}")
    print(f"len([1,2,3]): {len([1, 2, 3])}")
    print(f"len({'a':1, 'b':2}): {len({'a': 1, 'b': 2})}")
    print(f"len(MyNumber(5)): {len(MyNumber(5))}")
    print(f"len(MyString('test')): {len(MyString('test'))}")

    # bool() works with different types
    print(f"bool(0): {bool(0)}")
    print(f"bool([]): {bool([])}")
    print(f"bool(MyNumber(0)): {bool(MyNumber(0))}")
    print(f"bool(MyNumber(5)): {bool(MyNumber(5))}")


# ============================================================
# 9. PARAMETRIC POLYMORPHISM (GENERICS)
# ============================================================

from typing import TypeVar, List, Generic, Union

T = TypeVar('T')  # Generic type variable


class Stack(Generic[T]):
    """Generic stack class"""

    def __init__(self):
        self.items: List[T] = []

    def push(self, item: T) -> None:
        self.items.append(item)

    def pop(self) -> Union[T, None]:
        if self.is_empty():
            return None
        return self.items.pop()

    def peek(self) -> Union[T, None]:
        if self.is_empty():
            return None
        return self.items[-1]

    def is_empty(self) -> bool:
        return len(self.items) == 0

    def size(self) -> int:
        return len(self.items)

    def __str__(self):
        return f"Stack({self.items})"


def demonstrate_generic_stack():
    """Show polymorphism with generic types"""
    print("\n" + "=" * 60)
    print("PARAMETRIC POLYMORPHISM (GENERICS)")
    print("=" * 60)

    # Stack of integers
    int_stack = Stack[int]()
    int_stack.push(1)
    int_stack.push(2)
    int_stack.push(3)
    print(f"Integer Stack: {int_stack}")
    print(f"Pop: {int_stack.pop()}")

    # Stack of strings
    str_stack = Stack[str]()
    str_stack.push("Hello")
    str_stack.push("World")
    print(f"String Stack: {str_stack}")
    print(f"Pop: {str_stack.pop()}")


# ============================================================
# 10. RUNTIME POLYMORPHISM (DYNAMIC DISPATCH)
# ============================================================

class Computer:
    def execute(self, code):
        return f"Executing: {code}"

    def get_type(self):
        return "General Computer"


class Laptop(Computer):
    def execute(self, code):
        return f"Laptop executing: {code} (portable)"

    def get_type(self):
        return "Laptop"


class Server(Computer):
    def execute(self, code):
        return f"Server executing: {code} (high performance)"

    def get_type(self):
        return "Server"


class Tablet(Computer):
    def execute(self, code):
        return f"Tablet executing: {code} (touch interface)"

    def get_type(self):
        return "Tablet"


def run_computer(computer, code):
    """Polymorphic runtime dispatch"""
    print(f"Running on {computer.get_type()}")
    print(computer.execute(code))


# ============================================================
# 11. POLYMORPHISM WITH CONTEXT MANAGERS
# ============================================================

class FileResource:
    def __enter__(self):
        print("Opening file resource")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        print("Closing file resource")

    def process(self):
        print("Processing file")


class DatabaseResource:
    def __enter__(self):
        print("Connecting to database")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        print("Disconnecting from database")

    def process(self):
        print("Processing database query")


class NetworkResource:
    def __enter__(self):
        print("Opening network connection")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        print("Closing network connection")

    def process(self):
        print("Sending network request")


def use_resource(resource):
    """Works with any context manager"""
    with resource as r:
        r.process()


# ============================================================
# 12. COMPOSITION OVER INHERITANCE (STRATEGY PATTERN)
# ============================================================

class SortStrategy:
    """Strategy interface"""

    def sort(self, data):
        raise NotImplementedError


class BubbleSort(SortStrategy):
    def sort(self, data):
        print("Using Bubble Sort")
        return sorted(data)  # Simplified for demo


class QuickSort(SortStrategy):
    def sort(self, data):
        print("Using Quick Sort")
        return sorted(data)  # Simplified for demo


class MergeSort(SortStrategy):
    def sort(self, data):
        print("Using Merge Sort")
        return sorted(data)  # Simplified for demo


class DataProcessor:
    """Uses composition with different strategies"""

    def __init__(self, strategy: SortStrategy):
        self.strategy = strategy

    def process_data(self, data):
        print(f"Processing: {data}")
        result = self.strategy.sort(data)
        print(f"Result: {result}")
        return result

    def change_strategy(self, strategy):
        self.strategy = strategy


# ============================================================
# COMPREHENSIVE DEMONSTRATION
# ============================================================

def demonstrate_polymorphism():
    """Complete demonstration of polymorphism concepts"""

    print("=" * 70)
    print("COMPREHENSIVE POLYMORPHISM DEMONSTRATION")
    print("=" * 70)

    # 1. Basic Method Polymorphism
    print("\n1. BASIC METHOD POLYMORPHISM")
    print("-" * 50)
    animals = [
        Dog("Buddy"),
        Cat("Whiskers"),
        Bird("Tweety"),
        Fish("Nemo")
    ]

    # All animals respond to the same methods differently
    for animal in animals:
        print(f"{animal.speak():30} | {animal.move()}")

    # 2. Polymorphism with Functions
    print("\n2. POLYMORPHISM WITH FUNCTIONS")
    print("-" * 50)
    for animal in animals:
        print(animal_sound(animal))

    # 3. Different Class Hierarchies
    print("\n3. DIFFERENT CLASS HIERARCHIES")
    print("-" * 50)
    shapes = [
        Rectangle(5, 3),
        Circle(4),
        Triangle(3, 4, 5)
    ]

    for shape in shapes:
        print_shape_info(shape)

    # 4. Operator Overloading
    print("4. OPERATOR OVERLOADING")
    print("-" * 50)
    v1 = Vector(2, 3)
    v2 = Vector(4, 5)
    print(f"v1 = {v1}, v2 = {v2}")
    print(f"v1 + v2 = {v1 + v2}")
    print(f"v1 - v2 = {v1 - v2}")
    print(f"v1 * 3 = {v1 * 3}")
    print(f"2 * v2 = {2 * v2}")
    print(f"v1 == v2: {v1 == v2}")
    print(f"v1 magnitude: {v1.magnitude():.2f}")

    # 5. Duck Typing
    print("\n5. DUCK TYPING")
    print("-" * 50)
    duck = Duck()
    person = Person()
    robot = Robot()

    for obj in [duck, person, robot]:
        print(f"{obj.__class__.__name__}: {make_it_quack(obj)}")

    # 6. Abstract Base Classes
    print("\n6. ABSTRACT BASE CLASSES")
    print("-" * 50)
    payment_processors = [
        CreditCardProcessor(),
        PayPalProcessor(),
        CryptoProcessor()
    ]

    for processor in payment_processors:
        print(process_payment(processor, 100))

    # 7. Polymorphism in Collections
    print("\n7. POLYMORPHISM IN COLLECTIONS")
    print("-" * 50)
    employees = [
        Manager("Alice", 80000, 5),
        Developer("Bob", 70000, "Python"),
        Designer("Carol", 65000, "Figma")
    ]

    results = manage_team(employees)
    for result in results:
        print(f"{result['name']:10} | {result['work']:40} | {result['payment']}")

    # 8. Built-in Functions
    demonstrate_builtin_polymorphism()

    # 9. Generic Stack
    demonstrate_generic_stack()

    # 10. Runtime Polymorphism
    print("\n10. RUNTIME POLYMORPHISM (DYNAMIC DISPATCH)")
    print("-" * 50)
    computers = [
        Laptop(),
        Server(),
        Tablet()
    ]

    for computer in computers:
        run_computer(computer, "print('Hello World')")

    # 11. Context Managers
    print("\n11. POLYMORPHISM WITH CONTEXT MANAGERS")
    print("-" * 50)
    resources = [
        FileResource(),
        DatabaseResource(),
        NetworkResource()
    ]

    for resource in resources:
        use_resource(resource)

    # 12. Strategy Pattern
    print("\n12. STRATEGY PATTERN (COMPOSITION)")
    print("-" * 50)
    data = [5, 2, 8, 1, 9, 3]
    processor = DataProcessor(BubbleSort())
    processor.process_data(data)
    processor.change_strategy(QuickSort())
    processor.process_data(data)

    # 13. Polymorphism Summary
    print("\n" + "=" * 70)
    print("POLYMORPHISM TYPES SUMMARY")
    print("=" * 70)
    print("""
    1. SUBSET POLYMORPHISM (Inheritance-based)
       - Same method name, different implementations in subclasses
       - Example: Dog.speak(), Cat.speak()

    2. AD-HOC POLYMORPHISM (Operator overloading)
       - Same operator works with different types
       - Example: + works with numbers, strings, lists

    3. PARAMETRIC POLYMORPHISM (Generics)
       - Same code works with different types
       - Example: Stack[T] works with any type T

    4. DUCK TYPING (Structural typing)
       - Object's behavior determines its type
       - Example: Any object with quack() method

    5. RUNTIME POLYMORPHISM (Dynamic dispatch)
       - Method resolution at runtime
       - Example: Different computer types executing code

    6. FUNCTION OVERLOADING (Limited in Python)
       - Same function name with different parameters
       - Achieved through default arguments or *args/**kwargs
    """)


# ============================================================
# ADDITIONAL: POLYMORPHISM WITH DECORATORS
# ============================================================

def polymorphic_action(prefix="Action"):
    """Decorator demonstrating polymorphic behavior"""

    def decorator(func):
        def wrapper(self, *args, **kwargs):
            result = func(self, *args, **kwargs)
            return f"{prefix} ({self.__class__.__name__}): {result}"

        return wrapper

    return decorator


class RobotType:
    @polymorphic_action("Moving")
    def move(self):
        return "Moving forward"

    @polymorphic_action("Speaking")
    def speak(self):
        return "Hello world"


class AdvancedRobot(RobotType):
    @polymorphic_action("Moving")
    def move(self):
        return "Moving with AI navigation"

    @polymorphic_action("Speaking")
    def speak(self):
        return "Hello, I am an advanced robot"


def demonstrate_decorator_polymorphism():
    print("\n" + "=" * 60)
    print("DECORATOR-BASED POLYMORPHISM")
    print("=" * 60)

    basic = RobotType()
    advanced = AdvancedRobot()

    print(f"Basic: {basic.move()}")
    print(f"Basic: {basic.speak()}")
    print(f"Advanced: {advanced.move()}")
    print(f"Advanced: {advanced.speak()}")


# ============================================================
# PRACTICAL: POLYMORPHISM IN DATA PROCESSING
# ============================================================

class DataReader:
    def read(self, source):
        raise NotImplementedError


class CSVReader(DataReader):
    def read(self, source):
        print(f"Reading CSV from {source}")
        return [{"name": "John", "age": 30}, {"name": "Jane", "age": 25}]


class JSONReader(DataReader):
    def read(self, source):
        print(f"Reading JSON from {source}")
        return [{"name": "Bob", "age": 35}, {"name": "Alice", "age": 28}]


class XMLReader(DataReader):
    def read(self, source):
        print(f"Reading XML from {source}")
        return [{"name": "Charlie", "age": 40}, {"name": "Diana", "age": 32}]


class DataProcessorPipeline:
    def __init__(self, reader: DataReader):
        self.reader = reader

    def process(self, source):
        data = self.reader.read(source)
        processed = self._transform(data)
        self._save(processed)
        return processed

    def _transform(self, data):
        print("Transforming data...")
        for record in data:
            if 'age' in record:
                record['age'] = record['age'] + 1
        return data

    def _save(self, data):
        print(f"Saving {len(data)} records...")
        return True


def demonstrate_data_processing():
    print("\n" + "=" * 60)
    print("POLYMORPHISM IN DATA PROCESSING")
    print("=" * 60)

    for reader_class in [CSVReader, JSONReader, XMLReader]:
        reader = reader_class()
        pipeline = DataProcessorPipeline(reader)
        result = pipeline.process("data_source")
        print(f"Processed: {result}\n")


# ============================================================
# MAIN EXECUTION
# ============================================================

if __name__ == "__main__":
    # Run main demonstration
    demonstrate_polymorphism()

    # Additional demonstrations
    demonstrate_decorator_polymorphism()
    demonstrate_data_processing()

    # Final summary
    print("\n" + "=" * 70)
    print("POLYMORPHISM KEY BENEFITS")
    print("=" * 70)
    print("""
    ✅ CODE REUSABILITY: Write once, use with many types
    ✅ FLEXIBILITY: Add new types without changing existing code
    ✅ MAINTAINABILITY: Change behavior in one place
    ✅ EXTENSIBILITY: Easy to extend with new classes
    ✅ ABSTRACTION: Hide implementation details
    ✅ INTERFACE CONSISTENCY: Same method names across classes

    PYTHON'S POLYMORPHISM POWER COMES FROM:
    • Duck typing
    • Dynamic method resolution
    • Operator overloading
    • Abstract base classes
    • Protocol classes (Python 3.8+)
    • Type hints and generics
    """)

    print("=" * 70)
    print("✅ POLYMORPHISM DEMONSTRATION COMPLETE!")
    print("=" * 70)