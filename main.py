from bs4 import BeautifulSoup
import requests
import pandas as pd
from tabulate import tabulate

bad_chars = [';', ':', '!', "*", "[", "]", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]

url = 'https://en.wikipedia.org/wiki/List_of_the_largest_software_companies'

response = requests.get(url)

soup = BeautifulSoup(response.text, 'html.parser')

table = soup.find('table', class_ ='wikitable sortable plainrowheads')

table_titles = table.find_all('th')

titles = [title.text.strip() for title in table_titles]

df = pd.DataFrame(columns = titles)

column_data = table.find_all('tr')

for row in column_data[1:]:
    row_data = row.find_all('td')
    individual_data = [data.text.strip() for data in row_data]
    # Remove unwanted characters in Organization column
    updated_organization = ''.join(i for i in individual_data[1] if not i in bad_chars)
    del  individual_data[1]
    individual_data.insert(1, updated_organization)
    # Remove unwanted characters in Headquarters column
    updated_headquarters = ''.join(i for i in individual_data[5] if not i in bad_chars)
    del  individual_data[5]
    individual_data.insert(5, updated_headquarters)
    # Add the modified row data to the dataframe
    length = len(df)
    df.loc[length] = individual_data

#View dataframe in tabulation
print(tabulate(df, headers='keys', tablefmt='psql'))
#Save dataframe to csv file
# df.to_csv(r'<PATH>.csv', index=False)