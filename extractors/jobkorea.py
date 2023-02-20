from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

browser = webdriver.Chrome()

def get_page_count(keyword):
  base_url="https://www.jobkorea.co.kr/Search/?stext="
  browser.get(f"{base_url}{keyword}")
  
  soup = BeautifulSoup(browser.page_source, "html.parser")
  pagination=soup.find('div', class_="lists-cnt dev_list")
  pagination_list=pagination.find('div', class_="tplPagination")
  pages=pagination_list.select('ul li')
  count=len(pages)
  if count==10:
      return 10
  else:
      return count


def extract_jobkorea_jobs(keyword):
    pages=get_page_count(keyword)
    print("Found",pages,"pages")
    results=[]
    for page in range(pages):
        base_url="https://www.jobkorea.co.kr/Search/?stext="
        final_url=f"{base_url}{keyword}&tabType=recruit&Page_No={page}"
        print("Requesting", final_url)
        browser.get(final_url)

        soup = BeautifulSoup(browser.page_source, "html.parser")
        list_default = soup.find('div', class_="list-default")
        jobs=list_default.find_all('li',class_="list-post")

        for job in jobs:
            position=job.find("a", class_="title dev_view")["title"]
            company=job.find("a", class_="name dev_view")["title"]
            location=job.find("span",  class_="loc long")
            link=job.find("a", class_="name dev_view")["href"]
            job_data = {
                    'company': company.replace(",", " "),
                    'location': location.string.replace(",", " "),
                    'position': position.replace(",", " "),
                    'link': f"https://kr.indeed.com{link}",
                }
            results.append(job_data)            
    return results