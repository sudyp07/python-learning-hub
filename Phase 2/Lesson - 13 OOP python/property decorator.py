"""
COMPREHENSIVE GUIDE TO @PROPERTY DECORATOR IN PYTHON
=====================================================
The @property decorator allows you to define methods that can be accessed
like attributes, enabling controlled access to instance attributes with
getters, setters, and deleters.
"""


# ============================================================
# 1. BASIC PROPERTY DECORATOR (GETTER)
# ============================================================

class Person:
    """Basic class using property decorator"""

    def __init__(self, first_name, last_name):
        self._first_name = first_name  # Convention: protected attribute
        self._last_name = last_name

    @property
    def full_name(self):
        """Getter: returns the full name"""
        return f"{self._first_name} {self._last_name}"

    @property
    def first_name(self):
        """Getter for first name"""
        return self._first_name

    @property
    def last_name(self):
        """Getter for last name"""
        return self._last_name


# ============================================================
# 2. PROPERTY WITH SETTER AND DELETER
# ============================================================

class Employee:
    """Class demonstrating full property usage"""

    def __init__(self, name, salary):
        self._name = name
        self._salary = salary
        self._email = None

    @property
    def name(self):
        """Getter for name"""
        return self._name

    @name.setter
    def name(self, value):
        """Setter for name with validation"""
        if not value or not isinstance(value, str):
            raise ValueError("Name must be a non-empty string")
        self._name = value.strip()

    @property
    def salary(self):
        """Getter for salary"""
        return self._salary

    @salary.setter
    def salary(self, value):
        """Setter for salary with validation"""
        if not isinstance(value, (int, float)):
            raise TypeError("Salary must be a number")
        if value < 0:
            raise ValueError("Salary cannot be negative")
        if value > 1000000:
            raise ValueError("Salary exceeds maximum allowed")
        self._salary = value

    @property
    def email(self):
        """Getter for email (computed property)"""
        if self._email:
            return self._email
        return f"{self._name.lower().replace(' ', '.')}@company.com"

    @email.setter
    def email(self, value):
        """Setter for email with validation"""
        if not value or '@' not in value:
            raise ValueError("Invalid email address")
        self._email = value

    @email.deleter
    def email(self):
        """Deleter for email"""
        print(f"Deleting email for {self._name}")
        self._email = None

    @property
    def annual_salary(self):
        """Computed property: annual salary"""
        return self._salary * 12

    @property
    def tax(self):
        """Computed property: tax calculation"""
        if self._salary < 5000:
            rate = 0.1
        elif self._salary < 10000:
            rate = 0.2
        else:
            rate = 0.3
        return self._salary * rate


# ============================================================
# 3. REAL-WORLD: USER MANAGEMENT WITH PROPERTIES
# ============================================================

import re
from datetime import datetime, date


class User:
    """User class with comprehensive property usage"""

    def __init__(self, username, email, password, birth_date):
        self._username = None
        self._email = None
        self._password = None
        self._birth_date = None
        self._is_active = True
        self._created_at = datetime.now()

        # Use setters for validation
        self.username = username
        self.email = email
        self.password = password
        self.birth_date = birth_date

    @property
    def username(self):
        """Get username"""
        return self._username

    @username.setter
    def username(self, value):
        """Set username with validation"""
        if not value or len(value) < 3:
            raise ValueError("Username must be at least 3 characters")
        if not re.match(r'^[a-zA-Z0-9_]+$', value):
            raise ValueError("Username can only contain letters, numbers, and underscore")
        self._username = value

    @property
    def email(self):
        """Get email"""
        return self._email

    @email.setter
    def email(self, value):
        """Set email with validation"""
        if not value or '@' not in value or '.' not in value:
            raise ValueError("Invalid email address")
        # Simple email validation
        local, domain = value.split('@')
        if not local or not domain or '.' not in domain:
            raise ValueError("Invalid email format")
        self._email = value.lower()

    @property
    def password(self):
        """Password getter (security: raise error)"""
        raise AttributeError("Password is not readable for security reasons")

    @password.setter
    def password(self, value):
        """Set password with strength validation"""
        if not value or len(value) < 8:
            raise ValueError("Password must be at least 8 characters")
        if not any(c.isupper() for c in value):
            raise ValueError("Password must contain at least one uppercase letter")
        if not any(c.islower() for c in value):
            raise ValueError("Password must contain at least one lowercase letter")
        if not any(c.isdigit() for c in value):
            raise ValueError("Password must contain at least one digit")
        # In real application, you would hash the password
        self._password = value  # Store hashed version in real app

    @property
    def birth_date(self):
        """Get birth date"""
        return self._birth_date

    @birth_date.setter
    def birth_date(self, value):
        """Set birth date with age validation"""
        if isinstance(value, str):
            value = datetime.strptime(value, '%Y-%m-%d').date()
        elif not isinstance(value, date):
            raise TypeError("Birth date must be a date object")

        # Calculate age
        today = date.today()
        age = today.year - value.year - ((today.month, today.day) < (value.month, value.day))

        if age < 13:
            raise ValueError("User must be at least 13 years old")
        if age > 120:
            raise ValueError("Invalid birth date")
        self._birth_date = value

    @property
    def age(self):
        """Computed property: age"""
        if not self._birth_date:
            return None
        today = date.today()
        return today.year - self._birth_date.year - (
                (today.month, today.day) < (self._birth_date.month, self._birth_date.day)
        )

    @property
    def is_active(self):
        """Get active status"""
        return self._is_active

    @is_active.setter
    def is_active(self, value):
        """Set active status"""
        if not isinstance(value, bool):
            raise TypeError("is_active must be a boolean")
        self._is_active = value

    @property
    def account_age_days(self):
        """Computed property: account age in days"""
        delta = datetime.now() - self._created_at
        return delta.days

    @property
    def profile_summary(self):
        """Computed property: summary of user profile"""
        return {
            'username': self._username,
            'email': self._email,
            'age': self.age,
            'active': self._is_active,
            'account_age_days': self.account_age_days
        }

    def __str__(self):
        return f"User(username='{self._username}', email='{self._email}')"


# ============================================================
# 4. PROPERTY WITH CACHING AND LAZY EVALUATION
# ============================================================

import time
import math


class DataProcessor:
    """Class demonstrating lazy loading and caching with properties"""

    def __init__(self, data):
        self.data = data
        self._processed_data = None
        self._stats = None

    @property
    def processed_data(self):
        """Lazy load: process data only when needed"""
        if self._processed_data is None:
            print("Processing data... (lazy loading)")
            time.sleep(1)  # Simulate expensive operation
            self._processed_data = [x * 2 for x in self.data]
        return self._processed_data

    @property
    def stats(self):
        """Lazy load: compute statistics only when needed"""
        if self._stats is None:
            print("Computing statistics... (lazy loading)")
            time.sleep(0.5)  # Simulate expensive operation
            data = self.data
            self._stats = {
                'sum': sum(data),
                'mean': sum(data) / len(data),
                'min': min(data),
                'max': max(data),
                'count': len(data),
                'range': max(data) - min(data),
                'variance': sum((x - sum(data) / len(data)) ** 2 for x in data) / len(data),
                'std_dev': math.sqrt(sum((x - sum(data) / len(data)) ** 2 for x in data) / len(data))
            }
        return self._stats

    @property
    def square_root_sum(self):
        """Property with expensive computation"""
        print("Calculating square root sum...")
        return sum(math.sqrt(x) for x in self.data)

    def clear_cache(self):
        """Clear cached property values"""
        self._processed_data = None
        self._stats = None
        print("Cache cleared")


# ============================================================
# 5. PROPERTY WITH CLASS-LEVEL DATA
# ============================================================

class Product:
    """Product class with class-level property"""
    _discount_rate = 0.1  # Class variable
    _tax_rate = 0.08

    def __init__(self, name, price, category):
        self.name = name
        self._price = price
        self.category = category

    @property
    def price(self):
        """Get price with tax"""
        return self._price

    @price.setter
    def price(self, value):
        """Set price with validation"""
        if value < 0:
            raise ValueError("Price cannot be negative")
        self._price = value

    @property
    def price_with_tax(self):
        """Compute price with tax"""
        return self._price * (1 + self._tax_rate)

    @property
    def discounted_price(self):
        """Compute discounted price"""
        return self._price * (1 - self._discount_rate)

    @property
    def final_price(self):
        """Compute final price with discount and tax"""
        return self.discounted_price * (1 + self._tax_rate)

    @classmethod
    @property
    def discount_rate(cls):
        """Class-level property getter"""
        return cls._discount_rate

    @discount_rate.setter
    def discount_rate(cls, value):
        """Class-level property setter"""
        if not 0 <= value <= 1:
            raise ValueError("Discount rate must be between 0 and 1")
        cls._discount_rate = value

    @classmethod
    @property
    def tax_rate(cls):
        """Class-level property getter"""
        return cls._tax_rate

    @tax_rate.setter
    def tax_rate(cls, value):
        """Class-level property setter"""
        if not 0 <= value <= 1:
            raise ValueError("Tax rate must be between 0 and 1")
        cls._tax_rate = value


# ============================================================
# 6. READ-ONLY PROPERTIES
# ============================================================

class ImmutablePoint:
    """Class demonstrating read-only properties"""

    def __init__(self, x, y):
        self._x = x
        self._y = y
        self._created_at = datetime.now()

    @property
    def x(self):
        """Read-only x coordinate"""
        return self._x

    @property
    def y(self):
        """Read-only y coordinate"""
        return self._y

    @property
    def created_at(self):
        """Read-only creation timestamp"""
        return self._created_at

    @property
    def distance_from_origin(self):
        """Computed read-only property"""
        return math.sqrt(self._x ** 2 + self._y ** 2)

    @property
    def coordinates(self):
        """Tuple of coordinates (read-only)"""
        return (self._x, self._y)


# ============================================================
# 7. PROPERTY WITH DEPENDENCY TRACKING
# ============================================================

class Rectangle:
    """Rectangle with dependent properties"""

    def __init__(self, width, height):
        self._width = width
        self._height = height
        self._area = None
        self._perimeter = None
        self._diagonal = None
        self._dirty = True  # Track if values need recalculation

    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, value):
        if value <= 0:
            raise ValueError("Width must be positive")
        self._width = value
        self._dirty = True  # Mark as dirty when changed

    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, value):
        if value <= 0:
            raise ValueError("Height must be positive")
        self._height = value
        self._dirty = True  # Mark as dirty when changed

    @property
    def area(self):
        """Area with caching and dependency tracking"""
        if self._dirty or self._area is None:
            print("Recalculating area...")
            self._area = self._width * self._height
            self._dirty = False
        return self._area

    @property
    def perimeter(self):
        """Perimeter with caching and dependency tracking"""
        if self._dirty or self._perimeter is None:
            print("Recalculating perimeter...")
            self._perimeter = 2 * (self._width + self._height)
        return self._perimeter

    @property
    def diagonal(self):
        """Diagonal with caching and dependency tracking"""
        if self._dirty or self._diagonal is None:
            print("Recalculating diagonal...")
            self._diagonal = math.sqrt(self._width ** 2 + self._height ** 2)
        return self._diagonal

    @property
    def is_square(self):
        """Check if rectangle is a square (computed)"""
        return self._width == self._height


# ============================================================
# 8. PROPERTY WITH VALIDATION CHAIN
# ============================================================

class BankAccount:
    """Bank account with comprehensive validation"""

    def __init__(self, account_number, owner, balance=0):
        self._account_number = None
        self._owner = None
        self._balance = 0
        self._transactions = []

        # Use property setters for validation
        self.account_number = account_number
        self.owner = owner
        self.balance = balance

    @property
    def account_number(self):
        return self._account_number

    @account_number.setter
    def account_number(self, value):
        """Validate account number"""
        if not value or len(value) < 8:
            raise ValueError("Account number must be at least 8 characters")
        if not value.isdigit():
            raise ValueError("Account number must contain only digits")
        self._account_number = value

    @property
    def owner(self):
        return self._owner

    @owner.setter
    def owner(self, value):
        """Validate owner name"""
        if not value or len(value.strip()) < 2:
            raise ValueError("Owner name must be at least 2 characters")
        self._owner = value.strip()

    @property
    def balance(self):
        return self._balance

    @balance.setter
    def balance(self, value):
        """Validate balance"""
        if not isinstance(value, (int, float)):
            raise TypeError("Balance must be a number")
        if value < 0:
            raise ValueError("Balance cannot be negative")
        self._balance = value

    @property
    def transaction_count(self):
        """Number of transactions"""
        return len(self._transactions)

    @property
    def total_deposits(self):
        """Total deposits made"""
        return sum(t['amount'] for t in self._transactions if t['type'] == 'deposit')

    @property
    def total_withdrawals(self):
        """Total withdrawals made"""
        return sum(t['amount'] for t in self._transactions if t['type'] == 'withdrawal')

    @property
    def average_transaction(self):
        """Average transaction amount"""
        if not self._transactions:
            return 0
        return sum(t['amount'] for t in self._transactions) / len(self._transactions)

    def deposit(self, amount):
        """Deposit money with validation"""
        if amount <= 0:
            raise ValueError("Deposit amount must be positive")
        self._balance += amount
        self._transactions.append({
            'type': 'deposit',
            'amount': amount,
            'date': datetime.now(),
            'balance_after': self._balance
        })
        return f"Deposited ${amount:.2f}. New balance: ${self._balance:.2f}"

    def withdraw(self, amount):
        """Withdraw money with validation"""
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive")
        if amount > self._balance:
            raise ValueError("Insufficient funds")
        self._balance -= amount
        self._transactions.append({
            'type': 'withdrawal',
            'amount': amount,
            'date': datetime.now(),
            'balance_after': self._balance
        })
        return f"Withdrew ${amount:.2f}. New balance: ${self._balance:.2f}"


# ============================================================
# 9. PROPERTY WITH DYNAMIC BEHAVIOR
# ============================================================

class DynamicProperty:
    """Class with dynamic property behavior"""

    def __init__(self, **kwargs):
        self._data = kwargs

    @property
    def keys(self):
        """Get all keys"""
        return list(self._data.keys())

    @property
    def values(self):
        """Get all values"""
        return list(self._data.values())

    @property
    def items(self):
        """Get all items"""
        return list(self._data.items())

    @property
    def count(self):
        """Get number of items"""
        return len(self._data)

    @property
    def is_empty(self):
        """Check if empty"""
        return len(self._data) == 0

    @property
    def first_item(self):
        """Get first item"""
        if self._data:
            return next(iter(self._data.items()))
        return None

    @property
    def last_item(self):
        """Get last item"""
        if self._data:
            return next(reversed(self._data.items()))
        return None

    def get(self, key, default=None):
        """Get value by key"""
        return self._data.get(key, default)

    def set(self, key, value):
        """Set value by key"""
        self._data[key] = value
        return self


# ============================================================
# 10. PROPERTY DECORATOR WITH INHERITANCE
# ============================================================

class Vehicle:
    """Base class with properties"""

    def __init__(self, make, model, year):
        self._make = make
        self._model = model
        self._year = year

    @property
    def make(self):
        return self._make

    @property
    def model(self):
        return self._model

    @property
    def year(self):
        return self._year

    @property
    def description(self):
        return f"{self._year} {self._make} {self._model}"

    @property
    def age(self):
        return datetime.now().year - self._year


class Car(Vehicle):
    """Car class extending Vehicle"""

    def __init__(self, make, model, year, fuel_type, engine_size):
        super().__init__(make, model, year)
        self._fuel_type = fuel_type
        self._engine_size = engine_size
        self._mileage = 0

    @property
    def fuel_type(self):
        return self._fuel_type

    @fuel_type.setter
    def fuel_type(self, value):
        valid_fuels = ['Gasoline', 'Diesel', 'Electric', 'Hybrid']
        if value not in valid_fuels:
            raise ValueError(f"Fuel type must be one of {valid_fuels}")
        self._fuel_type = value

    @property
    def engine_size(self):
        return self._engine_size

    @property
    def mileage(self):
        return self._mileage

    @mileage.setter
    def mileage(self, value):
        if value < self._mileage:
            raise ValueError("Mileage cannot decrease")
        self._mileage = value

    @property
    def description(self):
        """Override parent property"""
        base_desc = super().description
        return f"{base_desc} ({self._fuel_type}, {self._engine_size}L)"


# ============================================================
# 11. PROPERTY FOR COMPUTED FIELDS IN DATABASE MODELS
# ============================================================

class Order:
    """Order class with computed fields"""

    def __init__(self, order_id, customer):
        self.order_id = order_id
        self.customer = customer
        self.items = []  # List of (item, quantity, price) tuples
        self._status = "Pending"
        self._created_at = datetime.now()

    def add_item(self, item, quantity, price):
        """Add item to order"""
        self.items.append({
            'item': item,
            'quantity': quantity,
            'price': price
        })

    @property
    def subtotal(self):
        """Subtotal before tax and shipping"""
        return sum(item['quantity'] * item['price'] for item in self.items)

    @property
    def tax(self):
        """Calculate tax (10% of subtotal)"""
        return self.subtotal * 0.1

    @property
    def shipping_cost(self):
        """Calculate shipping cost based on order value"""
        if self.subtotal > 100:
            return 0  # Free shipping
        elif self.subtotal > 50:
            return 10
        else:
            return 20

    @property
    def total(self):
        """Total order value"""
        return self.subtotal + self.tax + self.shipping_cost

    @property
    def item_count(self):
        """Total number of items"""
        return sum(item['quantity'] for item in self.items)

    @property
    def unique_items(self):
        """Number of unique items"""
        return len(self.items)

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, value):
        valid_statuses = ['Pending', 'Processing', 'Shipped', 'Delivered', 'Cancelled']
        if value not in valid_statuses:
            raise ValueError(f"Invalid status. Must be one of {valid_statuses}")
        self._status = value

    @property
    def age_in_hours(self):
        """Age of order in hours"""
        delta = datetime.now() - self._created_at
        return delta.total_seconds() / 3600


# ============================================================
# DEMONSTRATION AND USAGE
# ============================================================

def demonstrate_property():
    """Comprehensive demonstration of @property decorator"""

    print("=" * 70)
    print("PROPERTY DECORATOR COMPREHENSIVE DEMONSTRATION")
    print("=" * 70)

    # 1. Basic Property
    print("\n1. BASIC PROPERTY (GETTER)")
    print("-" * 50)
    person = Person("John", "Doe")
    print(f"First name: {person.first_name}")
    print(f"Last name: {person.last_name}")
    print(f"Full name: {person.full_name}")

    # 2. Property with Setter and Deleter
    print("\n2. PROPERTY WITH SETTER AND DELETER")
    print("-" * 50)
    employee = Employee("Alice Smith", 50000)
    print(f"Name: {employee.name}")
    print(f"Salary: ${employee.salary}")
    print(f"Annual Salary: ${employee.annual_salary}")
    print(f"Tax: ${employee.tax}")
    print(f"Email: {employee.email}")

    # Update email
    employee.email = "alice.smith@company.com"
    print(f"Updated Email: {employee.email}")

    # Update salary with validation
    try:
        employee.salary = 75000
        print(f"Updated Salary: ${employee.salary}")
    except ValueError as e:
        print(f"Error: {e}")

    # Delete email
    del employee.email
    print(f"Email after deletion: {employee.email}")

    # 3. User Management
    print("\n3. USER MANAGEMENT WITH PROPERTIES")
    print("-" * 50)
    try:
        user = User(
            username="john_doe",
            email="john@example.com",
            password="SecurePass123",
            birth_date="2000-01-15"
        )
        print(f"User created: {user}")
        print(f"Age: {user.age}")
        print(f"Account age: {user.account_age_days} days")
        print(f"Active: {user.is_active}")
        print(f"Profile: {user.profile_summary}")

        # Try to access password (should raise error)
        try:
            print(f"Password: {user.password}")
        except AttributeError as e:
            print(f"Security: {e}")

        # Try invalid username
        try:
            user.username = "ab"  # Too short
        except ValueError as e:
            print(f"Validation error: {e}")

    except ValueError as e:
        print(f"Error creating user: {e}")

    # 4. Lazy Loading and Caching
    print("\n4. LAZY LOADING AND CACHING")
    print("-" * 50)
    processor = DataProcessor([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])

    # First access (computes)
    print(f"Processed data: {processor.processed_data}")

    # Second access (cached)
    print(f"Processed data (cached): {processor.processed_data}")

    # Stats (computes)
    print(f"Stats: {processor.stats}")

    # Clear cache
    processor.clear_cache()
    print(f"Processed data after clearing: {processor.processed_data}")

    # 5. Class-level Properties
    print("\n5. CLASS-LEVEL PROPERTIES")
    print("-" * 50)
    product = Product("Laptop", 1000, "Electronics")
    print(f"Price: ${product.price}")
    print(f"Price with tax: ${product.price_with_tax:.2f}")
    print(f"Discounted price: ${product.discounted_price:.2f}")
    print(f"Final price: ${product.final_price:.2f}")

    # Change global discount
    Product.discount_rate = 0.2
    print(f"New discount rate: {Product.discount_rate}")
    print(f"New final price: ${product.final_price:.2f}")

    # 6. Read-only Properties
    print("\n6. READ-ONLY PROPERTIES")
    print("-" * 50)
    point = ImmutablePoint(3, 4)
    print(f"Coordinates: ({point.x}, {point.y})")
    print(f"Distance from origin: {point.distance_from_origin:.2f}")
    print(f"Created at: {point.created_at}")

    # Try to modify (will fail)
    try:
        point.x = 5
    except AttributeError as e:
        print(f"Cannot modify: {e}")

    # 7. Dependency Tracking
    print("\n7. DEPENDENCY TRACKING WITH CACHING")
    print("-" * 50)
    rect = Rectangle(4, 5)
    print(f"Area: {rect.area}")  # Calculates
    print(f"Area (cached): {rect.area}")  # Uses cache
    print(f"Perimeter: {rect.perimeter}")  # Calculates

    # Change width (marks dirty)
    rect.width = 6
    print(f"Width changed to {rect.width}")
    print(f"Area (recalculated): {rect.area}")  # Recalculates
    print(f"Is square: {rect.is_square}")

    # 8. Validation Chain
    print("\n8. VALIDATION CHAIN")
    print("-" * 50)
    account = BankAccount("12345678", "John Smith", 1000)
    print(f"Account: {account.account_number}")
    print(f"Owner: {account.owner}")
    print(f"Balance: ${account.balance:.2f}")

    account.deposit(500)
    account.withdraw(200)

    print(f"Transaction count: {account.transaction_count}")
    print(f"Total deposits: ${account.total_deposits:.2f}")
    print(f"Total withdrawals: ${account.total_withdrawals:.2f}")
    print(f"Average transaction: ${account.average_transaction:.2f}")

    # 9. Dynamic Properties
    print("\n9. DYNAMIC PROPERTIES")
    print("-" * 50)
    dynamic = DynamicProperty(name="Test", value=42, active=True)
    print(f"Keys: {dynamic.keys}")
    print(f"Values: {dynamic.values}")
    print(f"Items: {dynamic.items}")
    print(f"Count: {dynamic.count}")
    print(f"Empty: {dynamic.is_empty}")
    print(f"First item: {dynamic.first_item}")
    print(f"Last item: {dynamic.last_item}")

    # 10. Inheritance with Properties
    print("\n10. INHERITANCE WITH PROPERTIES")
    print("-" * 50)
    car = Car("Toyota", "Camry", 2021, "Hybrid", 2.5)
    print(f"Description: {car.description}")
    print(f"Fuel type: {car.fuel_type}")
    print(f"Engine size: {car.engine_size}L")
    print(f"Age: {car.age} years")

    car.mileage = 15000
    print(f"Mileage: {car.mileage} miles")

    # 11. Computed Fields
    print("\n11. COMPUTED FIELDS (Order System)")
    print("-" * 50)
    order = Order("ORD-001", "Jane Doe")
    order.add_item("Laptop", 1, 999.99)
    order.add_item("Mouse", 2, 24.99)
    order.add_item("Keyboard", 1, 49.99)

    print(f"Order ID: {order.order_id}")
    print(f"Customer: {order.customer}")
    print(f"Subtotal: ${order.subtotal:.2f}")
    print(f"Tax (10%): ${order.tax:.2f}")
    print(f"Shipping: ${order.shipping_cost:.2f}")
    print(f"Total: ${order.total:.2f}")
    print(f"Total items: {order.item_count}")
    print(f"Unique items: {order.unique_items}")
    print(f"Status: {order.status}")

    # Update status
    order.status = "Processing"
    print(f"Updated status: {order.status}")

    # 12. Property Performance Comparison
    print("\n12. PROPERTY PERFORMANCE COMPARISON")
    print("-" * 50)

    class DirectAccess:
        def __init__(self, value):
            self.value = value

    class PropertyAccess:
        def __init__(self, value):
            self._value = value

        @property
        def value(self):
            return self._value

    # Direct vs Property access
    direct = DirectAccess(42)
    prop = PropertyAccess(42)

    import timeit

    direct_time = timeit.timeit('direct.value', globals=locals(), number=1000000)
    prop_time = timeit.timeit('prop.value', globals=locals(), number=1000000)

    print(f"Direct access: {direct_time:.4f} seconds")
    print(f"Property access: {prop_time:.4f} seconds")
    print(f"Difference: {prop_time - direct_time:.4f} seconds (property is slightly slower but safer)")


# ============================================================
# ADDITIONAL: PROPERTY DECORATOR WITH DESCRIPTORS
# ============================================================

class ValidatedProperty:
    """Custom descriptor for property validation"""

    def __init__(self, validator=None):
        self.validator = validator
        self._data = {}

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        return self._data.get(id(obj), None)

    def __set__(self, obj, value):
        if self.validator and not self.validator(value):
            raise ValueError(f"Invalid value: {value}")
        self._data[id(obj)] = value

    def __delete__(self, obj):
        del self._data[id(obj)]


class PersonWithDescriptor:
    """Class using custom descriptor for validation"""
    age = ValidatedProperty(lambda x: isinstance(x, int) and 0 <= x <= 150)
    salary = ValidatedProperty(lambda x: isinstance(x, (int, float)) and x >= 0)

    def __init__(self, name, age, salary):
        self.name = name
        self.age = age
        self.salary = salary

    @property
    def is_adult(self):
        return self.age >= 18

    @property
    def annual_salary(self):
        return self.salary * 12


# ============================================================
# MAIN EXECUTION
# ============================================================

if __name__ == "__main__":
    # Run main demonstration
    demonstrate_property()

    # Additional descriptor demo
    print("\n" + "=" * 70)
    print("PROPERTY WITH DESCRIPTORS")
    print("=" * 70)

    try:
        person_desc = PersonWithDescriptor("Alice", 30, 50000)
        print(f"Name: {person_desc.name}")
        print(f"Age: {person_desc.age}")
        print(f"Salary: ${person_desc.salary}")
        print(f"Annual Salary: ${person_desc.annual_salary}")
        print(f"Is adult: {person_desc.is_adult}")

        # Try invalid age
        try:
            person_desc.age = 200  # Invalid
        except ValueError as e:
            print(f"Error: {e}")

    except ValueError as e:
        print(f"Error: {e}")

    # Summary
    print("\n" + "=" * 70)
    print("@PROPERTY DECORATOR KEY CONCEPTS")
    print("=" * 70)
    print("""
    ✅ WHAT @PROPERTY DOES
       - Allows method to be accessed like an attribute
       - Enables controlled access to instance attributes
       - Provides getter, setter, and deleter functionality

    ✅ BENEFITS
       - Encapsulation: Hide internal implementation
       - Validation: Ensure data integrity
       - Computed Properties: Dynamic values
       - Lazy Loading: Compute only when needed
       - Caching: Improve performance
       - Backward Compatibility: Change implementation without breaking API

    ✅ SYNTAX
       @property
       def method(self):
           return self._attribute

       @method.setter
       def method(self, value):
           self._attribute = value

       @method.deleter
       def method(self):
           del self._attribute

    ✅ BEST PRACTICES
       - Use for computed properties
       - Validate data in setters
       - Use for read-only attributes
       - Implement lazy loading for expensive operations
       - Cache results when appropriate
       - Use consistent naming (_attribute for backing field)
       - Don't overuse - simple attributes don't need properties

    ✅ COMMON USE CASES
       - Data validation
       - Computed fields (age, total, average)
       - Lazy loading of expensive data
       - Read-only attributes (ID, creation date)
       - Security (password hashing)
       - API compatibility
       - Database model fields       - User preferences

    ✅ PERFORMANCE
       - Slightly slower than direct attribute access
       - Caching can improve performance for expensive computations
       - Use for meaningful operations, not just simple getters/setters

    ✅ VS DESCRIPTORS
       - @property: Per-instance, simpler
       - Descriptors: Class-level, reusable, more complex
    """)

    print("=" * 70)
    print("✅ PROPERTY DECORATOR DEMONSTRATION COMPLETE!")
    print("=" * 70)