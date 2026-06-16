from ddgs import DDGS

with DDGS() as ddgs:
    results = list(
        ddgs.news(
            "latest sports news",
            max_results=5
        )
    )

print(results)