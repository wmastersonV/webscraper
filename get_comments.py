import mechanize
import json
import sys
from bs4 import BeautifulSoup
import pdb

def get_campaign_comments (url):

    br = mechanize.Browser ()
    br.set_handle_robots (False)
    br.set_handle_refresh (False)

    br.addheaders = [
        ('Accept-Language', 'en-US,en;q=0.8'),
        ('Connection', 'keep-alive'),
        ('User-agent','User-Agent:Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36')
    ]

    has_comments = True
    result_set = []

    # Find all comments
    while has_comments:

        pdb.set_trace()

        print 'Fetching : %s' % url
        sys.stdout.flush ()

        response = br.open (url)
        soup = BeautifulSoup(response.read(), 'html.parser')

        comments = soup.findAll ('li', attrs={'class': 'NS_comments__comment'})
        for i in range (0, len (comments)):
            comment = {}

            _author = comments[i].findAll ('a', attrs={'class': 'author'})

            author = ''
            author_url = ''
            if _author[0]:
                author     = _author[0].text
                author_url = 'https://www.kickstarter.com' + _author[0].get('href')

            _comment = comments[i].findAll ('p')

            comment_content = ''
            if _comment[0]:
                comment_content = _comment[0].text

            _date = comments[i].findAll ('data', attrs={'itemprop': 'Comment[created_at]'})

            date = ''
            if _date[0]:
                date = _date[0].get('data-value')

            # Add metadata to dictionary
            comment.update ({'author': author})
            comment.update ({'author_url': author_url})
            comment.update ({'comment': comment_content})
            comment.update ({'date': date})

            # Add dictionary to list
            result_set.append (comment)

        older_comments = soup.findAll ('a', attrs={'class': 'older_comments'})
        if older_comments:
            has_comments = True
            url = older_comments[0].get('href')
            url = 'https://www.kickstarter.com' + url
        else:
            has_comments = False

    return json.dumps (result_set, indent=4, sort_keys=True)

# Sample Campaign URLs to get comments
# url = 'https://www.kickstarter.com/projects/263291121/desktophero-free-3d-printable-character-maker/comments'
#url = 'https://www.kickstarter.com/projects/622508883/open-building-institute-eco-building-toolkit/comments'


import pandas as pd
# csv_f =  pd.DataFrame.from_csv('/home/dallam/Desktop/webScraper/kickstarter/tech3788.csv')
csv_f =  pd.DataFrame.from_csv('/Users/dmaste/Desktop/interviewing/code samples/old/webScraper/predictive model/data/tech3788.csv')

project_url = csv_f[[0]]
for i in range(0,csv_f[[0]].shape[0]):
    url = project_url.iloc[i][0].split("?")[0] + "/comments"
    print url

    # Get json data
    json_data = get_campaign_comments (url)
    # Write json data to file
    f = open ('/home/dallam/Desktop/webScraper/kickstarter/all/' + csv_f[[0]].iloc[i][0].split("?")[0].split("/")[-1] + '_campaign_comments.json', 'w')
    f.write (json_data)
    f.close ()

            
