import re
import requests

def get_substring_from_tag(page, target):
    text = page
    CLASS = re.compile(f'{target}.*?\/td>')

    c = re.findall(CLASS, text)
    c = [re.sub(target, '', m) for m in c]
    c = [re.sub("<.*?>", "", m) for m in c]

    if c:
        print(c)
        return c[0]
    else:
        print("nothing is found")
        return None

def get_page_type(page):
    text = page
    CLASS = re.compile(r'type_classification_parent.*?<\/')

    c = re.search(CLASS, text).group()
    if "Conference Papers" in c:
        print("this is a conference paper")
        return "Conference"
    elif "Journal" in c: 
        print("this is a journal")
        return "Journal"
    else:
        print("Unknown paper type")
        return None

def get_paper_title(page):
    text = page
    CLASS = re.compile(r'class="title".*?<\/')

    c = re.search(CLASS, text).group()
    c = c.replace("class=\"title\">", "")
    c = c.replace("</", "")

    if c:
        print(c)
        return c
    else:
        print("nothing found")
        return None

def get_scholar_list(page):
    text = page

    UNLESS = re.compile(r'And [0-9] others')
    LIST = r'class="relations persons">.*?<\/ul>'
    SCHOLARA = r'<li.*?>.*?<\/li>'
    UNLIST = re.compile(r'associates_authors_full_list">.*?<\/ul>')
    SCHOLARB = r'<li class="external">.*?<\/li>'
    a ,b = ([] for i in range(2))

    list_range = re.search(LIST, text).group()
    a = re.findall(SCHOLARA, list_range)
    a = [re.sub('<.*?>', '', m) for m in a]
    a_filtered = [m for m in a if not UNLESS.match(m)] 

    target = re.search(UNLIST, text)
    if target:
        unlist_range = target.group()
        b = re.findall(SCHOLARB, unlist_range)
        b = [re.sub('<.*?>', '', m) for m in b]
    else:
        print("no unlist is founded")
    print(a_filtered + b)

    return a_filtered + b

def page_exist(page):
    if "The page could not be found" in page:
        return False
    else:
        return True

def get_orcid(orcid):
    res = requests.get(f"https://orcid.org/{orcid}/public-record.json")

    if res.headers['Content-Type'] != 'text/html':
        if(res.status_code == 200):
            page = res.json()
            return (page["displayName"])
        else:
            return False


#get_substring_from_tag("https://scholars.cityu.edu.hk/en/publications/toward-secure-image-denoising(c6a30240-0cd1-4707-be95-e169cecd3c28).html", "DOI")
#get_page_type("https://scholars.cityu.edu.hk/en/publications/toward-secure-image-denoising(c6a30240-0cd1-4707-be95-e169cecd3c28).html")
#get_page_type("https://scholars.cityu.edu.hk/en/publications/soundid(d5d68b5b-5288-407e-bff4-666bb176dcd4).html")
#get_paper_title("https://scholars.cityu.edu.hk/en/publications/enhancing-cryptocurrency-blocklisting(8c5faa1d-7d37-45cf-ac02-11c21094a543).html")
#get_scholar_list("https://scholars.cityu.edu.hk/en/publications/soundid(d5d68b5b-5288-407e-bff4-666bb176dcd4).html")
#print(get_orcid("0000-0003-0547-315X"))