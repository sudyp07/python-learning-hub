# ==========================================
# LEGB = Local → Enclosed → Global → Built-in
# Python searches for a variable in THIS order.
# ==========================================

x = "🌍 Global x"      # Global Scope


def outer():
    x = "🏠 Enclosed x"    # Enclosed Scope (belongs to outer)

    def inner():
        x = "📦 Local x"   # Local Scope (belongs to inner)

        print("1.", x)
        # Python searches:
        # Local ✅ FOUND
        # Stops here.
        # Output: 📦 Local x

    inner()


outer()

print("-" * 40)


def outer2():
    x = "🏠 Enclosed x"

    def inner():
        # No local x here

        print("2.", x)
        # Search:
        # Local ❌
        # Enclosed ✅ FOUND
        # Output: 🏠 Enclosed x

    inner()


outer2()

print("-" * 40)


def outer3():

    def inner():
        # No local x
        # No enclosed x

        print("3.", x)
        # Search:
        # Local ❌
        # Enclosed ❌
        # Global ✅ FOUND
        # Output: 🌍 Global x

    inner()


outer3()

print("-" * 40)


def outer4():

    def inner():

        numbers = [10, 20, 30]

        print("4.", len(numbers))
        # Search for len:
        # Local ❌
        # Enclosed ❌
        # Global ❌
        # Built-in ✅ FOUND
        # Output: 3

    inner()


outer4()