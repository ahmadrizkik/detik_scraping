from selenium.webdriver.common.by import By
import requests
from bs4 import BeautifulSoup as bs
import time

def get_link_use_selenium(driver):
    """
    Will also get for photo news link
    """
    try:
        get_news = driver.find_element(By.CLASS_NAME, "list.media_rows.list-berita")
        get_news = get_news.find_elements(By.TAG_NAME, "article")
        links = []
        for link in get_news:
            link = link.find_element(By.TAG_NAME, "a")
            links.append(link.get_attribute("href"))
    except:
        print("Error: No Such Link Box Element")
    return links

def get_link_use_bs(link):
    """
    Only get for news link, not photo or 20detiknews
    """
    try:
        response = requests.get(link).content
        soup = bs(response)
        news_body_list = soup.find(class_="list media_rows list-berita")
        links = []
        for news_link in news_body_list.find_all("a"):
            links.append(news_link.get("href"))
    except:
        print("Error: No Such Link Box Element")
    return links

def get_news_use_bs(links, numbers):
    news = []
    for link in links:
        response = requests.get(link).content
        time.sleep(1)
        soup = bs(response)

        # title
        try:
            news_title = soup.find(class_="detail__title").get_text(strip=True)
        except:
            print("Use second algorithm to get news title")            
            try:
                news_title = soup.h1.get_text()
            except:
                news_title = None
                print("Error: No such news title element")

        # date
        try:
            news_date  = soup.find(class_="detail__date").get_text()
        except:
            print("Use second algorithm to get news date")            
            try:
                news_date = soup.find(class_="date").get_text()
            except:
                news_date = None
                print("Error: No such news date element")

        # body
        try:
            news_raw   = soup.find(class_="detail__body-text itp_bodycontent")
            news_body_raw = [body.get_text() for body in news_raw.find_all("p")]
            news_body_head  = soup.strong.get_text()
            news_body_bottom  = "\n".join(news_body_raw)
            news_body = news_body_head + " - " + news_body_bottom
            try:
                news_body_add_1 = news_raw.find("h2").get_text()
                news_body = news_body + "\n" + news_body_add_1
                try:
                    news_body_add_2 = [body.get_text() for body in news_raw.find("ul")]
                    news_body_add_2  = "\n".join(news_body_add_2)
                    news_body = news_body + "\n" + news_body_add_2
                except:
                    pass
            except:
                pass
            if news_body == " - ":
                news_body = None
            else:
                pass
        except:
            print("Use second algorithm to get news body")  
            try:
                news_raw = soup.find(class_="itp_bodycontent detail_text group")
                news_body_raw = [body.get_text() for body in news_raw.find_all("p")]
                news_body_head = soup.strong.get_text()
                news_body_bottom = "\n".join(news_body_raw)
                news_body = news_body_head + " - " + news_body_bottom
            except:
                try:
                    print("Use third algorithm to get news body")
                    news_raw = soup.find(id="detikdetailtext")
                    news_body_raw = [body.get_text() for body in news_raw.find_all("p")]
                    try:
                        news_body_head = news_raw.b.get_text()
                    except:
                        news_body_head = news_raw.strong.get_text()
                    news_body_bottom = "\n".join(news_body_raw)
                    news_body = news_body_head + " - " + news_body_bottom
                except:
                    news_body = None
                    print("Error: No such news body element")
            
        news.append({"judul":news_title, "tanggal":news_date, "isi":news_body})
        numbers += 1
        print(f"News: {numbers}\n{news_title}\n")
        
    return news, numbers

def get_news_and_photo_using_bs(links, numbers):
    news = []
    for link in links:
        response = requests.get(link).content
        time.sleep(1)
        soup = bs(response)
        try:
            lanjutan = soup.find(attrs= {"dtr-evt": "selanjutnya"}).get_text(strip=True)
            print(f"Berita ada {lanjutan}")
            # title
            try:
                news_title = soup.find(class_="detail__title").get_text(strip=True)
            except:
                news_title = None
                print("Error: No such news title element")
            # date
            try:
                news_date  = soup.find(class_="detail__date").get_text()
            except:
                news_date = None
                print("Error: No such news date element")
            # body
            try:
                news_raw   = soup.find(class_="detail__body-text itp_bodycontent")
                news_body_raw = [body.get_text() for body in news_raw.find_all("p")]
                news_body_head  = soup.strong.get_text()
                news_body_bottom  = "\n".join(news_body_raw)
                news_body = news_body_head + " - " + news_body_bottom
                try:
                    news_body_add_1 = news_raw.find("h2").get_text()
                    news_body = news_body + "\n" + news_body_add_1
                    try:
                        news_body_add_2 = [body.get_text() for body in news_raw.find("ul")]
                        news_body_add_2  = "\n".join(news_body_add_2)
                        news_body = news_body + "\n" + news_body_add_2
                    except:
                        pass
                except:
                    pass
            except:
                news_body = None
                print("Error: No such news body element")
            # body 2
            try:
                link_second = soup.find("a", attrs={"dtr-evt":"selanjutnya"}).get("href")
                response_second = requests.get(link_second).content
                soup_second = bs(response_second)
            except:
                print("Error: Cannot open second page")

            try:
                news_raw   = soup_second.find(class_="detail__body-text itp_bodycontent")
                news_body_raw = [body.get_text() for body in news_raw.find_all("p")]
                news_body_second  = "\n".join(news_body_raw)
                news_body = news_body + "\n" + "Halaman 2" +"\n" + news_body_second
            except:
                print("Error: No such second news body element")
            
        except:
            # title
            try:
                news_title = soup.find(class_="detail__title").get_text(strip=True)
            except:
                print("Use second algorithm to get news title")            
                try:
                    news_title = soup.h1.get_text()
                except:
                    news_title = None
                    print("Error: No such news title element")
            # date
            try:
                news_date  = soup.find(class_="detail__date").get_text()
            except:
                print("Use second algorithm to get news date")            
                try:
                    news_date = soup.find(class_="date").get_text()
                except:
                    news_date = None
                    print("Error: No such news date element")
            # body
            try:
                news_raw   = soup.find(class_="detail__body-text itp_bodycontent")
                news_body_raw = [body.get_text() for body in news_raw.find_all("p")]
                news_body_head  = soup.strong.get_text()
                news_body_bottom  = "\n".join(news_body_raw)
                news_body = news_body_head + " - " + news_body_bottom
                try:
                    news_body_add_1 = news_raw.find("h2").get_text()
                    news_body = news_body + "\n" + news_body_add_1
                    try:
                        news_body_add_2 = [body.get_text() for body in news_raw.find("ul")]
                        news_body_add_2  = "\n".join(news_body_add_2)
                        news_body = news_body + "\n" + news_body_add_2
                    except:
                        pass
                except:
                    pass
                if news_body == " - ":
                    news_body = None
                else:
                    pass
            except:
                print("Use second algorithm to get news body")  
                try:
                    news_raw = soup.find(class_="itp_bodycontent detail_text group")
                    news_body_raw = [body.get_text() for body in news_raw.find_all("p")]
                    news_body_head = soup.strong.get_text()
                    news_body_bottom = "\n".join(news_body_raw)
                    news_body = news_body_head + " - " + news_body_bottom
                except:
                    print("Use third algorithm to get news body")
                    try:
                        news_raw = soup.find(id="detikdetailtext")
                        news_body_raw = [body.get_text() for body in news_raw.find_all("p")]
                        try:
                            news_body_head = news_raw.b.get_text()
                        except:
                            news_body_head = news_raw.strong.get_text()
                        news_body_bottom = "\n".join(news_body_raw)
                        news_body = news_body_head + " - " + news_body_bottom
                    except:
                        print("Use Forth algorithm to get news body")
                        try:
                            news_body_head = soup.find("p").get_text()
                            news_body_bottom = soup.find("figcaption").get_text()
                            news_body = news_body_head + " " +news_body_bottom
                        except:
                            print("Use Fifth algorithm to get news body")
                            try:
                                news_body = soup.find("p").get_text()
                            except:
                                news_body = None
                                print("Error: No such news body element")

        news.append({"judul":news_title, "tanggal":news_date, "isi":news_body})
        numbers += 1
        print(f"News: {numbers}\n{news_title}\n")
    return news, numbers