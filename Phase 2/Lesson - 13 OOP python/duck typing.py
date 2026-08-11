"""
COMPREHENSIVE GUIDE TO DUCK TYPING IN PYTHON
============================================
"If it walks like a duck and quacks like a duck, then it's a duck"
Duck typing is a concept where the type or class of an object is
determined by its behavior (methods and properties) rather than
its explicit inheritance or class hierarchy.
"""


# ============================================================
# 1. BASIC DUCK TYPING CONCEPT
# ============================================================

class Duck:
    """A real duck"""

    def quack(self):
        return "Quack! Quack!"

    def swim(self):
        return "Swimming like a duck"

    def fly(self):
        return "Flying like a duck"


class Person:
    """A person who can imitate a duck"""

    def quack(self):
        return "I'm quacking like a duck!"

    def swim(self):
        return "Swimming in the pool"

    def walk(self):
        return "Walking on two legs"


class Robot:
    """A robot programmed to act like a duck"""

    def quack(self):
        return "Beep boop - Quack sound"

    def swim(self):
        return "Robot swimming with mechanical movements"

    def charge(self):
        return "Charging batteries"


def make_it_quack(thing):
    """Works with ANY object that has a quack() method"""
    return thing.quack()


def make_it_swim(thing):
    """Works with ANY object that has a swim() method"""
    return thing.swim()


def perform_duck_actions(thing):
    """Demonstrates duck typing - any object with required methods works"""
    print(f"{thing.__class__.__name__}: {thing.quack()}")
    print(f"{thing.__class__.__name__}: {thing.swim()}")
    print("-" * 30)


# ============================================================
# 2. DUCK TYPING WITH DIFFERENT OBJECT TYPES
# ============================================================

class Car:
    """Car has a horn instead of quack"""

    def horn(self):
        return "Beep! Beep!"

    def drive(self):
        return "Driving on the road"


class Bicycle:
    """Bicycle has a bell instead of quack"""

    def ring_bell(self):
        return "Ring! Ring!"

    def pedal(self):
        return "Pedaling forward"


def sound_maker(obj):
    """Duck typing: Try to call quack(), fallback to other methods"""
    if hasattr(obj, 'quack'):
        return obj.quack()
    elif hasattr(obj, 'horn'):
        return obj.horn()
    elif hasattr(obj, 'ring_bell'):
        return obj.ring_bell()
    else:
        return "No sound method found"


def movement(obj):
    """Works with objects that have different movement methods"""
    if hasattr(obj, 'swim'):
        return obj.swim()
    elif hasattr(obj, 'drive'):
        return obj.drive()
    elif hasattr(obj, 'pedal'):
        return obj.pedal()
    else:
        return "Unknown movement"


# ============================================================
# 3. DUCK TYPING WITH BUILT-IN TYPES
# ============================================================

def process_iterable(data):
    """Works with any iterable - duck typing at its finest!"""
    print(f"Processing {type(data).__name__}")
    print(f"Length: {len(data)}")
    print(f"First item: {data[0] if data else 'Empty'}")
    print(f"All items: {[item for item in data]}")
    print("-" * 30)


def custom_join(items, separator=", "):
    """Works with any iterable, not just lists!"""
    result = ""
    for item in items:
        if result:
            result += separator
        result += str(item)
    return result


# ============================================================
# 4. DUCK TYPING IN PRACTICAL SCENARIOS
# ============================================================

class EmailSender:
    def send(self, message):
        print(f"Sending email: {message}")
        return True

    def validate(self):
        return "Email validated"


class SMSSender:
    def send(self, message):
        print(f"Sending SMS: {message}")
        return True

    def validate(self):
        return "SMS validated"


class PushNotificationSender:
    def send(self, message):
        print(f"Sending push notification: {message}")
        return True

    def validate(self):
        return "Push notification validated"


def send_notification(sender, message):
    """Works with ANY object that has send() method"""
    if not hasattr(sender, 'send'):
        raise TypeError("Object must have a 'send' method")

    # Validate before sending
    if hasattr(sender, 'validate'):
        print(f"Validation: {sender.validate()}")

    return sender.send(message)


# ============================================================
# 5. DUCK TYPING WITH FILE-LIKE OBJECTS
# ============================================================

class FileWriter:
    def __init__(self, filename):
        self.filename = filename

    def write(self, data):
        with open(self.filename, 'w') as f:
            f.write(data)
        return f"Written to {self.filename}"

    def close(self):
        print(f"Closing {self.filename}")


class StringWriter:
    def __init__(self):
        self.content = ""

    def write(self, data):
        self.content += data
        return f"Appended: {data}"

    def get_content(self):
        return self.content

    def close(self):
        print("StringWriter closed")


class DatabaseWriter:
    def write(self, data):
        print(f"Writing to database: {data}")
        return "Database write successful"

    def close(self):
        print("Database connection closed")


def write_data(writer, data):
    """Works with any object that has write() method"""
    if not hasattr(writer, 'write'):
        raise TypeError("Object must have a 'write' method")

    result = writer.write(data)

    # Some writers might need closing
    if hasattr(writer, 'close'):
        writer.close()

    return result


# ============================================================
# 6. DUCK TYPING WITH CUSTOM ITERABLES
# ============================================================

class NumberRange:
    """Custom iterable class"""

    def __init__(self, start, end):
        self.start = start
        self.end = end

    def __iter__(self):
        self.current = self.start
        return self

    def __next__(self):
        if self.current >= self.end:
            raise StopIteration
        value = self.current
        self.current += 1
        return value


class FibonacciIterator:
    """Custom Fibonacci iterable"""

    def __init__(self, count):
        self.count = count
        self.index = 0
        self.a, self.b = 0, 1

    def __iter__(self):
        return self

    def __next__(self):
        if self.index >= self.count:
            raise StopIteration
        self.index += 1
        if self.index == 1:
            return 0
        if self.index == 2:
            return 1
        self.a, self.b = self.b, self.a + self.b
        return self.b


def process_iterable_advanced(iterable):
    """Works with any iterable, regardless of type"""
    print(f"Processing: {type(iterable).__name__}")

    # Check if it's iterable
    if hasattr(iterable, '__iter__'):
        print("✓ Has __iter__ method")
    else:
        print("✗ Not iterable")
        return

    # Iterate and process
    total = 0
    for i, item in enumerate(iterable):
        total += item if isinstance(item, (int, float)) else 0
        print(f"  Item {i}: {item}")

    print(f"Total sum: {total}")
    print("-" * 30)


# ============================================================
# 7. DUCK TYPING WITH CONTEXT MANAGERS
# ============================================================

class DatabaseConnection:
    def __enter__(self):
        print("Opening database connection")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        print("Closing database connection")

    def query(self, sql):
        return f"Querying: {sql}"


class NetworkConnection:
    def __enter__(self):
        print("Opening network connection")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        print("Closing network connection")

    def query(self, data):
        return f"Network request: {data}"


class FileConnection:
    def __enter__(self):
        print("Opening file")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        print("Closing file")

    def query(self, data):
        return f"File operation: {data}"


def use_connection(connection, query_data):
    """Works with any context manager that has query() method"""
    with connection as conn:
        if hasattr(conn, 'query'):
            return conn.query(query_data)
        else:
            return "Connection doesn't support query"


# ============================================================
# 8. DUCK TYPING WITH CUSTOM PROTOCOLS
# ============================================================

class DrawableProtocol:
    """Simulating a protocol (Python 3.8+ would use typing.Protocol)"""

    def draw(self):
        raise NotImplementedError("Must implement draw()")


class Circle:
    def draw(self):
        return "Drawing a circle ⭕"

    def area(self):
        return "πr²"


class Square:
    def draw(self):
        return "Drawing a square ⬛"

    def area(self):
        return "side²"


class Triangle:
    def draw(self):
        return "Drawing a triangle 🔺"

    def area(self):
        return "½ base × height"


class TextPrinter:
    def draw(self):
        return "Drawing text: Hello"

    def print_text(self):
        return "Printing text"


def render(objects):
    """Works with any object that has draw() method"""
    for obj in objects:
        if hasattr(obj, 'draw'):
            print(obj.draw())
        else:
            print(f"{obj.__class__.__name__} cannot be drawn")


# ============================================================
# 9. DUCK TYPING WITH CALLBACKS
# ============================================================

class EventHandler:
    """Works with any callable (duck typing for callbacks)"""

    def __init__(self):
        self.handlers = []

    def register(self, handler):
        """Register any callable object"""
        if callable(handler):
            self.handlers.append(handler)
            return f"Registered {handler.__name__}"
        else:
            return "Handler must be callable"

    def trigger(self, event_data):
        """Trigger all handlers"""
        results = []
        for handler in self.handlers:
            results.append(handler(event_data))
        return results


# Different callable objects
def simple_handler(data):
    return f"Simple: {data}"


class ClassHandler:
    def __call__(self, data):
        return f"Class callable: {data}"


class MethodHandler:
    def handle(self, data):
        return f"Method handler: {data}"


# ============================================================
# 10. DUCK TYPING WITH MAGIC METHODS
# ============================================================

class CustomNumber:
    """Implements numeric protocol"""

    def __init__(self, value):
        self.value = value

    def __add__(self, other):
        if isinstance(other, (int, float, CustomNumber)):
            other_value = other.value if isinstance(other, CustomNumber) else other
            return CustomNumber(self.value + other_value)
        return NotImplemented

    def __sub__(self, other):
        if isinstance(other, (int, float, CustomNumber)):
            other_value = other.value if isinstance(other, CustomNumber) else other
            return CustomNumber(self.value - other_value)
        return NotImplemented

    def __mul__(self, other):
        if isinstance(other, (int, float, CustomNumber)):
            other_value = other.value if isinstance(other, CustomNumber) else other
            return CustomNumber(self.value * other_value)
        return NotImplemented

    def __lt__(self, other):
        if isinstance(other, (int, float, CustomNumber)):
            other_value = other.value if isinstance(other, CustomNumber) else other
            return self.value < other_value
        return NotImplemented

    def __str__(self):
        return f"CustomNumber({self.value})"

    def __repr__(self):
        return f"CustomNumber({self.value})"


def numeric_operations(a, b):
    """Works with any object that implements numeric protocol"""
    print(f"a + b = {a + b}")
    print(f"a - b = {a - b}")
    print(f"a * b = {a * b}")
    print(f"a < b = {a < b}")
    print("-" * 30)


# ============================================================
# 11. DUCK TYPING WITH ATTRIBUTE CHECKING
# ============================================================

class SmartDuck:
    """Safe duck typing with attribute checking"""

    def __init__(self, name):
        self.name = name
        self._can_quack = True
        self._can_swim = True

    def quack(self):
        if self._can_quack:
            return f"{self.name} says Quack!"
        return f"{self.name} can't quack"

    def swim(self):
        if self._can_swim:
            return f"{self.name} is swimming"
        return f"{self.name} can't swim"


def safe_duck_action(obj, action, *args, **kwargs):
    """Safely call a method if it exists"""
    if hasattr(obj, action):
        method = getattr(obj, action)
        if callable(method):
            try:
                return method(*args, **kwargs)
            except Exception as e:
                return f"Error: {e}"
    return f"{obj.__class__.__name__} has no {action} method"


def check_duck_behavior(obj):
    """Comprehensive duck checking"""
    required_methods = ['quack', 'swim']
    optional_methods = ['fly', 'walk', 'eat']

    print(f"Checking {obj.__class__.__name__}")

    # Check required methods
    for method in required_methods:
        if hasattr(obj, method) and callable(getattr(obj, method)):
            print(f"✓ Has {method}()")
        else:
            print(f"✗ Missing {method}()")

    # Check optional methods
    for method in optional_methods:
        if hasattr(obj, method) and callable(getattr(obj, method)):
            print(f"✓ Has {method}()")
        else:
            print(f"  No {method}()")

    print("-" * 30)


# ============================================================
# 12. PRACTICAL: DUCK TYPING IN WEB SCRAPING
# ============================================================

class WebPageScraper:
    def fetch(self, url):
        return f"Fetching web page from {url}"

    def parse(self, html):
        return f"Parsing HTML: {html[:50]}..."

    def extract_data(self, parsed):
        return f"Extracted data from {parsed}"


class APIScraper:
    def fetch(self, url):
        return f"Calling API at {url}"

    def parse(self, response):
        return f"Parsing JSON: {response[:50]}..."

    def extract_data(self, parsed):
        return f"Extracted data from JSON {parsed}"


class FileScraper:
    def fetch(self, path):
        return f"Reading file from {path}"

    def parse(self, content):
        return f"Parsing file content: {content[:50]}..."

    def extract_data(self, parsed):
        return f"Extracted data from file {parsed}"


def scrape_data(scraper, source):
    """Works with any scraper that has fetch, parse, extract_data methods"""
    if not all(hasattr(scraper, method) for method in ['fetch', 'parse', 'extract_data']):
        raise TypeError("Scraper missing required methods")

    raw = scraper.fetch(source)
    parsed = scraper.parse(raw)
    data = scraper.extract_data(parsed)
    return data


# ============================================================
# 13. DUCK TYPING WITH TYPE HINTS (For documentation)
# ============================================================

from typing import Any, Callable, Iterable, Union


class TypeHintedExample:
    """Demonstrates duck typing with type hints"""

    def process(self, data: Union[list, tuple, set, Iterable]) -> list:
        """Works with any iterable, type hints are documentation"""
        return [item for item in data]

    def callback_handler(self, func: Callable) -> Any:
        """Works with any callable"""
        return func()

    def any_object(self, obj: Any) -> str:
        """Works with any object (duck typing)"""
        if hasattr(obj, '__str__'):
            return str(obj)
        return repr(obj)


# ============================================================
# DEMONSTRATION FUNCTION
# ============================================================

def demonstrate_duck_typing():
    """Comprehensive demonstration of duck typing concepts"""

    print("=" * 70)
    print("DUCK TYPING COMPREHENSIVE DEMONSTRATION")
    print("=" * 70)

    # 1. Basic Duck Typing
    print("\n1. BASIC DUCK TYPING")
    print("-" * 50)
    duck = Duck()
    person = Person()
    robot = Robot()

    for obj in [duck, person, robot]:
        print(f"{obj.__class__.__name__}: {make_it_quack(obj)}")
        print(f"{obj.__class__.__name__}: {make_it_swim(obj)}")

    print("\nPerforming duck actions:")
    perform_duck_actions(duck)
    perform_duck_actions(person)
    perform_duck_actions(robot)

    # 2. Duck Typing with Different Objects
    print("\n2. DUCK TYPING WITH DIFFERENT OBJECTS")
    print("-" * 50)
    car = Car()
    bicycle = Bicycle()

    print(f"Car sound: {sound_maker(car)}")
    print(f"Bicycle sound: {sound_maker(bicycle)}")
    print(f"Car movement: {movement(car)}")
    print(f"Bicycle movement: {movement(bicycle)}")

    # 3. Duck Typing with Built-in Types
    print("\n3. DUCK TYPING WITH BUILT-IN TYPES")
    print("-" * 50)
    process_iterable([1, 2, 3])
    process_iterable((4, 5, 6))
    process_iterable({7, 8, 9})
    process_iterable({'a': 1, 'b': 2})
    process_iterable("Hello")

    print(f"Custom join on list: {custom_join(['a', 'b', 'c'])}")
    print(f"Custom join on tuple: {custom_join((1, 2, 3), ' - ')}")
    print(f"Custom join on set: {custom_join({10, 20, 30}, ' | ')}")

    # 4. Practical Scenarios
    print("\n4. PRACTICAL SCENARIOS (Notification System)")
    print("-" * 50)
    send_notification(EmailSender(), "Welcome email")
    send_notification(SMSSender(), "SMS alert")
    send_notification(PushNotificationSender(), "Push notification")

    # 5. File-like Objects
    print("\n5. FILE-LIKE OBJECTS")
    print("-" * 50)
    file_writer = FileWriter("test.txt")
    string_writer = StringWriter()
    db_writer = DatabaseWriter()

    print(write_data(file_writer, "Hello World"))
    print(write_data(string_writer, "Hello "))
    print(write_data(string_writer, "World!"))
    print(f"StringWriter content: {string_writer.get_content()}")
    print(write_data(db_writer, "User data"))

    # 6. Custom Iterables
    print("\n6. CUSTOM ITERABLES")
    print("-" * 50)
    process_iterable_advanced(NumberRange(1, 5))
    process_iterable_advanced(FibonacciIterator(7))
    process_iterable_advanced([x for x in range(10)])  # List comprehension

    # 7. Context Managers
    print("\n7. CONTEXT MANAGERS")
    print("-" * 50)
    print(use_connection(DatabaseConnection(), "SELECT * FROM users"))
    print(use_connection(NetworkConnection(), "GET /api/data"))
    print(use_connection(FileConnection(), "read file"))

    # 8. Drawing Protocol
    print("\n8. DRAWING PROTOCOL (Interface by Duck Typing)")
    print("-" * 50)
    shapes = [Circle(), Square(), Triangle(), TextPrinter()]
    render(shapes)

    # 9. Callbacks
    print("\n9. CALLBACKS")
    print("-" * 50)
    event_handler = EventHandler()
    print(event_handler.register(simple_handler))
    print(event_handler.register(ClassHandler()))

    method_handler = MethodHandler()
    print(event_handler.register(method_handler.handle))

    results = event_handler.trigger("event data")
    for result in results:
        print(result)

    # 10. Magic Methods
    print("\n10. MAGIC METHODS (Numeric Protocol)")
    print("-" * 50)
    c1 = CustomNumber(10)
    c2 = CustomNumber(3)
    print(f"c1 = {c1}, c2 = {c2}")
    numeric_operations(c1, c2)
    numeric_operations(c1, 5)

    # 11. Attribute Checking
    print("\n11. ATTRIBUTE CHECKING")
    print("-" * 50)
    smart_duck = SmartDuck("Daffy")
    safe_duck_action(smart_duck, 'quack')
    safe_duck_action(smart_duck, 'fly')

    check_duck_behavior(duck)
    check_duck_behavior(person)
    check_duck_behavior(car)

    # 12. Web Scraping (Practical Example)
    print("\n12. PRACTICAL: WEB SCRAPING")
    print("-" * 50)
    print(scrape_data(WebPageScraper(), "https://example.com"))
    print(scrape_data(APIScraper(), "https://api.example.com/users"))
    print(scrape_data(FileScraper(), "/data/users.txt"))

    # 13. Duck Typing with Error Handling
    print("\n13. ERROR HANDLING IN DUCK TYPING")
    print("-" * 50)

    def safe_process(obj, method_name, *args, **kwargs):
        """Safely process any object with method checking"""
        if hasattr(obj, method_name):
            method = getattr(obj, method_name)
            if callable(method):
                try:
                    return method(*args, **kwargs)
                except Exception as e:
                    return f"Error calling {method_name}: {e}"
        return f"{obj.__class__.__name__} has no {method_name} method"

    print(safe_process(duck, 'quack'))
    print(safe_process(duck, 'fly'))
    print(safe_process(car, 'drive'))
    print(safe_process(car, 'fly'))


# ============================================================
# ADDITIONAL: DUCK TYPING WITH UNITTESTS
# ============================================================

def duck_typing_tests():
    """Demonstrate duck typing with testing mentality"""
    print("\n" + "=" * 70)
    print("DUCK TYPING TESTING PATTERNS")
    print("=" * 70)

    def test_duck(obj):
        """Test if object is duck-like"""
        errors = []

        # Check required methods
        if not hasattr(obj, 'quack'):
            errors.append("Missing quack() method")
        elif not callable(obj.quack):
            errors.append("quack is not callable")

        if not hasattr(obj, 'swim'):
            errors.append("Missing swim() method")
        elif not callable(obj.swim):
            errors.append("swim is not callable")

        # Try to call methods
        if not errors:
            try:
                obj.quack()
                obj.swim()
            except Exception as e:
                errors.append(f"Method error: {e}")

        return errors

    # Test different objects
    test_objects = [Duck(), Person(), Robot(), Car()]

    for obj in test_objects:
        result = test_duck(obj)
        if result:
            print(f"✗ {obj.__class__.__name__} failed: {result}")
        else:
            print(f"✓ {obj.__class__.__name__} passed duck test")


# ============================================================
# MAIN EXECUTION
# ============================================================

if __name__ == "__main__":
    # Run main demonstration
    demonstrate_duck_typing()

    # Run additional tests
    duck_typing_tests()

    # Final summary
    print("\n" + "=" * 70)
    print("DUCK TYPING KEY CONCEPTS SUMMARY")
    print("=" * 70)
    print("""
    ✅ WHAT IS DUCK TYPING?
    - Focus on object's behavior (methods/properties) not its type
    - "If it walks like a duck and quacks like a duck, it's a duck"
    - Dynamic typing: object suitability determined at runtime

    ✅ ADVANTAGES:
    - Flexibility: Works with any object that has required methods
    - Code reusability: One function works with many types
    - Reduced boilerplate: No need for complex inheritance hierarchies
    - Rapid prototyping: Easier to change and extend

    ✅ BEST PRACTICES:
    1. Check for methods using hasattr() before calling
    2. Use EAFP (Easier to Ask for Forgiveness than Permission)
    3. Provide clear error messages for missing methods
    4. Document expected interface (which methods are required)
    5. Use type hints for documentation (not enforcement)
    6. Consider using Protocols (Python 3.8+) for formal interfaces

    ✅ COMMON USE CASES:
    - File-like objects (any object with read/write methods)
    - Iterables (any object with __iter__ or __getitem__)
    - Callbacks (any callable object)
    - Context managers (any object with __enter__/__exit__)
    - Protocol implementations (multiple classes share methods)
    - Testing/mocking (mock objects with required methods)

    ✅ PATTERNS TO USE:
    - hasattr(obj, 'method') - Check if method exists
    - getattr(obj, 'method', default) - Get method with fallback
    - try/except AttributeError - EAFP style
    - callable(obj) - Check if object is callable
    - isinstance(obj, collections.abc.Iterable) - For duck typing with ABCs

    ✅ PYTHON'S DUCK TYPING POWER COMES FROM:
    - Dynamic nature of the language
    - Method resolution at runtime
    - Support for magic/special methods
    - Flexibility to define any method on objects
    """)

    print("=" * 70)
    print("✅ DUCK TYPING DEMONSTRATION COMPLETE!")
    print("=" * 70)