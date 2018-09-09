from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup

def simple_get(url):
    try:
        with closing(get(url, stream=True)) as resp:
            if is_good_response(resp):
                return resp.content
            else:
                return None

    except RequestException as e:
        log_error('Error during requests to {0} : {1}'.format(url, str(e)))
        return None


def is_good_response(resp):
    content_type = resp.headers['Content-Type'].lower()
    return (resp.status_code == 200 
            and content_type is not None 
            and content_type.find('html') > -1)


def log_error(e):
    print(e)

raw_html = simple_get('https://entropymag.org/where-to-submit-september-october-and-november-2018/')
html = BeautifulSoup(raw_html, 'html.parser')

for p in html.select('p strong'):
    print p.parent

''' so we have sections are divided into anchor tags with <h3><b> within them. One word categories.
    everything from there to the next example (or the pdf img for end) is a section of types of
    submissions.

    from there indivisual entries are listed as 
    <p><strong><a href="link for submission">Name of the press</a> </strong>/ (Deadline: Date OR Now OR Year-Round) / Type of submissions looked for / Submission Price</p>

    with variations of course. What we can do is stripe this of price and use it regardless.

    The real fun comes in doing text searched of the accompaning links and maybe providing some text analysis of those pages
    for examples of writing.

    This is a great first step though. Next I will need to seperate the entries into sections (beautiful soup reference/ css selectors)
    if I can just have a list of all entries with the approparte type beside it I will be in a great place to make a dump of the data.