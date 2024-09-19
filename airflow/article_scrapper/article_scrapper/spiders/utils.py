from bs4 import BeautifulSoup

def text_cleaner(html_contents):
    # Join the list of HTML content strings into one long string
    combined_html = ''.join(html_contents)
    
    # Parse the combined HTML content
    soup = BeautifulSoup(combined_html, 'html.parser')
    
    # Extract text from the parsed HTML
    text = soup.get_text()
    
    return text