import csv
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

if __name__ == '__main__':
    opts = Options()
    opts.set_headless()
    assert opts.headless
    url = "https://www.prokabaddi.com/stats/49-96-total-points-scored-statistics"
    browser = webdriver.Firefox(executable_path='/home/akumargs/Software/geckodriver', options=opts)
    browser.get(url)
    html = browser.page_source

    time.sleep(1)

    selections = browser.find_element_by_id('si_dropdown').find_elements_by_xpath(".//*")
    teams = {}

    with open('teams.csv', 'w', newline='') as csvfile:
        fieldnames = ['Team', 'Games', 'TOTAL POINTS SCORED', 'TOTAL POINTS CONCEDED', 'AVG POINTS SCORED', 'SUCCESSFUL RAIDS', 'RAID POINTS', 'AVG RAID POINTS', 'SUCCESSFUL TACKLES', 'TACKLE POINTS', 'AVG TACKLE POINTS', 'SUPER RAID', 'SUPER TACKLES', 'DO-OR-DIE RAID POINTS', 'ALL-OUTS INFLICTED', 'ALL-OUTS CONCEDED']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for(i,selection) in enumerate(selections):
            selection.click()
            WebDriverWait(browser, 10).until(
                EC.presence_of_element_located((By.XPATH, ('//span[@class="btn btn-load-more"]'))))
            browser.find_element_by_class_name('btn-load-more').click()
            teams_div = browser.find_elements_by_class_name('wl-team-detail')
            for (j,team) in enumerate(teams_div):
                strs = team.text.split('\n')
                team = strs[1]
                point = strs[2].split(' ')
                if not teams.get(team):
                    teams[team] = {"Team":team, "Games": point[0], selection.text: point[1]}
                else:
                    teams[team].update({selection.text: point[1]})
        for(row) in teams.values():
            writer.writerow(row)
    browser.close()


