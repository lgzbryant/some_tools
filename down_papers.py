#author: LGZ

#DATE: 2019/12/5

#TIME:16:01

#IDE: PyCharm

import urllib.request
from bs4 import BeautifulSoup
import os
import time
import datetime

config_save_path = 'G:/000_yan_san/paper'
config_keyword = 'adversarial gan'
config_number_of_papers = 200   # 25，50，100，200 only can be choose


def getHtml(url):
    page = urllib.request.urlopen(url)
    html = page.read()
    return html

def strip_tags(soup, invalid_tags):
    # soup = BeautifulSoup(html)

    for tag in soup.findAll(True):
        if tag.name in invalid_tags:
            s = ""
            for c in tag.contents:
                # print(str(c))
                s += str(c)
            tag.replaceWith(s)
    return soup

def get_papers_infor(soup):

    papers_list = []
    papers = []
    papers_authors = []
    papers_url = []
    papers_date = []

    for p in soup.find_all('p', "title is-5 mathjax"):
        p = strip_tags(p, 'span')
        papers.append(str(p.text).replace('\n', '').replace('\r', '').replace('?', '_').replace('!', '_').replace(':', '_').replace(',', '').lstrip().rstrip().replace('\/', '_').replace('\"', '_').replace('\"', '_').replace(' ', '_'))

        # print(p)
        # # p1 = BeautifulSoup(p)
        # print(p.text)
        # print('#'*100)


    for p in soup.find_all('p', "authors"):
        each_paper_authors = []
        for each_author in p.find_all('a'):
            each_paper_authors.append(each_author.text)
            # print(each_author.text)
        papers_authors.append(each_paper_authors)
        # print('*'*100)


    for p in soup.find_all('p', "list-title is-inline-block"):
        for number in p.find('a'):
            # print('https://arxiv.org/pdf/'+str(number.string).split(':')[1]+'.pdf')

            #papers_url.append('https://arxiv.org/pdf/' + str(number.string).split(':')[1] + '.pdf')

            papers_url.append('https://arxiv.xilesou.top/pdf/' + str(number.string).split(':')[1] + '.pdf')

            # print('*' * 100)

    month_idx = {'January': '01', 'February': '02', 'March': '03', 'April': '04', 'May': '05',
                 'June': '06', 'July': '07', 'August': '08', 'September': '09', 'October': '10',
                 'November': '11', 'December': '12'}

    for p in soup.select('p[class="is-size-7"]'):
        # print(str(p.text))
        # print(str(p.text).split(';')[0])
        submitted = str(p.text).split(';')[0].split(',')
        year = submitted[1]
        month = submitted[0].split(' ')[2]
        date = submitted[0].split(' ')[1]
        date = year + '_' + month_idx[month] + '_' + date + '_'
        papers_date.append(date)
        # print(date)
        # print('*'*100)


    for idx in range(len(papers)):
        each_paper = {}
        each_paper['title'] = papers[idx]
        each_paper['authors'] = papers_authors[idx]
        each_paper['url'] = papers_url[idx]
        each_paper['date'] = papers_date[idx]
        papers_list.append(each_paper)

        print(papers[idx])
        print(papers_authors[idx])
        print(papers_url[idx])
        print(papers_date[idx])
        print('*' * 100)

    return papers_list


def get_each_pdf(paper_dict, save_path):
    url = paper_dict['url']
    file_name = paper_dict['date']+paper_dict['title']+'.pdf'
    try:
        u = urllib.request.urlopen(url, timeout=10)

        f = open(save_path + '/' + file_name, 'wb')
        block_sz = 8192
        while True:
            buffer = u.read(block_sz)
            if not buffer:
                break
            f.write(buffer)
        f.close()
        print("Sucessful to download" + " " + file_name)
    except Exception as e:
        print('time_out: ', str(e))


def download_pdfs(keywords, number_of_papers, save_path):

    #arxiv = 'https://arxiv.org/search/?searchtype=all&query='

    arxiv = 'https://arxiv.xilesou.top/search/?searchtype=all&query='
    keywords_list = keywords.replace(' ', '+')
    arxiv += keywords_list+'&abstracts=show&size='+str(number_of_papers)+'&order=-announced_date_first'

    # arxiv = 'https://arxiv.org/search/?searchtype=all&query=adversarial&abstracts=show&size=5&order=-announced_date_first'
    print(arxiv)
    soup = BeautifulSoup(getHtml(arxiv), 'lxml')
    papers_list = get_papers_infor(soup)

    print('*'*100)
    print('begin to download the [{}] papers, total {} !'.format(str(keywords), str(number_of_papers)))
    print()

    for each_paper_dict in papers_list:
        begin_time = time.time()
        get_each_pdf(each_paper_dict, save_path)
        end_time = time.time()
        print('use {} minutes !'.format(str((end_time-begin_time)/60.0)))
        print()


def download_pdfs_info_to_txt(keywords, number_of_papers, save_path):

    # arxiv = 'https://arxiv.org/search/?searchtype=all&query='

    arxiv = 'https://arxiv.xilesou.top/search/?searchtype=all&query='
    keywords_list = keywords.replace(' ', '+')
    arxiv += keywords_list + '&abstracts=show&size=' + str(number_of_papers) + '&order=-announced_date_first'

    # arxiv = 'https://arxiv.org/search/?searchtype=all&query=adversarial&abstracts=show&size=5&order=-announced_date_first'
    print(arxiv)
    soup = BeautifulSoup(getHtml(arxiv), 'lxml')
    papers_list = get_papers_infor(soup)

    print('*' * 100)
    print('begin to save txt about the [{}] papers, total {} !'.format(str(keywords), str(number_of_papers)))
    print()

    big_dict = {}
    i=1
    for each_dict in papers_list:
        big_dict[str(i)] = each_dict
        i += 1

    print(big_dict)

    file = open(save_path + '/' + 'test.txt', 'w')
    print(save_path + '/' + 'test.txt')

    for k, v in big_dict.items():

        file.write(str("%03d" % int(k)) + '  ' + '('+str(v['date'])[:-1].replace('_', '-').lstrip()+') '+str(v['title']).replace('_', ' ') + '\n')
        file.write(' '*len(str("%03d" % int(k)) + '  ')+str(v['url']) + '\n')
        file.write('\n')

    file.close()


if __name__ == '__main__':

    file_name = config_keyword.lstrip().rstrip().replace(' ', '_')
    nowTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    save_path = config_save_path+'/'+nowTime.split(' ')[0]+'-'+file_name
    if not os.path.exists(save_path):
        os.makedirs(save_path)

    #download_pdfs(config_keyword, config_number_of_papers, save_path)

    download_pdfs_info_to_txt(config_keyword, config_number_of_papers, save_path)


