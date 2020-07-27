import re
# from datetime import datetime
from django.utils import timezone as datetime
import urllib
import traceback
import requests
from bs4 import BeautifulSoup

from results.models import Tag, Result


def updateTagData(tagName, pageNum=20):
    '''
    返回总排行榜前20页的数据
    '''
    targetURL = 'https://www.lofter.com/tag/{}/total'.format(
        urllib.parse.quote(tagName))
    for pn in range(1, pageNum+1):
        url = targetURL + '?page={}'.format(pn)
        # 获取lofter数据
        results = getOnePageData(url)

        # 将数据加入项目数据库中
        for item_info in results:
            tags = item_info['tags']
            del item_info['tags']

            # 如果该result已存在则略过 -> 如果作者更新了tags，这里不会同步更新
            if Result.objects.filter(blogID=item_info['blogID']):
                continue
            else:
                result = Result.objects.create(**item_info)

            for tagName in tags:
                if not Tag.objects.filter(tagName=tagName):
                    tag = Tag.objects.create(
                        tagName=tagName, lastUpdate=datetime.now()
                    )
                else:
                    tag = Tag.objects.get(tagName=tagName)
                result.tags.add(tag)
            result.save()


def getOnePageData(url):
    '''
    获取lofter排行榜中指定页面的数据
    '''
    results = []

    with requests.get(url) as res:
        html = res.text

    # 利用soup对象解析单条数据
    soup = BeautifulSoup(html, 'lxml')
    items = soup.find_all(attrs={'class': 'm-mlist'})
    for item in items[1:]:
        try:
            item_info = extract_item_info(item)
            if item_info:
                results.append(item_info)
        except Exception as e:
            print(traceback.format_exc())

    return results


def extract_item_info(item):
    '''
    利用soup对象解析单条数据
    '''
    item_info = {}

    # 如果主体是图就略过 -> 只扫文不扫图
    if item.find(attrs={'class': 'img'}):
        return

    # 文章链接
    item_info['blogURL'] = item.find(attrs={'class': 'isayc'})['href']
    item_info['blogID'] = item_info['blogURL'].split('/')[-1]
    # 作者信息
    writer_item = item.find(attrs={'class': 'w-who'})
    item_info['writer'] = writer_item.find(attrs={'class': 'ptag'}).text
    item_info['writerURL'] = writer_item.find(attrs={'class': 'ptag'})['href']

    # 文本信息
    title_item = item.find(attrs={'class': 'tit'})
    # 标题并不总是有
    if title_item:
        item_info['title'] = title_item.text
    else:
        item_info['title'] = '-'

    # 文章简介
    abstract = item.find(attrs={'class': 'txt js-digest ptag'}).text
    item_info['abstract'] = ' '.join(abstract.split())

    # tags
    item_info['tags'] = item.find(attrs={'class': 'opta'}).text.split()

    # 点赞和评论
    interactions = item.find(attrs={'class': 'optb'}).text
    item_info['likedCount'] = re.search(
        r'\((\d+)\).+\((\d+)\)', interactions).group(1)
    item_info['commentCount'] = re.search(
        r'\((\d+)\).+\((\d+)\)', interactions).group(2)

    return item_info
