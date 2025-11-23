from pymongo import MongoClient, ASCENDING, TEXT

class PaperDatabase:

    def __init__(self, connection_string="mongodb://localhost:27017/"):
        self.client = MongoClient(connection_string)
        self.db = self.client['neurips_papers']
        self.collection = self.db['papers_2024']
        self._create_indexes()

    def _create_indexes(self):
        try:
            self.collection.create_index([
                ("title", TEXT),
                ("authors", TEXT)
            ])
            self.collection.create_index([("title", ASCENDING)])
            self.collection.create_index([("authors", ASCENDING)])

            print("✓ Database indexes created")
        except:
            pass

    def insert_papers(self, papers):
        if not papers:
            print("No papers to insert")
            return 0

        self.collection.delete_many({})

        result = self.collection.insert_many(papers)
        count = len(result.inserted_ids)

        print(f"✓ Inserted {count} papers into MongoDB")
        return count

    def get_all_papers(self):
        return list(self.collection.find())

    def count_papers(self):
        return self.collection.count_documents({})

    def get_stats(self):
        total = self.count_papers()
        unique_authors = len(self.collection.distinct("authors"))

        return {
            'total_papers': total,
            'unique_authors': unique_authors
        }

    def close(self):
        self.client.close()

