# Object-Oriented Programming in Python: Complete Master Guide

> A practical beginner-to-advanced guide to classes, objects, methods, encapsulation, inheritance, polymorphism, abstraction, composition, special methods, dataclasses, typing, SOLID design, testing, and advanced Python object-model features.

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Topic](https://img.shields.io/badge/Topic-Object--Oriented%20Programming-2E8B57)](#)
[![Level](https://img.shields.io/badge/Level-Beginner%20to%20Advanced-orange)](#)

---

## Table of Contents

1. [Introduction](#1-introduction)
2. [Why OOP Matters](#2-why-oop-matters)
3. [Project Setup and Suggested Files](#3-project-setup-and-suggested-files)
4. [Core OOP Terminology](#4-core-oop-terminology)
5. [Creating Classes and Objects](#5-creating-classes-and-objects)
6. [Attributes and Namespaces](#6-attributes-and-namespaces)
7. [Instance, Class, and Static Methods](#7-instance-class-and-static-methods)
8. [Encapsulation and Properties](#8-encapsulation-and-properties)
9. [Inheritance](#9-inheritance)
10. [Polymorphism and Duck Typing](#10-polymorphism-and-duck-typing)
11. [Abstraction, ABCs, and Protocols](#11-abstraction-abcs-and-protocols)
12. [Composition, Aggregation, and Association](#12-composition-aggregation-and-association)
13. [Special Methods and Operator Overloading](#13-special-methods-and-operator-overloading)
14. [Iterable, Iterator, Callable, and Context-Manager Objects](#14-iterable-iterator-callable-and-context-manager-objects)
15. [Dataclasses](#15-dataclasses)
16. [Type Hints and Generic Classes](#16-type-hints-and-generic-classes)
17. [Object Identity, Equality, Copying, and Hashing](#17-object-identity-equality-copying-and-hashing)
18. [Exceptions and Resource Management](#18-exceptions-and-resource-management)
19. [SOLID Principles in Python](#19-solid-principles-in-python)
20. [Useful Design Patterns](#20-useful-design-patterns)
21. [Testing OOP Code](#21-testing-oop-code)
22. [Advanced Object-Model Features](#22-advanced-object-model-features)
23. [Common Mistakes and Fixes](#23-common-mistakes-and-fixes)
24. [Clean-Code, Performance, and Security Tips](#24-clean-code-performance-and-security-tips)
25. [Practice Exercises](#25-practice-exercises)
26. [Mini-Projects](#26-mini-projects)
27. [Mastery Roadmap](#27-mastery-roadmap)
28. [Complete OOP Cheat Sheet](#28-complete-oop-cheat-sheet)
29. [Official References](#29-official-references)

---

## 1. Introduction

Object-oriented programming, usually called **OOP**, organizes software around objects that combine **state** and **behavior**.

- **State** is the data an object currently holds.
- **Behavior** is what the object can do.

For example, a bank account object may store an owner's name and balance while providing deposit and withdrawal behaviors.

```python
class BankAccount:
    def __init__(self, owner: str, balance: float = 0.0) -> None:
        self.owner = owner
        self.balance = balance

    def deposit(self, amount: float) -> None:
        self.balance += amount


account = BankAccount("Ankita", 1_000.0)
account.deposit(500.0)
print(account.balance)  # 1500.0
```

Python is a **multi-paradigm language**. OOP is useful, but it is not required for every problem. Good Python programs often combine classes with functions, modules, comprehensions, generators, and immutable values.

### Learning outcomes

After studying this guide, you should be able to:

- create well-designed classes and objects;
- explain instance, class, and static methods;
- apply encapsulation, inheritance, polymorphism, and abstraction;
- choose composition or inheritance appropriately;
- implement properties and common special methods;
- use abstract base classes, protocols, dataclasses, and type hints;
- understand method resolution order and cooperative `super()`;
- make intentional choices about equality, copying, and hashing;
- test classes without depending on hidden global state; and
- recognize when a class improves a design and when a function is simpler.

---

## 2. Why OOP Matters

OOP can help a program by providing:

- **organization:** related data and behavior live together;
- **reuse:** carefully designed components can serve multiple parts of a system;
- **maintainability:** responsibilities can be separated into focused classes;
- **testability:** collaborators can be replaced with controlled test doubles;
- **extensibility:** new implementations can follow an existing interface;
- **abstraction:** callers use a clear public API without knowing every internal detail; and
- **modeling:** software concepts can represent accounts, users, files, sensors, reports, or security policies.

### When a class is a good choice

Consider a class when:

- several operations share the same state;
- an invariant must remain true across multiple operations;
- many objects follow the same structure but hold different data;
- behavior varies by implementation;
- a resource needs a controlled lifecycle; or
- a meaningful domain concept has both data and behavior.

### When a class may be unnecessary

A function, dictionary, tuple, or module may be clearer when:

- there is no lasting state;
- the task is one small transformation;
- the class would contain only one trivial method;
- a namespace is the only goal; or
- procedural code expresses the workflow more directly.

Avoid creating “manager,” “helper,” or “utility” classes merely to place unrelated functions under one name.

---

## 3. Project Setup and Suggested Files

A study repository can be organized like this:

```text
python-oop/
├── README.md
├── basics/
│   ├── classes_and_objects.py
│   ├── attributes.py
│   └── method_types.py
├── principles/
│   ├── encapsulation.py
│   ├── inheritance.py
│   ├── polymorphism.py
│   └── abstraction.py
├── advanced/
│   ├── composition.py
│   ├── dataclasses_example.py
│   ├── magic_methods.py
│   ├── protocols.py
│   └── slots_and_descriptors.py
├── projects/
│   ├── bank_system.py
│   └── secure_vault_model.py
└── tests/
    └── test_bank_account.py
```

### Requirements

- Python 3.10 or later is recommended.
- Most examples use only the standard library.
- Examples using `typing.Self` require Python 3.11+, so this guide shows a compatible alternative when needed.

Check the Python version:

```bash
python --version
```

Run a file:

```bash
python classes_and_objects.py
```

Run standard-library tests:

```bash
python -m unittest discover -s tests -v
```

---

## 4. Core OOP Terminology

| Term | Meaning |
|---|---|
| Class | A definition that describes attributes and behavior |
| Object/instance | A concrete value created from a class |
| Attribute | Data or behavior accessed with dotted syntax |
| Instance variable | Data normally unique to one instance |
| Class variable | Data stored on and normally shared through the class |
| Method | A function accessed through a class or instance |
| Constructor call | Calling a class to create an instance |
| `__new__()` | Creates and returns an instance |
| `__init__()` | Initializes an already-created instance |
| Encapsulation | Managing state through a clear public interface |
| Inheritance | Defining a class based on another class |
| Polymorphism | Different objects responding to the same operation |
| Abstraction | Exposing essential behavior while hiding unnecessary details |
| Composition | Building an object from other objects |
| MRO | Method Resolution Order used for attribute lookup in inheritance |
| Interface | The operations an object promises to support |

### The four commonly taught OOP pillars

| Pillar | Central question | Python approach |
|---|---|---|
| Encapsulation | How does the object keep its state valid? | Public APIs, conventions, properties, descriptors |
| Inheritance | How can a true subtype extend a base type? | Base classes, overriding, `super()`, MRO |
| Polymorphism | How can different objects support one operation? | Duck typing, protocols, overriding, special methods |
| Abstraction | What may callers rely on without knowing the implementation? | Focused APIs, ABCs, protocols, composition |

These pillars overlap. For example, a protocol provides abstraction and enables polymorphism, while a property supports encapsulation.

### Everything is an object

In Python, integers, strings, functions, classes, modules, and instances are objects.

```python
print(type(42))          # <class 'int'>
print(type("Python"))    # <class 'str'>
print(type(BankAccount)) # <class 'type'>
```

Classes are themselves objects, usually created by the metaclass `type`.

---

## 5. Creating Classes and Objects

### 5.1 A minimal class

```python
class Student:
    pass


student = Student()
print(type(student))
print(isinstance(student, Student))  # True
```

Class names normally use `PascalCase`.

### 5.2 Initializing instance state

```python
class Student:
    def __init__(self, name: str, course: str) -> None:
        self.name = name
        self.course = course


ankita = Student("Ankita", "Artificial Intelligence")
maya = Student("Maya", "Cybersecurity")

print(ankita.name)
print(maya.course)
```

Each call creates a separate object with its own instance state.

### 5.3 What `self` means

`self` refers to the instance on which an instance method operates. It is passed automatically when a method is called through an instance.

```python
class Greeter:
    def greet(self, name: str) -> str:
        return f"Hello, {name}!"


greeter = Greeter()
print(greeter.greet("Ankita"))
```

This call:

```python
greeter.greet("Ankita")
```

is conceptually equivalent to:

```python
Greeter.greet(greeter, "Ankita")
```

`self` is a strong convention rather than a reserved keyword. Always follow the convention for readability.

### 5.4 `__init__()` is not the object creator

Python normally performs object construction in two stages:

1. `__new__(cls, ...)` creates and returns an instance.
2. `__init__(self, ...)` initializes that instance and must return `None`.

Most classes need only `__init__()`.

```python
class User:
    def __new__(cls, *args, **kwargs):
        instance = super().__new__(cls)
        return instance

    def __init__(self, username: str) -> None:
        self.username = username
```

Override `__new__()` mainly for immutable subclasses, controlled construction, or advanced frameworks.

### 5.5 Methods define behavior

```python
class Rectangle:
    def __init__(self, width: float, height: float) -> None:
        if width <= 0 or height <= 0:
            raise ValueError("dimensions must be positive")
        self.width = width
        self.height = height

    def area(self) -> float:
        return self.width * self.height

    def perimeter(self) -> float:
        return 2 * (self.width + self.height)


rectangle = Rectangle(4, 3)
print(rectangle.area())       # 12
print(rectangle.perimeter())  # 14
```

### 5.6 Documentation

```python
class PasswordPolicy:
    """Validate passwords against configurable minimum requirements."""

    def __init__(self, minimum_length: int = 12) -> None:
        """Create a policy with a required minimum length."""
        self.minimum_length = minimum_length

    def is_valid(self, password: str) -> bool:
        """Return whether the password satisfies this policy."""
        return len(password) >= self.minimum_length
```

Use `help(PasswordPolicy)` or access `PasswordPolicy.__doc__` to inspect documentation.

---

## 6. Attributes and Namespaces

### 6.1 Instance variables

Instance variables hold state for a particular object.

```python
class Employee:
    def __init__(self, name: str, salary: float) -> None:
        self.name = name
        self.salary = salary
```

### 6.2 Class variables

Class variables are stored on the class and are normally shared through its instances.

```python
class Employee:
    organization = "TechStart"

    def __init__(self, name: str) -> None:
        self.name = name


first = Employee("Asha")
second = Employee("Nima")

print(first.organization)   # TechStart
print(second.organization)  # TechStart
```

Changing the class attribute affects instances that have not shadowed it:

```python
Employee.organization = "SecureTech"
print(first.organization)  # SecureTech
```

Assigning through one instance creates or changes an instance attribute:

```python
first.organization = "Local Office"
print(first.organization)    # Local Office
print(second.organization)   # SecureTech
```

### 6.3 Mutable class-variable trap

Wrong: every instance shares the same list.

```python
class Student:
    subjects = []

    def __init__(self, name: str) -> None:
        self.name = name


first = Student("Asha")
second = Student("Nima")
first.subjects.append("Python")
print(second.subjects)  # ['Python'] — unexpectedly shared
```

Correct: create mutable state for each instance.

```python
class Student:
    def __init__(self, name: str) -> None:
        self.name = name
        self.subjects: list[str] = []
```

Use class variables intentionally for constants, shared configuration, registries, or counters.

### 6.4 Attribute lookup

In a simplified view, `instance.attribute` searches:

1. relevant data descriptors on the class hierarchy;
2. the instance namespace, usually `instance.__dict__`;
3. the class and base-class namespaces; and
4. fallback hooks such as `__getattr__()`.

Descriptors and special attribute hooks make the full process more detailed.

### 6.5 Inspecting attributes

```python
employee = Employee("Asha")

print(hasattr(employee, "name"))
print(getattr(employee, "name"))
setattr(employee, "department", "Security")
delattr(employee, "department")
```

Use dynamic attribute functions when the attribute name is genuinely data-driven. Normal dotted access is clearer for fixed names.

```python
print(vars(employee))
print(dir(employee))
```

- `vars(obj)` commonly returns the object's attribute dictionary.
- `dir(obj)` returns a broader list of available names and is mainly useful for inspection.

---

## 7. Instance, Class, and Static Methods

| Method type | First parameter | Main purpose |
|---|---|---|
| Instance method | `self` | Work with one instance's state |
| Class method | `cls` | Work with the class; often an alternative constructor |
| Static method | None supplied automatically | Utility closely related to the class concept |

### 7.1 Instance methods

```python
class Counter:
    def __init__(self) -> None:
        self.value = 0

    def increment(self, amount: int = 1) -> None:
        self.value += amount
```

### 7.2 Class methods

Use `@classmethod` when the operation needs the class rather than a particular instance.

```python
class Temperature:
    def __init__(self, celsius: float) -> None:
        self.celsius = celsius

    @classmethod
    def from_fahrenheit(cls, fahrenheit: float) -> "Temperature":
        celsius = (fahrenheit - 32) * 5 / 9
        return cls(celsius)


temperature = Temperature.from_fahrenheit(86)
print(temperature.celsius)  # 30.0
```

Using `cls(...)` supports subclasses better than hard-coding `Temperature(...)`.

Class-level state example:

```python
class Session:
    created_count = 0

    def __init__(self) -> None:
        type(self).created_count += 1

    @classmethod
    def total_created(cls) -> int:
        return cls.created_count
```

### 7.3 Static methods

```python
class PasswordPolicy:
    @staticmethod
    def contains_digit(password: str) -> bool:
        return any(character.isdigit() for character in password)
```

A static method receives neither `self` nor `cls`. Use it when a function belongs conceptually to the class's public API but needs no object or class state.

If the function is useful independently, a module-level function may be simpler and easier to reuse.

### 7.4 Choosing the method type

- Needs instance data? Use an instance method.
- Needs the class, subclass-aware construction, or class state? Use a class method.
- Needs neither but strongly belongs to the concept? Consider a static method.
- Does not belong specifically to the class? Use a module-level function.

---

## 8. Encapsulation and Properties

Encapsulation means protecting a valid internal state behind a clear public interface. Python relies more on conventions and cooperation than strict access restrictions.

### 8.1 Naming conventions

| Form | Meaning |
|---|---|
| `name` | Public API |
| `_name` | Non-public implementation detail by convention |
| `__name` | Name-mangled to reduce accidental subclass clashes |
| `__name__` | Special Python-defined name; do not invent casually |

Python does not have truly private instance attributes in the Java/C++ sense.

### 8.2 Single leading underscore

```python
class ApiClient:
    def __init__(self, token: str) -> None:
        self._token = token
```

`_token` can still be accessed, but callers are told that it is an implementation detail and may change.

### 8.3 Double leading underscore and name mangling

```python
class Base:
    def __init__(self) -> None:
        self.__internal_state = "base"
```

Inside the class definition, Python transforms the name approximately to `_Base__internal_state`. This is designed mainly to avoid accidental name collisions in subclasses, not to enforce security.

Never store secrets in an object assuming name mangling makes them inaccessible.

### 8.4 Properties

A property gives attribute-style access while running controlled logic.

```python
class BankAccount:
    def __init__(self, owner: str, balance: float = 0.0) -> None:
        self.owner = owner
        self.balance = balance

    @property
    def balance(self) -> float:
        return self._balance

    @balance.setter
    def balance(self, value: float) -> None:
        if value < 0:
            raise ValueError("balance must not be negative")
        self._balance = float(value)
```

Usage remains natural:

```python
account = BankAccount("Ankita", 500)
print(account.balance)
account.balance = 750
```

### 8.5 Read-only computed property

```python
class Rectangle:
    def __init__(self, width: float, height: float) -> None:
        self.width = width
        self.height = height

    @property
    def area(self) -> float:
        return self.width * self.height
```

With no setter, `rectangle.area = value` raises `AttributeError`.

### 8.6 Property deletion

```python
class User:
    def __init__(self, token: str) -> None:
        self._token = token

    @property
    def token(self) -> str:
        return self._token

    @token.deleter
    def token(self) -> None:
        del self._token
```

Deletion methods are uncommon; explicit methods such as `revoke_token()` often communicate intent better.

### 8.7 Avoid Java-style boilerplate

Do not write trivial getters and setters merely because another language requires them.

```python
class Student:
    def __init__(self, name: str) -> None:
        self.name = name  # normal public attribute is fine
```

Start with a public attribute. Convert it to a property later when validation or computed behavior becomes necessary; existing attribute-style callers can remain unchanged.

---

## 9. Inheritance

Inheritance expresses an **is-a** relationship. A subclass receives behavior from one or more base classes and may extend or override it.

### 9.1 Basic inheritance

```python
class Employee:
    def __init__(self, name: str) -> None:
        self.name = name

    def describe_role(self) -> str:
        return "Employee"


class SecurityAnalyst(Employee):
    def describe_role(self) -> str:
        return "Security Analyst"


analyst = SecurityAnalyst("Ankita")
print(analyst.name)
print(analyst.describe_role())
```

### 9.2 Calling parent behavior with `super()`

```python
class Employee:
    def __init__(self, name: str, email: str) -> None:
        self.name = name
        self.email = email


class SecurityAnalyst(Employee):
    def __init__(self, name: str, email: str, skills: list[str]) -> None:
        super().__init__(name, email)
        self.skills = list(skills)
```

`super()` does not simply mean “my parent.” It returns a proxy that continues lookup according to the class's method resolution order, which is essential for cooperative multiple inheritance.

### 9.3 Method overriding

```python
class Notification:
    def send(self, message: str) -> str:
        return f"Generic notification: {message}"


class EmailNotification(Notification):
    def send(self, message: str) -> str:
        return f"Email sent: {message}"
```

The subclass implementation is selected when called on a subclass instance.

### 9.4 Extending instead of replacing

```python
class AuditedAccount(BankAccount):
    def deposit(self, amount: float) -> None:
        super().deposit(amount)
        print(f"Audit: deposited {amount}")
```

### 9.5 Type checks

```python
print(isinstance(analyst, SecurityAnalyst))  # True
print(isinstance(analyst, Employee))         # True
print(issubclass(SecurityAnalyst, Employee)) # True
```

Prefer polymorphic behavior over repeated exact-type checks. When a check is justified, `isinstance()` usually supports subclasses better than `type(obj) is SomeClass`.

### 9.6 Multiple inheritance

```python
class JsonMixin:
    def to_json(self) -> str:
        import json
        return json.dumps(vars(self))


class User:
    def __init__(self, username: str) -> None:
        self.username = username


class SerializableUser(JsonMixin, User):
    pass
```

Multiple inheritance works best with small, focused mixins or carefully cooperative classes.

### 9.7 Method Resolution Order

```python
print(SerializableUser.mro())
print(SerializableUser.__mro__)
```

Python uses a consistent C3 linearization to determine attribute lookup order. The MRO:

- respects the base-class order written in each class;
- prevents the same base class from being visited repeatedly in a diamond; and
- supports cooperative `super()` calls.

### 9.8 Cooperative multiple inheritance

```python
class Root:
    def process(self) -> list[str]:
        return ["Root"]


class LoggingMixin(Root):
    def process(self) -> list[str]:
        return ["Logging"] + super().process()


class ValidationMixin(Root):
    def process(self) -> list[str]:
        return ["Validation"] + super().process()


class Service(LoggingMixin, ValidationMixin):
    pass


print(Service().process())
# ['Logging', 'Validation', 'Root']
```

Cooperative methods must use compatible signatures and consistently call `super()`.

### 9.9 Favor shallow inheritance trees

Deep inheritance can make behavior difficult to trace. Prefer composition when a class wants to **use** another service rather than truly represent a specialized form of it.

---

## 10. Polymorphism and Duck Typing

Polymorphism allows one operation to work with objects of different classes.

### 10.1 Common method interface

```python
class EmailSender:
    def send(self, message: str) -> None:
        print(f"Email: {message}")


class SmsSender:
    def send(self, message: str) -> None:
        print(f"SMS: {message}")


def notify(sender, message: str) -> None:
    sender.send(message)


notify(EmailSender(), "System updated")
notify(SmsSender(), "System updated")
```

The function depends on supported behavior, not a shared parent class.

### 10.2 Duck typing

Python often follows the idea: “If it behaves like the required object, use it.” The object's concrete class matters less than the operations it supports.

```python
def save_report(destination, content: str) -> None:
    destination.write(content)
```

This can work with a real file, an in-memory `io.StringIO`, or another object implementing a compatible `write()` method.

### 10.3 EAFP versus LBYL

Python often prefers **EAFP**: Easier to Ask Forgiveness than Permission.

```python
try:
    sender.send(message)
except AttributeError as error:
    raise TypeError("sender must provide send(message)") from error
```

**LBYL** means Look Before You Leap:

```python
if hasattr(sender, "send"):
    sender.send(message)
```

EAFP avoids race conditions between checking and acting and works naturally with duck typing. Catch only the specific exception you can meaningfully handle; broad exception handling can hide real bugs inside the method.

### 10.4 Built-in polymorphism

```python
print(len("Python"))
print(len([1, 2, 3]))
print(len({"name": "Ankita"}))
```

Each type responds to the same `len()` operation through its own implementation.

### 10.5 Overriding versus overloading

| Concept | Meaning in Python |
|---|---|
| Method overriding | A subclass provides a new implementation of an inherited method |
| Traditional signature-based overloading | Multiple same-named methods selected only by argument types/count; Python does not do this automatically |

Defining the same method name twice in one class replaces the earlier definition:

```python
class Calculator:
    def add(self, first, second):
        return first + second

    def add(self, first, second, third):
        return first + second + third


# Only the second add() definition remains.
```

Common Python alternatives include default arguments and flexible argument lists:

```python
class Calculator:
    def add(self, first: float, second: float, third: float = 0) -> float:
        return first + second + third


class FlexibleCalculator:
    def add(self, *numbers: float) -> float:
        return sum(numbers)
```

For deliberate runtime dispatch on the first non-`self` argument, the standard library provides `functools.singledispatchmethod`:

```python
from functools import singledispatchmethod


class Formatter:
    @singledispatchmethod
    def format(self, value: object) -> str:
        return str(value)

    @format.register
    def _(self, value: list) -> str:
        return ", ".join(map(str, value))
```

`typing.overload` describes multiple call signatures to a type checker but still requires one runtime implementation.

---

## 11. Abstraction, ABCs, and Protocols

Abstraction defines what clients may rely on while leaving implementation details to concrete classes.

### 11.1 Abstract base classes

```python
from abc import ABC, abstractmethod


class Storage(ABC):
    @abstractmethod
    def save(self, key: str, data: bytes) -> None:
        """Store bytes under a key."""

    @abstractmethod
    def load(self, key: str) -> bytes:
        """Return bytes stored under a key."""


class MemoryStorage(Storage):
    def __init__(self) -> None:
        self._data: dict[str, bytes] = {}

    def save(self, key: str, data: bytes) -> None:
        self._data[key] = data

    def load(self, key: str) -> bytes:
        return self._data[key]
```

An abstract class cannot normally be instantiated until all abstract methods are implemented.

```python
storage = MemoryStorage()
storage.save("report", b"contents")
```

### 11.2 Abstract methods may contain code

```python
class Report(ABC):
    @abstractmethod
    def render(self) -> str:
        return "Report header\n"
```

A subclass may call this implementation with `super()`. Abstract does not necessarily mean empty.

### 11.3 Protocols: structural interfaces

Protocols describe required behavior for static type checkers without requiring inheritance.

```python
from typing import Protocol


class Sender(Protocol):
    def send(self, message: str) -> None:
        ...


def broadcast(sender: Sender, message: str) -> None:
    sender.send(message)
```

Any appropriately typed object with a compatible `send()` method satisfies the protocol structurally.

### 11.4 Runtime-checkable protocols

```python
from typing import Protocol, runtime_checkable


@runtime_checkable
class Closable(Protocol):
    def close(self) -> None:
        ...


print(isinstance(storage, Closable))
```

Runtime protocol checks test only the presence of required attributes, not full signatures or semantic correctness. Do not treat them as data validation.

### 11.5 ABC versus Protocol

| Need | Good choice |
|---|---|
| Shared implementation and enforced abstract methods | ABC |
| Structural typing without required inheritance | Protocol |
| Simple dynamic behavior with no static contract | Duck typing |
| Only a function signature is needed | `Callable` type |

---

## 12. Composition, Aggregation, and Association

### 12.1 Composition: a strong has-a relationship

```python
class Engine:
    def start(self) -> str:
        return "Engine started"


class Car:
    def __init__(self) -> None:
        self._engine = Engine()

    def start(self) -> str:
        return self._engine.start()
```

The car creates and owns its engine component.

### 12.2 Dependency injection

Passing the collaborator from outside makes code more flexible and testable.

```python
class Car:
    def __init__(self, engine: Engine) -> None:
        self._engine = engine

    def start(self) -> str:
        return self._engine.start()
```

### 12.3 Aggregation: externally owned collaborator

```python
class Teacher:
    def __init__(self, name: str) -> None:
        self.name = name


class Department:
    def __init__(self, teachers: list[Teacher]) -> None:
        self.teachers = list(teachers)
```

Teacher objects can exist independently of the department.

### 12.4 Association

Association is a general relationship where objects know about or temporarily use each other.

```python
class PaymentService:
    def charge(self, account: BankAccount, amount: float) -> None:
        account.withdraw(amount)
```

### 12.5 Composition versus inheritance

| Question | Likely design |
|---|---|
| “Is this genuinely a specialized form of that?” | Inheritance may fit |
| “Does this object use or contain that?” | Composition likely fits |
| “Must behavior change at runtime?” | Composition is often easier |
| “Is only a small capability reused?” | Mixins, functions, or composition |

Prefer composition by default when the relationship is not clearly **is-a**.

---

## 13. Special Methods and Operator Overloading

Special methods, often called **dunder methods**, integrate classes with Python syntax and built-in functions.

### 13.1 Common special methods

| Method | Triggered by | Purpose |
|---|---|---|
| `__new__()` | `Class(...)` | Create an instance |
| `__init__()` | After creation | Initialize an instance |
| `__repr__()` | `repr(obj)` | Unambiguous developer representation |
| `__str__()` | `str(obj)`, `print(obj)` | Friendly user representation |
| `__len__()` | `len(obj)` | Length |
| `__bool__()` | `bool(obj)`, conditions | Truth value |
| `__eq__()` | `obj == other` | Equality |
| `__lt__()` | `obj < other` | Less-than comparison |
| `__hash__()` | `hash(obj)` | Hash for sets/dictionary keys |
| `__contains__()` | `item in obj` | Membership |
| `__getitem__()` | `obj[key]` | Index or key access |
| `__setitem__()` | `obj[key] = value` | Indexed assignment |
| `__iter__()` | `iter(obj)`, loops | Obtain iterator |
| `__next__()` | `next(iterator)` | Produce next item |
| `__call__()` | `obj(...)` | Make instance callable |
| `__enter__()` | `with obj` | Enter context |
| `__exit__()` | Leaving `with` | Exit context |
| `__add__()` | `obj + other` | Addition |
| `__sub__()` | `obj - other` | Subtraction |
| `__mul__()` | `obj * other` | Multiplication |
| `__format__()` | `format(obj, spec)` | Formatting |

### 13.2 `__repr__()` and `__str__()`

```python
class Student:
    def __init__(self, name: str, score: int) -> None:
        self.name = name
        self.score = score

    def __repr__(self) -> str:
        return f"Student(name={self.name!r}, score={self.score!r})"

    def __str__(self) -> str:
        return f"{self.name}: {self.score}"
```

Guidelines:

- `__repr__()` should be precise and useful for debugging.
- `__str__()` should be readable for users.
- When `__str__()` is absent, Python can fall back to `__repr__()`.
- Never include passwords, tokens, encryption keys, or personal secrets in representations.

### 13.3 Equality

```python
class Coordinate:
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Coordinate):
            return NotImplemented
        return self.x == other.x and self.y == other.y
```

Return `NotImplemented` for an unsupported type instead of `False`, allowing Python to try the reflected comparison.

### 13.4 Ordering

```python
from functools import total_ordering


@total_ordering
class Score:
    def __init__(self, value: int) -> None:
        self.value = value

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Score):
            return NotImplemented
        return self.value == other.value

    def __lt__(self, other: object) -> bool:
        if not isinstance(other, Score):
            return NotImplemented
        return self.value < other.value
```

`@total_ordering` fills in remaining ordering methods from `__eq__()` and one ordering method. Defining all comparisons directly can be faster and produce clearer stack traces in performance-sensitive code.

### 13.5 Arithmetic operator overloading

```python
class Vector:
    def __init__(self, x: float, y: float) -> None:
        self.x = x
        self.y = y

    def __add__(self, other: object) -> "Vector":
        if not isinstance(other, Vector):
            return NotImplemented
        return Vector(self.x + other.x, self.y + other.y)

    def __repr__(self) -> str:
        return f"Vector(x={self.x!r}, y={self.y!r})"
```

Operator behavior should be natural, predictable, and free from surprising unrelated side effects.

### 13.6 Reflected and in-place operators

| Operation | Primary | Reflected | In-place |
|---|---|---|---|
| Addition | `__add__()` | `__radd__()` | `__iadd__()` |
| Subtraction | `__sub__()` | `__rsub__()` | `__isub__()` |
| Multiplication | `__mul__()` | `__rmul__()` | `__imul__()` |
| Matrix multiplication | `__matmul__()` | `__rmatmul__()` | `__imatmul__()` |

Do not implement an in-place method unless mutation semantics are clear and appropriate.

### 13.7 Container-style behavior

```python
class GradeBook:
    def __init__(self) -> None:
        self._scores: dict[str, int] = {}

    def __len__(self) -> int:
        return len(self._scores)

    def __contains__(self, student: object) -> bool:
        return student in self._scores

    def __getitem__(self, student: str) -> int:
        return self._scores[student]

    def __setitem__(self, student: str, score: int) -> None:
        if not 0 <= score <= 100:
            raise ValueError("score must be between 0 and 100")
        self._scores[student] = score
```

Usage:

```python
grades = GradeBook()
grades["Ankita"] = 92

print(grades["Ankita"])
print("Ankita" in grades)
print(len(grades))
```

---

## 14. Iterable, Iterator, Callable, and Context-Manager Objects

### 14.1 Iterable objects

An iterable provides `__iter__()` returning an iterator. A generator often keeps the implementation simple.

```python
class Team:
    def __init__(self, members: list[str]) -> None:
        self._members = list(members)

    def __iter__(self):
        return iter(self._members)
```

```python
for member in Team(["Asha", "Nima"]):
    print(member)
```

Each call to `iter(team)` gets an independent list iterator.

### 14.2 Iterator objects

An iterator provides `__next__()` and returns itself from `__iter__()`.

```python
class Countdown:
    def __init__(self, start: int) -> None:
        self._current = start

    def __iter__(self) -> "Countdown":
        return self

    def __next__(self) -> int:
        if self._current <= 0:
            raise StopIteration
        value = self._current
        self._current -= 1
        return value
```

Iterators are stateful and are usually consumed once. A generator function is often easier:

```python
def countdown(start: int):
    while start > 0:
        yield start
        start -= 1
```

### 14.3 Callable objects

```python
class Threshold:
    def __init__(self, minimum: float) -> None:
        self.minimum = minimum

    def __call__(self, value: float) -> bool:
        return value >= self.minimum


is_passing = Threshold(50)
print(is_passing(72))  # True
```

Callable objects are useful when behavior needs configuration and retained state.

### 14.4 Context managers

```python
class AuditSession:
    def __init__(self, name: str) -> None:
        self.name = name

    def __enter__(self) -> "AuditSession":
        print(f"Starting audit: {self.name}")
        return self

    def record(self, event: str) -> None:
        print(f"Audit event: {event}")

    def __exit__(self, exc_type, exc_value, traceback) -> bool:
        print(f"Closing audit: {self.name}")
        return False
```

```python
with AuditSession("login-review") as audit:
    audit.record("Started analysis")
```

Returning `False` from `__exit__()` allows an exception to propagate. Returning `True` suppresses it; suppress only exceptions the context manager genuinely handles.

For simple context managers, `contextlib.contextmanager` may be more concise.

---

## 15. Dataclasses

Dataclasses reduce boilerplate for classes primarily storing structured data. The decorator can generate methods such as `__init__()`, `__repr__()`, and `__eq__()`.

### 15.1 Basic dataclass

```python
from dataclasses import dataclass


@dataclass
class InventoryItem:
    name: str
    unit_price: float
    quantity: int = 0

    def total_cost(self) -> float:
        return self.unit_price * self.quantity
```

```python
item = InventoryItem("Keyboard", 45.0, 2)
print(item)
print(item.total_cost())
```

### 15.2 Mutable defaults

Use `default_factory` for a new mutable value per instance.

```python
from dataclasses import dataclass, field


@dataclass
class Student:
    name: str
    subjects: list[str] = field(default_factory=list)
```

### 15.3 Validation with `__post_init__()`

```python
@dataclass
class Product:
    name: str
    price: float

    def __post_init__(self) -> None:
        if not self.name.strip():
            raise ValueError("name must not be empty")
        if self.price < 0:
            raise ValueError("price must not be negative")
```

### 15.4 Frozen dataclass

```python
@dataclass(frozen=True)
class Coordinate:
    latitude: float
    longitude: float
```

`frozen=True` emulates read-only fields but does not make nested mutable values deeply immutable.

### 15.5 Ordering, keyword-only fields, and slots

```python
@dataclass(order=True, kw_only=True, slots=True)
class Task:
    priority: int
    title: str
```

```python
task = Task(priority=1, title="Review logs")
```

- `order=True` generates ordering comparisons based on field order.
- `kw_only=True` requires keyword arguments for generated initialization.
- `slots=True` generates slots and returns a new slotted class.

Use these options deliberately; field order becomes part of comparison semantics when ordering is enabled.

### 15.6 Field options

```python
from dataclasses import dataclass, field


@dataclass
class Account:
    username: str
    password_hash: bytes = field(repr=False, compare=False)
    roles: set[str] = field(default_factory=set)
```

Sensitive fields should normally use `repr=False` so accidental logs do not expose them.

### 15.7 Dataclass utilities

```python
from dataclasses import asdict, replace

data = asdict(item)
updated = replace(item, quantity=5)
```

`asdict()` recursively converts nested dataclasses and deep-copies other nested data. It may be more expensive than a shallow field mapping.

### 15.8 When to use a dataclass

Use a dataclass when:

- the object primarily represents structured data;
- generated initialization and representation are appropriate; and
- field-based equality matches the domain.

Use a normal class when construction, invariants, identity, or behavior is the central design concern and generated behavior would be misleading.

---

## 16. Type Hints and Generic Classes

Type hints document intended usage and enable static analysis. Python does not enforce most annotations at runtime.

### 16.1 Annotated class

```python
class User:
    platform: str = "web"

    def __init__(self, username: str, roles: set[str] | None = None) -> None:
        self.username: str = username
        self.roles: set[str] = set() if roles is None else set(roles)

    def has_role(self, role: str) -> bool:
        return role in self.roles
```

Avoid mutable default arguments such as `roles: set[str] = set()`.

### 16.2 Class variables

```python
from typing import ClassVar


class User:
    platform: ClassVar[str] = "web"
```

`ClassVar` tells type checkers that the annotation describes class-level state.

### 16.3 Generic classes

```python
from typing import Generic, TypeVar


T = TypeVar("T")


class Box(Generic[T]):
    def __init__(self, value: T) -> None:
        self.value = value

    def get(self) -> T:
        return self.value
```

```python
number_box: Box[int] = Box(42)
name_box: Box[str] = Box("Ankita")
```

### 16.4 Subclass-aware return types

For Python 3.11+, `typing.Self` expresses that a method returns the current class type.

```python
from typing import Self


class User:
    @classmethod
    def anonymous(cls) -> Self:
        return cls("anonymous")
```

For Python 3.10, use a bound `TypeVar` or a string annotation suitable for your design.

### 16.5 Callable collaborators

```python
from collections.abc import Callable


class Processor:
    def __init__(self, transform: Callable[[str], str]) -> None:
        self._transform = transform

    def process(self, value: str) -> str:
        return self._transform(value)
```

### 16.6 Type-checking tools

Common static type checkers include mypy, Pyright, and IDE-integrated analyzers. Annotations improve tooling, but tests and runtime validation are still required at trust boundaries.

---

## 17. Object Identity, Equality, Copying, and Hashing

### 17.1 Identity versus equality

```python
first = Coordinate(10, 20)
second = Coordinate(10, 20)
alias = first

print(first == second)  # value equality if implemented/generated
print(first is second)  # False
print(first is alias)   # True
```

- `==` asks whether values are considered equal.
- `is` asks whether two references point to the same object.
- Use `is None` for the singleton `None`.

### 17.2 Assignment does not copy

```python
original = Student("Ankita")
alias = original
alias.subjects.append("Python")
print(original.subjects)  # ['Python']
```

### 17.3 Shallow and deep copying

```python
from copy import copy, deepcopy

shallow = copy(original)
deep = deepcopy(original)
```

- A shallow copy creates a new outer object while sharing referenced nested objects.
- A deep copy recursively copies many nested objects.

Copying objects that wrap locks, files, database connections, or network clients may be meaningless or unsafe. Consider an explicit `clone()` or reconstruction method when domain rules matter.

### 17.4 Equality and hashing contract

If two objects compare equal, their hashes must be equal.

Mutable value objects should normally be unhashable because changing a field involved in hashing would corrupt set or dictionary behavior.

```python
@dataclass(frozen=True)
class UserId:
    value: int
```

Frozen, field-hashable dataclasses can often be used safely as set elements or dictionary keys.

### 17.5 Avoid unsafe custom hashing

Do not hash mutable fields or force `unsafe_hash=True` without understanding the lifetime and mutation rules of the object.

---

## 18. Exceptions and Resource Management

### 18.1 Domain-specific exceptions

```python
class InsufficientFundsError(Exception):
    """Raised when an account cannot cover a withdrawal."""


class BankAccount:
    def __init__(self, balance: float = 0.0) -> None:
        self._balance = balance

    def withdraw(self, amount: float) -> None:
        if amount <= 0:
            raise ValueError("amount must be positive")
        if amount > self._balance:
            raise InsufficientFundsError("insufficient funds")
        self._balance -= amount
```

Custom exceptions help callers distinguish expected domain failures from programming errors.

### 18.2 Preserve exception context

```python
class ConfigurationError(Exception):
    pass


try:
    port = int(raw_port)
except ValueError as error:
    raise ConfigurationError("port must be an integer") from error
```

### 18.3 Do not catch everything

```python
# Avoid hiding unrelated bugs:
# try:
#     perform_operation()
# except Exception:
#     pass
```

Catch specific exceptions you can handle, add useful context, and otherwise let the error propagate.

### 18.4 Resource ownership

A class that opens a resource should clearly define who closes it. Prefer context managers for deterministic cleanup.

```python
with open("report.txt", "w", encoding="utf-8") as file:
    file.write("Report")
```

Do not depend on `__del__()` for important cleanup. Finalization timing is not a reliable substitute for `with`, `close()`, or `try`/`finally`.

---

## 19. SOLID Principles in Python

SOLID is a set of design guidelines, not rigid rules. Apply them in proportion to the program's complexity.

### 19.1 Single Responsibility Principle

A class should have one focused reason to change.

Less focused:

```python
class Report:
    def calculate(self): ...
    def save_to_database(self): ...
    def send_email(self): ...
```

More focused:

```python
class ReportCalculator:
    def calculate(self): ...


class ReportRepository:
    def save(self, report): ...


class ReportMailer:
    def send(self, report): ...
```

Do not split classes so aggressively that the design becomes fragmented and difficult to navigate.

### 19.2 Open/Closed Principle

Software should be open to extension without requiring repeated modification of stable code.

```python
class DiscountPolicy(Protocol):
    def discount(self, total: float) -> float:
        ...


class NoDiscount:
    def discount(self, total: float) -> float:
        return 0.0


class PercentageDiscount:
    def __init__(self, rate: float) -> None:
        self.rate = rate

    def discount(self, total: float) -> float:
        return total * self.rate
```

New policies can be introduced without editing a long conditional in the checkout service.

### 19.3 Liskov Substitution Principle

Where a base type is accepted, a subtype should preserve the expected contract.

A subclass should not:

- require stricter inputs than the base contract;
- provide weaker guarantees;
- throw surprising unrelated exceptions; or
- silently violate the meaning of inherited operations.

If `Square` cannot honor a mutable `Rectangle` interface consistently, they may be better modeled as separate immutable shapes sharing a protocol.

### 19.4 Interface Segregation Principle

Clients should not depend on methods they do not need.

```python
class Reader(Protocol):
    def read(self) -> bytes:
        ...


class Writer(Protocol):
    def write(self, data: bytes) -> None:
        ...
```

Small capability-focused protocols are often more reusable than one large interface.

### 19.5 Dependency Inversion Principle

High-level policy should depend on abstractions rather than constructing every low-level detail itself.

```python
class UserRepository(Protocol):
    def find(self, username: str) -> User | None:
        ...


class LoginService:
    def __init__(self, repository: UserRepository) -> None:
        self._repository = repository
```

Dependency injection makes production adapters and test doubles interchangeable.

---

## 20. Useful Design Patterns

Patterns are reusable design ideas, not mandatory templates.

### 20.1 Factory method

```python
class User:
    def __init__(self, username: str, active: bool) -> None:
        self.username = username
        self.active = active

    @classmethod
    def from_record(cls, record: dict[str, object]) -> "User":
        return cls(
            username=str(record["username"]),
            active=bool(record.get("active", True)),
        )
```

### 20.2 Strategy

```python
class PricingStrategy(Protocol):
    def final_price(self, subtotal: float) -> float:
        ...


class RegularPricing:
    def final_price(self, subtotal: float) -> float:
        return subtotal


class SalePricing:
    def __init__(self, discount_rate: float) -> None:
        self.discount_rate = discount_rate

    def final_price(self, subtotal: float) -> float:
        return subtotal * (1 - self.discount_rate)
```

### 20.3 Adapter

```python
class LegacyNotifier:
    def deliver_text(self, text: str) -> None:
        print(text)


class NotifierAdapter:
    def __init__(self, legacy: LegacyNotifier) -> None:
        self._legacy = legacy

    def send(self, message: str) -> None:
        self._legacy.deliver_text(message)
```

### 20.4 Repository

A repository hides persistence details behind domain-friendly operations such as `find()`, `add()`, and `remove()`. Keep transaction behavior and error semantics explicit.

### 20.5 Observer

```python
from collections.abc import Callable


class Event:
    def __init__(self) -> None:
        self._subscribers: list[Callable[[str], None]] = []

    def subscribe(self, callback: Callable[[str], None]) -> None:
        self._subscribers.append(callback)

    def publish(self, message: str) -> None:
        for callback in tuple(self._subscribers):
            callback(message)
```

Consider failure handling, unsubscription, ordering, and thread safety in production event systems.

### 20.6 Avoid pattern overuse

Python's functions, closures, modules, decorators, generators, and context managers can replace class-heavy patterns found in some other languages. Use the simplest design that clearly supports current requirements.

---

## 21. Testing OOP Code

### 21.1 Unit test example

```python
import unittest


class TestBankAccount(unittest.TestCase):
    def test_deposit_increases_balance(self) -> None:
        account = BankAccount("Ankita", 100)

        account.deposit(50)

        self.assertEqual(account.balance, 150)

    def test_negative_balance_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            BankAccount("Ankita", -1)


if __name__ == "__main__":
    unittest.main()
```

### 21.2 Test behavior, not implementation details

Prefer:

```python
self.assertEqual(account.balance, 150)
```

Avoid tests that depend unnecessarily on `_balance`, exact internal helper calls, or `__dict__` layout. Tests tied to private implementation make safe refactoring difficult.

### 21.3 Inject collaborators

```python
class FakeSender:
    def __init__(self) -> None:
        self.messages: list[str] = []

    def send(self, message: str) -> None:
        self.messages.append(message)


fake = FakeSender()
service = AlertService(sender=fake)
service.alert("Test")
assert fake.messages == ["Test"]
```

### 21.4 What to test

- valid construction;
- invalid inputs and invariants;
- public method results;
- state transitions;
- equality and representation when they matter;
- subclass or protocol substitutability;
- failure behavior;
- resource cleanup; and
- boundary cases.

---

## 22. Advanced Object-Model Features

Use these features only when they solve a real problem.

### 22.1 `__slots__`

```python
class Point:
    __slots__ = ("x", "y")

    def __init__(self, x: float, y: float) -> None:
        self.x = x
        self.y = y
```

Potential benefits:

- reduced per-instance memory when creating many objects;
- prevention of arbitrary new attributes unless `__dict__` is included; and
- sometimes faster attribute access.

Tradeoffs:

- more complicated inheritance;
- no automatic instance `__dict__` unless requested or inherited;
- weak references require `__weakref__`; and
- less flexibility for dynamic attributes and some tools.

Measure before using slots solely for optimization.

### 22.2 Descriptors

A descriptor defines one or more of `__get__()`, `__set__()`, and `__delete__()` to control attribute access.

```python
class PositiveNumber:
    def __set_name__(self, owner, name: str) -> None:
        self._name = f"_{name}"

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return getattr(instance, self._name)

    def __set__(self, instance, value: float) -> None:
        if value <= 0:
            raise ValueError("value must be positive")
        setattr(instance, self._name, value)


class Product:
    price = PositiveNumber()

    def __init__(self, price: float) -> None:
        self.price = price
```

Properties, instance methods, class methods, and static methods all rely on descriptor behavior internally.

### 22.3 `__getattr__()` and `__getattribute__()`

```python
class Settings:
    def __init__(self, values: dict[str, object]) -> None:
        self._values = values

    def __getattr__(self, name: str):
        try:
            return self._values[name]
        except KeyError as error:
            raise AttributeError(name) from error
```

- `__getattr__()` runs after normal lookup fails.
- `__getattribute__()` runs for nearly every attribute access and can easily cause infinite recursion.

Prefer properties or explicit methods unless dynamic attribute access is central to the design.

### 22.4 `__init_subclass__()`

```python
class Plugin:
    registry: dict[str, type["Plugin"]] = {}

    def __init_subclass__(cls, *, name: str, **kwargs) -> None:
        super().__init_subclass__(**kwargs)
        Plugin.registry[name] = cls


class CsvPlugin(Plugin, name="csv"):
    pass
```

This hook runs when a subclass is created and can support validation, registration, or framework conventions without a custom metaclass.

### 22.5 Class decorators

```python
def register(cls):
    PLUGINS[cls.__name__] = cls
    return cls


@register
class JsonPlugin:
    pass
```

A class decorator receives a class and returns a class-like object, often the original after modification or registration.

### 22.6 Metaclasses

A metaclass controls class creation. `type` is the usual metaclass.

```python
class LoggedType(type):
    def __new__(mcls, name, bases, namespace):
        print(f"Creating class {name}")
        return super().__new__(mcls, name, bases, namespace)


class Service(metaclass=LoggedType):
    pass
```

Before using a metaclass, consider whether a class decorator, `__init_subclass__()`, descriptor, or normal composition solves the problem more clearly.

### 22.7 Structural pattern matching with classes

```python
from dataclasses import dataclass


@dataclass
class LoginEvent:
    username: str
    successful: bool


def describe(event: LoginEvent) -> str:
    match event:
        case LoginEvent(username=name, successful=True):
            return f"Successful login: {name}"
        case LoginEvent(username=name, successful=False):
            return f"Failed login: {name}"
```

Pattern matching is useful for structured branching, but simple attribute access or polymorphism may be clearer when behavior naturally belongs to the object.

---

## 23. Common Mistakes and Fixes

### Mistake 1: Forgetting `self`

```python
class User:
    def greet(self) -> str:
        return "Hello"
```

### Mistake 2: Forgetting `self.` on attributes

```python
class User:
    def __init__(self, username: str) -> None:
        self.username = username
```

`username = username` only reassigns a local parameter.

### Mistake 3: Calling an instance method on the class incorrectly

```python
user = User("ankita")
user.greet()
```

`User.greet(user)` works but is rarely the clearest normal call.

### Mistake 4: Mutable class attributes used as instance state

Create `self.items = []` inside `__init__()` instead of using `items = []` on the class unless sharing is intentional.

### Mistake 5: Mutable default arguments

```python
class Team:
    def __init__(self, members: list[str] | None = None) -> None:
        self.members = [] if members is None else list(members)
```

### Mistake 6: Returning a value from `__init__()`

```python
class User:
    def __init__(self, username: str) -> None:
        self.username = username
        # no return value
```

Returning anything other than `None` raises `TypeError`.

### Mistake 7: Treating double underscore as secure privacy

Name mangling prevents accidental clashes; it does not protect secrets from callers who can inspect the process.

### Mistake 8: Excessive getters and setters

Use public attributes when appropriate and properties when controlled access is genuinely needed.

### Mistake 9: Inheritance used only for code reuse

If the subtype cannot honor the base class contract, use composition or a shared helper function.

### Mistake 10: Hard-coding the base class instead of cooperative `super()`

```python
super().__init__(...)
```

This normally preserves MRO behavior better than `BaseClass.__init__(self, ...)`.

### Mistake 11: Deep or confusing inheritance

Flatten hierarchies, extract collaborators, or replace inheritance with protocols and composition.

### Mistake 12: Returning `False` instead of `NotImplemented`

In binary special methods, return `NotImplemented` for unsupported operand types so Python can try the other operand's reflected method.

### Mistake 13: Exposing secrets in `__repr__()`

Mask or omit passwords, tokens, API keys, private keys, and personally sensitive values.

### Mistake 14: Making mutable objects hashable

Never use a hash based on fields that can change while the object is in a set or used as a dictionary key.

### Mistake 15: Depending on `__del__()` for cleanup

Use context managers or explicit cleanup methods.

### Mistake 16: Catching broad exceptions inside methods

Catch only expected errors and avoid silently hiding programming mistakes.

### Mistake 17: Using `type(obj) is Class`

Use `isinstance(obj, Class)` when subclasses should be accepted, or prefer a protocol/behavior-based design.

### Mistake 18: One giant “God object”

Split unrelated responsibilities into focused services or domain objects. Do not place database access, validation, formatting, emailing, and user-interface logic in one class.

### Mistake 19: Classes containing only static methods

A module of related functions may be simpler.

### Mistake 20: Overusing advanced features

Metaclasses, descriptors, multiple inheritance, and dynamic attribute hooks are powerful but increase cognitive cost. Prefer ordinary classes until a concrete need appears.

---

## 24. Clean-Code, Performance, and Security Tips

### Keep public APIs small

Expose only the methods and attributes callers need. A smaller public surface is easier to understand, test, and change safely.

### Establish invariants at construction

```python
class Percentage:
    def __init__(self, value: float) -> None:
        if not 0 <= value <= 100:
            raise ValueError("percentage must be between 0 and 100")
        self.value = value
```

Do not allow an object to exist in a state that every later method must defensively repair.

### Make invalid operations explicit

Use descriptive methods and domain exceptions. Avoid silently ignoring a failed withdrawal, unauthorized state change, or invalid transition.

### Minimize shared mutable state

Shared class variables, global registries, and singletons can create unpredictable tests and concurrency problems. Prefer explicit dependencies and instance-local state.

### Protect sensitive values

- exclude secrets from `__repr__()` and logs;
- store password hashes rather than plaintext passwords;
- do not assume `_private` or `__mangled` means secure;
- clear or rotate tokens through explicit lifecycle methods; and
- validate data at system boundaries.

### Avoid hidden I/O in properties

A property should normally be inexpensive and unsurprising. Database queries, network requests, or destructive behavior are clearer as named methods.

### Design for testability

Pass clocks, repositories, senders, random generators, and external clients as dependencies when deterministic tests need control over them.

### Use `__slots__` only after measurement

Slots can reduce memory for large numbers of simple instances, but their design tradeoffs are not automatically worth it.

### Prefer immutable value objects when appropriate

Frozen dataclasses, tuples, or carefully designed read-only objects reduce aliasing bugs and are easier to reason about.

### Follow naming conventions

- `PascalCase` for classes;
- `snake_case` for methods and attributes;
- `_leading_underscore` for non-public implementation details;
- meaningful nouns for domain classes; and
- meaningful verbs for behavior methods.

### Keep methods focused

Long methods with several branches often indicate multiple responsibilities. Extract small helpers or collaborators when that makes the main behavior clearer.

---

## 25. Practice Exercises

### Beginner

1. Create a `Student` class with name, course, and score attributes.
2. Add a method that returns whether the student passed.
3. Create three objects and prove that each has independent state.
4. Add a class variable representing the college name.
5. Write a class method that constructs a student from a dictionary.
6. Write a static method that validates a score range.
7. Add useful `__repr__()` and `__str__()` methods.

### Intermediate

1. Build a `BankAccount` with validated deposits and withdrawals.
2. Add a read-only account-number property and controlled balance behavior.
3. Create an `Employee` base class with two specialized subclasses.
4. Demonstrate overriding and `super()`.
5. Define a `NotificationSender` protocol with email and SMS implementations.
6. Build an abstract `Shape` class and concrete circle and rectangle classes.
7. Replace an inheritance design with composition and compare both versions.
8. Create a dataclass with `default_factory`, `__post_init__()`, and `repr=False`.

### Advanced

1. Create a hashable frozen value object and explain its equality contract.
2. Implement a collection class with `__len__()`, `__iter__()`, `__contains__()`, and `__getitem__()`.
3. Build a context manager that records start time, finish time, and exceptions.
4. Implement cooperative multiple inheritance and print the MRO.
5. Create a reusable validation descriptor.
6. Build a plugin registry with `__init_subclass__()`.
7. Implement a generic repository with `TypeVar` and `Generic`.
8. Test a service using an injected fake repository and sender.

### Design questions

For each case, choose a function, dataclass, normal class, ABC, protocol, or composition-based service and justify the decision:

1. An immutable latitude-longitude pair.
2. A password strength calculation with no retained state.
3. Several storage backends with shared operations.
4. A database connection requiring deterministic cleanup.
5. A user account with validated state transitions.
6. A configurable text transformation passed into a pipeline.

---

## 26. Mini-Projects

### 26.1 Secure file-vault domain model

Suggested classes:

- `User` for identity and password-hash metadata;
- `PasswordPolicy` for validation behavior;
- `KeyDeriver` protocol for key-derivation implementations;
- `VaultService` coordinating encryption and storage;
- `EncryptedFile` dataclass for safe file metadata;
- `AuditLogger` protocol for security events; and
- custom exceptions for invalid credentials and corrupted ciphertext.

Keep encryption keys out of `__repr__()` and avoid placing cryptographic work in property accessors.

### 26.2 Library management system

Model books, members, loans, catalog search, and overdue policies. Use composition for repositories and notification services.

### 26.3 Student result manager

Use dataclasses for records, a grading strategy protocol, a report service, and custom validation exceptions.

### 26.4 Banking system

Model accounts, transactions, transfer services, account-status transitions, and an audit trail. Test insufficient funds and invalid amounts.

### 26.5 Cybersecurity incident tracker

Model incidents, severity value objects, status transitions, analysts, evidence items, repositories, and notification strategies.

### 26.6 E-commerce checkout

Use pricing strategies, discount policies, inventory repositories, payment gateways, order value objects, and injected external services.

### 26.7 Role-based access control

Create users, roles, permissions, policies, and an authorization service. Make denial explicit, keep audit information, and test least-privilege rules.

---

## 27. Mastery Roadmap

### Stage 1: Foundations

- Create classes and independent instances.
- Understand `self`, `__init__()`, attributes, and methods.
- Distinguish instance and class variables.
- Use clear naming and docstrings.

### Stage 2: Controlled behavior

- Maintain invariants.
- Use properties only when useful.
- Choose instance, class, static, or module-level functions.
- Handle domain errors explicitly.

### Stage 3: OOP principles

- Practise encapsulation, inheritance, polymorphism, and abstraction.
- Learn duck typing and protocols.
- Prefer composition when the relationship is has-a.
- Keep inheritance shallow.

### Stage 4: Python integration

- Implement representations, equality, iteration, membership, and context management.
- Use dataclasses appropriately.
- Understand aliases, copying, and hashing.
- Add accurate type hints.

### Stage 5: Design and testing

- Inject dependencies.
- Apply SOLID principles proportionally.
- Test behavior and state transitions.
- Use patterns only when they clarify repeated design problems.

### Stage 6: Advanced object model

- Understand MRO and cooperative `super()`.
- Explore descriptors and `__slots__`.
- Learn `__init_subclass__()` and class decorators.
- Use metaclasses only after simpler mechanisms are insufficient.

### Recommended study method

1. Type each example yourself.
2. Predict behavior before running it.
3. Change one design choice and observe the effect.
4. Deliberately trigger validation and type errors.
5. Write tests before adding the next behavior.
6. Explain why the class is better than a function or dictionary.
7. Refactor one mini-project after receiving feedback.

---

## 28. Complete OOP Cheat Sheet

### Basic class

```python
class User:
    platform = "web"  # class variable

    def __init__(self, username: str) -> None:
        self.username = username  # instance variable

    def greet(self) -> str:
        return f"Hello, {self.username}"
```

### Method types

```python
class Example:
    def instance_method(self):
        pass

    @classmethod
    def class_method(cls):
        pass

    @staticmethod
    def static_method():
        pass
```

### Property

```python
class Product:
    @property
    def price(self) -> float:
        return self._price

    @price.setter
    def price(self, value: float) -> None:
        if value < 0:
            raise ValueError("price must not be negative")
        self._price = value
```

### Inheritance

```python
class Child(Parent):
    def __init__(self, value):
        super().__init__(value)

    def behavior(self):
        return super().behavior()
```

### Abstract base class

```python
from abc import ABC, abstractmethod


class Service(ABC):
    @abstractmethod
    def execute(self) -> None:
        ...
```

### Protocol

```python
from typing import Protocol


class Saver(Protocol):
    def save(self, data: bytes) -> None:
        ...
```

### Dataclass

```python
from dataclasses import dataclass, field


@dataclass
class Record:
    name: str
    tags: list[str] = field(default_factory=list)
```

### Key special methods

```python
__new__     # create instance
__init__    # initialize instance
__repr__    # developer representation
__str__     # user representation
__eq__      # equality
__hash__    # hashing
__len__     # length
__bool__    # truthiness
__iter__    # iteration
__next__    # next iterator value
__contains__# membership
__getitem__ # indexing
__call__    # callable object
__enter__   # context-manager entry
__exit__    # context-manager exit
```

### Core memory rules

- A class defines behavior; an object is an instance of that class.
- `self` is the current instance; `cls` is the current class.
- Instance variables are per object; class variables are normally shared.
- Python privacy is convention-based; name mangling is not security.
- Use properties for controlled attribute access, not automatic boilerplate.
- Inheritance means is-a; composition means has-a.
- Polymorphism depends on supported behavior, often without shared inheritance.
- `super()` follows the MRO.
- Assignment creates an alias, not a copy.
- Equal objects must have equal hashes.
- Mutable objects should not normally be hashable.
- Dataclasses are excellent for data-focused objects, not every domain object.
- Inject collaborators for flexibility and testing.
- Prefer the simplest design that keeps responsibilities clear.

---

## 29. Official References

- [Python Tutorial: Classes](https://docs.python.org/3/tutorial/classes.html)
- [Python Language Reference: Data Model](https://docs.python.org/3/reference/datamodel.html)
- [Python Standard Library: `abc`](https://docs.python.org/3/library/abc.html)
- [Python Standard Library: `dataclasses`](https://docs.python.org/3/library/dataclasses.html)
- [Python Standard Library: `typing`](https://docs.python.org/3/library/typing.html)
- [Python Descriptor Guide](https://docs.python.org/3/howto/descriptor.html)
- [Python Method Resolution Order](https://docs.python.org/3/howto/mro.html)
- [Python Standard Library: `contextlib`](https://docs.python.org/3/library/contextlib.html)
- [PEP 8: Style Guide for Python Code](https://peps.python.org/pep-0008/)
- [PEP 557: Data Classes](https://peps.python.org/pep-0557/)
- [PEP 544: Protocols](https://peps.python.org/pep-0544/)

---

## Final Note

OOP mastery is not measured by how many classes a program contains. It is measured by whether objects have clear responsibilities, valid state, understandable interfaces, predictable behavior, and tests that support safe change. Learn the mechanisms, then use only the ones that make the program easier to reason about.
