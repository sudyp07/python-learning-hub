"""
COMPREHENSIVE GUIDE TO WEAK REFERENCES IN PYTHON
================================================
Weak references allow you to reference objects without preventing
garbage collection. They're essential for memory management in
caching, observers, and avoiding reference cycles.
"""

import weakref
import gc
import sys
from typing import Any, Dict, List, Optional


# ============================================================
# 1. BASIC WEAK REFERENCE CONCEPT
# ============================================================

class Person:
    """Simple class to demonstrate weak references"""

    def __init__(self, name):
        self.name = name
        print(f"Person {self.name} created")

    def __del__(self):
        print(f"Person {self.name} being destroyed")

    def greet(self):
        return f"Hello, I'm {self.name}"


def demonstrate_basic():
    """Basic weak reference demonstration"""
    print("=" * 70)
    print("BASIC WEAK REFERENCES")
    print("=" * 70)

    # Create a strong reference
    person = Person("Alice")

    # Create a weak reference
    weak_person = weakref.ref(person)
    print(f"Strong ref: {person}")
    print(f"Weak ref: {weak_person}")
    print(f"Weak ref object: {weak_person()}")

    # Delete strong reference
    print("\nDeleting strong reference:")
    del person
    print(f"Weak ref after deletion: {weak_person()}")

    # The weak reference returns None after object is GC'd


# ============================================================
# 2. WEAK REFERENCE TYPES
# ============================================================

class DemoObject:
    """Object for demonstrating weak reference types"""

    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f"DemoObject({self.value})"


def demonstrate_weak_types():
    """Demonstrate different weak reference types"""
    print("\n" + "=" * 70)
    print("WEAK REFERENCE TYPES")
    print("=" * 70)

    # 1. weakref.ref - Simple weak reference
    obj = DemoObject(42)
    weak_ref = weakref.ref(obj)
    print(f"1. weakref.ref: {weak_ref()}")

    # 2. weakref.proxy - Weak proxy (behaves like original)
    proxy = weakref.proxy(obj)
    print(f"2. weakref.proxy: {proxy}")
    print(f"   Proxy value: {proxy.value}")

    # 3. weakref.WeakKeyDictionary - Keys are weak references
    weak_key_dict = weakref.WeakKeyDictionary()
    key_obj = DemoObject("key")
    weak_key_dict[key_obj] = "value with weak key"
    print(f"3. WeakKeyDictionary: {weak_key_dict}")
    print(f"   Before deletion: {len(weak_key_dict)} items")
    del key_obj
    gc.collect()
    print(f"   After deletion: {len(weak_key_dict)} items")

    # 4. weakref.WeakValueDictionary - Values are weak references
    weak_value_dict = weakref.WeakValueDictionary()
    value_obj = DemoObject("value")
    weak_value_dict['key'] = value_obj
    print(f"4. WeakValueDictionary: {weak_value_dict}")
    print(f"   Before deletion: {len(weak_value_dict)} items")
    del value_obj
    gc.collect()
    print(f"   After deletion: {len(weak_value_dict)} items")

    # 5. weakref.WeakSet - Set of weak references
    weak_set = weakref.WeakSet()
    set_obj = DemoObject("set")
    weak_set.add(set_obj)
    print(f"5. WeakSet: {weak_set}")
    print(f"   Before deletion: {len(weak_set)} items")
    del set_obj
    gc.collect()
    print(f"   After deletion: {len(weak_set)} items")


# ============================================================
# 3. WEAK REFERENCE WITH FINALIZERS
# ============================================================

class Resource:
    """Resource class with finalizer"""

    def __init__(self, name):
        self.name = name
        self._is_open = True
        print(f"Resource {name} opened")

    def close(self):
        if self._is_open:
            self._is_open = False
            print(f"Resource {self.name} closed")

    def __del__(self):
        self.close()

    def __repr__(self):
        return f"Resource({self.name}, open={self._is_open})"


def demonstrate_finalizer():
    """Demonstrate weak reference with finalizers"""
    print("\n" + "=" * 70)
    print("WEAK REFERENCES WITH FINALIZERS")
    print("=" * 70)

    # Create a resource with a weak reference
    resource = Resource("Database")
    weak_resource = weakref.ref(resource)

    def cleanup(ref):
        """Callback when resource is garbage collected"""
        print(f"Cleanup: Resource was collected!")

    # Add finalizer
    finalizer = weakref.finalize(resource, cleanup, weak_resource)
    print(f"Finalizer registered: {finalizer.alive}")

    # Delete the resource
    print("\nDeleting resource:")
    del resource
    gc.collect()
    print(f"Finalizer alive: {finalizer.alive}")


# ============================================================
# 4. CACHING WITH WEAK REFERENCES
# ============================================================

class ResourceCache:
    """Cache that uses weak references for automatic cleanup"""

    def __init__(self):
        self._cache: Dict[str, weakref.ref] = {}
        self._callback_called = 0

    def get_or_create(self, key, factory):
        """Get resource from cache or create it"""
        weak_ref = self._cache.get(key)

        if weak_ref is None:
            # Cache miss - create new resource
            resource = factory(key)
            self._cache[key] = weakref.ref(resource, self._cleanup_callback)
            print(f"Created resource for key: {key}")
            return resource

        # Check if resource still exists
        resource = weak_ref()
        if resource is None:
            # Resource was garbage collected - recreate
            resource = factory(key)
            self._cache[key] = weakref.ref(resource, self._cleanup_callback)
            print(f"Recreated resource for key: {key}")
            return resource

        print(f"Cache hit for key: {key}")
        return resource

    def _cleanup_callback(self, ref):
        """Callback when a cached object is garbage collected"""
        self._callback_called += 1
        print(f"Cache cleanup: {self._callback_called} objects cleaned up")

    def size(self):
        """Get number of live objects in cache"""
        count = 0
        dead_keys = []
        for key, ref in self._cache.items():
            if ref() is not None:
                count += 1
            else:
                dead_keys.append(key)

        # Clean up dead entries
        for key in dead_keys:
            del self._cache[key]

        return count

    def __repr__(self):
        return f"ResourceCache(size={self.size()})"


class ExpensiveResource:
    """Resource that's expensive to create"""

    def __init__(self, name):
        self.name = name
        self.data = list(range(1000000))  # Large data
        print(f"Creating ExpensiveResource: {name}")

    def __del__(self):
        print(f"Destroying ExpensiveResource: {self.name}")

    def __repr__(self):
        return f"ExpensiveResource({self.name})"


def demonstrate_cache():
    """Demonstrate caching with weak references"""
    print("\n" + "=" * 70)
    print("CACHING WITH WEAK REFERENCES")
    print("=" * 70)

    cache = ResourceCache()

    # Create factory function
    def create_resource(key):
        return ExpensiveResource(key)

    # Get/create resources
    print("Getting resources:")
    res1 = cache.get_or_create("resource1", create_resource)
    res2 = cache.get_or_create("resource2", create_resource)
    res3 = cache.get_or_create("resource1", create_resource)  # Cache hit

    print(f"\nCache size: {cache.size()}")

    # Delete all strong references
    print("\nDeleting strong references:")
    del res1
    del res2
    del res3

    # Force garbage collection
    gc.collect()

    print(f"\nCache size after GC: {cache.size()}")
    print(f"Cache cleanup callbacks: {cache._callback_called}")


# ============================================================
# 5. OBSERVER PATTERN WITH WEAK REFERENCES
# ============================================================

class Subject:
    """Subject that notifies observers (with weak references)"""

    def __init__(self):
        self._observers = weakref.WeakSet()  # Automatic cleanup

    def attach(self, observer):
        """Attach an observer"""
        self._observers.add(observer)
        print(f"Attached observer: {observer}")

    def notify(self, message):
        """Notify all observers"""
        print(f"\nSubject notifying: {message}")
        for observer in list(self._observers):
            # WeakSet automatically handles dead references
            if observer is not None:
                observer.update(message)
            else:
                print("  Dead observer cleaned up")


class Observer:
    """Observer that can be attached to subjects"""

    def __init__(self, name):
        self.name = name

    def update(self, message):
        print(f"Observer {self.name} received: {message}")

    def __repr__(self):
        return f"Observer({self.name})"


def demonstrate_observer():
    """Demonstrate observer pattern with weak references"""
    print("\n" + "=" * 70)
    print("OBSERVER PATTERN WITH WEAK REFERENCES")
    print("=" * 70)

    subject = Subject()

    # Create observers
    obs1 = Observer("A")
    obs2 = Observer("B")
    obs3 = Observer("C")

    # Attach observers
    subject.attach(obs1)
    subject.attach(obs2)
    subject.attach(obs3)

    # Notify
    subject.notify("Hello observers!")

    # Delete one observer
    print("\nDeleting Observer B:")
    del obs2
    gc.collect()

    # Notify again - obs2 is automatically removed
    subject.notify("Goodbye observers!")


# ============================================================
# 6. AVOIDING REFERENCE CYCLES
# ============================================================

class Node:
    """Node that can reference parent using weak reference"""

    def __init__(self, name):
        self.name = name
        self.children = []
        self._parent = None

    @property
    def parent(self):
        """Parent getter"""
        if self._parent is not None:
            return self._parent()
        return None

    @parent.setter
    def parent(self, value):
        """Parent setter (uses weak reference)"""
        if value is not None:
            self._parent = weakref.ref(value)
        else:
            self._parent = None

    def add_child(self, child):
        """Add a child node"""
        self.children.append(child)
        child.parent = self  # Set parent using weak reference

    def __repr__(self):
        return f"Node({self.name}, children={len(self.children)})"

    def __del__(self):
        print(f"Deleting Node: {self.name}")


def demonstrate_cycles():
    """Demonstrate avoiding reference cycles"""
    print("\n" + "=" * 70)
    print("AVOIDING REFERENCE CYCLES")
    print("=" * 70)

    # Create nodes
    root = Node("Root")
    child1 = Node("Child1")
    child2 = Node("Child2")
    child3 = Node("Child3")

    # Build tree
    root.add_child(child1)
    root.add_child(child2)
    child1.add_child(child3)

    # Check references
    print(f"Root: {root}")
    print(f"Child1 parent: {child1.parent}")
    print(f"Child2 parent: {child2.parent}")
    print(f"Child3 parent: {child3.parent}")

    # Delete all strong references
    print("\nDeleting strong references:")
    del root
    del child1
    del child2
    del child3

    # Force garbage collection
    gc.collect()
    print("All nodes should be cleaned up (no cycle)")


# ============================================================
# 7. WEAKREF.CALLABLE_PROXY
# ============================================================

class CallableObject:
    """Callable object for proxy demonstration"""

    def __call__(self, *args, **kwargs):
        return f"Called with {args}, {kwargs}"

    def method(self):
        return "Method called"


def demonstrate_callable_proxy():
    """Demonstrate weakref.callable_proxy"""
    print("\n" + "=" * 70)
    print("WEAKREF.CALLABLE_PROXY")
    print("=" * 70)

    obj = CallableObject()
    proxy = weakref.proxy(obj)

    print(f"Original: {obj()}")
    print(f"Proxy: {proxy()}")
    print(f"Proxy method: {proxy.method()}")

    # Delete original
    print("\nDeleting original:")
    del obj
    try:
        proxy()
    except ReferenceError as e:
        print(f"Proxy error: {e}")


# ============================================================
# 8. WEAK REFERENCE WITH DATACLASSES
# ============================================================

from dataclasses import dataclass, field
from typing import Any


@dataclass
class WeakRefCache:
    """Cache using weak references with dataclass"""
    cache: Dict[str, Any] = field(default_factory=dict)
    _callback_count: int = field(default=0, init=False)

    def add(self, key: str, obj: Any) -> None:
        """Add object to cache"""
        self.cache[key] = weakref.ref(obj, self._on_cleanup)

    def get(self, key: str) -> Optional[Any]:
        """Get object from cache"""
        ref = self.cache.get(key)
        if ref is not None:
            return ref()
        return None

    def _on_cleanup(self, ref):
        """Called when cached object is collected"""
        self._callback_count += 1

    def cleanup(self) -> None:
        """Remove dead references from cache"""
        dead_keys = []
        for key, ref in self.cache.items():
            if ref() is None:
                dead_keys.append(key)

        for key in dead_keys:
            del self.cache[key]


def demonstrate_dataclass_cache():
    """Demonstrate weak references with dataclasses"""
    print("\n" + "=" * 70)
    print("WEAK REFERENCES WITH DATACLASSES")
    print("=" * 70)

    cache = WeakRefCache()

    # Create objects
    obj1 = ExpensiveResource("cache1")
    obj2 = ExpensiveResource("cache2")

    # Add to cache
    cache.add("key1", obj1)
    cache.add("key2", obj2)

    # Get from cache
    print(f"Cache hit: {cache.get('key1')}")

    # Delete objects
    print("\nDeleting objects:")
    del obj1
    del obj2
    gc.collect()

    # Check cache
    print(f"Cache after deletion: {cache.get('key1')}")
    print(f"Cache cleanup count: {cache._callback_count}")

    # Run cleanup
    cache.cleanup()
    print(f"Cache size after cleanup: {len(cache.cache)}")


# ============================================================
# 9. WEAK REFERENCES WITH THREADS
# ============================================================

import threading
import time


class Worker:
    """Worker that runs in a thread"""

    def __init__(self, name):
        self.name = name
        self.running = False
        self._thread = None

    def start(self):
        """Start the worker thread"""
        self.running = True
        self._thread = threading.Thread(target=self._run)
        self._thread.start()
        print(f"Worker {self.name} started")

    def _run(self):
        """Main worker loop"""
        while self.running:
            print(f"Worker {self.name} running...")
            time.sleep(0.5)
        print(f"Worker {self.name} stopped")

    def stop(self):
        """Stop the worker"""
        self.running = False

    def __del__(self):
        print(f"Worker {self.name} destroyed")


class WorkerManager:
    """Manages workers with weak references"""

    def __init__(self):
        self._workers = weakref.WeakValueDictionary()
        self._lock = threading.Lock()

    def create_worker(self, name):
        """Create and start a worker"""
        with self._lock:
            worker = Worker(name)
            self._workers[name] = worker
            worker.start()
            return worker

    def get_worker(self, name):
        """Get a worker by name"""
        with self._lock:
            return self._workers.get(name)

    def stop_all(self):
        """Stop all workers"""
        with self._lock:
            for worker in list(self._workers.values()):
                if worker is not None:
                    worker.stop()
            self._workers.clear()


def demonstrate_threads():
    """Demonstrate weak references with threads"""
    print("\n" + "=" * 70)
    print("WEAK REFERENCES WITH THREADS")
    print("=" * 70)

    manager = WorkerManager()

    # Create workers
    w1 = manager.create_worker("Worker1")
    w2 = manager.create_worker("Worker2")

    # Get worker
    worker = manager.get_worker("Worker1")
    print(f"Got worker: {worker}")

    # Delete one worker (thread continues until stopped)
    print("\nDeleting Worker1 reference:")
    del w1
    gc.collect()

    time.sleep(1)

    # Stop all workers
    print("\nStopping all workers:")
    manager.stop_all()
    time.sleep(1)


# ============================================================
# 10. PERFORMANCE COMPARISON
# ============================================================

def performance_comparison():
    """Compare performance of weak references vs strong references"""
    print("\n" + "=" * 70)
    print("PERFORMANCE COMPARISON")
    print("=" * 70)

    # Create many objects
    n = 100000

    # Strong references
    import time
    start = time.time()
    strong_list = [Person(f"Strong{i}") for i in range(n)]
    strong_time = time.time() - start

    # Weak references
    start = time.time()
    weak_list = [weakref.ref(Person(f"Weak{i}")) for i in range(n)]
    weak_time = time.time() - start

    print(f"Strong references ({n} objects): {strong_time:.2f} seconds")
    print(f"Weak references ({n} objects): {weak_time:.2f} seconds")

    # Memory usage
    import sys
    strong_size = sum(sys.getsizeof(obj) for obj in strong_list)
    weak_size = n * sys.getsizeof(weakref.ref(Person("test"))) + sum(
        sys.getsizeof(obj()) for obj in weak_list if obj() is not None)

    print(f"Strong memory: {strong_size:,} bytes")
    print(f"Weak memory: {weak_size:,} bytes")


# ============================================================
# DEMONSTRATION
# ============================================================

def demonstrate_weakref():
    """Complete demonstration of weak references"""

    print("=" * 70)
    print("WEAK REFERENCES COMPREHENSIVE DEMONSTRATION")
    print("=" * 70)

    # 1. Basic usage
    demonstrate_basic()

    # 2. Weak reference types
    demonstrate_weak_types()

    # 3. Finalizers
    demonstrate_finalizer()

    # 4. Caching
    demonstrate_cache()

    # 5. Observer pattern
    demonstrate_observer()

    # 6. Avoiding cycles
    demonstrate_cycles()

    # 7. Callable proxy
    demonstrate_callable_proxy()

    # 8. Dataclass cache
    demonstrate_dataclass_cache()

    # 9. Threads
    demonstrate_threads()

    # 10. Performance
    performance_comparison()


# ============================================================
# MAIN EXECUTION
# ============================================================

if __name__ == "__main__":
    demonstrate_weakref()

    print("\n" + "=" * 70)
    print("WEAK REFERENCES KEY CONCEPTS")
    print("=" * 70)
    print("""
    ✅ WHAT ARE WEAK REFERENCES
       - References that don't prevent garbage collection
       - Allow tracking objects without ownership
       - Essential for memory management

    ✅ TYPES OF WEAK REFERENCES
       - weakref.ref: Basic weak reference
       - weakref.proxy: Acts like original object
       - weakref.WeakKeyDictionary: Weak keys
       - weakref.WeakValueDictionary: Weak values
       - weakref.WeakSet: Set of weak references
       - weakref.finalize: Cleanup callbacks

    ✅ USE CASES
       - Caching (objects can be evicted automatically)
       - Observer pattern (prevent reference cycles)
       - Avoiding memory leaks
       - Resource management
       - Large data structures

    ✅ BEST PRACTICES
       - Use weak references for parent references in trees
       - Use WeakKeyDictionary for caching
       - Use WeakSet for observer collections
       - Use finalize for resource cleanup
       - Check if reference is alive before using
       - Handle ReferenceError for proxies

    ✅ MEMORY MANAGEMENT
       - Automatic cleanup when objects are garbage collected
       - Prevents reference cycles
       - Helps avoid memory leaks
       - Reduces memory usage
    """)
    print("=" * 70)