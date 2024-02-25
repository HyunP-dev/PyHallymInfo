import requests
from bs4 import BeautifulSoup
from datetime import date
from dataclasses import dataclass


@dataclass
class Notice:
    id: int
    title: str
    author: str
    written_at: date
    views: int
    url: str
    
def get_notices(page: int) -> list[Notice]:
    url = f"https://www.hallym.ac.kr/hallym_univ/sub05/cP3/sCP1?pageIndex={page}"
    bs = BeautifulSoup(requests.get(url).text, "html5lib")
    items = bs.select("#container > div > div:nth-child(5) > div.tbl-press > div > ul > li")
    notices = []
    for item in items:
        cols = [col for col in item.select("span.col > span:not(.screen_out)")]
        notice = Notice(id = int(cols[0].text.strip()), 
                        title = cols[1].text.strip(), 
                        author = cols[2].text.strip(), 
                        written_at = date.fromisoformat(cols[-2].text.strip()),
                        views = int(cols[-1].text.strip()),
                        url = cols[1].select_one("a")["href"])
        notices.append(notice)
    return notices
        