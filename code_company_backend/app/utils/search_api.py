import requests
from datetime import datetime, timedelta
from config import Config
from supabase import create_client

# Initialize Supabase (safe even if empty)
supabase = create_client(Config.SUPABASE_URL, Config.SUPABASE_KEY)
CACHE_TTL = 300  # 5 minutes


# 🔹 Retrieve cached search results from Supabase
def _get_cached_result(query, provider):
    """Check Supabase cache before making a new search request."""
    try:
        now = datetime.utcnow().isoformat()
        response = supabase.table("search_cache") \
            .select("results, expiry") \
            .eq("query", query) \
            .eq("provider", provider) \
            .execute()

        if response.data:
            item = response.data[0]
            expiry = item.get("expiry")
            if expiry and expiry > now:
                return item["results"]
    except Exception as e:
        print(f"⚠️ Cache fetch error: {e}")
    return None


# 🔹 Save search results to Supabase cache
def _set_cached_result(query, provider, results):
    """Save result to Supabase cache."""
    try:
        expiry = (datetime.utcnow() + timedelta(seconds=CACHE_TTL)).isoformat()
        supabase.table("search_cache").insert({
            "query": query,
            "provider": provider,
            "results": results,
            "expiry": expiry
        }).execute()
    except Exception as e:
        print(f"⚠️ Cache save error: {e}")


# 🔹 Main Search Function
def search(query: str, provider: str = None):
    """Search function with Supabase caching and Serper.dev fallback."""
    provider = provider or Config.SEARCH_MODE

    # Step 1: Check Supabase cache
    cached = _get_cached_result(query, provider)
    if cached:
        print("✅ Using cached results")
        return cached

    results = []

    # Step 2: Perform actual search
    if provider == "mock":
        results = [{"title": f"Mock result for '{query}'", "snippet": "Demo snippet", "url": "#"}]
    else:
        try:
            api_url = Config.SEARCH_API_URL or "https://google.serper.dev/search"
            api_key = Config.SEARCH_API_KEY or Config.SERPER_API_KEY

            headers = {
                "X-API-KEY": api_key,
                "Content-Type": "application/json"
            }
            payload = {"q": query, "gl": "in", "hl": "en", "num": 10}

            response = requests.post(api_url, headers=headers, json=payload, timeout=Config.SEARCH_TIMEOUT)
            response.raise_for_status()
            data = response.json()

            # Safe parsing
            for item in data.get("organic", []):
                title = item.get("title", "Untitled Result")
                snippet = item.get("snippet", "No description available.")
                link = item.get("link") or item.get("url") or "#"
                results.append({
                    "title": title,
                    "snippet": snippet,
                    "url": link
                })

        except Exception as e:
            print(f"⚠️ Serper.dev API error: {e}")
            results = [{"title": "Error fetching results", "snippet": str(e), "url": "#"}]

    # Step 3: Save to Supabase cache
    _set_cached_result(query, provider, results)
    return results


# 🔹 Compatibility Wrapper
def search_project(query: str):
    """Wrapper around `search()` for Technical Manager compatibility."""
    return search(query)
