import requests
from typing import List, Dict

BASE_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
DETAILS_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi"

def fetch_pubmed_papers(query: str, max_results: int = 10) -> List[Dict]:
    """Fetch research papers from PubMed API based on a query."""
    details_params = {
        "db": "pubmed",
        "term": query,
        "retmax": max_results,
        "retmode": "json"
    }

    response = requests.get(BASE_URL, params=details_params)
    response.raise_for_status()
    
    paper_ids = response.json().get("esearchresult", {}).get("idlist", [])
    
    if not paper_ids:
        return []

    details_params = {
        "db": "pubmed",
        "id": ",".join(paper_ids),
        "retmode": "json"
    }
    
    details_response = requests.get(DETAILS_URL, params=details_params)
    details_response.raise_for_status()
    
    papers = details_response.json().get("result", {})

    return [papers[pid] for pid in paper_ids if pid in papers]
