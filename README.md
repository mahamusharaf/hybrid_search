# NeurIPS 2024 Paper Search System

A simple **hybrid search system** for NeurIPS 2024 conference papers using Python and MongoDB.

This project can:

* Scrape all **NeurIPS 2024 papers** (title, authors, links)
* Store structured paper data in **MongoDB**
* Run **search queries** on titles, authors, and keywords
* Demonstrate hybrid search (exact + full-text)

---

##  Features

### 1. Web Scraper (Beautiful Soup)

* Extracts paper title
* Extracts author list
* Extracts paper link
* Stores all results in JSON format and MongoDB

### 2. MongoDB Storage

* Saved into a collection named `papers2024`
* Schema:

  ```json
  {
    "title": "Paper Title",
    "authors": ["Author 1", "Author 2"],
    "link": "https://nips.cc/.../"
  }
  ```

### 3. Search Engine

Supports:

* Search by title
* Search by author name
* Keyword search


