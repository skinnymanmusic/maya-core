"""
MAYA BACKEND ENDPOINT CHECKER
Automated by Claude for Skinny - Tests which endpoints are actually live!
"""

import asyncio
import json
from datetime import datetime
from pathlib import Path
import httpx

# Backend URL - UPDATE THIS if your Railway URL is different!
BACKEND_URL = "http://localhost:8000"  # Change to Railway URL when deployed

# All endpoints the frontend expects (from omega-client.ts)
EXPECTED_ENDPOINTS = {
    "health": {
        "GET /api/health": "System health check",
        "GET /api/health/db": "Database health",
        "GET /api/health/encryption": "Encryption check",
    },
    "auth": {
        "GET /api/auth/me": "Get current user",
        "POST /api/auth/login": "Login",
        "POST /api/auth/refresh": "Refresh token",
        "GET /api/auth/google/start": "Start Google OAuth",
        "GET /api/auth/google/callback": "Google OAuth callback",
    },
    "bookings": {
        "GET /api/bookings": "List bookings",
        "POST /api/bookings": "Create booking",
        "GET /api/bookings/{id}": "Get booking",
        "PATCH /api/bookings/{id}": "Update booking",
        "DELETE /api/bookings/{id}": "Delete booking",
    },
    "stripe": {
        "GET /api/stripe/payment-status/{id}": "Payment status",
        "POST /api/stripe/webhook": "Stripe webhook",
    },
    "clients": {
        "GET /api/clients": "List clients",
        "POST /api/clients": "Create client",
        "GET /api/clients/{id}": "Get client",
        "PUT /api/clients/{id}": "Update client",
        "DELETE /api/clients/{id}": "Delete client",
    },
    "calendar": {
        "GET /api/calendar/events": "List events",
        "POST /api/calendar/events": "Create event",
        "GET /api/calendar/availability": "Get availability",
        "POST /api/calendar/block": "Block time",
    },
    "agents": {
        "GET /api/agents": "List agents",
        "POST /api/agents": "Create agent",
        "GET /api/agents/{id}": "Get agent",
        "PATCH /api/agents/{id}": "Update agent",
    },
    "messages": {
        "GET /api/messages": "List messages",
        "POST /api/messages": "Send message",
    },
    "sms": {
        "GET /api/sms/conversations": "List SMS conversations",
        "POST /api/sms/send": "Send SMS",
    },
}


async def check_endpoint(client: httpx.AsyncClient, method: str, path: str, description: str):
    """Test a single endpoint"""
    try:
        url = f"{BACKEND_URL}{path}"
        
        if method == "GET":
            response = await client.get(url, timeout=5.0)
        elif method == "POST":
            response = await client.post(url, json={}, timeout=5.0)
        elif method == "PATCH":
            response = await client.patch(url, json={}, timeout=5.0)
        elif method == "PUT":
            response = await client.put(url, json={}, timeout=5.0)
        elif method == "DELETE":
            response = await client.delete(url, timeout=5.0)
        else:
            return {
                "method": method,
                "path": path,
                "description": description,
                "status": "UNKNOWN_METHOD",
                "response": None,
            }
        
        return {
            "method": method,
            "path": path,
            "description": description,
            "status_code": response.status_code,
            "status": "✅ LIVE" if response.status_code < 500 else "⚠️ ERROR",
            "response": response.text[:200] if response.text else None,
        }
        
    except httpx.ConnectError:
        return {
            "method": method,
            "path": path,
            "description": description,
            "status": "❌ NO_CONNECTION",
            "response": "Backend not running or URL incorrect",
        }
    except httpx.TimeoutException:
        return {
            "method": method,
            "path": path,
            "description": description,
            "status": "⏱️ TIMEOUT",
            "response": "Request timed out",
        }
    except Exception as e:
        return {
            "method": method,
            "path": path,
            "description": description,
            "status": "❌ ERROR",
            "response": str(e),
        }


async def check_all_endpoints():
    """Check all expected endpoints"""
    print("=" * 60)
    print("MAYA BACKEND ENDPOINT CHECKER")
    print("=" * 60)
    print(f"\n🔍 Testing backend at: {BACKEND_URL}\n")
    
    results = {
        "timestamp": datetime.now().isoformat(),
        "backend_url": BACKEND_URL,
        "categories": {},
        "summary": {
            "total": 0,
            "live": 0,
            "errors": 0,
            "no_connection": 0,
        }
    }
    
    async with httpx.AsyncClient() as client:
        for category, endpoints in EXPECTED_ENDPOINTS.items():
            print(f"\n📂 {category.upper()}")
            print("-" * 60)
            
            category_results = []
            
            for endpoint, description in endpoints.items():
                method, path = endpoint.split(" ", 1)
                
                # Skip templated paths for now (would need real IDs)
                if "{id}" in path or "{booking_id}" in path:
                    print(f"  ⏭️  {method} {path} - Skipped (needs ID)")
                    continue
                
                result = await check_endpoint(client, method, path, description)
                category_results.append(result)
                
                results["summary"]["total"] += 1
                
                if result["status"] == "✅ LIVE":
                    results["summary"]["live"] += 1
                    print(f"  ✅ {method} {path} - {result.get('status_code', 'N/A')}")
                elif result["status"] == "❌ NO_CONNECTION":
                    results["summary"]["no_connection"] += 1
                    print(f"  ❌ {method} {path} - No connection")
                else:
                    results["summary"]["errors"] += 1
                    print(f"  ⚠️  {method} {path} - {result.get('status_code', 'Error')}")
            
            results["categories"][category] = category_results
    
    # Summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"Total endpoints tested: {results['summary']['total']}")
    print(f"✅ Live: {results['summary']['live']}")
    print(f"⚠️ Errors: {results['summary']['errors']}")
    print(f"❌ No connection: {results['summary']['no_connection']}")
    
    if results['summary']['no_connection'] > 0:
        print("\n⚠️  WARNING: Backend not responding!")
        print("   Make sure your backend is running at:", BACKEND_URL)
        print("   Or update BACKEND_URL in this script if deployed to Railway.")
    
    # Save to file
    output_file = Path(__file__).parent / "BACKEND_ENDPOINT_TEST_RESULTS.json"
    with open(output_file, "w") as f:
        json.dump(results, f, indent=2)
    
    print(f"\n💾 Results saved to: {output_file}")
    
    return results


if __name__ == "__main__":
    print("\n⏳ Starting endpoint tests...\n")
    asyncio.run(check_all_endpoints())
    print("\n✅ Testing complete!\n")
