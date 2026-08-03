# Temperature Converter: Fahrenheit (°F) to Celsius (°C)

# Get the temperature in Fahrenheit from the user
fahrenheit = float(input("Enter the temperature in Fahrenheit (°F): "))

# Convert Fahrenheit to Celsius
celsius = (fahrenheit - 32) * 5 / 9

# Display the result
print(f"{fahrenheit:.2f}°F is equal to {celsius:.2f}°C.")