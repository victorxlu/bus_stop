import urllib.parse

def build_url(url):
    """
    Constructs a complete URL based on the environment (local or Netlify server).

    Args:
        url (str): The complete URL to process.

    Returns:
        str: The constructed URL.
    """
    # Check if the URL is for localhost or 127.0.0.1
    if "localhost" in url or "127.0.0.1" in url:
        # Directly return the URL for localhost
        return url
    
    # Check if the URL is for a Netlify server
    if "netlify" in url:
        # Encode the URL and return it through the proxy service
        return f'https://busetaproxy.victorxlu.workers.dev/?url={urllib.parse.quote(url)}'
    
    # For other environments, return the original URL
    return url