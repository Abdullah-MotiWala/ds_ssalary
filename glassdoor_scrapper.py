from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import sys


import time
import pandas as pd


def get_jobs(keyword, num_jobs, verbose, path, slp_time):
    '''Gathers jobs as a dataframe, scraped from Glassdoor'''

    # Initializing the webdriver
    # options = webdriver.ChromeOptions()

    # Uncomment the line below if you'd like to scrape without a new Chrome window every time.
    # options.add_argument('headless')

    # Change the path to where chromedriver is in your home folder.
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.set_window_size(1120, 1000)

    url = 'https://www.glassdoor.com/Job/jobs.htm?sc.keyword="' + keyword + \
        '"&locT=C&locId=1147401&locKeyword=San%20Francisco,%20CA&jobType=all&fromAge=-1&minSalary=0&includeNoSalaryJobs=true&radius=100&cityId=-1&minRating=0.0&industryId=-1&sgocId=-1&seniorityType=all&companyId=-1&employerSizes=0&applicationType=0&remoteWorkType=0'
    driver.get(url)
    jobs = []

    # If true, should be still looking for new jobs.
    while len(jobs) < num_jobs:

        # Let the page load. Change this number based on your internet speed.
        # Or, wait until the webpage is loaded, instead of hardcoding it.
        time.sleep(slp_time)

        # Test for the "Sign Up" prompt and get rid of it.
        try:
            # driver.find_element_by_class_name("selected").click()
            # driver.find_element(By.CLASS_NAME("selected")).click()
            print(" x worked out")
        except ElementClickInterceptedException:
            print(" x out failed")
            pass

        time.sleep(.1)

        try:
            # driver.find_element(By.CLASS_NAME("react-job-listing")).Click()  #clicking to the X.
            driver.find_element(by=By.CSS_SELECTOR,
                                value='[alt="Close"]').click()
        except NoSuchElementException:
            pass

        # Going through each job in this page
        # jl for Job Listing. These are the buttons we're going to click.
        job_buttons = driver.find_elements(
            by=By.CLASS_NAME, value="react-job-listing")
        # for job_button in job_buttons:
        for x in range(len(job_buttons)):

            job_button = job_buttons[x]
            reloadBtn = False
            print("Progress: {}".format(
                "" + str(len(jobs)) + "/" + str(num_jobs)))
            if len(jobs) >= num_jobs:
                break

            job_button.click()  # You might
            time.sleep(5)
            collected_successfully = False

            # reloading button if comes so handle it this way
            # try:

            # except NoSuchElementException:
            #     print("not still")

            if (len(jobs) == 0):
                try:
                    signUpBtn = driver.find_element(
                    by=By.XPATH, value='.//span[@class="SVGInline modal_closeIcon"]')
                    signUpBtn.click()
                    time.sleep(.5)
                    job_button.click()  # You might
                    time.sleep(1)
                    collected_successfully = False
                except NoSuchElementException:
                    pass

            while not collected_successfully:
                try:
                    company_name = driver.find_element(
                        by=By.XPATH, value='.//div[contains(@class,"e1tk4kwz5")]').text
                    # splitted_company_name = company_name.split(" ").pop()
                    # company_name.join(" ")

                    location = driver.find_element(
                        by=By.XPATH, value='.//div[contains(@class,"e1tk4kwz1")]').text
                    job_title = driver.find_element(
                        by=By.XPATH, value='.//div[contains(@class, "e1tk4kwz2")]').text
                    # job_description = driver.find_element(by=By.XPath,value='.//div[@class="jobDescriptionContent desc"]').text
                    collected_successfully = True
                except:
                    time.sleep(5)
                    print("issue come")
                    reloadBtn = True
                    collected_successfully = True


            if (reloadBtn):
                print("outer")
                continue
            try:
                salary_estimate = driver.find_element(
                    by=By.XPATH, value='.//div[contains(@class,"e2u4hf18")]').text
            except NoSuchElementException:
                salary_estimate = -1  # You need to set a "not found value. It's important."

            try:
                rating = driver.find_element(
                    by=By.XPATH, value='.//span[contains(@class,"e1tk4kwz4")]').text
            except NoSuchElementException:
                rating = -1  # You need to set a "not found value. It's important."

            # Printing for debugging
            if verbose:
                print("Job Title: {}".format(job_title))
                print("Salary Estimate: {}".format(salary_estimate))
                # print("Job Description: {}".format(job_description[:500]))
                print("Rating: {}".format(rating))
                print("Company Name: {}".format(company_name))
                print("Location: {}".format(location))

            # Going to the Company tab...
            # clicking on this:
            # <div class="tab" data-tab-type="overview"><span>Company</span></div>
            # try:
            #     driver.find_element(by=By.XPATH,value='.//div[@class="tab" and @data-tab-type="overview"]').click()

            # try:
            #     #<div class="infoEntity">
            #     #    <label>Headquarters</label>
            #     #    <span class="value">San Francisco, CA</span>
            #     #</div>
            #     headquarters = driver.find_element(by=By.XPATH,value='.//div[@class="infoEntity"]//label[text()="Headquarters"]//following-sibling::*').text
            # except NoSuchElementException:
            #     headquarters = -1

            try:
                size = driver.find_element(
                    by=By.XPATH, value='//*[@id="EmpBasicInfo"]/div[1]/div/div[1]/span[2]').text
            except NoSuchElementException:
                size = -1

            try:
                founded = driver.find_element(
                    by=By.XPATH, value='//*[@id="EmpBasicInfo"]/div[1]/div/div[2]/span[2]').text
            except NoSuchElementException:
                founded = -1

            try:
                type_of_ownership = driver.find_element(
                    by=By.XPATH, value='.//*[@id="EmpBasicInfo"]/div[1]/div/div[3]/span[2]').text
            except NoSuchElementException:
                type_of_ownership = -1

            try:
                industry = driver.find_element(
                    by=By.XPATH, value='//*[@id="EmpBasicInfo"]/div[1]/div/div[4]/span[2]').text
            except NoSuchElementException:
                industry = -1

            try:
                sector = driver.find_element(
                    by=By.XPATH, value='//*[@id="EmpBasicInfo"]/div[1]/div/div[5]/span[2]').text
            except NoSuchElementException:
                sector = -1

            try:
                revenue = driver.find_element(
                    by=By.XPATH, value='//*[@id="EmpBasicInfo"]/div[1]/div/div[6]/span[2]').text
            except NoSuchElementException:
                revenue = -1

            # try:
            #     competitors = driver.find_element(by=By.XPATH,value='.//div[@class="infoEntity"]//label[text()="Competitors"]//following-sibling::*').text
            # except NoSuchElementException:
            #     competitors = -1

            # except NoSuchElementException:  #Rarely, some job postings do not have the "Company" tab.
            #     headquarters = -1
            #     size = -1
            #     founded = -1
            #     type_of_ownership = -1
            #     industry = -1
            #     sector = -1
            #     revenue = -1
            #     competitors = -1

            if verbose:
                print("Size: {}".format(size))
                print("Founded: {}".format(founded))
                print("Type of Ownership: {}".format(type_of_ownership))
                print("Industry: {}".format(industry))
                print("Sector: {}".format(sector))
                print("Revenue: {}".format(revenue))
                print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")

            jobs.append({"Job Title": job_title,
                         "Salary Estimate": salary_estimate,
                         "Rating": rating,
                         "Company Name": company_name,
                         "Location": location,
                         "Size": size,
                         "Founded": founded,
                         "Type of ownership": type_of_ownership,
                         "Industry": industry,
                         "Sector": sector,
                         "Revenue": revenue, })
            time.sleep(1)
            # add job to jobs

        # Clicking on the "next page" button
        try:
            driver.find_element(by=By.XPATH,value='//*[@id="MainCol"]/div[2]/div/div[1]/button[7]').click()
        except NoSuchElementException:
            print("Scraping terminated before reaching target number of jobs. Needed {}, got {}.".format(num_jobs, len(jobs)))
            break

    # This line converts the dictionary object into a pandas DataFrame.
    return pd.DataFrame(jobs)
