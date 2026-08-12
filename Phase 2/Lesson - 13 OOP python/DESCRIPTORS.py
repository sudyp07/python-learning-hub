"""
COMPREHENSIVE GUIDE TO DESCRIPTORS IN PYTHON
============================================
Descriptors are Python objects that define how attribute access works.
They implement the descriptor protocol: __get__, __set__, __delete__.
Properties are built using descriptors under the hood!
"""


# ============================================================
# 1. BASIC DESCRIPTOR PROTOCOL
# ============================================================

class DescriptorExample:
    """Basic descriptor showing the protocol methods"""

    def __init__(self, name):
        self.name = name
        print(f"Descriptor {name} created")

    def __get__(self, instance, owner):
        """Called when attribute is accessed"""
        print(f"__get__ called on {self.name}")
        if instance is None:
            return self
        return instance.__dict__.get(self.name, None)

    def __set__(self, instance, value):
        """Called when attribute is set"""
        print(f"__set__ called on {self.name} with value {value}")
        instance.__dict__[self.name] = value

    def __delete__(self, instance):
        """Called when attribute is deleted"""
        print(f"__delete__ called on {self.name}")
        del instance.__dict__[self.name]


class MyClass:
    """Class using descriptors"""
    attr = DescriptorExample("attr")
    name = DescriptorExample("name")

    def __init__(self, name):
        self.name = name


# ============================================================
# 2. DATA DESCRIPTOR VS NON-DATA DESCRIPTOR
# ============================================================

class DataDescriptor:
    """Data descriptor - implements __get__ and __set__"""

    def __init__(self, name):
        self.name = name

    def __get__(self, instance, owner):
        if instance is None:
            return self
        print(f"DataDescriptor: Getting {self.name}")
        return instance.__dict__.get(self.name, "Default")

    def __set__(self, instance, value):
        print(f"DataDescriptor: Setting {self.name} to {value}")
        instance.__dict__[self.name] = value


class NonDataDescriptor:
    """Non-data descriptor - only implements __get__"""

    def __init__(self, name):
        self.name = name

    def __get__(self, instance, owner):
        if instance is None:
            return self
        print(f"NonDataDescriptor: Getting {self.name}")
        return f"Non-data descriptor value for {self.name}"


class TestClass:
    """Class demonstrating both types of descriptors"""
    data_attr = DataDescriptor("data_attr")
    non_data_attr = NonDataDescriptor("non_data_attr")

    def __init__(self):
        self.instance_attr = "instance value"


# ============================================================
# 3. VALIDATING DESCRIPTOR (REAL-WORLD EXAMPLE)
# ============================================================

class ValidatedAttribute:
    """Descriptor that validates attribute values"""

    def __init__(self, name, validator=None, default=None):
        self.name = name
        self.validator = validator
        self.default = default

    def __get__(self, instance, owner):
        if instance is None:
            return self
        # Return default if attribute doesn't exist
        return instance.__dict__.get(self.name, self.default)

    def __set__(self, instance, value):
        # Validate before setting
        if self.validator:
            if not self.validator(value):
                raise ValueError(f"Invalid value for {self.name}: {value}")
        instance.__dict__[self.name] = value

    def __delete__(self, instance):
        del instance.__dict__[self.name]


class Person:
    """Using validated descriptors"""

    # Define validators
    def validate_age(age):
        return isinstance(age, int) and 0 <= age <= 150

    def validate_email(email):
        return isinstance(email, str) and '@' in email and '.' in email

    def validate_positive_number(value):
        return isinstance(value, (int, float)) and value >= 0

    # Create descriptor attributes
    name = ValidatedAttribute("name", lambda x: isinstance(x, str) and len(x) > 0)
    age = ValidatedAttribute("age", validate_age, default=0)
    email = ValidatedAttribute("email", validate_email)
    salary = ValidatedAttribute("salary", validate_positive_number, default=0.0)

    def __init__(self, name, age, email, salary=0):
        self.name = name
        self.age = age
        self.email = email
        self.salary = salary

    def __str__(self):
        return f"Person({self.name}, {self.age}, {self.email})"


# ============================================================
# 4. TYPE-CHECKING DESCRIPTOR
# ============================================================

class TypedAttribute:
    """Descriptor that enforces type checking"""

    def __init__(self, name, expected_type):
        self.name = name
        self.expected_type = expected_type

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return instance.__dict__.get(self.name, None)

    def __set__(self, instance, value):
        if not isinstance(value, self.expected_type):
            raise TypeError(f"{self.name} must be {self.expected_type.__name__}, got {type(value).__name__}")
        instance.__dict__[self.name] = value


class Product:
    """Class using typed descriptors"""
    name = TypedAttribute("name", str)
    price = TypedAttribute("price", (int, float))
    quantity = TypedAttribute("quantity", int)
    is_available = TypedAttribute("is_available", bool)

    def __init__(self, name, price, quantity, is_available=True):
        self.name = name
        self.price = price
        self.quantity = quantity
        self.is_available = is_available

    def __str__(self):
        return f"Product({self.name}, ${self.price}, {self.quantity})"


# ============================================================
# 5. CACHING DESCRIPTOR (LAZY EVALUATION)
# ============================================================

class LazyProperty:
    """Descriptor that computes value once and caches it"""

    def __init__(self, func):
        self.func = func
        self.name = func.__name__

    def __get__(self, instance, owner):
        if instance is None:
            return self

        # Check if value already computed
        if self.name not in instance.__dict__:
            print(f"Computing {self.name}...")
            value = self.func(instance)
            instance.__dict__[self.name] = value

        return instance.__dict__[self.name]


class ExpensiveCalculation:
    """Class using lazy properties"""

    def __init__(self, data):
        self.data = data
        self._cache = {}  # Manual cache

    @LazyProperty
    def sum_values(self):
        """Expensive computation - sum of data"""
        import time
        time.sleep(1)  # Simulate expensive operation
        return sum(self.data)

    @LazyProperty
    def average(self):
        """Expensive computation - average of data"""
        import time
        time.sleep(0.5)  # Simulate expensive operation
        return sum(self.data) / len(self.data) if self.data else 0

    @LazyProperty
    def stats(self):
        """Complex statistics computation"""
        import time
        import math
        time.sleep(1.5)  # Simulate expensive operation
        data = self.data
        mean = sum(data) / len(data)
        variance = sum((x - mean) ** 2 for x in data) / len(data)
        return {
            'mean': mean,
            'variance': variance,
            'std_dev': math.sqrt(variance),
            'min': min(data),
            'max': max(data),
            'count': len(data)
        }


# ============================================================
# 6. READ-ONLY DESCRIPTOR
# ============================================================

class ReadOnlyAttribute:
    """Descriptor that creates read-only attributes"""

    def __init__(self, name):
        self.name = name

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return instance.__dict__.get(self.name, None)

    def __set__(self, instance, value):
        raise AttributeError(f"{self.name} is read-only and cannot be modified")


class ImmutableObject:
    """Class with read-only attributes"""

    # Read-only attributes
    id = ReadOnlyAttribute("id")
    created_at = ReadOnlyAttribute("created_at")
    version = ReadOnlyAttribute("version")

    def __init__(self, id, created_at, version=1):
        # Set values directly in __dict__ to bypass descriptor
        self.__dict__['id'] = id
        self.__dict__['created_at'] = created_at
        self.__dict__['version'] = version
        self.name = "Mutable object"

    def __str__(self):
        return f"ImmutableObject(id={self.id}, created={self.created_at})"


# ============================================================
# 7. DESCRIPTOR WITH HISTORY TRACKING
# ============================================================

class HistoryDescriptor:
    """Descriptor that tracks attribute change history"""

    def __init__(self, name, max_history=10):
        self.name = name
        self.max_history = max_history

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return instance.__dict__.get(self.name, None)

    def __set__(self, instance, value):
        old_value = instance.__dict__.get(self.name, None)

        # Store history
        if not hasattr(instance, '_history'):
            instance._history = {}

        if self.name not in instance._history:
            instance._history[self.name] = []

        # Add to history
        if old_value is not None:
            instance._history[self.name].append({
                'old': old_value,
                'new': value,
                'timestamp': __import__('datetime').datetime.now()
            })

            # Limit history size
            if len(instance._history[self.name]) > self.max_history:
                instance._history[self.name].pop(0)

        # Set new value
        instance.__dict__[self.name] = value

    def get_history(self, instance):
        """Get change history for this attribute"""
        if hasattr(instance, '_history') and self.name in instance._history:
            return instance._history[self.name]
        return []


class TrackedObject:
    """Class with history tracking"""
    name = HistoryDescriptor("name")
    status = HistoryDescriptor("status")
    value = HistoryDescriptor("value")

    def __init__(self, name, status, value):
        self.name = name
        self.status = status
        self.value = value

    def show_history(self, attr_name):
        """Display history for a specific attribute"""
        descriptor = getattr(self.__class__, attr_name)
        if isinstance(descriptor, HistoryDescriptor):
            history = descriptor.get_history(self)
            if not history:
                print(f"No history for {attr_name}")
            else:
                print(f"History for {attr_name}:")
                for i, change in enumerate(history, 1):
                    print(f"  {i}. {change['old']} -> {change['new']} at {change['timestamp']}")
        else:
            print(f"{attr_name} is not tracked")


# ============================================================
# 8. BUILDING YOUR OWN @PROPERTY USING DESCRIPTORS
# ============================================================

class CustomProperty:
    """Custom implementation of @property using descriptors"""

    def __init__(self, fget=None, fset=None, fdel=None, doc=None):
        self.fget = fget
        self.fset = fset
        self.fdel = fdel
        self.__doc__ = doc

    def __get__(self, instance, owner):
        if instance is None:
            return self
        if self.fget is None:
            raise AttributeError("Unreadable attribute")
        return self.fget(instance)

    def __set__(self, instance, value):
        if self.fset is None:
            raise AttributeError("Can't set attribute")
        self.fset(instance, value)

    def __delete__(self, instance):
        if self.fdel is None:
            raise AttributeError("Can't delete attribute")
        self.fdel(instance)

    def setter(self, func):
        """Set the setter method"""
        self.fset = func
        return self

    def deleter(self, func):
        """Set the deleter method"""
        self.fdel = func
        return self


class CustomClass:
    """Class using custom property implementation"""

    def __init__(self, name, age):
        self._name = name
        self._age = age

    @CustomProperty
    def name(self):
        """Get name"""
        return self._name

    @name.setter
    def name(self, value):
        """Set name with validation"""
        if not value or len(value) < 2:
            raise ValueError("Name must be at least 2 characters")
        self._name = value

    @CustomProperty
    def age(self):
        """Get age"""
        return self._age

    @age.setter
    def age(self, value):
        """Set age with validation"""
        if not isinstance(value, int) or value < 0:
            raise ValueError("Age must be a positive integer")
        self._age = value


# ============================================================
# 9. DESCRIPTOR IN DATABASE MODELS (ORM-like)
# ============================================================

class Field:
    """Base field descriptor for ORM-like models"""

    def __init__(self, name, field_type, required=True, default=None):
        self.name = name
        self.field_type = field_type
        self.required = required
        self.default = default

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return instance.__dict__.get(self.name, self.default)

    def __set__(self, instance, value):
        # Validate type
        if value is None:
            if self.required:
                raise ValueError(f"{self.name} is required")
            instance.__dict__[self.name] = value
            return

        if not isinstance(value, self.field_type):
            raise TypeError(f"{self.name} must be {self.field_type.__name__}, got {type(value).__name__}")

        # Additional validation
        self._validate(value)
        instance.__dict__[self.name] = value

    def _validate(self, value):
        """Override in subclasses for custom validation"""
        pass


class StringField(Field):
    """String field with length validation"""

    def __init__(self, name, max_length=None, min_length=None, **kwargs):
        super().__init__(name, str, **kwargs)
        self.max_length = max_length
        self.min_length = min_length

    def _validate(self, value):
        if self.min_length and len(value) < self.min_length:
            raise ValueError(f"{self.name} must be at least {self.min_length} characters")
        if self.max_length and len(value) > self.max_length:
            raise ValueError(f"{self.name} must be at most {self.max_length} characters")


class IntegerField(Field):
    """Integer field with range validation"""

    def __init__(self, name, min_value=None, max_value=None, **kwargs):
        super().__init__(name, int, **kwargs)
        self.min_value = min_value
        self.max_value = max_value

    def _validate(self, value):
        if self.min_value is not None and value < self.min_value:
            raise ValueError(f"{self.name} must be at least {self.min_value}")
        if self.max_value is not None and value > self.max_value:
            raise ValueError(f"{self.name} must be at most {self.max_value}")


class EmailField(StringField):
    """Email field with format validation"""

    def __init__(self, name, **kwargs):
        super().__init__(name, **kwargs)

    def _validate(self, value):
        super()._validate(value)
        if '@' not in value or '.' not in value:
            raise ValueError(f"{self.name} must be a valid email address")


class Model:
    """Base model class with field validation"""

    def __init__(self, **kwargs):
        # Validate and set fields
        for name, field in self._get_fields():
            if name in kwargs:
                setattr(self, name, kwargs[name])
            elif field.required:
                raise ValueError(f"{name} is required")

    @classmethod
    def _get_fields(cls):
        """Get all Field descriptors in the class"""
        fields = []
        for attr_name in dir(cls):
            attr = getattr(cls, attr_name)
            if isinstance(attr, Field):
                fields.append((attr_name, attr))
        return fields

    def to_dict(self):
        """Convert model to dictionary"""
        result = {}
        for name, field in self._get_fields():
            value = getattr(self, name, field.default)
            if value is not None:
                result[name] = value
        return result

    def __repr__(self):
        fields = self.to_dict()
        field_str = ', '.join(f"{k}={v}" for k, v in fields.items())
        return f"{self.__class__.__name__}({field_str})"


class User(Model):
    """User model using ORM-like fields"""
    username = StringField("username", min_length=3, max_length=20, required=True)
    email = EmailField("email", max_length=100, required=True)
    age = IntegerField("age", min_value=13, max_value=120, required=False)
    is_active = Field("is_active", bool, required=False, default=True)


# ============================================================
# DEMONSTRATION
# ============================================================

def demonstrate_descriptors():
    """Complete demonstration of descriptors"""

    print("=" * 70)
    print("DESCRIPTORS COMPREHENSIVE DEMONSTRATION")
    print("=" * 70)

    # 1. Basic Descriptor
    print("\n1. BASIC DESCRIPTOR PROTOCOL")
    print("-" * 50)
    obj = MyClass("Test")
    print(f"Object: {obj.name}")
    obj.attr = "New value"
    print(f"New attr: {obj.attr}")
    del obj.attr

    # 2. Data vs Non-Data Descriptor
    print("\n2. DATA VS NON-DATA DESCRIPTOR")
    print("-" * 50)
    test = TestClass()
    print(f"Data descriptor: {test.data_attr}")
    print(f"Non-data descriptor: {test.non_data_attr}")

    # Override instance attribute
    test.data_attr = "Instance override"
    test.non_data_attr = "Instance override"
    print(f"Data descriptor after override: {test.data_attr}")
    print(f"Non-data descriptor after override: {test.non_data_attr}")

    # 3. Validating Descriptor
    print("\n3. VALIDATING DESCRIPTOR")
    print("-" * 50)
    try:
        person = Person("Alice", 25, "alice@email.com", 50000)
        print(f"Person: {person}")
        print(f"Age: {person.age}, Salary: ${person.salary}")

        # Try invalid data
        person.age = 200  # Should raise error
    except ValueError as e:
        print(f"Validation error: {e}")

    # 4. Type Checking Descriptor
    print("\n4. TYPE-CHECKING DESCRIPTOR")
    print("-" * 50)
    try:
        product = Product("Laptop", 999.99, 10)
        print(product)

        # Try wrong type
        product.price = "100"  # Should raise TypeError
    except TypeError as e:
        print(f"Type error: {e}")

    # 5. Lazy Property
    print("\n5. LAZY PROPERTY (CACHING)")
    print("-" * 50)
    calc = ExpensiveCalculation(list(range(100)))

    print("First access (computing):")
    print(f"Sum: {calc.sum_values}")

    print("\nSecond access (cached):")
    print(f"Sum: {calc.sum_values}")

    print("\nStats:")
    stats = calc.stats
    for key, value in stats.items():
        print(f"  {key}: {value}")

    # 6. Read-Only Descriptor
    print("\n6. READ-ONLY DESCRIPTOR")
    print("-" * 50)
    import datetime
    immut = ImmutableObject(1, datetime.datetime.now())
    print(immut)
    print(f"ID: {immut.id}")

    try:
        immut.id = 2  # Should raise error
    except AttributeError as e:
        print(f"Error: {e}")

    # But mutable attributes work
    immut.name = "New name"
    print(f"Name: {immut.name}")

    # 7. History Tracking Descriptor
    print("\n7. HISTORY TRACKING")
    print("-" * 50)
    tracked = TrackedObject("Start", "Pending", 0)

    # Make some changes
    tracked.name = "Updated"
    tracked.status = "Active"
    tracked.value = 10
    tracked.value = 20
    tracked.status = "Completed"

    tracked.show_history("name")
    tracked.show_history("status")
    tracked.show_history("value")

    # 8. Custom Property Implementation
    print("\n8. CUSTOM PROPERTY IMPLEMENTATION")
    print("-" * 50)
    custom = CustomClass("Bob", 30)
    print(f"Name: {custom.name}, Age: {custom.age}")

    custom.name = "Robert"
    custom.age = 35
    print(f"Updated: {custom.name}, {custom.age}")

    try:
        custom.age = -5  # Should raise error
    except ValueError as e:
        print(f"Error: {e}")

    # 9. ORM-like Model
    print("\n9. ORM-LIKE MODEL WITH DESCRIPTORS")
    print("-" * 50)

    # Create valid user
    user = User(username="john_doe", email="john@example.com", age=25)
    print(f"User: {user}")
    print(f"User dict: {user.to_dict()}")

    # Try invalid user
    try:
        invalid_user = User(username="jd", email="invalid-email", age=12)
    except (ValueError, TypeError) as e:
        print(f"Validation error: {e}")

    # 10. Performance Comparison
    print("\n10. PERFORMANCE COMPARISON")
    print("-" * 50)

    class RegularAttribute:
        def __init__(self):
            self.value = 42

    class DescriptorAttribute:
        value = DataDescriptor("value")

        def __init__(self):
            self.value = 42

    import timeit

    reg = RegularAttribute()
    desc = DescriptorAttribute()

    reg_time = timeit.timeit('reg.value', globals=locals(), number=1000000)
    desc_time = timeit.timeit('desc.value', globals=locals(), number=1000000)

    print(f"Regular attribute: {reg_time:.4f} seconds")
    print(f"Descriptor attribute: {desc_time:.4f} seconds")
    print(f"Descriptor is {desc_time / reg_time:.2f}x slower (but provides more features)")


# ============================================================
# MAIN EXECUTION
# ============================================================

if __name__ == "__main__":
    demonstrate_descriptors()

    print("\n" + "=" * 70)
    print("DESCRIPTORS KEY CONCEPTS")
    print("=" * 70)
    print("""
    ✅ DESCRIPTOR PROTOCOL
       - __get__(self, instance, owner) - Get attribute
       - __set__(self, instance, value) - Set attribute
       - __delete__(self, instance) - Delete attribute

    ✅ TYPES OF DESCRIPTORS
       - Data Descriptor: Implements __get__ and __set__
       - Non-data Descriptor: Only implements __get__

    ✅ USE CASES
       - Validation (type checking, range checking)
       - Lazy loading and caching
       - Read-only attributes
       - ORM models (Django, SQLAlchemy)
       - History tracking
       - Property implementation
       - Framework development

    ✅ DESCRIPTOR VS PROPERTY
       - Property: Simpler, per-instance
       - Descriptor: More complex, reusable, class-level

    ✅ BEST PRACTICES
       - Store data in instance __dict__
       - Handle instance is None case
       - Use descriptors for reusable attribute logic
       - Document descriptor behavior
       - Consider performance implications
    """)
    print("=" * 70)