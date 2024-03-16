from bs4 import BeautifulSoup
import requests
import re

link = "https://scholar.google.com/scholar?hl=en&as_sdt=0%252C44&q="

replace_dict = {
    " ": "+",
    ",": "%2C",
}

def get_citations(query: str) -> int:
    url = get_query_url(query)
    return fetch_cited_by_link(url)

def fetch_cited_by_link(url: str) -> int:
    response = requests.get(url)
    response.raise_for_status()  
    
    soup = BeautifulSoup(response.text, 'html.parser')
    cited_by_links = soup.find_all('a', string=lambda text: 'Cited by' in text if text else False)
    
    cited_by  = -1
    if cited_by_links:
        text = cited_by_links[0].text
        cited_by = int(re.findall(r'\d+', text)[0])
    
    return cited_by
    
def get_query_url(query: str) -> str:
    for key, value in replace_dict.items():
        query = query.replace(key, value)

    return link + query
    
def main():
    query = input("Enter the query: ")
    
    citations = get_citations(query)
    print("citations: ", citations)
    
if __name__ == "__main__":
    main()