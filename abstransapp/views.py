from googletrans import Translator
import semanticscholar as sch
from django.shortcuts import render, redirect
import urllib
import time
from ipware import get_client_ip
# Create your views here.


def trans(src):
    if src == None:
        return None
    return Translator().translate(src, src="en", dest='ja').text

def make_deepl_request(text):
    enc = urllib.parse.quote(text)
    url = 'https://www.deepl.com/translator#en/ja/' + enc
    return url

def url2doi(url):
    req = urllib.request.Request(url)
    with urllib.request.urlopen(req) as res:
        body = str(res.read())
    point = body.find("citation_pdf_url")
    doi = body[point: point+1000].split("\"")[2]
    doi = doi[16:]
    return doi

def doi2info(doi, paper_count=3, citaions=False, placed=0):
    # doiで論文指定
    # paper_countで取得する関連研究の数を指定
    # citaions=True  で、この論文「を」引用している論文を表示
    # citaions=False で、この論文「が」引用している論文を表示
    papers = []
    if placed < 1:
        if 'http' in doi:
            doi = url2doi(doi)

        paper = sch.paper(doi, timeout=10)
        if len(paper) == 0:
            return None
        title_en = paper['title']
        title_ja = trans(title_en)
        abst_en = paper['abstract']
        abst_ja = trans(abst_en)

        papers.append({
            'title_en': title_en,
            'title_ja': title_ja,
            'abst_en': abst_en,
            'abst_deepl': make_deepl_request(abst_en),
            'abst_ja': abst_ja,
            'doi': paper['doi'],
            'url': paper['url'],
            'inf_cnt': paper['influentialCitationCount'],
            'topics': paper['topics'],
            'authors': paper['authors'],
            'year': paper['year'],
            'arxiv': paper['arxivId']
        })
        
    if citaions:
        key = 'citations'
    else:
        key = 'references'

    refs = sch.paper(doi, timeout=10)[key]
    inf_count = 0  # 影響度のある関連論文の数
    for ref in refs:
        if ref['isInfluential']:
            inf_count += 1

    count = 0  # 登録した関連論文の数
    for ref in refs:

        # すでに表示されている論文は除く

        if ref['doi'] == None:
            continue

        

        if (not ref['isInfluential']):
            if inf_count < paper_count:
                # 影響度のある論文の合計数が指定された数(paper_count)より少ないなら表示
                inf_count += 1
            else:
                # 影響度のない論文は表示しないので次へ
                continue

        if count > paper_count + placed:
            # 関連論文が指定された数読み込めたなら終了
            break

        count += 1

        if count < placed:
            continue

        paper = sch.paper(ref['doi'], timeout=10)
        title_en = paper['title']
        title_ja = trans(title_en)
        abst_en = paper['abstract']
        abst_ja = trans(abst_en)
        print(title_en)

        papers.append({
            'title_en': paper['title'],
            'title_ja': title_ja,
            'abst_en': paper['abstract'],
            'abst_deepl': make_deepl_request(abst_en),
            'abst_ja': abst_ja,
            'doi': paper['doi'],
            'url': paper['url'],
            'inf_cnt': paper['influentialCitationCount'],
            'topics': paper['topics'],
            'authors': paper['authors'],
            'year': paper['year'],
            'arxiv': paper['arxivId']
        })

    return papers


# ホーム画面
def home(request):
    print("home OK")
    return render(request, 'index.html', {'msg': '論文のDOIかSemantic ScholarのURLを入力してください'})

# URLにdoiを入れるための苦肉の策
def search(request):
    print("search OK")


    if request.POST['doi']:
        doi = request.POST['doi']
    else:
        return render(request, 'index.html', {'msg': '指定されたDOI，またはURLが見つかりません'})

    return redirect('abstrans', doi)


def exec_ajax(request):
    print("ajax ok")

    #if request.method == 'GET':  # GETの処理
    doi = request.POST.get("param1")
    ajax_count = 5
    print(doi)
    print(ajax_count)

    data = doi2info(doi=doi, placed=ajax_count)
    #print(data)

    return render(request,"next.html", {"data":data})



def abstrans(request, doi):
    print('abstrans OK')

    # APIの呼び出し時間計測
    start = time.perf_counter()

    """
    doi = '10.1109/cvpr.2016.90'
    """
    client_addr, _ = get_client_ip(request)
    print(client_addr)
    papers = doi2info(doi)

    end = time.perf_counter()
    print(f"API処理時間: {end - start:.3f} s.")

    return render(request, 'abstrans.html', {'papers': papers, 'doi':doi})
