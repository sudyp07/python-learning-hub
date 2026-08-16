import requests


def fetch_pokemon_data(pokemon_name):
    """
    Fetch detailed information about a Pokémon from the PokeAPI

    Args:
        pokemon_name (str): Name of the Pokémon (e.g., 'pikachu', 'charizard')

    Returns:
        dict: Pokémon data or None if not found
    """
    # 1. Construct the API endpoint URL
    # PokeAPI uses RESTful endpoints: https://pokeapi.co/api/v2/{resource}/{id_or_name}/
    base_url = "https://pokeapi.co/api/v2"
    endpoint = f"{base_url}/pokemon/{pokemon_name.lower()}"

    try:
        # 2. Make GET request to the API
        # requests.get() sends an HTTP GET request to the specified URL
        response = requests.get(endpoint)

        # 3. Check if the request was successful (status code 200)
        # HTTP status codes: 200 = OK, 404 = Not Found, 500 = Server Error
        if response.status_code == 200:
            # 4. Parse the JSON response into a Python dictionary
            # response.json() converts JSON string to Python dict
            data = response.json()
            return data
        elif response.status_code == 404:
            print(f"❌ Pokémon '{pokemon_name}' not found!")
            return None
        else:
            print(f"❌ Error {response.status_code}: Unable to fetch data")
            return None

    except requests.exceptions.ConnectionError:
        print("❌ Network error: Could not connect to the API")
        return None
    except requests.exceptions.Timeout:
        print("❌ Timeout error: Request took too long")
        return None
    except requests.exceptions.RequestException as e:
        print(f"❌ Request error: {e}")
        return None


def display_pokemon_info(data):
    """
    Display formatted Pokémon information from API data

    Args:
        data (dict): Pokémon data from the API
    """
    if not data:
        return

    print("\n" + "=" * 50)
    print(f"📊 POKÉMON DETAILS")
    print("=" * 50)

    # 1. Basic Information
    print(f"🎯 Name: {data['name'].capitalize()}")
    print(f"📏 Height: {data['height'] / 10:.1f} m")  # API returns decimeters
    print(f"⚖️ Weight: {data['weight'] / 10:.1f} kg")  # API returns hectograms

    # 2. Types (A Pokémon can have 1-2 types)
    types = [t['type']['name'].capitalize() for t in data['types']]
    print(f"🏷️ Types: {', '.join(types)}")

    # 3. Abilities (with hidden ability marked)
    abilities = []
    for a in data['abilities']:
        ability_name = a['ability']['name'].replace('-', ' ').capitalize()
        if a['is_hidden']:
            abilities.append(f"{ability_name} (Hidden)")
        else:
            abilities.append(ability_name)
    print(f"💪 Abilities: {', '.join(abilities)}")

    # 4. Base Stats
    print("\n📈 BASE STATS:")
    stats = {
        'HP': 'hp',
        'Attack': 'attack',
        'Defense': 'defense',
        'Sp. Atk': 'special-attack',
        'Sp. Def': 'special-defense',
        'Speed': 'speed'
    }
    for stat_name, stat_key in stats.items():
        for stat in data['stats']:
            if stat['stat']['name'] == stat_key:
                print(f"   {stat_name}: {stat['base_stat']}")

    # 5. Experience and Catch Rate
    print(f"\n⭐ Base Experience: {data['base_experience']}")

    # 6. Moves (show first 5 only)
    moves = [m['move']['name'].replace('-', ' ').capitalize()
             for m in data['moves'][:5]]
    print(f"🎮 Sample Moves: {', '.join(moves)}")
    if len(data['moves']) > 5:
        print(f"   ... and {len(data['moves']) - 5} more moves")

    # 7. Evolution chain URL (for deeper API calls)
    species_url = data['species']['url']
    print(f"\n🔄 Species URL: {species_url}")
    print("=" * 50)


def save_pokemon_to_file(data, filename="pokemon_data.json"):
    """
    Save Pokémon data to a JSON file

    Args:
        data (dict): Pokémon data
        filename (str): Output filename
    """
    import json

    try:
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
        print(f"💾 Data saved to {filename}")
    except Exception as e:
        print(f"⚠️ Could not save file: {e}")


def get_pokemon_by_id(pokemon_id):
    """
    Alternative: Fetch Pokémon by ID number instead of name

    Args:
        pokemon_id (int): Pokémon ID (e.g., 25 for Pikachu)
    """
    return fetch_pokemon_data(str(pokemon_id))


def search_pokemon():
    """
    Main function: Let user search for Pokémon
    """
    print("🐉 POKÉMON SEARCH 🐉")
    print("-" * 30)

    while True:
        # Get user input
        name = input("\nEnter Pokémon name (or 'quit' to exit): ").strip()

        if name.lower() in ['quit', 'exit', 'q']:
            print("👋 Goodbye!")
            break

        if not name:
            print("⚠️ Please enter a Pokémon name")
            continue

        # Fetch data
        print(f"🔍 Searching for '{name}'...")
        pokemon_data = fetch_pokemon_data(name)

        if pokemon_data:
            # Display formatted information
            display_pokemon_info(pokemon_data)

            # Ask if user wants to save
            save_choice = input("\n💾 Save this data to file? (y/n): ").lower()
            if save_choice in ['y', 'yes']:
                save_pokemon_to_file(pokemon_data, f"{name.lower()}_data.json")

        # Ask if user wants to continue
        cont = input("\n🔍 Search another Pokémon? (y/n): ").lower()
        if cont not in ['y', 'yes']:
            print("👋 Goodbye!")
            break


# Entry point: Run the program
if __name__ == "__main__":
    search_pokemon()