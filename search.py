import re

class SearchEngine:


    def __init__(self, database):
        self.db = database
        self.collection = database.collection

    def search_by_title(self, query, limit=10):
        pattern = re.compile(query, re.IGNORECASE)
        results = self.collection.find(
            {"title": {"$regex": pattern}}
        ).limit(limit)

        return list(results)

    def search_by_author(self, author_name, limit=10):
        pattern = re.compile(author_name, re.IGNORECASE)
        results = self.collection.find(
            {"authors": {"$regex": pattern}}
        ).limit(limit)

        return list(results)

    def search_by_keywords(self, keywords, limit=10):
        results = self.collection.find(
            {"$text": {"$search": keywords}},
            {"score": {"$meta": "textScore"}}
        ).sort([("score", {"$meta": "textScore"})]).limit(limit)

        return list(results)

    def hybrid_search(self, query=None, author=None, limit=10):
        filters = {}

        # Add text search
        if query:
            filters["$text"] = {"$search": query}

        # Add author filter
        if author:
            pattern = re.compile(author, re.IGNORECASE)
            filters["authors"] = {"$regex": pattern}

        # Execute search
        if filters:
            if "$text" in filters:
                results = self.collection.find(
                    filters,
                    {"score": {"$meta": "textScore"}}
                ).sort([("score", {"$meta": "textScore"})]).limit(limit)
            else:
                results = self.collection.find(filters).limit(limit)
        else:
            results = self.collection.find().limit(limit)

        return list(results)

    def get_all_authors(self):
        authors = self.collection.distinct("authors")
        return sorted([a for a in authors if a != 'Unknown'])


def display_results(results, max_show=5):
    if not results:
        print("\n No results found\n")
        return

    print(f"\n{'=' * 80}")
    print(f"Found {len(results)} results (showing {min(len(results), max_show)}):")
    print(f"{'=' * 80}\n")

    for i, paper in enumerate(results[:max_show], 1):
        print(f"{i}. {paper['title']}")
        authors = ', '.join(paper['authors'][:3])
        if len(paper['authors']) > 3:
            authors += f" ... (+{len(paper['authors']) - 3} more)"
        print(f"   Authors: {authors}")
        print(f"   Link: {paper['link']}")
        print()


