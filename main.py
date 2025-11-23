from scrap import PaperScraper
from database import PaperDatabase
from search import SearchEngine, display_results


def main():
    print("NeurIPS 2024 Paper Search System")

    # Step 1: Scrape papers
    print(" Scraping papers from NeurIPS website...")
    scraper = PaperScraper()
    papers = scraper.scrape()

    if not papers:
        print("No papers found. Exiting...")
        return

    print()

    # Step 2: Store in MongoDB
    print(" Storing papers in MongoDB...")
    db = PaperDatabase()
    db.insert_papers(papers)

    # Show stats
    stats = db.get_stats()
    print(f" Total papers: {stats['total_papers']}")
    print(f" Unique authors: {stats['unique_authors']}")
    print()

    # Step 3: Demo searches
    print(" Running demo searches...")

    search = SearchEngine(db)

    # Search 1: By title
    print("\n Search 1: Papers with 'neural' in title")
    results = search.search_by_title("neural", limit=5)
    display_results(results)

    # Search 2: By keywords
    print("\n Search 2: Papers about 'deep learning'")
    results = search.search_by_keywords("deep learning", limit=5)
    display_results(results)

    # Search 3: By author (get first available author)
    print("\n Search 3: Papers by author")
    authors = search.get_all_authors()
    if authors:
        sample_author = authors[0].split()[0]
        print(f"Searching for: {sample_author}")
        results = search.search_by_author(sample_author, limit=5)
        display_results(results)

    # Search 4: Hybrid search
    print("\n Search 4: Hybrid search - 'reinforcement' + specific author")
    if authors:
        results = search.hybrid_search(
            query="reinforcement",
            author=authors[0].split()[0],
            limit=5
        )
        display_results(results)

    # Close database
    db.close()



if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n Interrupted by user")
    except Exception as e:
        print(f"\n Error: {e}")