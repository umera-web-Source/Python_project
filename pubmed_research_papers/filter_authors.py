import re
from typing import List, Dict
from email_validator import validate_email, EmailNotValidError

NON_ACADEMIC_KEYWORDS = ["pharma", "biotech", "corporation", "inc", "ltd", "company", "corp"]

def is_non_academic_email(email: str) -> bool:
    """Check if an email belongs to a non-academic institution."""
    try:
        email_info = validate_email(email, check_deliverability=False)
        domain = email_info.domain.lower()
        return any(keyword in domain for keyword in NON_ACADEMIC_KEYWORDS)
    except EmailNotValidError:
        return False

def filter_non_academic_authors(papers: List[Dict]) -> List[Dict]:
    """Filter out papers where all authors are from pharmaceutical/biotech companies."""
    filtered_papers = []

    for paper in papers:
        if not isinstance(paper, dict):
            print(f"Skipping invalid entry: {paper}")  
            continue

        authors = paper.get("authors", [])
        if not isinstance(authors, list):
            continue  

        valid_authors = []
        
        for author in authors:
            if not isinstance(author, dict):
                continue  

            affiliation = author.get("affiliation", "").lower()
            email = author.get("email", "")

 
            if any(keyword in affiliation for keyword in NON_ACADEMIC_KEYWORDS) or is_non_academic_email(email):
                continue  
            
            valid_authors.append(author)  

        if valid_authors:  
            paper["authors"] = valid_authors
            filtered_papers.append(paper)

    return filtered_papers
