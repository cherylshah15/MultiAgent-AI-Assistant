from ddgs import DDGS

def search_web(query):

    results = []

    try:

        with DDGS() as ddgs:

            news_results = list(
                ddgs.news(
                    query,
                    max_results=5
                )
            )

            print("\nRAW NEWS RESULTS:\n")
            print(news_results)

            for result in news_results:

                results.append(
                    f"""
Title: {result.get('title','')}
Body: {result.get('body','')}
Date: {result.get('date','')}
Source: {result.get('source','')}
"""
                )

    except Exception as e:

        return f"Search Error: {e}"

    return "\n".join(results)