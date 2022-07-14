from os import path
import csv
from datetime import datetime
from colorama import Fore, init
from selenium import webdriver
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

class Job:
    # Constructor
    def __init__(self):
        init(autoreset=True)
        self.createLog("-----------------------------------------------------------------------------")
        self.createLog("Started")

        self.options = webdriver.ChromeOptions()
        self.options.add_experimental_option('excludeSwitches', ['enable-logging', 'enable-automation'])
        now = datetime.now()
        self.time = "[" + str(now.day) + "-" + str(now.month) + "-" + str(now.year) + " " + str(now.hour) + ":" + str(now.minute) + ":" + str(now.second) + "]"
        print(Fore.CYAN + self.time)
        
        if path.exists(path.dirname(__file__) + "\job.log"):
            print("log file created...")
        else:
            try:
                self.log = open(self.logfile, "x")
                print("job.log" + " created...")
            except Exception as e:
                print("job.log" + " created... [" + str(e.strerror) + "]")
        
        self.links = []
        self.titles = []
        self.company = []
        self.location = []
        self.experience = []
        self.salary = []



    # function to create all logs
    def createLog(self, msg:str):
        now = datetime.now()
        self.time = "[" + str(now.day) + "-" + str(now.month) + "-" + str(now.year) + " " + str(now.hour) + ":" + str(now.minute) + ":" + str(now.second) + "]"
        log = open("job.log", "a")
        log.write( "[*] " + msg + "\t" + self.time + "\n")
        log.close()


    # function to create webdriver
    def createDriver(self):
        self.browser = webdriver.Chrome(service = Service(path.dirname(__file__) + '\chromedriver.exe'), options=self.options)
        self.createLog("driver created")
        self.browser.maximize_window()
        self.browser.implicitly_wait(30)

    # function to crawl naukri.com
    def crawl(self):
        self.browser.get("https://naukri.com/")
        self.createLog("url fetched")
        print(Fore.CYAN + "[+] Title: " + self.browser.title)
        self.createLog("Working on: " + self.browser.title)
    

    # function to search jobs
    def searchJobs(self, keywords="python", loc="delhi"):
        print(Fore.CYAN + "searching jobs...")
        search = self.browser.find_element(By.XPATH, '//*[contains(concat( " ", @class, " " ), concat( " ", "keywordSugg", " " ))]//*[contains(concat( " ", @class, " " ), concat( " ", "suggestor-input", " " ))]')
        search.send_keys(keywords)
        self.createLog("Keywords sent: " + keywords)
        location = self.browser.find_element(By.XPATH, '//*[contains(concat( " ", @class, " " ), concat( " ", "locationSugg", " " ))]//*[contains(concat( " ", @class, " " ), concat( " ", "suggestor-input", " " ))]')
        location.send_keys(loc)
        self.createLog("location sent: " + loc)

        btn = self.browser.find_element(By.XPATH, '//*[contains(concat( " ", @class, " " ), concat( " ", "qsbSubmit", " " ))]').click()
        self.createLog("searching...")


    # function to collect data from web site
    def fetchData(self):
        try:
            print(Fore.CYAN + "Collecting data...")
            self.createLog("Collecting data...")
            self.titles = self.browser.find_elements(By.XPATH, '//*[contains(concat( " ", @class, " " ), concat( " ", "info", " " ))]//*[contains(concat( " ", @class, " " ), concat( " ", "fw500", " " ))]')
            self.links = self.browser.find_elements(By.XPATH, '//*[contains(concat( " ", @class, " " ), concat( " ", "mb-8", " " ))]/a')
            self.company = self.browser.find_elements(By.XPATH, '//*[contains(concat( " ", @class, " " ), concat( " ", "subTitle", " " ))]')
            self.location = self.browser.find_elements(By.XPATH, '//*[contains(concat( " ", @class, " " ), concat( " ", "location", " " ))]//*[contains(concat( " ", @class, " " ), concat( " ", "fs12", " " ))]')
            self.experience = self.browser.find_elements(By.XPATH, '//*[contains(concat( " ", @class, " " ), concat( " ", "experience", " " ))]//*[contains(concat( " ", @class, " " ), concat( " ", "fs12", " " ))]')
            self.salary = self.browser.find_elements(By.XPATH, '//*[contains(concat( " ", @class, " " ), concat( " ", "salary", " " ))]//*[contains(concat( " ", @class, " " ), concat( " ", "fs12", " " ))]')
            
            print(Fore.CYAN + "[*] length of titles     : " + str(len(self.titles)))
            print(Fore.CYAN + "[*] length of company    : " + str(len(self.company)))
            print(Fore.CYAN + "[*] length of location   : " + str(len(self.location)))
            print(Fore.CYAN + "[*] length of Experience : " + str(len(self.experience)))
            print(Fore.CYAN + "[*] length of Salary     : " + str(len(self.salary)))

            length = min(len(self.titles), len(self.company), len(self.location), len(self.experience), len(self.salary))
            self.save(length, self.titles, self.company, self.location, self.experience, self.salary)
            
        except Exception as e:
            self.createLog("error: " + str(e))
            print(Fore.LIGHTRED_EX + "Error: " + str(e))
            self.createLog("Quitting...")
            self.closeDriver()


    # function to save collected data in file
    def save(self,length, title, company, location, experience, salary):
        self.createLog("Saving collected data...")
        try:
            with open("job.csv", "x") as file:
                print(Fore.GREEN + "[+] " + "job.csv created successfully...")
        
        except FileExistsError as err:
            print(Fore.RED + "[+]" + "File already exist...")
            print(Fore.YELLOW + "[+] Opening in append mode...")

        finally:
            with open("job.csv", "a") as file:
                print(Fore.GREEN + "[+] file opened...")
                write = csv.writer(file)
                
                for i in range(length):
                    row = [i+1,title[i].text, company[i].text, location[i].text, experience[i].text, salary[i].text, title[i].get_attribute("href")]
                    write.writerow(row)
            print("[+] Operation Successfull")
            self.createLog("File saved...")                
            file.close()
            print(Fore.GREEN + "[+] File Closed")


    # function to follow next page
    def nextPage(self):
        ans = input("Follow next page ?(Y/y or n/N): ")
        if ans in ["y", "Y"]:
            self.createLog("searching for next page...")
            print(Fore.CYAN + "getting next page...")
            self.browser.find_element(By.XPATH, '//*+[contains(concat( " ", @class, " " ), concat( " ", "selected", " " ))]//a').click()
        else:
            pass

    # function to close the driver
    def closeDriver(self):
        print("Exiting...")
        self.browser.close()
        self.createLog("driver closed")
        print("Bye...")


    # main function 
    def main(self):
        self.createLog("Starting operation...")
        self.createDriver()
        self.crawl()
        self.searchJobs("bcom graduate", "delhi, faridabad")
        self.fetchData()
        # self.nextPage()
        self.closeDriver()


if __name__ == "__main__":
    job = Job()
    job.main()
    