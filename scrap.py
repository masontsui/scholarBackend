
import requests #
from scholar import ScholarJournal, ScholarConference
import find 

def create_scholar(url, _orcid = None):
    web = requests.get(url)
    page = web.text
    page_exist = find.page_exist(page)
    print("request finished")
    if page_exist:
        paper_type = find.get_page_type(page) 
        title = find.get_paper_title(page) 
        pages = find.get_substring_from_tag(page, "Pages")
        public_status = find.get_substring_from_tag(page, "Publication status")
        doi = find.get_substring_from_tag(page, "DOI")
        scholar_list = find.get_scholar_list(page)
        orcid = None
        if _orcid:
            orcid = find.get_orcid(_orcid)
        if paper_type == "Conference":
            print(scholar_list)
            period = find.get_substring_from_tag(page, "Period")
            scholar = ScholarConference(title, scholar_list, pages, public_status, period, url, doi)
        elif paper_type == "Journal":
            print(scholar_list)
            online_status = find.get_substring_from_tag(page, "Online published")
            if online_status:
                online_status = online_status.replace(' - ', '')
                print(online_status)
            scholar = ScholarJournal(title, scholar_list, pages, public_status, online_status, url, doi, orcid)
        return scholar.to_json()
    else:
        return {"status": 404, "error": "Page not found"}

def create_orcid(_orcid):
    orcid = find.get_orcid(_orcid)
    if orcid:
        return {"status": 200, "data": orcid}
    else:
        return {"status": 404, "error": "Page not found"}