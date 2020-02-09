import requests
import csv
import time
import credentials
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import applicant as applicants

uni_dict = {
    168: 'University of Southern California;Computer Science',
    588: 'New York University;Computer Science',
    135: 'Northeastern University;Computer Science'
}

login_url = "https://yocket.in/account/login"
login_payload = {
    "email": credentials.get_email(),
    "password": credentials.get_password()
}
proxies = {
    "http": 'http://94.21.118.140:61379',
    "https": 'https://185.189.199.75:23500'
}


def extract_session_cookie():
    print("Waiting for session cookie extraction.....")
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(options=options)
    driver.get(login_url)
    driver.find_element_by_xpath("""/html/body/div[4]/div/div/div/div[1]/div/div[2]/form/div[2]/input""") \
        .send_keys(login_payload.get("email"))
    driver.find_element_by_xpath("""/html/body/div[4]/div/div/div/div[1]/div/div[2]/form/div[3]/button""").click()
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((
            By.XPATH, """/html/body/div[4]/div/div/div/div[1]/div/div[2]/form/div[2]/div[2]/input"""))
    )
    driver.find_element_by_xpath("""/html/body/div[4]/div/div/div/div[1]/div/div[2]/form/div[2]/div[2]/input""") \
        .send_keys(login_payload.get("password"))
    driver.find_element_by_xpath("""/html/body/div[4]/div/div/div/div[1]/div/div[2]/form/div[3]/button""").click()
    time.sleep(10)
    result = driver.execute_script("""
                return document.cookie.split(";")[8];
            """)
    print(result)
    return result


def login_with_credentials(yocket_session):
    session = requests.session()
    session.cookies['yocket_session'] = credentials.get_yocket_session()
    session.post(login_url, data=login_payload, headers=dict(referer=login_url))
    print("Logged in with email: " + login_payload.get("email"))
    return session


def scrape_results(session, input):
    print('scraping results...')
    base_url = "https://yocket.in/applications-admits-rejects/"
    uni_name = uni_dict.get(input).split(";")[0]
    course = uni_dict.get(input).split(";")[1]
    file_name = uni_name + ".csv"
    writer = csv.writer(open("datasets/"+file_name, 'w', newline=''))

    # iterating for admits
    i = 1
    admits_url = base_url + str(input) + "-null/" + "2?page="
    while True:
        response = session.get(admits_url + str(i))
        out_to_html(response.content)
        soup = BeautifulSoup(response.content, 'html.parser')
        elements_in_page = soup.find_all("div", class_="col-sm-6")[2:]
        if len(elements_in_page) == 0:
            print("Reached last page in admits...")
            break
        for element in elements_in_page:
            result = extract_applicant_details(element, uni_name, course, "ADMIT")
            writer.writerow(result.split(","))
        print("Page " + str(i) + " in admits is done!")
        i += 1

    # iterating for rejects
    i = 1
    rejects_url = base_url + str(input) + "-null/" + "3?page="
    while True:
        response = session.get(admits_url + str(i))
        out_to_html(response.content)
        soup = BeautifulSoup(response.content, 'html.parser')
        elements_in_page = soup.find_all("div", class_="col-sm-6")[2:]
        if len(elements_in_page) == 0:
            print("Reached last page in rejects...")
            break
        for element in elements_in_page:
            result = extract_applicant_details(element, uni_name, course, "REJECT")
            writer.writerow(result.split(","))
        print("Page " + str(i) + " in rejects is done!")
        i += 1
    print("Scraping completed")

def extract_applicant_details(element, uni_name, course, status):
    applicant = applicants.Applicant()
    other_details = element.find_all("div", class_="col-sm-3")
    undergrad_details = other_details.__getitem__(3).get_text().split("\n").__getitem__(2).split(" ")
    applicant.__setattr__("name", element.find_all("a").__getitem__(0).get_text().strip())
    applicant.__setattr__("profile_link", element.find_all("a").__getitem__(0).get("href").strip())
    applicant.__setattr__("uni_name", uni_name)
    applicant.__setattr__("course_name", course)
    applicant.__setattr__("period", element.find_all("small").__getitem__(0).get_text().split("\n")[1:][1])
    applicant.__setattr__("gre", other_details.__getitem__(1).get_text().split("\n").__getitem__(2).strip())
    applicant.__setattr__("eng_test", other_details.__getitem__(2).get_text().split("\n").__getitem__(1).strip())
    applicant.__setattr__("eng_test_marks", other_details.__getitem__(2).get_text().split("\n").__getitem__(2).strip())
    applicant.__setattr__("undergrad_college", "")
    applicant.__setattr__("undergrad_marks", undergrad_details.__getitem__(0).strip())
    applicant.__setattr__("scoring", undergrad_details.__getitem__(1).strip())
    applicant.__setattr__("experience", other_details.__getitem__(4).get_text().split("\n").__getitem__(2).strip())
    applicant.__setattr__("status", status)
    return str(applicant)


def out_to_html(response):
    f = open("html.html", "w")
    f.write(str(response))


def main():
    print(uni_dict)
    # result = extract_session_cookie()
    session = login_with_credentials("str(result)")
    scrape_results(session, 588)


if __name__ == '__main__':
    main()
