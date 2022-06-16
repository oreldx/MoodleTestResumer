from creds import *
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import codecs


def startBrowser():
    return webdriver.Firefox()


def loginMoodle(driver, page):
    driver.get(page)
    element = driver.find_element(By.XPATH, "/html/body/div[3]/div[2]/div/section/div/"
                                            "div[2]/div/div/div/div[1]/div[1]/a")
    element.click()
    element = driver.find_element(By.XPATH, "//input[@name='username']")
    element.send_keys(LOGIN)
    element = driver.find_element(By.XPATH, "//input[@name='password']")
    element.send_keys(PASS)
    driver.find_element(By.XPATH, "//input[@name='submit']").click()
    time.sleep(20)


def getAnswers(driver, quantityQuestions, outputFile):
    driver.find_element(By.XPATH, "/html/body/div[3]/div[2]/div[2]/div/"
                                  "div/section/div[1]/table/tbody/tr/td[4]/a").click()
    print('Test loaded')
    with codecs.open(outputFile, "w", "utf-8-sig") as f:
        for i in range(quantityQuestions):
            textQuestion = driver.find_element(By.CLASS_NAME, "qtext").text
            textAnswer = driver.find_element(By.CLASS_NAME, "rightanswer").text[26:]

            f.write(f"{textQuestion}\n")
            f.write(f"-> {textAnswer[:]}\n\n")
            print(f"Q n°{i} : {textQuestion}\n -> {textAnswer}")

            if i != 0:
                driver.find_element(By.XPATH, "/html/body/div[3]/div[2]/div[2]/div/div/section/div[1]/div/a[2]").click()
            else:
                driver.find_element(By.XPATH, "/html/body/div[3]/div[2]/div[2]/div/div/section/div[1]/div/a").click()

            time.sleep(1)


def scrapTests(tests):
    browser = startBrowser()
    print('Selenium Instance has been started')
    loginMoodle(browser, tests[0]['url'])
    for i, test in enumerate(tests):
        print(f"========== Scrapping Moodle Test {i} started ==========")
        browser.get(test['url'])
        getAnswers(browser, test['questions'], f"test_{i}.txt")
        print(f"========== Scrapping Moodle Test {i} done ==========")


if __name__ == '__main__':

    data = [
        {'url': "https://moodle.utt.fr/mod/quiz/view.php?id=67186", 'questions': 90},
        {'url': "https://moodle.utt.fr/mod/quiz/view.php?id=67187", 'questions': 90}
    ]

    scrapTests(data)
