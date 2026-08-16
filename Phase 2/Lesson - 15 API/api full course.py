"""
=======================================
🐍 PYTHON API TUTORIAL - COMPLETE GUIDE
=======================================

This tutorial covers:
1. What is an API?
2. Making GET requests
3. Handling responses
4. Error handling
5. Query parameters
6. Headers
7. POST requests
8. Authentication
9. Working with JSON data

Let's learn step by step!
"""

# STEP 1: IMPORT THE REQUESTS LIBRARY
# ===================================
# requests is the most popular Python library for making HTTP requests
# Install with: pip install requests
import requests
import json

print("=" * 60)
print("🐍 PYTHON API TUTORIAL")
print("=" * 60)

# ============================================================
# PART 1: WHAT IS AN API?
# ============================================================
"""
API stands for Application Programming Interface
Think of it like a waiter in a restaurant:
- You (client) make a request
- Waiter (API) takes your request to kitchen (server)
- Kitchen (server) prepares your food (processes request)
- Waiter (API) brings food back to you (response)
"""

print("\n📌 PART 1: UNDERSTANDING API REQUESTS")
print("-" * 40)

# ============================================================
# PART 2: MAKING A SIMPLE GET REQUEST
# ============================================================
"""
GET Request: Used to retrieve data from a server
- Like asking "Can I see the menu?"
- No data is sent, only received
"""

print("\n🔹 EXAMPLE 1: Basic GET Request")

# Define the API endpoint URL
# This is the address where the API lives
url = "https://jsonplaceholder.typicode.com/posts/1"

print(f"📡 Request URL: {url}")

# Make the GET request
# requests.get() sends a GET request to the specified URL
response = requests.get(url)

# The response object contains everything the server sent back
print(f"📊 Status Code: {response.status_code}")  # 200 = Success
print(f"📝 Response Type: {type(response)}")  # <class 'requests.Response'>

# Convert the response from JSON to Python dictionary
# response.json() parses the JSON string into a Python dict
data = response.json()

print(f"📦 Data Type: {type(data)}")  # <class 'dict'>
print(f"📄 Data: {data}")

# ============================================================
# PART 3: UNDERSTANDING HTTP STATUS CODES
# ============================================================
"""
HTTP Status Codes tell you what happened with your request:

2xx: Success! 🎉
- 200: OK (Everything worked)
- 201: Created (New resource made)

3xx: Redirection (Resource moved)
- 301: Moved permanently
- 302: Found (temporary redirect)

4xx: Client Error (Your fault) 😅
- 400: Bad Request (Wrong data sent)
- 401: Unauthorized (Need to login)
- 403: Forbidden (Not allowed)
- 404: Not Found (Doesn't exist)

5xx: Server Error (Their fault) 😱
- 500: Internal Server Error
- 503: Service Unavailable
"""

print("\n🔹 EXAMPLE 2: Checking Status Codes")

# Try a URL that doesn't exist
bad_url = "https://jsonplaceholder.typicode.com/posts/999999"
bad_response = requests.get(bad_url)

if bad_response.status_code == 200:
    print("✅ Success! Data found.")
elif bad_response.status_code == 404:
    print("❌ Error 404: Resource not found!")
else:
    print(f"⚠️ Status Code: {bad_response.status_code}")

# ============================================================
# PART 4: WORKING WITH RESPONSE DATA
# ============================================================
"""
The response can come in different formats:
- JSON (most common - like Python dictionaries)
- XML (older format)
- HTML (web pages)
- Text (plain text)
- Binary (images, files)
"""

print("\n🔹 EXAMPLE 3: Different Response Formats")

# JSON response (most common)
json_url = "https://api.github.com/users/octocat"
json_response = requests.get(json_url)

if json_response.status_code == 200:
    # Access as JSON
    user_data = json_response.json()
    print(f"👤 User: {user_data['login']}")
    print(f"📛 Name: {user_data.get('name', 'Not specified')}")
    print(f"📊 Followers: {user_data['followers']}")

    # JSON string representation
    json_string = json_response.text
    print(f"📝 Raw JSON (first 100 chars): {json_string[:100]}...")

# ============================================================
# PART 5: USING QUERY PARAMETERS
# ============================================================
"""
Query Parameters: Extra information sent in the URL
- Like asking "What's on the menu with gluten-free options?"
- Format: ?key1=value1&key2=value2
- Used for: Searching, filtering, sorting, pagination
"""

print("\n🔹 EXAMPLE 4: Query Parameters")

# Basic URL without parameters
base_url = "https://jsonplaceholder.typicode.com/posts"

# Parameters as a dictionary
params = {
    'userId': 1,  # Filter by user
    '_limit': 3  # Limit results to 3
}

print(f"📡 URL with parameters: {base_url}?{requests.compat.urlencode(params)}")

# requests automatically handles the parameter encoding
response_with_params = requests.get(base_url, params=params)

if response_with_params.status_code == 200:
    posts = response_with_params.json()
    print(f"📊 Found {len(posts)} posts for user 1:")
    for post in posts:
        print(f"  📝 Post {post['id']}: {post['title']}")

# ============================================================
# PART 6: ADDING HEADERS TO REQUESTS
# ============================================================
"""
Headers: Metadata sent with the request
- Like specifying dietary restrictions when ordering
- Common headers:
  - User-Agent: What browser/app you're using
  - Authorization: Your API key or token
  - Content-Type: What format your data is in
  - Accept: What format you want the response in
"""

print("\n🔹 EXAMPLE 5: Custom Headers")

# Create custom headers
headers = {
    'User-Agent': 'MyPythonApp/1.0',  # Tell server who we are
    'Accept': 'application/json',  # We want JSON response
    'X-Custom-Header': 'Hello API'  # Custom header (server may ignore)
}

# Make request with custom headers
url_with_headers = "https://httpbin.org/headers"
response_with_headers = requests.get(url_with_headers, headers=headers)

if response_with_headers.status_code == 200:
    header_data = response_with_headers.json()
    print("📨 Headers we sent:")
    print(f"  User-Agent: {header_data['headers']['User-Agent']}")
    print(f"  Accept: {header_data['headers']['Accept']}")

# ============================================================
# PART 7: MAKING POST REQUESTS
# ============================================================
"""
POST Request: Used to send data to the server
- Like placing an order: "I'll have the pasta"
- Used for: Creating new resources, submitting forms, sending data
- Data is sent in the request body (not in URL)
"""

print("\n🔹 EXAMPLE 6: POST Request")

# Data to send (as a dictionary)
post_data = {
    'title': 'My New Post',
    'body': 'This is the content of my post.',
    'userId': 1
}

print(f"📤 Sending data: {post_data}")

# POST endpoint
post_url = "https://jsonplaceholder.typicode.com/posts"

# Send POST request with data
post_response = requests.post(post_url, json=post_data)

if post_response.status_code == 201:  # 201 = Created
    created_data = post_response.json()
    print("✅ Successfully created!")
    print(f"📄 Created post ID: {created_data['id']}")
    print(f"📝 Title: {created_data['title']}")
    print(f"📋 Body: {created_data['body']}")
else:
    print(f"❌ Failed with status: {post_response.status_code}")

# ============================================================
# PART 8: DIFFERENT WAYS TO SEND DATA IN POST
# ============================================================
"""
Different ways to send data in POST requests:

1. JSON (json=): Most common, sends as application/json
2. Form Data (data=): Sends as application/x-www-form-urlencoded
3. Files (files=): For uploading files (multipart/form-data)
"""

print("\n🔹 EXAMPLE 7: Different Data Formats")

# Method 1: JSON data (most common for APIs)
json_payload = {"username": "john_doe", "email": "john@example.com"}
json_response = requests.post(
    "https://httpbin.org/post",
    json=json_payload
)

if json_response.status_code == 200:
    result = json_response.json()
    print("📦 JSON Method:")
    print(f"  Sent JSON: {result['json']}")
    print(f"  Content-Type: {result['headers']['Content-Type']}")

# Method 2: Form data (like submitting a form)
form_data = {"username": "john_doe", "email": "john@example.com"}
form_response = requests.post(
    "https://httpbin.org/post",
    data=form_data
)

if form_response.status_code == 200:
    result = form_response.json()
    print("\n📋 Form Data Method:")
    print(f"  Form data: {result['form']}")
    print(f"  Content-Type: {result['headers']['Content-Type']}")

# ============================================================
# PART 9: API AUTHENTICATION
# ============================================================
"""
Authentication: Proving who you are to the API
- Like showing your ID at a bar
- Common methods:
  1. API Key: Simple key in headers or URL
  2. Bearer Token: JWT in Authorization header
  3. Basic Auth: Username + password (Base64 encoded)
  4. OAuth2: Complex but very secure
"""

print("\n🔹 EXAMPLE 8: Authentication Methods")

# Method 1: API Key in URL (not very secure)
print("\n📌 Method 1: API Key in URL")
api_key_url = "https://httpbin.org/get?api_key=your_secret_key_123"
api_key_response = requests.get(api_key_url)

if api_key_response.status_code == 200:
    print("✅ API Key accepted (simulated)")

# Method 2: API Key in Headers (more secure)
print("\n📌 Method 2: API Key in Headers")
headers_with_key = {
    'X-API-Key': 'your_secret_api_key_123',
    'Authorization': 'Bearer your_jwt_token_here'
}
headers_response = requests.get(
    "https://httpbin.org/headers",
    headers=headers_with_key
)

if headers_response.status_code == 200:
    print("✅ Headers sent with authentication")
    result = headers_response.json()
    print(f"  Authorization: {result['headers'].get('Authorization', 'Not sent')}")

# Method 3: Basic Authentication
print("\n📌 Method 3: Basic Authentication")
# Username and password
username = "user123"
password = "pass456"

# requests handles base64 encoding automatically
basic_response = requests.get(
    "https://httpbin.org/basic-auth/user123/pass456",
    auth=(username, password)  # Simple tuple
)

if basic_response.status_code == 200:
    print("✅ Basic authentication successful!")
    auth_data = basic_response.json()
    print(f"  Authenticated user: {auth_data['user']}")
else:
    print(f"❌ Authentication failed: {basic_response.status_code}")

# ============================================================
# PART 10: ERROR HANDLING
# ============================================================
"""
Error Handling: Gracefully dealing with problems
- Network errors: Can't reach the server
- Timeouts: Server takes too long
- Invalid responses: Server returns unexpected data
- HTTP errors: 4xx or 5xx status codes
"""

print("\n🔹 EXAMPLE 9: Comprehensive Error Handling")


def safe_api_request(url, params=None, timeout=5):
    """
    Make a safe API request with comprehensive error handling

    Args:
        url: The API endpoint
        params: Optional query parameters
        timeout: Seconds to wait before timeout

    Returns:
        dict: Data if successful, None otherwise
    """
    try:
        # Try to make the request with timeout
        response = requests.get(url, params=params, timeout=timeout)

        # Check if status code indicates error
        # raise_for_status() raises an exception for 4xx/5xx codes
        response.raise_for_status()

        # Try to parse JSON
        try:
            return response.json()
        except json.JSONDecodeError:
            print("⚠️ Response is not valid JSON")
            return None

    except requests.exceptions.ConnectionError:
        print("❌ Connection Error: Could not connect to the server")
        print("   Check your internet connection and the URL")
        return None

    except requests.exceptions.Timeout:
        print(f"❌ Timeout Error: Server didn't respond in {timeout} seconds")
        print("   Server might be slow or down")
        return None

    except requests.exceptions.HTTPError as e:
        print(f"❌ HTTP Error: {e}")
        if response.status_code == 401:
            print("   Authentication required - check your API key")
        elif response.status_code == 403:
            print("   Access forbidden - you don't have permission")
        elif response.status_code == 404:
            print("   Resource not found - check the URL")
        return None

    except requests.exceptions.RequestException as e:
        print(f"❌ Request Error: {e}")
        return None


# Test the safe function
print("Testing safe request with good URL:")
good_result = safe_api_request("https://jsonplaceholder.typicode.com/posts/1")
if good_result:
    print(f"  ✅ Success! Got data for post {good_result.get('id', 'unknown')}")

print("\nTesting safe request with bad URL:")
bad_result = safe_api_request("https://jsonplaceholder.typicode.com/posts/99999")
if bad_result is None:
    print("  ✅ Correctly handled the error")

print("\nTesting timeout:")
timeout_result = safe_api_request(
    "https://httpbin.org/delay/10",  # Server delays 10 seconds
    timeout=2
)
if timeout_result is None:
    print("  ✅ Correctly handled timeout")

# ============================================================
# PART 11: WORKING WITH NESTED JSON DATA
# ============================================================
"""
Nested JSON: Data inside data inside data
- Like a Russian doll of information
- Access with multiple keys: data['key1']['key2']['key3']
"""

print("\n🔹 EXAMPLE 10: Navigating Nested JSON")

# Complex API with nested data
pokemon_url = "https://pokeapi.co/api/v2/pokemon/pikachu"
pokemon_response = requests.get(pokemon_url)

if pokemon_response.status_code == 200:
    pokemon_data = pokemon_response.json()

    print("📊 Exploring Nested Pokémon Data:")
    print(f"  Name: {pokemon_data['name']}")

    # Accessing nested data
    print(f"  Type: {pokemon_data['types'][0]['type']['name']}")

    # Loop through nested data
    print("  Abilities:")
    for ability in pokemon_data['abilities']:
        name = ability['ability']['name']
        is_hidden = ability['is_hidden']
        print(f"    • {name} {'(Hidden)' if is_hidden else ''}")

    # Stats with more nesting
    print("  Stats:")
    for stat in pokemon_data['stats']:
        stat_name = stat['stat']['name']
        base_value = stat['base_stat']
        print(f"    • {stat_name}: {base_value}")

# ============================================================
# PART 12: PAGINATION - GETTING LOTS OF DATA
# ============================================================
"""
Pagination: Getting data in chunks
- Like reading a book one page at a time
- Common parameters: page, limit, offset, count
"""

print("\n🔹 EXAMPLE 11: Pagination")


def get_paginated_data(base_url, page=1, limit=5):
    """
    Fetch paginated data from an API
    """
    params = {
        '_page': page,  # Current page
        '_limit': limit  # Items per page
    }

    response = requests.get(base_url, params=params)

    if response.status_code == 200:
        data = response.json()
        print(f"  Page {page}: Got {len(data)} items")
        return data
    return None


# Example with posts
posts_url = "https://jsonplaceholder.typicode.com/posts"

print("Fetching posts with pagination:")
for page in range(1, 4):  # Get first 3 pages
    data = get_paginated_data(posts_url, page=page, limit=3)
    if data:
        for post in data:
            print(f"    Post {post['id']}: {post['title'][:30]}...")

# ============================================================
# PART 13: RATE LIMITING - BEING NICE TO API SERVERS
# ============================================================
"""
Rate Limiting: Don't make too many requests too fast
- APIs often limit how many requests per minute
- Respect the limits to avoid getting blocked
- Use delays between requests
"""

print("\n🔹 EXAMPLE 12: Rate Limiting")

import time


def rate_limited_request(url, delay=1):
    """
    Make request with a delay to respect rate limits
    """
    print(f"⏰ Waiting {delay} second(s) before request...")
    time.sleep(delay)  # Pause execution

    response = requests.get(url)
    return response


# Make multiple requests with delays
print("Making requests with rate limiting:")
for i in range(3):
    response = rate_limited_request("https://jsonplaceholder.typicode.com/posts/1")
    if response.status_code == 200:
        data = response.json()
        print(f"  Request {i + 1}: Got post {data.get('id', 'unknown')}")

# ============================================================
# PART 14: CACHING - SAVING DATA TO AVOID RE-REQUESTING
# ============================================================
"""
Caching: Save API responses to avoid repeated calls
- Like taking notes so you don't have to ask again
- Saves time and respects rate limits
"""

print("\n🔹 EXAMPLE 13: Simple Caching")


class SimpleCache:
    """
    A simple cache to store API responses
    """

    def __init__(self):
        self.cache = {}  # Dictionary to store data

    def get(self, url):
        """Get data from cache"""
        return self.cache.get(url)

    def set(self, url, data):
        """Store data in cache"""
        self.cache[url] = data
        print(f"  💾 Cached: {url}")


# Use the cache
cache = SimpleCache()
test_url = "https://jsonplaceholder.typicode.com/posts/1"

# First request - not cached
print("First request (cache miss):")
cached_data = cache.get(test_url)
if cached_data is None:
    response = requests.get(test_url)
    if response.status_code == 200:
        data = response.json()
        cache.set(test_url, data)
        print(f"  ✅ Data fetched and cached: Post {data.get('id', 'unknown')}")

# Second request - cached
print("\nSecond request (cache hit):")
cached_data = cache.get(test_url)
if cached_data:
    print(f"  ✅ Data from cache: Post {cached_data.get('id', 'unknown')}")

# ============================================================
# PART 15: PUT AND DELETE REQUESTS
# ============================================================
"""
PUT Request: Update entire resource
- Like changing your whole order
- Replaces the entire resource with new data

PATCH Request: Partial update
- Like changing just the sauce on your pasta
- Updates only specific fields

DELETE Request: Remove resource
- Like canceling your order
"""

print("\n🔹 EXAMPLE 14: PUT, PATCH, DELETE")

# PUT - Full update
put_url = "https://jsonplaceholder.typicode.com/posts/1"
updated_data = {
    'id': 1,
    'title': 'Updated Title',
    'body': 'This is the updated content',
    'userId': 1
}

print("📤 Sending PUT request (full update):")
put_response = requests.put(put_url, json=updated_data)
if put_response.status_code == 200:
    put_result = put_response.json()
    print(f"  ✅ Updated post: {put_result['title']}")

# PATCH - Partial update
patch_data = {'title': 'Patched Title'}
patch_response = requests.patch(put_url, json=patch_data)
if patch_response.status_code == 200:
    patch_result = patch_response.json()
    print(f"  ✅ Patched post: {patch_result['title']}")

# DELETE
delete_response = requests.delete(put_url)
if delete_response.status_code == 200:
    print("  ✅ Deleted successfully!")
else:
    print(f"  ❌ Delete failed with status: {delete_response.status_code}")

# ============================================================
# SUMMARY: BEST PRACTICES CHEAT SHEET
# ============================================================
print("\n" + "=" * 60)
print("📚 API BEST PRACTICES SUMMARY")
print("=" * 60)

best_practices = """
✅ DO:
1. Always check status codes before processing data
2. Use try/except for error handling
3. Respect rate limits with delays
4. Cache repeated requests when possible
5. Use timeout to avoid hanging
6. Keep your API keys secret
7. Validate data before sending
8. Use appropriate HTTP methods

❌ DON'T:
1. Hardcode API keys in your code
2. Make too many requests too fast
3. Ignore error responses
4. Assume the API will always work
5. Send sensitive data without HTTPS
6. Store passwords in plain text
7. Ignore response content-type
8. Make unnecessary repeated requests

🔐 SECURITY:
- Use environment variables for API keys
- Always use HTTPS
- Validate all incoming data
- Never log sensitive information

🔄 ERROR CODES TO HANDLE:
- 400: Bad request - Check your data
- 401: Unauthorized - Check credentials
- 403: Forbidden - Insufficient permissions
- 404: Not found - Check URL
- 429: Too many requests - Slow down
- 500+: Server error - Try again later
"""

print(best_practices)

# ============================================================
# BONUS: INTERACTIVE API EXPLORER
# ============================================================
print("\n" + "=" * 60)
print("🎮 INTERACTIVE API EXPLORER")
print("=" * 60)


def explore_api():
    """Interactive function to explore APIs"""
    print("\nTry any API endpoint!")
    print("Examples:")
    print("  - https://api.github.com/users/octocat")
    print("  - https://pokeapi.co/api/v2/pokemon/pikachu")
    print("  - https://jsonplaceholder.typicode.com/posts/1")

    while True:
        url = input("\n🌐 Enter API URL (or 'quit'): ").strip()

        if url.lower() in ['quit', 'exit', 'q']:
            print("👋 Happy API exploring!")
            break

        if not url:
            print("⚠️ Please enter a URL")
            continue

        # Make the request
        print(f"📡 Fetching: {url}")
        try:
            response = requests.get(url, timeout=5)
            print(f"📊 Status Code: {response.status_code}")

            # Try to format the response nicely
            if response.status_code == 200:
                content_type = response.headers.get('content-type', '')

                if 'json' in content_type:
                    # Pretty print JSON
                    data = response.json()
                    print("📄 Response (JSON):")
                    print(json.dumps(data, indent=2)[:500] + "...")
                else:
                    # Show first 500 chars of text
                    print("📄 Response (first 500 chars):")
                    print(response.text[:500] + "...")
            else:
                print(f"❌ Error: {response.text[:200]}")

        except Exception as e:
            print(f"❌ Error: {e}")


# Uncomment to run the interactive explorer
# explore_api()

print("\n" + "=" * 60)
print("🎉 TUTORIAL COMPLETE! You now know:")
print("  ✅ What APIs are and how they work")
print("  ✅ How to make GET, POST, PUT, DELETE requests")
print("  ✅ How to handle errors gracefully")
print("  ✅ How to use query parameters and headers")
print("  ✅ How to authenticate with APIs")
print("  ✅ Best practices for API usage")
print("=" * 60)