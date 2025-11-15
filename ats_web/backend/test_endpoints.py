"""Test if all endpoints are registered"""
import sys
from main import app

print("Checking registered routes...")
print("=" * 60)

routes = []
for route in app.routes:
    if hasattr(route, 'methods') and hasattr(route, 'path'):
        for method in route.methods:
            if method != "HEAD":  # Skip HEAD methods
                routes.append(f"{method:6} {route.path}")

routes.sort()

for route in routes:
    print(route)

print("=" * 60)
print(f"Total routes: {len(routes)}")

# Check if /api/ask exists
ask_exists = any('/api/ask' in route for route in routes)
print(f"\n/api/ask endpoint exists: {ask_exists}")

if not ask_exists:
    print("\n⚠️  WARNING: /api/ask endpoint is missing!")
    print("This might be due to an import error or syntax issue.")
else:
    print("\n✓ /api/ask endpoint is registered correctly")
