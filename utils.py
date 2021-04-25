from googletrans import Translator
import semanticscholar as sch
from deepl import get_translated_text
import urllib
import urllib.request
from bs4 import BeautifulSoup

def print_paper(paper):
    print('doi: ', paper['doi'])
    print('influentialCitationCount: ', end = '')
    print(paper['inf_cnt'])
    print('url: ', paper['url'])
    print('year: ', str(paper['year']))
    print('arxiv: ', paper['arxiv'])

    print('authors: ', end = '')
    for author in paper['authors']:
        print(author['name'], end=', ')
    print()
    print('topics: ', end='')
    for topic in paper['topics']:
        print(topic['topic'], end=', ')
    print()
    print('Title')
    print()
    print(paper['title_en'])
    print(paper['title_ja'])
    print(end='\n\n')
    print('abstract')
    print()
    print(paper['abst_en'])
    print()
    print(paper['abst_ja'])
    print(end='\n\n\n\n\n')

def trans(src):
    if src == None:
        return None
    rtn = get_translated_text('en', 'ja', src)
    #return get_translated_text('en', 'ja', src)
    return Translator().translate(src, src="en", dest='ja').text
def make_deepl_request(text):
    enc = urllib.parse.quote(text)
    url = 'https://www.deepl.com/translator#en/ja/' + enc
    return url

def doi2info(doi, paper_count=5, citaions = False):
    # doiで論文指定
    # paper_countで取得する関連研究の数を指定
    # citaions=True  で、この論文「を」引用している論文を表示
    # citaions=False で、この論文「が」引用している論文を表示

    papers = []

    paper = sch.paper(doi, timeout=10)
    title_en = paper['title']
    title_ja = trans(title_en)
    abst_en  = paper['abstract']
    abst_ja  = trans(abst_en)

    papers.append({
        'title_en': title_en,
        'title_ja': title_ja,
        'abst_en' : abst_en,
        'abst_deepl': make_deepl_request(abst_en),
        'abst_ja' : abst_ja,
        'doi'     : paper['doi'],
        'url'     : paper['url'],
        'inf_cnt' : paper['influentialCitationCount'],
        'topics'  : paper['topics'],
        'authors' : paper['authors'],
        'year'    : paper['year'],
        'arxiv'   : paper['arxivId']
    })
    if citaions:
        key = 'citations'
    else:
        key = 'references'

    refs = paper[key]
    inf_count = 0 #影響度のある関連論文の数
    for ref in refs:
        if ref['isInfluential']:
            inf_count += 1


    count = 0 #登録した関連論文の数
    for ref in refs:

        if ref['doi'] == None:
            continue
        
        if (not ref['isInfluential']):
            if inf_count < paper_count:
                #影響度のある論文の合計数が指定された数(paper_count)より少ないなら表示
                inf_count += 1
            else:
                #影響度のない論文は表示しないので次へ
                continue

        if count > paper_count:
            #関連論文が指定された数読み込めたなら終了
            break

        count += 1

        paper = sch.paper(ref['doi'], timeout=10)
        title_en = paper['title']
        title_ja = trans(title_en)
        abst_en  = paper['abstract']
        abst_ja  = trans(abst_en)

        papers.append({
            'title_en': paper['title'],
            'title_ja': title_ja,
            'abst_en' : paper['abstract'],
            'abst_deepl': make_deepl_request(abst_en),
            'abst_ja' : abst_ja,
            'doi'     : paper['doi'],
            'url'     : paper['url'],
            'inf_cnt' : paper['influentialCitationCount'],
            'topics'  : paper['topics'],
            'authors' : paper['authors'],
            'year'    : paper['year'],
            'arxiv'   : paper['arxivId']
        })
    
    return papers

if __name__ == "__main__":

    url = 'https://www.semanticscholar.org/paper/Multi-step-short-term-wind-speed-forecasting-based-Fu-Wang/9c37dec8a5764ebc5be897adfd498acb41acc323'
    req = urllib.request.Request(url)
    with urllib.request.urlopen(req) as res:
        body = str(res.read())
    point = body.find("citation_pdf_url")
    doi = body[point: point+1000].split("\"")[2]
    doi = doi[16:]
    print(doi)
    paper = sch.paper('10.1016/J.ENCONMAN.2019.02.086', timeout=10)
    if len(paper) == 0:
        print(paper)
    # papers = doi2info('10.1109/cvpr.2016.90')

    # for paper in papers:
    #     print_paper(paper)

    # print('paper.keys()')
    # print(papers[0].keys())