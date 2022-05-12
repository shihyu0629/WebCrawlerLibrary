import requests
from bs4 import BeautifulSoup
import re
import urllib
import math
allbookdata = []

def getbooknamedata(bookname,allbooklocation):

    #print(urllib.parse.quote(bookname))
    
    urlstr  = 'https://book.tpml.edu.tw/webpac/booksearch.do?searchtype=simplesearch&execodeHidden=true&execode=&authoriz=1&search_field=TI&search_input='
    urlstr += urllib.parse.quote(bookname)
    urlstr += '&showtuple=50&resid=189035216&nowpage=1'
    
    r = requests.get(urlstr)
    #print(r.status_code)
    f = open("htmlpage.html", "w",encoding = 'utf-8')
    f.write(r.text)
    f.close()
    soup = BeautifulSoup(r.text,'html.parser')
    #print(soup.prettify())
    
    alldatacount = soup.find(id='totalpage')
    print(alldatacount.text)
    
    totalpage=int(alldatacount.text)/50
    print(math.ceil(totalpage))
    
    for ele in range(1,math.ceil(totalpage)+1):
        urlstr  = 'https://book.tpml.edu.tw/webpac/booksearch.do?searchtype=simplesearch&execodeHidden=true&execode=&authoriz=1&search_field=TI&search_input='
        urlstr += urllib.parse.quote(bookname)
        urlstr += ('&showtuple=50&resid=189035216&nowpage='+str(ele))
    
        print(urlstr)
    
        r = requests.get(urlstr)
    
        soup = BeautifulSoup(r.text,'html.parser')
    
        tables = soup.findChildren('table')
        #print(len(tables))
        my_table = tables[1]
        #print(my_table)
        trs = my_table.find_all('tr')[1:]
        rows = list()
        for tr in trs:
            rows.append([td for td in tr.find_all('td')])
    
        for ele in rows:
            #print('--------length----------')
            #print(len(ele))
            #print('------------------------')
    
            templist = list()
    
            if len(ele)==2:
                list1 = list()
                for ele0 in ele[0].contents:
                    list1.append(str(ele0).replace('\n','').replace('\t','').replace(' ','').replace('\r',''))
                #print(list1)
                templist.append(list1[4])
                res = re.findall("\"(\d+)",list1[1])
                templist.append(res[0])
                #print(res)
                list2 = list()
                for ele1 in ele[1].contents:
                    list2.append(str(ele1).replace('\n','').replace('\t','').replace(' ','').replace('\r',''))
                #print(list2)
                res1 = re.findall("(?<=\">)(.+)<\/a>",list2[1])
                #print(res1)
                templist.append(res1[0])
                templist.append(list2[2])
                templist.append(list2[4])
                templist.append(list2[6])
                #print(allbooklocation)
                templist.append(allbooklocation[res[0]])
                allbookdata.append(templist)
            
    return allbookdata

def getbooklocation(bookname):
    #print(urllib.parse.quote(bookname))
    
    urlstr  = 'https://book.tpml.edu.tw/webpac/booksearch.do?searchtype=simplesearch&execodeHidden=true&execode=&authoriz=1&search_field=TI&search_input='
    urlstr += urllib.parse.quote(bookname)
    urlstr += '&showtuple=50&resid=189035216&nowpage=1'
    
    r = requests.post(urlstr)
    #print(r.status_code)
    
    soup = BeautifulSoup(r.text,'html.parser')
    
    alldatacount = soup.find(id='totalpage')
    print('alldatacount='+alldatacount.text)
    
    totalpage=int(alldatacount.text)/50
    print(math.ceil(totalpage))
    
    alllocationarr=[]
    alllocationdata ={}
    
    for ele in range(1,math.ceil(totalpage)+1):
        urlstr  = 'https://book.tpml.edu.tw/webpac/booksearch.do?searchtype=simplesearch&execodeHidden=true&execode=&authoriz=1&search_field=TI&search_input='
        urlstr += urllib.parse.quote(bookname)
        urlstr += ('&showtuple=50&resid=189035216&nowpage='+str(ele))
        
        print(urlstr)
        
        r = requests.get(urlstr)
    
        soup = BeautifulSoup(r.text,'html.parser')
    
        alldata = re.findall('loadHoldIframe[\(\{]+(.+)(?=[\}])',r.text)
        for ele1 in alldata:
            locationdict = {}
            alldata1 = ele1.split(',')
            for ele2 in alldata1:
                alldata2 = ele2.split(':')
                if len(alldata2)==2:
                    locationdict[alldata2[0]]=alldata2[1].replace('"','')
            alllocationarr.append(locationdict)
    
        
    
        for ele1 in alllocationarr:
            temparr = []
            url2str = 'https://book.tpml.edu.tw/webpac/maintain/holdListAction.do?'
            url2str = url2str+'sid='+ele1['sid']+'&'
            url2str = url2str+'CLN='+ele1['CLN']+'&'
            url2str = url2str+'ExecCode1='+ele1['ExecCode1']+'&'
            url2str = url2str+'ExecCode2='+ele1['ExecCode2']+'&'
            url2str = url2str+'loc='+ele1['loc']
        
            r = requests.post(url2str)
            #print(r.text.replace('\n','').replace('\r','').replace(' ',''))        
            alllocationdata[ele1['sid']] = r.text.replace('\n','').replace('\r','').replace(' ','').replace('\t','')
    return alllocationdata
    

def main():
    print('Enter your BooknName:')
    bookname = input()

    allbooklocation = getbooklocation(bookname)
    Tenbookdata = getbooknamedata(bookname,allbooklocation)

    for ele in Tenbookdata:
        print(ele)


if __name__ == "__main__":
    main()

