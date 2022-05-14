from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
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

def algorithm_news_title(soup):
    try:
        news_title = soup.find(class_="detail__title").get_text(strip=True)
    except:
        try:
            news_title = soup.h1.get_text()
        except:
            news_title = None
            print("Error: No such news title element")
    return news_title

def algorithm_news_date(soup):
    try:
        news_date  = soup.find(class_="detail__date").get_text()
    except:
        try:
            news_date = soup.find(class_="date").get_text()
        except:
            news_date = None
            print("Error: No such news date element")
    return news_date

def first_algorithm_news_body(soup):
    news_raw   = soup.find(class_="detail__body-text itp_bodycontent")
    news_body_raw = [body.get_text() for body in news_raw.find_all("p")]
    news_body_head  = soup.strong.get_text()
    news_body_bottom  = "\n".join(news_body_raw)
    news_body = news_body_head + " - " + news_body_bottom
    # if theres some add in bottom
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
    return news_body

def second_algorithm_news_body(soup):
    news_raw = soup.find(class_="itp_bodycontent detail_text group")
    news_body_raw = [body.get_text() for body in news_raw.find_all("p")]
    news_body_head = soup.strong.get_text()
    news_body_bottom = "\n".join(news_body_raw)
    news_body = news_body_head + " - " + news_body_bottom
    # if theres some add in bottom
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
    return news_body

def third_algorithm_news_body(soup):
    news_raw = soup.find(id="detikdetailtext")
    news_body_raw = [body.get_text() for body in news_raw.find_all("p")]
    try:
        news_body_head = news_raw.b.get_text()
    except:
        news_body_head = news_raw.strong.get_text()
    news_body_bottom = "\n".join(news_body_raw)
    news_body = news_body_head + " - " + news_body_bottom
    # if theres some add in bottom
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
    return news_body

def forth_algorithm_news_body(soup):
    news_body_head = soup.find("p").get_text()
    news_body_bottom = soup.find("figcaption").get_text()
    news_body = news_body_head + " " +news_body_bottom
    return news_body

def fifth_algorithm_news_body(soup):
    news_body = soup.find("p").get_text()
    return news_body

def first_algorithm_news_body_second(soup_second, news_body):
    news_raw   = soup_second.find(class_="detail__body-text itp_bodycontent")
    news_body_raw = [body.get_text() for body in news_raw.find_all("p")]
    news_body_second  = "\n".join(news_body_raw)
    news_body = news_body + "\n" + "Halaman 2" +"\n" + news_body_second
    return news_body

def second_algorithm_news_body_second(soup_second, news_body):
    news_raw   = soup_second.find(id="detikdetailtext")
    news_body_raw = [body.get_text() for body in news_raw.find_all("p")]
    news_body_second  = "\n".join(news_body_raw)
    news_body = news_body + "\n" + "Halaman 2" +"\n" + news_body_second
    return news_body

def get_news_use_bs(links, numbers):
    news = []
    for link in links:
        response = requests.get(link).content
        time.sleep(1)
        soup = bs(response, "html.parser")
        # for news more than one page
        try:
            lanjutan = soup.find("a", attrs={"dtr-evt":"selanjutnya"}).get_text(strip=True)
            print(f"Berita ada {lanjutan}")
            news_title = algorithm_news_title(soup=soup)
            news_date = algorithm_news_date(soup=soup)
            # body 1
            try:
                news_body = first_algorithm_news_body(soup=soup)
            except:
                try:
                    news_body = second_algorithm_news_body(soup=soup)
                except:
                    try:
                        news_body = third_algorithm_news_body(soup=soup)
                    except:
                        news_body = None
                        print("Error: No such news body element")
            # body 2
            try:
                link_second = soup.find("a", attrs={"dtr-evt":"selanjutnya"}).get("href")
                response_second = requests.get(link_second).content
                soup_second = bs(response_second, "html.parser")
                try:
                    news_body = first_algorithm_news_body_second(soup_second=soup_second, news_body=news_body)
                except:
                    print("Error: No such second news body element")
            except:
                print("Error: Cannot get second page link")
                
        except:
            # algorithm 2 to get second news
            try:
                lanjutan = soup.find(class_="ap-view").get_text()
                print(f"Berita ada {lanjutan}: Use Second Algorithm")

                news_title = algorithm_news_title(soup=soup)
                news_date = algorithm_news_date(soup=soup)
                # body 1
                try:
                    news_body = first_algorithm_news_body(soup=soup)
                except:
                    try:
                        news_body = second_algorithm_news_body(soup=soup)
                    except:
                        try:
                            news_body = third_algorithm_news_body(soup=soup)
                        except:
                            news_body = None
                            print("Error: No such news body element")
                # body 2
                try:
                    link_second = soup.find("a", class_="ap-view").get("href")
                    response_second = requests.get(link_second).content
                    soup_second = bs(response_second, "html.parser")
                    try:
                        news_body = second_algorithm_news_body_second(soup_second=soup_second, news_body=news_body)
                    except:
                        print("Error: No such second news body element")
                except:
                    print("Error: Cannot get second page link")

            except:
                # for news that just one page
                news_title = algorithm_news_title(soup=soup)
                news_date = algorithm_news_date(soup=soup)
                try:
                    news_body = first_algorithm_news_body(soup=soup)
                except:
                    try:
                        news_body = second_algorithm_news_body(soup=soup)
                    except:
                        try:
                            news_body = third_algorithm_news_body(soup=soup)
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
        soup = bs(response, "html.parser")
        # for news more than one page
        try:
            lanjutan = soup.find(class_="btn btn--red-base btn--sm mgb-24").get_text(strip=True)
            print(f"Berita ada {lanjutan}")
            news_title = algorithm_news_title(soup=soup)
            news_date = algorithm_news_date(soup=soup)
            # body 1
            try:
                news_body = first_algorithm_news_body(soup=soup)
            except:
                try:
                    news_body = second_algorithm_news_body(soup=soup)
                except:
                    try:
                        news_body = third_algorithm_news_body(soup=soup)
                    except:
                        news_body = None
                        print("Error: No such news body element")
            # body 2
            try:
                link_second = soup.find(class_="btn btn--red-base btn--sm mgb-24").get("href")
                response_second = requests.get(link_second).content
                soup_second = bs(response_second, "html.parser")
                try:
                    news_body = first_algorithm_news_body_second(soup_second=soup_second, news_body=news_body)
                except:
                    print("Error: No such second news body element")
            except:
                print("Error: Cannot get second page link")
            
        except:
            # algorithm 2 to get second news
            try:
                lanjutan = soup.find(class_="ap-view").get_text()
                print(f"Berita ada {lanjutan}: Use Second Algorithm")

                news_title = algorithm_news_title(soup=soup)
                news_date = algorithm_news_date(soup=soup)
                # body 1
                try:
                    news_body = first_algorithm_news_body(soup=soup)
                except:
                    try:
                        news_body = second_algorithm_news_body(soup=soup)
                    except:
                        try:
                            news_body = third_algorithm_news_body(soup=soup)
                        except:
                            news_body = None
                            print("Error: No such news body element")
                # body 2
                try:
                    link_second = soup.find("a", class_="ap-view").get("href")
                    response_second = requests.get(link_second).content
                    soup_second = bs(response_second, "html.parser")
                    try:
                        news_body = second_algorithm_news_body_second(soup_second=soup_second, news_body=news_body)
                    except:
                        print("Error: No such second news body element")
                except:
                    print("Error: Cannot get second page link")
            
            except:
                # for news that just one page
                news_title = algorithm_news_title(soup=soup)
                news_date = algorithm_news_date(soup=soup)
                try:
                    news_body = first_algorithm_news_body(soup=soup)
                except:
                    try:
                        news_body = second_algorithm_news_body(soup=soup)
                    except:
                        try:
                            news_body = third_algorithm_news_body(soup=soup)
                        except:
                            try:
                                news_body = forth_algorithm_news_body(soup=soup)
                            except:
                                try:
                                    news_body = fifth_algorithm_news_body(soup=soup)
                                except:
                                    news_body = None
                                    print("Error: No such news body element")

        news.append({"judul":news_title, "tanggal":news_date, "isi":news_body})
        numbers += 1
        print(f"News: {numbers}\n{news_title}\n")
    return news, numbers

def news_use_keyword():
    keyword = input("Looking For? ")
    end_page = int(input("Search Until Page: "))
    number = 0
    all_news = []

    driver = webdriver.Edge()
    driver.get("https://www.detik.com")

    search_box = driver.find_element(By.NAME, "query")
    search_box.send_keys(keyword)
    search_box.send_keys(Keys.RETURN)

    time.sleep(1)
    links = get_link_use_selenium(driver=driver)
    clean_links = [link for link in links if link[:4] == "http"]
    news, number = get_news_use_bs(links=clean_links, numbers=number)
    all_news.extend(news)

    if end_page > 1:
        for page in range(2, end_page+1):
            driver.find_element(By.LINK_TEXT, str(page)).click()
            time.sleep(1)
            links = get_link_use_selenium(driver=driver)
            clean_links = [link for link in links if link[:4] == "http"]
            news, number = get_news_use_bs(links=clean_links, numbers=number)
            all_news.extend(news)
    else:
        pass

    print("Done")
    driver.quit()

    return all_news

def news_use_keyword_include_photo():
    keyword = input("Looking For? ")
    end_page = int(input("Search Until Page: "))
    number = 0
    all_news = []

    driver = webdriver.Edge()
    driver.get("https://www.detik.com")

    search_box = driver.find_element(By.NAME, "query")
    search_box.send_keys(keyword)
    search_box.send_keys(Keys.RETURN)

    time.sleep(1)
    links = get_link_use_selenium(driver=driver)
    clean_links = [link for link in links if link[:4] == "http"]
    news, number = get_news_and_photo_using_bs(links=clean_links, numbers=number)
    all_news.extend(news)

    if end_page > 1:
        for page in range(2, end_page+1):
            driver.find_element(By.LINK_TEXT, str(page)).click()
            time.sleep(1)
            links = get_link_use_selenium(driver=driver)
            clean_links = [link for link in links if link[:4] == "http"]
            news, number = get_news_and_photo_using_bs(links=clean_links, numbers=number)
            all_news.extend(news)
    else:
        pass

    print("Done")
    driver.quit()
    return all_news
    
def news_use_tag():
    tag_name = input("Insert Tag: ")
    end_page = int(input("Search Until Page: "))
    numbers = 0
    all_news = []
    link = "https://www.detik.com/tag/" + tag_name.replace(" ", "-")

    driver = webdriver.Edge()
    driver.get(link)

    time.sleep(1)
    links = get_link_use_selenium(driver=driver)
    clean_links = [link for link in links if link[:4] == "http"]
    news, numbers = get_news_use_bs(links=clean_links, numbers=numbers)
    all_news.extend(news)

    if end_page > 1:
        for page in range(2, end_page+1):
            driver.find_element(By.LINK_TEXT, str(page)).click()
            time.sleep(1)
            links = get_link_use_selenium(driver=driver)
            clean_links = [link for link in links if link[:4] == "http"]
            news, numbers = get_news_use_bs(links=clean_links, numbers=numbers)
            all_news.extend(news)
    else:
        pass

    print("Done")
    driver.quit()
    return all_news

def news_use_tag_include_photo():
    tag_name = input("Insert Tag: ")
    end_page = int(input("Search Until Page: "))
    numbers = 0
    all_news = []
    link = "https://www.detik.com/tag/" + tag_name.replace(" ", "-")

    driver = webdriver.Edge()
    driver.get(link)

    time.sleep(1)
    links = get_link_use_selenium(driver=driver)
    clean_links = [link for link in links if link[:4] == "http"]
    news, numbers = get_news_and_photo_using_bs(links=clean_links, numbers=numbers)
    all_news.extend(news)

    if end_page > 1:
        for page in range(2, end_page+1):
            driver.find_element(By.LINK_TEXT, str(page)).click()
            time.sleep(1)
            links = get_link_use_selenium(driver=driver)
            clean_links = [link for link in links if link[:4] == "http"]
            news, numbers = get_news_and_photo_using_bs(links=clean_links, numbers=numbers)
            all_news.extend(news)
    else:
        pass

    print("Done")
    driver.quit()
    return all_news