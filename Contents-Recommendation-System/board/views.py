import json
import urllib.request
import pandas as pd
from django.http import HttpResponse
from django.shortcuts import render
import csv
import re
import numpy as np
import requests

client_id = "vT0sbB55Azv8G7YykLD9"
client_secret = "dR2M27Ko_X"

API_KEY = "AIzaSyDXzAdjetUJXQlNJT21fOM73060IV0Gjws"
pageToken = ""
videoId_list = []
title_column = []
tag_column = []
view_column = []
select_tag = []

def store_videoId_list(channelID, API_KEY, token):
    response = requests.get(
        "https://www.googleapis.com/youtube/v3/search?channelId=" + channelID + "&order=date&part=snippet&type=video&maxResults=50&key=" + API_KEY + "&pageToken=" + token)
    json_data = response.json()
    global pageToken
    pageToken = json_data['nextPageToken']
    for i in json_data['items']:
        videoId_list.append(i['id']['videoId'])
    return

def store_video_info(videoId):
    response = requests.get("https://www.googleapis.com/youtube/v3/videos?key=" + API_KEY + "&fields=items(snippet(title,tags),statistics(viewCount))&part=snippet,statistics&id=" + videoId)
    json_data = response.json()
    if json_data['items'][0]['snippet']['tags'] is not None:
        title = json_data['items'][0]['snippet']['title']
        tags = json_data['items'][0]['snippet']['tags']
        view = json_data['items'][0]['statistics']['viewCount']
        title_column.append(title)
        tag_column.append(','.join(tags))
        view_column.append(view)
    return

# 리스트 내의 문자열의 공백 제거 후 반환
def delete_blank(list):
    result = []
    for i in list:
        result.append(i.replace(' ', ''))
    return result

# 사용자가 선택한 태그들을 갖고있는 데이터를 반환
def select_datalist(prev_data, select_list):
    result = {}
    for i in prev_data.keys():
        count = 0
        temp = i.split(",")
        for j in select_list:
            if j in temp:
                count += 1
        if count == len(select_list):
            result[i] = prev_data[i]
    return result


# tag_count : 해당 태그 나온 횟수
# tag_view : 해당 태그가 포함된 영상의 조회수들의 합
# data_num : 전체 영상 수
# idf = ln(전체 영상 수/해당 태그를 갖고있는 영상의 수)
# (idf x 해당 태그가 포함된 영상의 조회수들의 합)으로 내림차순 출력
def calculate_idf(prev_data, select_list):
    # 사용자가 선택한 태그가 없는경우(1회차)
    if not select_list:
        data = prev_data
    else:
        data = select_datalist(prev_data, select_list)

    data_num = len(data)
    tag_view = {}
    tag_count = {}
    idf = {}
    result = []

    # n회차 수행결과 특정 한 영상 하나까지 도달 할 경우
    if data_num == 1:
        print("특정 영상 찝어짐")
        return []

    # 태그들을 '/' 기준으로 토큰화 하고, 토큰화 된 태그와 해당 태그가 포함된 영상의 조회수를 딕셔너리에 저장
    for i in data.keys():
        temp = i.split(",")
        temp = list(set(temp))
        for k in temp:
            if k in tag_view.keys():
                tag_view[k] = int(tag_view[k]) + int(data[i])
            else:
                tag_view[k] = int(data[i])

    # 태그들을 '/' 기준으로 토큰화 하고, 토큰화 된 태그와 해당 태그가 포함된 영상의 수를 딕셔너리에 저장
    for i in data.keys():
        temp = i.split(",")
        temp = list(set(temp))
        for k in temp:
            if k in tag_count.keys():
                tag_count[k] = tag_count[k] + 1
            else:
                tag_count[k] = 1

    # 토큰화된 각 태그들의 idf를 계산 후 해당 태그가 포함된 영상의 조회수들의 합을 곱셈
    for i in tag_view.keys():
        idf[i] = np.log(data_num / tag_count[i]) * tag_view[i]

    rank = sorted(idf.items(), key=lambda t: t[1], reverse=True)
    # 순위별로 나열된 딕셔너리에서 태그만 뽑아서 리스트에 저장 후 반환
    for i in rank:
        result.append(i[0])
    return result

def recommend_tag(request):
    if request.method == 'GET':
        youtubeURL = request.GET.get('youtubeURL')
        if (youtubeURL is None):
            youtubeURL = ""
        searchNum = request.GET.get('searchnum')
        if (searchNum is None):
            searchNum = "10"
        searchVideo = request.GET.get('searchvideo')
        if (searchVideo is None):
            searchVideo = "50"
        checkfirst = request.GET.get('checkfirst')
        if(checkfirst is None):
            checkfirst = '0'
        select_tag = request.GET.get('select_tag')
        if(select_tag is None):
            select_tag = []
        prev_data = request.GET.get('prev_data')
        if(prev_data is None):
            prev_data = {}
        prev_url = request.GET.get('prev_url')
        if(prev_url is None):
            prev_url = ""
        prev_vdnum = request.GET.get('prev_vdnum')
        if(prev_vdnum is None):
            prev_vdnum = '0'

        # 여기부터 조건문줘서 초기화면, 블로그검색, 카페검색 분류
        if(checkfirst == '1'):
            if(youtubeURL == prev_url and searchVideo == prev_vdnum):
                tagView_dict = prev_data
            else:
                if (searchVideo == "50"):
                    store_videoId_list(youtubeURL, API_KEY, pageToken)
                    print("영상50개")
                elif (searchVideo == "100"):
                    store_videoId_list(youtubeURL, API_KEY, pageToken)
                    store_videoId_list(youtubeURL, API_KEY, pageToken)
                    print("영상100개")
                elif (searchVideo == "150"):
                    store_videoId_list(youtubeURL, API_KEY, pageToken)
                    store_videoId_list(youtubeURL, API_KEY, pageToken)
                    store_videoId_list(youtubeURL, API_KEY, pageToken)
                    print("영상150개")

                for i in videoId_list:
                    store_video_info(i)

                global tag_column
                tag_column = delete_blank(tag_column)
                tagView_dict = dict(zip(tag_column, view_column))

            result = calculate_idf(tagView_dict, select_tag)
            # select_tag.append('빅헤드오버워치')
            # calculate_idf(tagView_dict, select_tag)
            # select_tag.append('레식')
            # calculate_idf(tagView_dict, select_tag)

            tmplist = []
            for idx, val in enumerate(result):
                if idx < int(searchNum):
                    tmplist.append({"no": idx+1, "tag1": val, "tag2": "", "tag3": "", "tag4": "", "title": "", "link": ""})
                else:
                    break
            #print(tmplist)

            context = {
                'items': tmplist,
                'prev_data': tagView_dict,
                'prev_url' : youtubeURL,
                'prev_vdnum': searchVideo,
                'keyword': youtubeURL,
                'searchnum': searchNum,
                'searchvideo': searchVideo,
                'select_tag': select_tag
            }
            return render(request, 'board/main.html', context=context)

        else:
            # 초기 화면
            tmplist = [{"no": "", "tag1": "", "tag2": "", "tag3": "", "tag4": "", "title": "", "link": ""}]
            context = {
                'items': tmplist
            }
            return render(request, 'board/main.html', context=context)