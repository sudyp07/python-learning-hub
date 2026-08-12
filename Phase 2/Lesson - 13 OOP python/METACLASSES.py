"""
COMPREHENSIVE GUIDE TO METACLASSES IN PYTHON
============================================
Metaclasses are classes of classes. They define how classes behave.
Think of them as "class factories" - they create classes.

Key Concepts:
- type() is the default metaclass
- Metaclasses can intercept class creation
- Used in frameworks like Django, SQLAlchemy
"""


# ============================================================
# 1. UNDERSTANDING type() - THE BUILT-IN METACLASS
# ============================================================

def understand_type():
    """Demonstrate how type() works as a metaclass"""
    print("=" * 70)
    print("UNDERSTANDING TYPE() - BUILT-IN METACLASS")
    print("=" * 70)

    # 1. type(object) - returns type of object
    print("\n1. type(object) - Get type:")
    print(f"type(42) = {type(42)}")
    print(f"type('hello') = {type('hello')}")
    print(f"type([]) = {type([])}")

    # 2. type(name, bases, dict) - creates a new class
    print("\n2. type(name, bases, dict) - Create class:")

    # Create class dynamically
    MyClass = type('MyClass', (object,), {
        'x': 10,
        'hello': lambda self: "Hello from dynamic class!"
    })

    obj = MyClass()
    print(f"Dynamic class: {MyClass}")
    print(f"Attribute x: {obj.x}")
    print(f"Method hello: {obj.hello()}")

    # 3. Creating a more complex class
    def __init__(self, name):
        self.name = name

    def greet(self):
        return f"Hello, {self.name}!"

    Person = type('Person', (object,), {
        '__init__': __init__,
        'greet': greet,
        'species': 'Homo sapiens'
    })

    person = Person("Alice")
    print(f"\nPerson class: {person.greet()}")
    print(f"Person species: {person.species}")


# ============================================================
# 2. BASIC METACLASS IMPLEMENTATION
# ============================================================

class SimpleMeta(type):
    """A simple metaclass that adds functionality to classes"""

    def __new__(meta, name, bases, class_dict):
        """Called when creating a new class"""
        print(f"🔧 Creating class: {name}")
        print(f"   Bases: {bases}")
        print(f"   Attributes: {list(class_dict.keys())}")

        # Add a class attribute
        class_dict['created_by_meta'] = True
        class_dict['meta_version'] = '1.0'

        # Create the class
        return super().__new__(meta, name, bases, class_dict)

    def __init__(cls, name, bases, class_dict):
        """Called after class is created"""
        print(f"📝 Initializing class: {name}")
        super().__init__(name, bases, class_dict)

        # Add a class method
        def get_info(cls):
            return f"Class: {cls.__name__}, Created by meta: {cls.created_by_meta}"

        cls.get_info = classmethod(get_info)


class MyClass(metaclass=SimpleMeta):
    """Class using custom metaclass"""
    x = 10

    def __init__(self, value):
        self.value = value


# ============================================================
# 3. VALIDATING METACLASS
# ============================================================

class ValidatingMeta(type):
    """Metaclass that validates class definitions"""

    def __new__(meta, name, bases, class_dict):
        # Validate naming convention
        if not name[0].isupper():
            raise ValueError(f"Class name '{name}' must start with uppercase letter")

        # Validate methods
        for key, value in class_dict.items():
            if callable(value) and not key.startswith('_'):
                # All public methods should have docstrings
                if not value.__doc__:
                    print(f"⚠️ Warning: Method {key} has no docstring")

        # Ensure required methods exist
        if 'process' not in class_dict:
            raise ValueError("Class must implement 'process' method")

        print(f"✅ Class {name} validation passed")
        return super().__new__(meta, name, bases, class_dict)


class ValidClass(metaclass=ValidatingMeta):
    """Valid class definition"""

    def process(self):
        """Process data"""
        return "Processing..."

    def helper(self):
        """Helper method"""
        return "Helper"


# ============================================================
# 4. SINGLETON METACLASS
# ============================================================

class SingletonMeta(type):
    """Metaclass implementing Singleton pattern"""

    _instances = {}

    def __call__(cls, *args, **kwargs):
        """Called when creating an instance of the class"""
        if cls not in cls._instances:
            print(f"🔨 Creating new singleton instance of {cls.__name__}")
            cls._instances[cls] = super().__call__(*args, **kwargs)
        else:
            print(f"♻️ Returning existing singleton instance of {cls.__name__}")
        return cls._instances[cls]

    def clear_instance(cls):
        """Clear the singleton instance (for testing)"""
        if cls in cls._instances:
            del cls._instances[cls]
            print(f"🗑️ Cleared singleton instance of {cls.__name__}")


class SingletonClass(metaclass=SingletonMeta):
    """Singleton class using metaclass"""

    def __init__(self, value):
        self.value = value
        print(f"   Initializing singleton with value: {value}")

    def get_value(self):
        return self.value


# ============================================================
# 5. ORM METACLASS (Django/SQLAlchemy Style)
# ============================================================

class ORMMeta(type):
    """Metaclass for ORM-like models"""

    def __new__(meta, name, bases, class_dict):
        # Separate fields from other attributes
        fields = {}
        meta_options = {}

        for key, value in list(class_dict.items()):
            if isinstance(value, Field):
                fields[key] = value
            elif key == 'Meta':
                meta_options = value.__dict__

        # Remove fields from class dict (they go in __fields__)
        for key in fields:
            del class_dict[key]

        # Store fields and meta options
        class_dict['_fields'] = fields
        class_dict['_meta'] = meta_options

        # Add the table name
        if 'db_table' not in meta_options:
            class_dict['_table_name'] = name.lower()
        else:
            class_dict['_table_name'] = meta_options['db_table']

        # Add utility methods
        def get_fields(cls):
            return cls._fields

        def get_table_name(cls):
            return cls._table_name

        def create_table_sql(cls):
            """Generate CREATE TABLE SQL"""
            fields_sql = []
            for name, field in cls._fields.items():
                field_type = field.field_type
                sql = f"    {name} {field_type}"
                if field.required:
                    sql += " NOT NULL"
                if field.primary_key:
                    sql += " PRIMARY KEY"
                fields_sql.append(sql)

            return f"CREATE TABLE {cls._table_name} (\n" + ",\n".join(fields_sql) + "\n);"

        class_dict['get_fields'] = classmethod(get_fields)
        class_dict['get_table_name'] = classmethod(get_table_name)
        class_dict['create_table_sql'] = classmethod(create_table_sql)

        return super().__new__(meta, name, bases, class_dict)

    def __call__(cls, *args, **kwargs):
        """Create instance with field validation"""
        instance = super().__call__(*args, **kwargs)

        # Validate all fields have values
        for field_name, field in cls._fields.items():
            if field.required and not hasattr(instance, field_name):
                raise ValueError(f"Field {field_name} is required")

        return instance


class Field:
    """Base field class for ORM"""

    def __init__(self, field_type, required=True, primary_key=False, default=None):
        self.field_type = field_type
        self.required = required
        self.primary_key = primary_key
        self.default = default


class UserModel(metaclass=ORMMeta):
    """User model using ORM metaclass"""

    id = Field('INTEGER', required=True, primary_key=True)
    username = Field('VARCHAR(50)', required=True)
    email = Field('VARCHAR(100)', required=True)
    age = Field('INTEGER', required=False)
    is_active = Field('BOOLEAN', required=False, default=True)

    class Meta:
        db_table = 'users'

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    def __repr__(self):
        return f"User(username={getattr(self, 'username', None)})"


# ============================================================
# 6. AUTOMATIC REGISTRATION METACLASS
# ============================================================

class RegistryMeta(type):
    """Metaclass that automatically registers classes"""

    registry = {}  # Global registry

    def __new__(meta, name, bases, class_dict):
        cls = super().__new__(meta, name, bases, class_dict)

        # Register the class
        if name != 'BasePlugin':  # Don't register base class
            meta.registry[name] = cls
            print(f"📝 Registered: {name}")

        return cls


class BasePlugin(metaclass=RegistryMeta):
    """Base plugin class"""

    def execute(self):
        raise NotImplementedError("Plugin must implement execute()")


class LoggingPlugin(BasePlugin):
    """Logging plugin"""

    def execute(self):
        return "Logging plugin executed"


class DatabasePlugin(BasePlugin):
    """Database plugin"""

    def execute(self):
        return "Database plugin executed"


class EmailPlugin(BasePlugin):
    """Email plugin"""

    def execute(self):
        return "Email plugin executed"


# ============================================================
# 7. METACLASS WITH DESCRIPTOR COMBINATION
# ============================================================

class ValidatedAttribute:
    """Descriptor for validation"""

    def __init__(self, validator, error_msg=None):
        self.validator = validator
        self.error_msg = error_msg or "Invalid value"

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return instance.__dict__.get(self._name, None)

    def __set__(self, instance, value):
        if not self.validator(value):
            raise ValueError(f"{self._name}: {self.error_msg}")
        instance.__dict__[self._name] = value


class ValidationMeta(type):
    """Metaclass that sets up validation attributes"""

    def __new__(meta, name, bases, class_dict):
        # Find all ValidatedAttribute descriptors
        for key, value in list(class_dict.items()):
            if isinstance(value, ValidatedAttribute):
                # Set the name on the descriptor
                value._name = key

        return super().__new__(meta, name, bases, class_dict)


class ValidatedPerson(metaclass=ValidationMeta):
    """Class with validation"""

    name = ValidatedAttribute(
        lambda x: isinstance(x, str) and len(x) > 0,
        "Name must be a non-empty string"
    )

    age = ValidatedAttribute(
        lambda x: isinstance(x, int) and 0 <= x <= 150,
        "Age must be between 0 and 150"
    )

    email = ValidatedAttribute(
        lambda x: isinstance(x, str) and '@' in x,
        "Must be a valid email"
    )

    def __init__(self, name, age, email):
        self.name = name
        self.age = age
        self.email = email

    def __repr__(self):
        return f"ValidatedPerson(name={self.name}, age={self.age}, email={self.email})"


# ============================================================
# 8. TIMING METACLASS
# ============================================================

import time
from functools import wraps


class TimingMeta(type):
    """Metaclass that adds timing to all methods"""

    def __new__(meta, name, bases, class_dict):
        # Wrap all methods with timing
        for key, value in class_dict.items():
            if callable(value) and not key.startswith('_'):
                class_dict[key] = meta._timed_method(value)

        return super().__new__(meta, name, bases, class_dict)

    @staticmethod
    def _timed_method(method):
        """Decorator to time method execution"""

        @wraps(method)
        def timed(*args, **kwargs):
            start = time.time()
            result = method(*args, **kwargs)
            end = time.time()
            print(f"⏱️ {method.__name__} took {end - start:.4f} seconds")
            return result

        return timed


class TimedClass(metaclass=TimingMeta):
    """Class with timed methods"""

    def slow_method(self):
        """A slow method"""
        time.sleep(0.5)
        return "Slow method done"

    def fast_method(self):
        """A fast method"""
        return "Fast method done"

    def compute(self, n):
        """Compute something"""
        result = 0
        for i in range(n):
            result += i
        return result


# ============================================================
# 9. THREAD-SAFE SINGLETON METACLASS
# ============================================================

import threading


class ThreadSafeSingletonMeta(type):
    """Thread-safe singleton metaclass"""

    _instances = {}
    _lock = threading.Lock()

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            with cls._lock:
                if cls not in cls._instances:
                    print(f"🔒 Creating thread-safe singleton: {cls.__name__}")
                    cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


class ThreadSafeSingleton(metaclass=ThreadSafeSingletonMeta):
    """Thread-safe singleton class"""

    def __init__(self, value):
        self.value = value
        print(f"   Singleton initialized with {value}")

    def get_value(self):
        return self.value


# ============================================================
# 10. IMMUTABLE CLASS METACLASS
# ============================================================

class ImmutableMeta(type):
    """Metaclass that makes classes immutable after creation"""

    def __call__(cls, *args, **kwargs):
        instance = super().__call__(*args, **kwargs)
        instance.__frozen = True
        return instance

    def __setattr__(cls, name, value):
        if hasattr(cls, '__frozen') and cls.__frozen:
            raise AttributeError(f"Cannot modify {name} on immutable class")
        super().__setattr__(name, value)


class ImmutableClass(metaclass=ImmutableMeta):
    """Immutable class"""

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __setattr__(self, name, value):
        if hasattr(self, '__frozen') and self.__frozen:
            raise AttributeError(f"Cannot modify {name} on immutable instance")
        super().__setattr__(name, value)

    def __repr__(self):
        return f"ImmutableClass(x={self.x}, y={self.y})"


# ============================================================
# DEMONSTRATION
# ============================================================

def demonstrate_metaclasses():
    """Complete demonstration of metaclasses"""

    print("=" * 70)
    print("METACLASSES COMPREHENSIVE DEMONSTRATION")
    print("=" * 70)

    # 1. Understanding type()
    understand_type()

    # 2. Simple Meta Class
    print("\n" + "=" * 70)
    print("2. BASIC METACLASS")
    print("=" * 70)

    obj = MyClass(42)
    print(f"Class: {MyClass}")
    print(f"Created by meta: {obj.created_by_meta}")
    print(f"Meta version: {obj.meta_version}")
    print(f"Class info: {MyClass.get_info()}")

    # 3. Validating Meta
    print("\n" + "=" * 70)
    print("3. VALIDATING METACLASS")
    print("=" * 70)

    valid = ValidClass()
    print(f"Process: {valid.process()}")
    print(f"Helper: {valid.helper()}")

    # 4. Singleton Meta
    print("\n" + "=" * 70)
    print("4. SINGLETON METACLASS")
    print("=" * 70)

    s1 = SingletonClass(10)
    s2 = SingletonClass(20)  # Should return existing instance

    print(f"Instance 1 value: {s1.get_value()}")
    print(f"Instance 2 value: {s2.get_value()}")
    print(f"Same instance? {s1 is s2}")

    # 5. ORM Meta
    print("\n" + "=" * 70)
    print("5. ORM METACLASS")
    print("=" * 70)

    print(f"UserModel fields: {UserModel.get_fields()}")
    print(f"UserModel table: {UserModel.get_table_name()}")
    print("\nCREATE TABLE SQL:")
    print(UserModel.create_table_sql())

    user = UserModel(id=1, username="john_doe", email="john@example.com")
    print(f"User: {user}")

    # 6. Registry Meta
    print("\n" + "=" * 70)
    print("6. REGISTRY METACLASS")
    print("=" * 70)

    print("Registered plugins:")
    for name, cls in RegistryMeta.registry.items():
        if name != 'BasePlugin':
            plugin = cls()
            print(f"  {name}: {plugin.execute()}")

    # 7. Validation Meta
    print("\n" + "=" * 70)
    print("7. VALIDATION METACLASS")
    print("=" * 70)

    try:
        person = ValidatedPerson("Alice", 25, "alice@email.com")
        print(person)

        # Try invalid data
        person.age = 200  # Should raise error
    except ValueError as e:
        print(f"Validation error: {e}")

    # 8. Timing Meta
    print("\n" + "=" * 70)
    print("8. TIMING METACLASS")
    print("=" * 70)

    timed = TimedClass()
    timed.slow_method()
    timed.fast_method()
    timed.compute(100000)

    # 9. Thread-safe Singleton
    print("\n" + "=" * 70)
    print("9. THREAD-SAFE SINGLETON")
    print("=" * 70)

    def test_singleton(value):
        instance = ThreadSafeSingleton(value)
        print(f"Thread {threading.current_thread().name}: {instance.get_value()}")

    # Create multiple threads
    threads = []
    for i in range(5):
        t = threading.Thread(target=test_singleton, args=(i,))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    # 10. Immutable Class
    print("\n" + "=" * 70)
    print("10. IMMUTABLE CLASS")
    print("=" * 70)

    immut = ImmutableClass(1, 2)
    print(f"Immutable: {immut}")

    try:
        immut.x = 3  # Should raise error
    except AttributeError as e:
        print(f"Error: {e}")


# ============================================================
# MAIN EXECUTION
# ============================================================

if __name__ == "__main__":
    demonstrate_metaclasses()

    print("\n" + "=" * 70)
    print("METACLASSES KEY CONCEPTS")
    print("=" * 70)
    print("""
    ✅ METACLASS BASICS
       - A metaclass is the class of a class
       - Controls how classes are created and behave
       - type() is the default metaclass

    ✅ WHEN TO USE METACLASSES
       - Framework development (Django, SQLAlchemy)
       - ORM implementations
       - Singleton pattern
       - Class validation
       - Automatic registration
       - API creation
       - AST manipulation

    ✅ METACLASS METHODS
       - __new__(meta, name, bases, class_dict) - Create class
       - __init__(cls, name, bases, class_dict) - Initialize class
       - __call__(cls, *args, **kwargs) - Create instance

    ✅ BEST PRACTICES
       - Use sparingly (advanced feature)
       - Document clearly
       - Consider alternatives (decorators, descriptors)
       - Keep it simple
       - Test thoroughly

    ✅ COMMON PATTERNS
       - Singleton pattern
       - ORM models
       - Plugin systems
       - Validation frameworks
       - Timing/debugging
       - Automatic registration
    """)
    print("=" * 70)