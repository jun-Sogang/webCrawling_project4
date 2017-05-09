import requests
from bs4 import BeautifulSoup

firstUrl = 'http://cspro.sogang.ac.kr/~cse20121611'


urlText = open("URL.txt", "w")



visitedUrl = []
queueAboutUrl = [firstUrl]

def parser(url):

    if len(queueAboutUrl) is 0:
        return
    if '#' in url:
        url = url.split('#')[0]
    if '?' in url:
        url = url.split('?')[0]
    if not 'http' in url:
        url = firstUrl + url
    if url == firstUrl or url == 'http://cspro.sogang.ac.kr/~cse20121611/':
        url = firstUrl + '/index.html'
    print('count : ' + str(len(visitedUrl)))
    print('now url : ' + str(url))
    print('check url : ' + url)
    if url not in visitedUrl:
        r = requests.get(url)
        if r.status_code == 404:
            print(404)
        else :
            soup = BeautifulSoup(r.content, "html.parser")
            results = soup.find_all('a')

            visitedUrl.append(url)
            for element in results:
                if 'http' in element.get('href'):
                    queueAboutUrl.append(element.get('href'))
                else:
                    queueAboutUrl.append(firstUrl + '/' + element.get('href'))
                print('href : ' + element.get('href'))

            fileName = "Output_%04d.txt" %(len(visitedUrl))
            fileOpen = open(fileName, 'w')
            fileOpen.writelines(soup.get_text())
            fileOpen.close()

    queueAboutUrl.pop(0)
    if len(queueAboutUrl) is 0:
        return ;
    else :
        nextUrl = queueAboutUrl[0]
        print('nextUrl : ' + nextUrl)
        parser(nextUrl)

parser(queueAboutUrl[0])
for text in visitedUrl:
    urlText.writelines(text + '\n')
urlText.close()
