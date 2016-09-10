#pip install bs4
#pip install mechanize
#pip install xlsxwriter

import mechanize
import xlsxwriter
import time
from bs4 import BeautifulSoup



# Code Configuration
# set selection to 'all' if all categories
# set page_limit to -1 if all pages

selection = 'Technology'
page_limit = 5


# Select a category
category = {
    'Art': '1',
    'Comics': '3',
    'Crafts': '26',
    'Dance': '6',
    'Design': '7',
    'Fashion': '9',
    'Film': '11',
    'Food': '10',
    'Games': '12',
    'Journalism': '13',
    'Music': '14',
    'Photography': '15',
    'Publishing': '18',
    'Technology': '16',
    'Theater': '17'
}


# Create an new Excel file and add a worksheet.
filename = 'kickstarter-%s.xlsx' % selection
workbook = xlsxwriter.Workbook(filename)
worksheet = workbook.add_worksheet()
bold = workbook.add_format({'bold': True})
worksheet.set_column('A:A', 15)
worksheet.set_column('B:C', 70)
worksheet.write ('A1', 'Category', bold)
worksheet.write ('B1', 'URL', bold)
worksheet.write ('C1', 'Name', bold)

br = mechanize.Browser ()

br.set_handle_robots (False)
br.set_handle_refresh (False)

if selection != 'all':
    cid = category[selection]

page = 1
writer_row = 1

cookies = ''
while True:
    br.addheaders = [
        ('Accept-Language', 'en-US,en;q=0.8'),
        ('Connection', 'keep-alive'),
        ('Cookies', cookies),
        ('User-agent','User-Agent:Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36')
    ]

    if selection != 'all':
        url = 'https://www.kickstarter.com/discover/advanced?state=successful&category_id=%s&sort=popularity&seed=2439956&page=%d' % (cid, page)
    else:
        url = 'https://www.kickstarter.com/discover/advanced?state=successful&sort=popularity&seed=2439956&page=%d' % page

    print 'Fetching : %s' % url
    response = br.open (url)

    if cookies == "":
        cookiejar = br._ua_handlers['_cookies'].cookiejar
        cookies = str(cookiejar).split(" ")[1]

    time.sleep (5)

    # No more projects found
    if response.code == 404:
        break

    soup = BeautifulSoup(response.read(), 'html.parser')

    # Find all projects
    project_list = soup.findAll ('ul', attrs={'id': 'projects_list'})
    projects = project_list[0].findAll ('div', attrs={'class': 'project-card-content'})

    # Scrape project data
    for project in projects:
        link = project.find ('a')
        url = 'https://www.kickstarter.com' + link['href']
        name = link.contents[0]

        worksheet.write (writer_row, 0, selection)
        worksheet.write (writer_row, 1, url)
        worksheet.write (writer_row, 2, name)
        writer_row += 1

    # Next page
    page += 1

    if page == page_limit:
        break

workbook.close ()
print 'Done generating ' + filename
