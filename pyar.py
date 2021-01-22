import requests
import bs4
import re
import time

#Create a BeautifulSoup object from url
def get_soup(url):
    while(True):
        try:
            request = requests.get(url, verify=False) #disable ssl verification, this will show a warning but still work
            soup = bs4.BeautifulSoup(request.text, 'html.parser')
            break
        except:
            print('Connection refused by the server...')
            time.sleep(5)
            print('Trying again...')
            continue
    return soup

#Get the link of every job offer
def get_offers():
    jobs_links = []
    #i choose navigate until the page 10
    pages = [str(i) for i in range(1,10)]
    for page in pages:
        body = get_soup('http://www.python.org.ar/trabajo/' + '?page=' + page).body
        for h4 in body.findAll('h4'):
            url = h4.a
            if (re.match(r'/trabajo/', url.get('href'))):
                jobs_links.append('https://www.python.org.ar' + url.get('href'))
    return jobs_links

#Search the email from every contact link
def main():
    #Save the list on a txt file
    f = open("emails.txt", "w")
    emails_list = []
    unrepeated_list = []
    links = get_offers()
    for l in links:
        bs = get_soup(l)
        email = bs.find('dt', text = 'Email de contacto ').findNext("dd").string        
        emails_list.append(email + '\n')
    #Cleaning repeated emails
    unrepeated_list = set(emails_list)
    for e in unrepeated_list:
        f.write(e)
    f.close()

if __name__ == '__main__':
    main()
