"""
COMPREHENSIVE GUIDE TO __SLOTS__ IN PYTHON
==========================================
__slots__ is a special attribute that prevents the creation of __dict__
for instances, significantly reducing memory usage and improving attribute
access speed.
"""


# ============================================================
# 1. BASIC SLOTS USAGE
# ============================================================

class WithoutSlots:
    """Normal class with __dict__"""

    def __init__(self, name, age):
        self.name = name
        self.age = age

    def __repr__(self):
        return f"WithoutSlots(name={self.name}, age={self.age})"


class WithSlots:
    """Class using __slots__ to optimize memory"""
    __slots__ = ['name', 'age']  # Only these attributes allowed

    def __init__(self, name, age):
        self.name = name
        self.age = age

    def __repr__(self):
        return f"WithSlots(name={self.name}, age={self.age})"


# ============================================================
# 2. MEMORY USAGE COMPARISON
# ============================================================

import sys
import tracemalloc


def compare_memory_usage():
    """Compare memory usage with and without slots"""
    print("=" * 70)
    print("MEMORY USAGE COMPARISON")
    print("=" * 70)

    # Create many instances
    n = 100000

    # Without slots
    without_slots = [WithoutSlots(f"Name{i}", i) for i in range(n)]

    # With slots
    with_slots = [WithSlots(f"Name{i}", i) for i in range(n)]

    # Calculate memory usage
    size_without = sum(sys.getsizeof(obj) for obj in without_slots)
    size_with = sum(sys.getsizeof(obj) for obj in with_slots)

    print(f"Without slots ({n} objects): {size_without:,} bytes")
    print(f"With slots ({n} objects): {size_with:,} bytes")
    print(f"Savings: {(size_without - size_with):,} bytes ({(1 - size_with / size_without) * 100:.1f}%)")
    print(f"Average per object without slots: {size_without / n:.1f} bytes")
    print(f"Average per object with slots: {size_with / n:.1f} bytes")


# ============================================================
# 3. ATTRIBUTE ACCESS SPEED COMPARISON
# ============================================================

import timeit


def compare_access_speed():
    """Compare attribute access speed with and without slots"""
    print("\n" + "=" * 70)
    print("ATTRIBUTE ACCESS SPEED COMPARISON")
    print("=" * 70)

    without = WithoutSlots("Test", 25)
    with_slots = WithSlots("Test", 25)

    # Test get access
    get_without = timeit.timeit('without.name', globals=locals(), number=1000000)
    get_with = timeit.timeit('with_slots.name', globals=locals(), number=1000000)

    # Test set access
    set_without = timeit.timeit('without.name = "New"', globals=locals(), number=100000)
    set_with = timeit.timeit('with_slots.name = "New"', globals=locals(), number=100000)

    print(f"Get access - Without slots: {get_without:.4f}s, With slots: {get_with:.4f}s")
    print(f"Get speed improvement: {(get_without - get_with) / get_without * 100:.1f}%")
    print(f"Set access - Without slots: {set_without:.4f}s, With slots: {set_with:.4f}s")
    print(f"Set speed improvement: {(set_without - set_with) / set_without * 100:.1f}%")


# ============================================================
# 4. SLOTS WITH INHERITANCE
# ============================================================

class ParentWithSlots:
    """Parent class with slots"""
    __slots__ = ['name', 'age']

    def __init__(self, name, age):
        self.name = name
        self.age = age


class ChildWithSlots(ParentWithSlots):
    """Child class inheriting slots"""
    __slots__ = ['email']  # Adds to parent slots

    def __init__(self, name, age, email):
        super().__init__(name, age)
        self.email = email


class ChildWithoutSlots(ParentWithSlots):
    """Child class that doesn't use slots (has __dict__)"""

    # No __slots__ defined - will have __dict__
    def __init__(self, name, age, email):
        super().__init__(name, age)
        self.email = email


def demonstrate_inheritance():
    """Show how slots work with inheritance"""
    print("\n" + "=" * 70)
    print("SLOTS WITH INHERITANCE")
    print("=" * 70)

    # Child with slots
    child1 = ChildWithSlots("Alice", 25, "alice@email.com")
    print(f"Child with slots: {child1.name}, {child1.age}, {child1.email}")

    # Child without slots (has __dict__)
    child2 = ChildWithoutSlots("Bob", 30, "bob@email.com")
    print(f"Child without slots: {child2.name}, {child2.age}, {child2.email}")

    # Show memory difference
    print(f"Child with slots memory: {sys.getsizeof(child1)} bytes")
    print(f"Child without slots memory: {sys.getsizeof(child2)} bytes")

    # Dynamic attributes
    try:
        child1.new_attr = "test"  # Should fail
    except AttributeError as e:
        print(f"Can't add attribute to child with slots: {e}")

    child2.new_attr = "test"  # Works
    print(f"Child without slots can add attributes: {child2.new_attr}")


# ============================================================
# 5. SLOTS WITH MULTIPLE INHERITANCE
# ============================================================

class A:
    __slots__ = ['x', 'y']


class B:
    __slots__ = ['z', 'w']


class C(A, B):
    __slots__ = ['t']  # Must include all slots from parents


def demonstrate_multiple_inheritance():
    """Show slots with multiple inheritance"""
    print("\n" + "=" * 70)
    print("SLOTS WITH MULTIPLE INHERITANCE")
    print("=" * 70)

    try:
        # This will work if slots are properly defined
        class ValidC(A, B):
            __slots__ = ['t', 'x', 'y', 'z', 'w']  # Must include parent slots

        obj = ValidC()
        obj.x = 1
        obj.y = 2
        obj.z = 3
        obj.w = 4
        obj.t = 5
        print(f"ValidC instance with slots: x={obj.x}, y={obj.y}, z={obj.z}, w={obj.w}, t={obj.t}")
    except Exception as e:
        print(f"Error: {e}")


# ============================================================
# 6. SLOTS WITH PROPERTIES AND DESCRIPTORS
# ============================================================

class PersonWithSlotsAndProperties:
    """Using slots with properties"""
    __slots__ = ['_name', '_age']

    def __init__(self, name, age):
        self._name = name
        self._age = age

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if not value or len(value) < 2:
            raise ValueError("Name must be at least 2 characters")
        self._name = value

    @property
    def age(self):
        return self._age

    @age.setter
    def age(self, value):
        if not isinstance(value, int) or value < 0:
            raise ValueError("Age must be a positive integer")
        self._age = value

    @property
    def description(self):
        return f"{self.name} is {self.age} years old"


def demonstrate_properties_with_slots():
    """Show properties working with slots"""
    print("\n" + "=" * 70)
    print("SLOTS WITH PROPERTIES")
    print("=" * 70)

    person = PersonWithSlotsAndProperties("John", 30)
    print(person.description)

    person.name = "Jonathan"
    person.age = 35
    print(person.description)

    try:
        person.name = "A"  # Too short
    except ValueError as e:
        print(f"Validation error: {e}")


# ============================================================
# 7. SLOTS WITH __DICT__ (GIVING SLOTS OBJECTS A DICT)
# ============================================================

class WithDictAndSlots:
    """Class with both slots and __dict__ for dynamic attributes"""
    __slots__ = ['name', 'age', '__dict__']

    def __init__(self, name, age):
        self.name = name
        self.age = age

    def __repr__(self):
        return f"WithDictAndSlots(name={self.name}, age={self.age})"


def demonstrate_dict_with_slots():
    """Show how to have both slots and dict"""
    print("\n" + "=" * 70)
    print("SLOTS WITH DICT")
    print("=" * 70)

    obj = WithDictAndSlots("Alice", 25)
    print(f"Base: {obj}")
    print(f"Slots memory: {sys.getsizeof(obj)} bytes")

    # Can add dynamic attributes
    obj.new_attr = "Dynamic"
    obj.another = 42
    print(f"Dynamic attributes: {obj.new_attr}, {obj.another}")


# ============================================================
# 8. SLOTS PERFORMANCE TEST
# ============================================================

class TestWithoutSlots:
    def __init__(self, name, value):
        self.name = name
        self.value = value
        self.cache = {}


class TestWithSlots:
    __slots__ = ['name', 'value']

    def __init__(self, name, value):
        self.name = name
        self.value = value


def run_performance_tests():
    """Comprehensive performance comparison"""
    print("\n" + "=" * 70)
    print("PERFORMANCE BENCHMARK")
    print("=" * 70)

    # Test 1: Memory usage with large number of objects
    print("\n1. Memory usage (1,000,000 objects):")
    n = 1000000

    import tracemalloc

    # Without slots
    tracemalloc.start()
    without = [TestWithoutSlots(f"Name{i}", i) for i in range(n)]
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    print(f"  Without slots: {current / 1024 / 1024:.2f} MB (peak: {peak / 1024 / 1024:.2f} MB)")

    # With slots
    tracemalloc.start()
    with_slots = [TestWithSlots(f"Name{i}", i) for i in range(n)]
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    print(f"  With slots:    {current / 1024 / 1024:.2f} MB (peak: {peak / 1024 / 1024:.2f} MB)")

    # Test 2: Attribute creation speed
    print("\n2. Attribute creation time (100,000 attributes):")

    def create_without():
        obj = TestWithoutSlots("Test", 1)
        for i in range(100000):
            setattr(obj, f"attr_{i}", i)

    def create_with():
        obj = TestWithSlots("Test", 1)
        # Can't create dynamic attributes with slots!
        return "Not possible (slots prevents it)"

    time_without = timeit.timeit(create_without, number=1)
    print(f"  Without slots: {time_without:.2f} seconds")
    print(f"  With slots:    Not possible (prevents dynamic attributes)")

    # Test 3: Attribute access speed
    print("\n3. Attribute access speed (1,000,000 accesses):")

    obj1 = TestWithoutSlots("Test", 42)
    obj2 = TestWithSlots("Test", 42)

    get_without = timeit.timeit('obj1.name', globals=locals(), number=1000000)
    get_with = timeit.timeit('obj2.name', globals=locals(), number=1000000)

    print(f"  Without slots: {get_without:.4f} seconds")
    print(f"  With slots:    {get_with:.4f} seconds")
    print(f"  Speedup:       {((get_without - get_with) / get_without * 100):.1f}%")


# ============================================================
# 9. SLOTS IN REAL-WORLD APPLICATIONS
# ============================================================

class DataPointWithSlots:
    """Data point class optimized with slots"""
    __slots__ = ['x', 'y', 'z', 'label', 'timestamp', '_cache']

    def __init__(self, x, y, z, label=None):
        self.x = x
        self.y = y
        self.z = z
        self.label = label
        self.timestamp = __import__('time').time()
        self._cache = {}  # Still can have dict for caching

    @property
    def magnitude(self):
        """Calculate magnitude (with caching)"""
        if 'magnitude' not in self._cache:
            self._cache['magnitude'] = (self.x ** 2 + self.y ** 2 + self.z ** 2) ** 0.5
        return self._cache['magnitude']

    def __repr__(self):
        return f"DataPoint({self.x}, {self.y}, {self.z})"


class PointCloud:
    """Collection of data points with slots optimization"""
    __slots__ = ['points', 'name']

    def __init__(self, name):
        self.points = []
        self.name = name

    def add_point(self, x, y, z, label=None):
        self.points.append(DataPointWithSlots(x, y, z, label))

    def average_position(self):
        if not self.points:
            return (0, 0, 0)
        avg_x = sum(p.x for p in self.points) / len(self.points)
        avg_y = sum(p.y for p in self.points) / len(self.points)
        avg_z = sum(p.z for p in self.points) / len(self.points)
        return (avg_x, avg_y, avg_z)

    def __repr__(self):
        return f"PointCloud(name={self.name}, points={len(self.points)})"


def demonstrate_realworld():
    """Show real-world usage of slots"""
    print("\n" + "=" * 70)
    print("REAL-WORLD APPLICATION")
    print("=" * 70)

    # Create point cloud
    cloud = PointCloud("Test Cloud")

    # Add many points efficiently
    import random
    for i in range(10000):
        cloud.add_point(
            random.uniform(-100, 100),
            random.uniform(-100, 100),
            random.uniform(-100, 100),
            f"Point_{i}"
        )

    print(f"Cloud: {cloud}")
    avg = cloud.average_position()
    print(f"Average position: ({avg[0]:.2f}, {avg[1]:.2f}, {avg[2]:.2f})")

    # Show memory savings
    point = DataPointWithSlots(1, 2, 3)
    print(f"Single point memory: {sys.getsizeof(point)} bytes")

    # Compare with regular class
    class RegularDataPoint:
        def __init__(self, x, y, z):
            self.x = x
            self.y = y
            self.z = z

    regular_point = RegularDataPoint(1, 2, 3)
    print(f"Regular point memory: {sys.getsizeof(regular_point)} bytes")


# ============================================================
# 10. SLOTS BEST PRACTICES AND LIMITATIONS
# ============================================================

def demonstrate_limitations():
    """Show limitations and best practices of slots"""
    print("\n" + "=" * 70)
    print("SLOTS LIMITATIONS AND BEST PRACTICES")
    print("=" * 70)

    print("✅ ADVANTAGES:")
    print("  • Significantly reduced memory usage")
    print("  • Faster attribute access")
    print("  • Prevents accidental attribute creation")
    print("  • Better performance in tight loops")

    print("\n⚠️ LIMITATIONS:")
    print("  • Cannot add new attributes dynamically")
    print("  • Cannot use with inheritance without care")
    print("  • Some Python features might not work (e.g., weakref)")
    print("  • Not suitable for all use cases")

    print("\n📋 WHEN TO USE SLOTS:")
    print("  • Creating many instances (thousands/millions)")
    print("  • Memory-constrained environments")
    print("  • Data structures (nodes, points, records)")
    print("  • Performance-critical code")

    print("\n📋 WHEN NOT TO USE SLOTS:")
    print("  • Small number of instances")
    print("  • Need dynamic attributes")
    print("  • Complex inheritance hierarchies")
    print("  • When using frameworks that expect __dict__")


# ============================================================
# DEMONSTRATION
# ============================================================

def demonstrate_slots():
    """Complete demonstration of __slots__"""

    print("=" * 70)
    print("SLOTS COMPREHENSIVE DEMONSTRATION")
    print("=" * 70)

    # 1. Basic usage
    print("\n1. BASIC SLOTS USAGE")
    print("-" * 50)

    with_slots = WithSlots("Alice", 30)
    print(f"Object: {with_slots}")
    print(f"Memory: {sys.getsizeof(with_slots)} bytes")

    try:
        with_slots.new_attr = "Test"  # Should fail
    except AttributeError as e:
        print(f"Error: {e}")

    # 2. Memory comparison
    compare_memory_usage()

    # 3. Speed comparison
    compare_access_speed()

    # 4. Inheritance
    demonstrate_inheritance()

    # 5. Multiple inheritance
    demonstrate_multiple_inheritance()

    # 6. Properties with slots
    demonstrate_properties_with_slots()

    # 7. Dict with slots
    demonstrate_dict_with_slots()

    # 8. Performance tests
    run_performance_tests()

    # 9. Real-world example
    demonstrate_realworld()

    # 10. Limitations
    demonstrate_limitations()


# ============================================================
# MAIN EXECUTION
# ============================================================

if __name__ == "__main__":
    demonstrate_slots()

    print("\n" + "=" * 70)
    print("SLOTS KEY CONCEPTS")
    print("=" * 70)
    print("""
    ✅ WHAT __SLOTS__ DOES
       - Prevents creation of __dict__ for instances
       - Only allows specified attributes
       - Significantly reduces memory usage
       - Improves attribute access speed

    ✅ MEMORY SAVINGS
       - Without slots:  ~56-64 bytes per instance (Python 3.8+)
       - With slots:     ~16-24 bytes per instance
       - Savings:        up to 70% memory reduction

    ✅ SPEED IMPROVEMENTS
       - Attribute access: ~20-30% faster
       - Attribute assignment: ~10-20% faster
       - Better CPU cache locality

    ✅ SYNTAX
       __slots__ = ['attr1', 'attr2', 'attr3']
       __slots__ = ('attr1', 'attr2')  # Tuple also works

    ✅ BEST PRACTICES
       - Use for classes with many instances
       - Use for simple data containers
       - Include parent slots in inheritance
       - Consider adding '__dict__' to slots for flexibility
       - Test thoroughly when using with frameworks

    ✅ ALTERNATIVES
       - __slots__ is not a replacement for __dict__
       - Consider namedtuple, dataclass, attrs
       - Use for performance-critical code
    """)
    print("=" * 70)