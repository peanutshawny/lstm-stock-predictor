import requests
from bs4 import BeautifulSoup

# gets the latest GDP
def getGDP():
    page = requests.get("https://www.bea.gov/data/gdp/gross-domestic-product")
    soup = BeautifulSoup(page.content, 'html.parser')
    gdpValue = soup.find_all(class_='field field--name-field-value field--type-string field--label-hidden field--item')[
        0].get_text()
    gdpValue = gdpValue.replace("%", "")
    return (float(gdpValue))

# gets the latest fund rate
def getFund_Rate():
    page = requests.get("https://www.bankrate.com/rates/interest-rates/federal-funds-rate.aspx")
    soup = BeautifulSoup(page.content, 'html.parser')
    fundValue = soup.find_all('tbody')
    fundValue = str(fundValue[0])
    fundValue = fundValue.split("<td>")
    fundValue = fundValue[2].replace("</td>", "")
    return (float(fundValue))

# gets the latest unemployment numbers
def getUmemployment():
    page = requests.get("https://fred.stlouisfed.org/series/UNRATE")
    soup = BeautifulSoup(page.content, 'html.parser')
    uRate = soup.find_all(class_='series-meta-observation-value')[0].get_text()
    return (float(uRate))


print("Current GDP: " + str(getGDP()))
print("Current Fund Rate: " + str(getFund_Rate()))
print("Current Unemployement Rate: " + str(getUmemployement()))
