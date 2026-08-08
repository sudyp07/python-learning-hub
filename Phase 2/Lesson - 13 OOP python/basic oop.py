# ============================================
# 1. CLASS - Blueprint for creating objects
# ============================================
class Smartphone:
    # Class attribute (shared by ALL instances)
    device_type = "Mobile Phone"

    # ==========================================
    # 2. CONSTRUCTOR - Creates & sets up object
    # ==========================================
    def __init__(self, brand, model, price):
        self.brand = brand  # Instance attribute
        self.model = model  # Instance attribute
        self.price = price  # Instance attribute
        self.is_on = False  # Default attribute

    # ==========================================
    # 3. METHODS - Actions the object can do
    # ==========================================
    def turn_on(self):
        self.is_on = True
        print(f"{self.brand} {self.model} is now ON")

    def turn_off(self):
        self.is_on = False
        print(f"{self.brand} {self.model} is now OFF")

    def make_call(self, number):
        if self.is_on:
            print(f"Calling {number} from {self.brand} {self.model}...")
        else:
            print("Phone is OFF! Turn it on first.")

    def show_info(self):
        print(f"📱 {self.brand} {self.model}")
        print(f"   Price: ${self.price}")
        print(f"   Status: {'ON' if self.is_on else 'OFF'}")
        print(f"   Type: {self.device_type}")


# ==========================================
# 4. INHERITANCE - Child inherits from Parent
# ==========================================
class Smartwatch(Smartphone):  # Smartwatch INHERITS from Smartphone
    # New attribute specific to Smartwatch
    def __init__(self, brand, model, price, strap_color):
        # SUPER() calls parent's __init__
        super().__init__(brand, model, price)
        self.strap_color = strap_color
        self.steps = 0

    # New method specific to Smartwatch
    def track_steps(self, steps):
        self.steps += steps
        print(f"👣 Steps tracked: {self.steps} total")

    # OVERRIDE - Changing parent's method
    def show_info(self):
        # Call parent's method first
        super().show_info()
        # Add extra info
        print(f"   Strap: {self.strap_color}")
        print(f"   Steps: {self.steps}")


# ==========================================
# 5. CREATING OBJECTS (Instances)
# ==========================================
# Creating objects from Smartphone class
phone1 = Smartphone("Apple", "iPhone 15", 999)
phone2 = Smartphone("Samsung", "Galaxy S24", 899)

# Creating object from Smartwatch class
watch = Smartwatch("Apple", "Watch Series 9", 399, "Blue")

# ==========================================
# 6. USING OBJECTS
# ==========================================
print("=" * 40)
print("SMARTPHONE DEMO")
print("=" * 40)

# Using Smartphone objects
phone1.show_info()
print()
phone1.turn_on()
phone1.make_call("555-1234")
print()

phone2.show_info()
phone2.make_call("555-5678")  # Phone is OFF
print()

print("=" * 40)
print("SMARTWATCH DEMO (INHERITANCE)")
print("=" * 40)

# Using Smartwatch object
watch.show_info()
print()
watch.turn_on()  # Inherited from Smartphone
watch.track_steps(100)  # Smartwatch's own method
watch.track_steps(50)  # Smartwatch's own method
watch.make_call("555-9999")  # Inherited from Smartphone