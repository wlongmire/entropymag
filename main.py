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

def selectParent(element, selector):
    while element != None and element.name != selector:
        element = element.parent
    
    return element

raw_html = simple_get('https://entropymag.org/where-to-submit-september-october-and-november-2018/')
html = BeautifulSoup(raw_html, 'html.parser')

content = html.select_one('h3 b')


section = content.findNext(href="#top")

moreSections = True
while (moreSections):
    print 'SectionType: ', section.findNext().string.encode('utf-8').replace(':', '')
    
    section = section.findNext()
    nextSection = True

    while nextSection:
        entity = selectParent(section, 'p')
        
        if (entity != None):
            try:
                #detecting the end of the a section
                if entity.a.attrs['href'] == "#top" or entity == None:
                    nextSection = False
            except KeyError:
                pass
            
            print 'Entry: ', entity
        
        if section == None:
            moreSections = False
        elif nextSection:
            section = section.findNext('a')

# so we have sections are divided into anchor tags with <h3><b> within them. One word categories.
# everything from there to the next example (or the pdf img for end) is a section of types of
# submissions.

# from there indivisual entries are listed as 

# with variations of course. What we can do is stripe this of price and use it regardless.

# The real fun comes in doing text searched of the accompaning links and maybe providing some text analysis of those pages
# for examples of writing.

# This is a great first step though. Next I will need to seperate the entries into sections (beautiful soup reference/ css selectors)
# if I can just have a list of all entries with the approparte type beside it I will be in a great place to make a dump of the data.
