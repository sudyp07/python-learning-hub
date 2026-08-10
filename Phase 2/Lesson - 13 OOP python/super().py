"""
COMPREHENSIVE GUIDE TO super() IN PYTHON
=========================================
super() is used to call methods from parent classes. It's essential for:
- Proper inheritance
- Method overriding
- Multiple inheritance (MRO)
- Avoiding diamond problem
- Maintaining code flexibility
"""


# ============================================================
# 1. BASIC super() USAGE
# ============================================================

class Animal:
    """Base class"""

    def __init__(self, name, species):
        self.name = name
        self.species = species
        print(f"Animal __init__ called for {name}")

    def speak(self):
        return f"{self.name} makes a sound"

    def get_info(self):
        return f"Animal: {self.name}, Species: {self.species}"


class Dog(Animal):
    """Child class using super()"""

    def __init__(self, name, breed):
        # Call parent __init__ with super()
        super().__init__(name, "Canine")
        self.breed = breed
        print(f"Dog __init__ called for {name}")

    def speak(self):
        # Call parent method and add to it
        base_sound = super().speak()
        return f"{base_sound} - actually barks: Woof!"

    def get_info(self):
        # Extend parent method
        base_info = super().get_info()
        return f"{base_info}, Breed: {self.breed}"


# ============================================================
# 2. super() IN MULTI-LEVEL INHERITANCE
# ============================================================

class Mammal(Animal):
    """Intermediate class"""

    def __init__(self, name, species, has_fur=True):
        super().__init__(name, species)
        self.has_fur = has_fur
        print(f"Mammal __init__ called for {name}")

    def feed_milk(self):
        return f"{self.name} feeds milk to babies"

    def get_info(self):
        base_info = super().get_info()
        return f"{base_info}, Fur: {self.has_fur}"


class Cat(Mammal):
    """Further inheritance"""

    def __init__(self, name, breed, is_indoor=True):
        super().__init__(name, "Feline", True)
        self.breed = breed
        self.is_indoor = is_indoor
        print(f"Cat __init__ called for {name}")

    def speak(self):
        return f"{self.name} says: Meow!"

    def get_info(self):
        base_info = super().get_info()
        return f"{base_info}, Breed: {self.breed}, Indoor: {self.is_indoor}"


# ============================================================
# 3. super() WITH MULTIPLE INHERITANCE (DIAMOND PROBLEM)
# ============================================================

class A:
    """Base class A"""

    def __init__(self):
        print("A __init__ called")
        self.value_a = "A value"

    def method(self):
        print("A.method() called")
        return "A"


class B(A):
    """Class B inherits from A"""

    def __init__(self):
        print("B __init__ called")
        super().__init__()
        self.value_b = "B value"

    def method(self):
        print("B.method() called")
        return super().method() + " -> B"


class C(A):
    """Class C inherits from A"""

    def __init__(self):
        print("C __init__ called")
        super().__init__()
        self.value_c = "C value"

    def method(self):
        print("C.method() called")
        return super().method() + " -> C"


class D(B, C):
    """Class D inherits from B and C (Multiple Inheritance)"""

    def __init__(self):
        print("D __init__ called")
        # super() follows MRO
        super().__init__()
        self.value_d = "D value"

    def method(self):
        print("D.method() called")
        return super().method() + " -> D"


# ============================================================
# 4. super() WITH DIFFERENT ARGUMENTS
# ============================================================

class Parent:
    def __init__(self, name, age, *args, **kwargs):
        self.name = name
        self.age = age
        print(f"Parent init: name={name}, age={age}")

    def display(self):
        return f"Name: {self.name}, Age: {self.age}"


class Child(Parent):
    def __init__(self, name, age, grade, *args, **kwargs):
        # Using super() with different arguments
        super().__init__(name, age, *args, **kwargs)
        self.grade = grade
        print(f"Child init: grade={grade}")

    def display(self):
        # Call parent method and extend
        parent_info = super().display()
        return f"{parent_info}, Grade: {self.grade}"


class GrandChild(Child):
    def __init__(self, name, age, grade, hobby, *args, **kwargs):
        # Pass extra arguments up the chain
        super().__init__(name, age, grade, *args, **kwargs)
        self.hobby = hobby
        print(f"GrandChild init: hobby={hobby}")

    def display(self):
        parent_info = super().display()
        return f"{parent_info}, Hobby: {self.hobby}"


# ============================================================
# 5. super() WITHOUT ARGUMENTS (Python 3 only)
# ============================================================

class Base:
    def method(self):
        print("Base.method()")
        return "Base"


class Derived(Base):
    def method(self):
        print("Derived.method()")
        # In Python 3, super() is equivalent to super(Derived, self)
        return super().method() + " -> Derived"


class Derived2(Derived):
    def method(self):
        print("Derived2.method()")
        # super() automatically knows the current class and instance
        return super().method() + " -> Derived2"


# ============================================================
# 6. super() IN CLASSMETHODS AND STATICMETHODS
# ============================================================

class ClassBase:
    @classmethod
    def factory(cls, *args):
        print(f"ClassBase.factory called from {cls.__name__}")
        return cls(*args)

    @staticmethod
    def static_info():
        return "Base static info"


class ClassDerived(ClassBase):
    @classmethod
    def factory(cls, *args):
        print(f"ClassDerived.factory called from {cls.__name__}")
        # super() works in classmethods too
        return super().factory(*args)

    @staticmethod
    def static_info():
        base_info = ClassBase.static_info()
        return f"{base_info} -> Derived static info"


# ============================================================
# 7. super() WITH PROPERTY GETTERS/SETTERS
# ============================================================

class Product:
    def __init__(self, name, price):
        self._name = name
        self._price = price

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value):
        if value < 0:
            raise ValueError("Price cannot be negative")
        self._price = value

    def get_info(self):
        return f"Product: {self._name}, Price: ${self._price}"


class DiscountedProduct(Product):
    def __init__(self, name, price, discount):
        super().__init__(name, price)
        self.discount = discount

    @property
    def price(self):
        # Override getter to apply discount
        original_price = super().price
        return original_price * (1 - self.discount / 100)

    @price.setter
    def price(self, value):
        # Use parent setter
        super(DiscountedProduct, DiscountedProduct).price.__set__(self, value)
        # Or: super().__class__.price.fset(self, value)

    def get_info(self):
        parent_info = super().get_info()
        return f"{parent_info}, Discount: {self.discount}%, Final Price: ${self.price:.2f}"


# ============================================================
# 8. SUPER() IN DIAMOND INHERITANCE WITH MIXINS
# ============================================================

class LoggerMixin:
    """Mixin for logging"""

    def log(self, message):
        print(f"[LOG] {self.__class__.__name__}: {message}")

    def process(self):
        self.log("Processing in LoggerMixin")
        return "LoggerMixin"


class ValidatorMixin:
    """Mixin for validation"""

    def validate(self, data):
        print(f"[VALIDATE] Validating in {self.__class__.__name__}")
        return data is not None

    def process(self):
        print("Processing in ValidatorMixin")
        return "ValidatorMixin"


class CoreProcessor:
    """Base class"""

    def process(self):
        print("Processing in CoreProcessor")
        return "CoreProcessor"


class ExtendedProcessor(LoggerMixin, ValidatorMixin, CoreProcessor):
    """Class with multiple inheritance and mixins"""

    def process(self):
        print("Processing in ExtendedProcessor")
        # super() calls next class in MRO
        result = super().process()
        self.log("Extended processing complete")
        return f"ExtendedProcessor -> {result}"


# ============================================================
# 9. super() ADVANCED: CALLING SPECIFIC PARENT METHODS
# ============================================================

class Parent1:
    def method(self):
        print("Parent1.method()")
        return "Parent1"


class Parent2:
    def method(self):
        print("Parent2.method()")
        return "Parent2"


class ChildMultiple(Parent1, Parent2):
    def method(self):
        print("ChildMultiple.method()")
        # Call specific parent's method
        result1 = Parent1.method(self)
        result2 = Parent2.method(self)
        return f"{result1} + {result2}"

    def method_with_super(self):
        print("ChildMultiple.method_with_super()")
        # super() follows MRO
        result = super().method()
        return f"super() -> {result}"


# ============================================================
# 10. PRACTICAL EXAMPLE: DATABASE MODEL WITH SUPER()
# ============================================================

class Model:
    """Base model class"""
    table_name = None

    def __init__(self, **kwargs):
        self._data = kwargs
        self._validate()
        print(f"Model __init__: {kwargs}")

    def _validate(self):
        """Base validation"""
        return True

    def save(self):
        print(f"Saving {self.table_name} with data: {self._data}")
        return True

    def delete(self):
        print(f"Deleting from {self.table_name}")
        return True

    def __str__(self):
        return f"{self.table_name}: {self._data}"


class User(Model):
    """User model"""
    table_name = "users"

    def __init__(self, username, email, **kwargs):
        # Store extra attributes
        self.username = username
        self.email = email
        # Call parent with remaining kwargs
        super().__init__(username=username, email=email, **kwargs)
        print(f"User __init__: {username}")

    def _validate(self):
        """User-specific validation"""
        super()._validate()  # Call parent validation
        if not self.username or len(self.username) < 3:
            raise ValueError("Username must be at least 3 characters")
        if "@" not in self.email:
            raise ValueError("Invalid email")
        return True

    def save(self):
        print(f"Validating user before saving...")
        self._validate()
        # Call parent save with additional logic
        result = super().save()
        print(f"User {self.username} saved successfully")
        return result

    def get_profile(self):
        return f"User: {self.username}, Email: {self.email}"


class AdminUser(User):
    """Admin user with extended functionality"""
    table_name = "admin_users"

    def __init__(self, username, email, permissions=None, **kwargs):
        self.permissions = permissions or []
        super().__init__(username, email, **kwargs)
        print(f"AdminUser __init__: {username}")

    def _validate(self):
        """Admin-specific validation"""
        super()._validate()
        if not self.permissions:
            print("Warning: Admin has no permissions")
        return True

    def save(self):
        print(f"Setting admin-specific fields...")
        # Call parent save with super()
        result = super().save()
        print(f"Admin {self.username} permissions: {self.permissions}")
        return result

    def get_profile(self):
        parent_profile = super().get_profile()
        return f"{parent_profile}, Permissions: {self.permissions}"


# ============================================================
# 11. UNDERSTANDING METHOD RESOLUTION ORDER (MRO)
# ============================================================

def demonstrate_mro():
    """Demonstrate MRO and super() behavior"""
    print("\n" + "=" * 60)
    print("METHOD RESOLUTION ORDER (MRO) DEMONSTRATION")
    print("=" * 60)

    # Show MRO for different classes
    print("\nMRO for D (multiple inheritance):")
    for cls in D.__mro__:
        print(f"  {cls.__name__}")

    print("\nMRO for ExtendedProcessor (with mixins):")
    for cls in ExtendedProcessor.__mro__:
        print(f"  {cls.__name__}")

    # Demonstrate method call order
    print("\nMethod call order with super():")
    d = D()
    print(f"Result: {d.method()}")

    print("\nExtendedProcessor method call order:")
    ep = ExtendedProcessor()
    print(f"Result: {ep.process()}")


# ============================================================
# 12. super() IN CONTEXT MANAGERS
# ============================================================

class BaseContext:
    def __enter__(self):
        print("BaseContext: Entering")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        print("BaseContext: Exiting")
        return False  # Don't suppress exceptions


class ExtendedContext(BaseContext):
    def __enter__(self):
        print("ExtendedContext: Entering")
        # Call parent's __enter__
        result = super().__enter__()
        return result

    def __exit__(self, exc_type, exc_val, exc_tb):
        print("ExtendedContext: Exiting")
        # Call parent's __exit__
        return super().__exit__(exc_type, exc_val, exc_tb)


# ============================================================
# DEMONSTRATION FUNCTION
# ============================================================

def demonstrate_super():
    """Comprehensive demonstration of super() features"""

    print("=" * 60)
    print("SUPER() COMPREHENSIVE DEMONSTRATION")
    print("=" * 60)

    # 1. Basic super()
    print("\n1. BASIC super() USAGE")
    print("-" * 40)
    dog = Dog("Buddy", "Golden Retriever")
    print(dog.speak())
    print(dog.get_info())

    # 2. Multi-level inheritance
    print("\n2. MULTI-LEVEL INHERITANCE")
    print("-" * 40)
    cat = Cat("Whiskers", "Persian", True)
    print(cat.speak())
    print(cat.get_info())
    print(cat.feed_milk())

    # 3. Multiple inheritance with super()
    print("\n3. MULTIPLE INHERITANCE WITH super()")
    print("-" * 40)
    d = D()
    print(f"Method result: {d.method()}")
    print(f"D values: a={d.value_a}, b={d.value_b}, c={d.value_c}, d={d.value_d}")

    # 4. super() with different arguments
    print("\n4. super() WITH DIFFERENT ARGUMENTS")
    print("-" * 40)
    grandchild = GrandChild("Alice", 10, 5, "Reading")
    print(grandchild.display())

    # 5. super() without arguments (Python 3)
    print("\n5. super() WITHOUT ARGUMENTS")
    print("-" * 40)
    derived = Derived2()
    print(derived.method())

    # 6. super() in classmethods
    print("\n6. super() IN CLASSMETHODS")
    print("-" * 40)
    obj = ClassDerived.factory("Test", 25)
    print(obj.static_info())

    # 7. super() with properties
    print("\n7. super() WITH PROPERTIES")
    print("-" * 40)
    product = DiscountedProduct("Laptop", 1000, 10)
    print(f"Original price: ${1000}")
    print(f"Discounted price: ${product.price:.2f}")
    product.price = 1200
    print(f"Updated price: ${product.price:.2f}")
    print(product.get_info())

    # 8. super() with mixins
    print("\n8. super() WITH MIXINS")
    print("-" * 40)
    ep = ExtendedProcessor()
    print(f"Process result: {ep.process()}")

    # 9. Calling specific parent methods
    print("\n9. CALLING SPECIFIC PARENT METHODS")
    print("-" * 40)
    child = ChildMultiple()
    print(f"Specific parents: {child.method()}")
    print(f"Super MRO: {child.method_with_super()}")

    # 10. Practical database model example
    print("\n10. PRACTICAL DATABASE MODEL")
    print("-" * 40)
    user = User("john_doe", "john@email.com", age=25, city="NYC")
    print(user.save())
    print(user.get_profile())
    print()
    admin = AdminUser("admin", "admin@system.com",
                      permissions=["read", "write", "delete"],
                      department="IT")
    print(admin.save())
    print(admin.get_profile())

    # 11. Context manager with super()
    print("\n11. super() IN CONTEXT MANAGERS")
    print("-" * 40)
    with ExtendedContext() as ctx:
        print("Inside context")

    # 12. MRO demonstration
    demonstrate_mro()


# ============================================================
# HELPER FUNCTION: UNDERSTANDING SUPER() BEHAVIOR
# ============================================================

def explain_super():
    """Explain key super() concepts"""
    print("\n" + "=" * 60)
    print("KEY SUPER() CONCEPTS")
    print("=" * 60)

    print("""
    1. WHAT IS super()?
       - Returns a proxy object that delegates method calls to parent class
       - Follows Method Resolution Order (MRO)
       - Essential for cooperative multiple inheritance

    2. WHY USE super()?
       - Avoids explicitly naming parent class
       - Makes code more maintainable
       - Handles multiple inheritance correctly
       - Prevents diamond problem

    3. super() SYNTAX:
       - super() -> automatically uses current class and instance
       - super(Class, instance) -> explicit form
       - super(Class, cls) -> for classmethods

    4. MRO ORDER:
       - Python uses C3 linearization algorithm
       - Ensures each class appears once in MRO
       - Maintains local precedence order

    5. COMMON PATTERNS:
       - __init__ super() call: super().__init__(*args, **kwargs)
       - Method extension: return super().method() + additional logic
       - Cooperative multiple inheritance: all classes use super()
    """)


# ============================================================
# MAIN EXECUTION
# ============================================================

if __name__ == "__main__":
    demonstrate_super()
    explain_super()

    # Additional demonstration: Compare super() with direct parent calls
    print("\n" + "=" * 60)
    print("SUPER() VS DIRECT PARENT CALL COMPARISON")
    print("=" * 60)


    class DirectParent:
        def method(self):
            return "Parent"


    class DirectChild(DirectParent):
        def method(self):
            # Direct parent call (hardcoded)
            return DirectParent.method(self) + " -> Child"


    class SuperChild(DirectParent):
        def method(self):
            # super() call (dynamic)
            return super().method() + " -> Child"


    direct = DirectChild()
    super_child = SuperChild()

    print(f"Direct call: {direct.method()}")
    print(f"Super call: {super_child.method()}")
    print("\n✅ Direct call works but super() is more maintainable!")

    print("\n" + "=" * 60)
    print("✅ super() DEMONSTRATION COMPLETE")
    print("=" * 60)