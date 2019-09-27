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
    url = "https://www.prokabaddi.com/stats/49-21-successful-raids-statistics"
    browser = webdriver.Firefox(executable_path='/home/akumargs/Software/geckodriver')
    browser.get(url)
    html = browser.page_source

    time.sleep(1)

    selections = browser.find_element_by_id('si_dropdown').find_elements_by_xpath(".//*")
    players = {}

    with open('players.csv', 'w', newline='') as csvfile:
        fieldnames = ['Player', 'Team', 'Type', 'Location', 'Games', 'TOTAL POINTS', 'SUCCESSFUL RAIDS', 'RAID POINTS', 'SUCCESSFUL TACKLES', 'TACKLE POINTS', 'AVG RAID POINTS', 'AVG TACKLE POINTS', 'DO-OR-DIE RAID POINTS', 'SUPER RAIDS', 'SUPER TACKLES', 'SUPER 10S', 'HIGH 5S']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for(i,selection) in enumerate(selections):
            selection.click()
            WebDriverWait(browser, 10).until(
                EC.presence_of_element_located((By.XPATH, ('//span[@class="btn btn-load-more"]'))))
            loadmore = browser.find_elements_by_xpath('//*[@id="load_more"]/span')
            try:
                while (len(loadmore) > 0):
                    loadmore[0].click()
                    WebDriverWait(browser, 10).until(
                        EC.presence_of_element_located((By.XPATH, ('//span[@class="btn btn-load-more"]'))))
                    loadmore = browser.find_elements_by_xpath('//*[@id="load_more"]/span')
            except:
                pass

            players_div = browser.find_elements_by_class_name('wl-team-detail')
            for (j,player) in enumerate(players_div):
                team_name_split = player.find_element_by_xpath('.//a[contains(@href, "teams")]').get_attribute('href').split('/')[4].split('-')
                team_name_split = team_name_split[:len(team_name_split)-2]
                team = ' '.join(team_name_split).title()
                strs = player.text.split('\n')
                playerName = strs[1]
                typeList = strs[2].split(',')
                type = typeList[0]
                location = ''
                if len(typeList) > 1:
                    location = typeList[1]
                point = strs[3].split(' ')
                if not players.get(playerName):
                    players[playerName] = {"Player":playerName, "Team":team, "Type":type, "Location":location, "Games": point[0], selection.text: point[1]}
                else:
                    players[playerName].update({selection.text: point[1]})
        for(row) in players.values():
            writer.writerow(row)
    browser.close()


