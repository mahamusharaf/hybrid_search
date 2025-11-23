import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime


class PaperScraper:
    def __init__(self):
        self.base_url = "https://papers.nips.cc"
        self.papers_url = f"{self.base_url}/paper_files/paper/2024"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }

    def scrape(self):

        print(f"Scraping papers from: {self.papers_url}\n")

        try:
            response = requests.get(self.papers_url, headers=self.headers, timeout=30)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, 'html.parser')
            papers = []

            for li in soup.find_all('li'):
                paper = self._parse_paper(li)
                if paper:
                    papers.append(paper)
                    if len(papers) % 50 == 0:
                        print(f"Scraped {len(papers)} papers...")

            print(f"\n✓ Total papers scraped: {len(papers)}")
            return papers

        except Exception as e:
            print(f"✗ Error scraping: {e}")
            return []

    def _parse_paper(self, element):
        try:

            link_tag = element.find('a')
            if not link_tag:
                return None

            title = link_tag.get_text(strip=True)
            if len(title) < 10:
                return None

            link = link_tag.get('href', '')
            if link and not link.startswith('http'):
                link = f"{self.base_url}{link}"

            authors = []
            author_tag = element.find('i')
            if author_tag:
                author_text = author_tag.get_text(strip=True)
                authors = [a.strip() for a in re.split(r'[,;]|\sand\s', author_text)
                           if a.strip()]

            if not authors:
                authors = ['Unknown']

            return {
                'title': title,
                'authors': authors,
                'link': link,
                'year': 2024,
                'conference': 'NeurIPS',
                'scraped_at': datetime.now()
            }

        except:
            return None

