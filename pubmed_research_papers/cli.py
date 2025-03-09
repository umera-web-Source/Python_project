import click
import csv
from pubmed_research_papers.fetch_papers import fetch_pubmed_papers as fetch_papers
from pubmed_research_papers.filter_authors import filter_non_academic_authors

@click.command()
@click.argument("query")
@click.option("-f", "--file", type=str, default="results.csv", help="Output file name")
@click.option("-d", "--debug", is_flag=True, help="Enable debug mode")
def main(query, file, debug):
    """Fetch research papers from PubMed based on QUERY and filter non-academic authors."""
    
    if debug:
        click.echo("Debug mode enabled")

    papers = fetch_papers(query)
    
    if debug:
        click.echo(f"Fetched {len(papers)} papers from PubMed")

    filtered_papers = filter_non_academic_authors(papers)

    if debug:
        click.echo(f"Filtered {len(filtered_papers)} papers with academic authors")

    click.echo(f"Saving results to {file}")
    
    with open(file, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["Title", "Authors", "Journal", "Publication Date"])
        writer.writeheader()
        
        for paper in filtered_papers:
            writer.writerow({
                "Title": paper.get("title", "N/A"),
                "Authors": "; ".join([author["name"] for author in paper.get("authors", [])]),
                "Journal": paper.get("source", "N/A"),
                "Publication Date": paper.get("pubdate", "N/A"),
            })
    
    click.echo("Results saved successfully!")

if __name__ == "__main__":
    main()
