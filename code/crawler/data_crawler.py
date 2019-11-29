import requests

API_KEY = "AIzaSyDXzAdjetUJXQlNJT21fOM73060IV0Gjws"
channelID = "UCAJ-meoCh1TrPZ7La3UpPrw"
pageToken = ""
videoId_list = []
title_column = []
tag_column = []
view_column = []

def store_videoId_list(channelID, API_KEY, token):
    response = requests.get(
        "https://www.googleapis.com/youtube/v3/search?channelId=" + channelID + "&order=date&part=snippet&type=video&maxResults=20&key=" + API_KEY + "&pageToken=" + token)
    json_data = response.json()
    global pageToken
    pageToken = json_data['nextPageToken']
    for i in json_data['items']:
        videoId_list.append(i['id']['videoId'])
    return

def store_video_info(videoId):
    response = requests.get("https://www.googleapis.com/youtube/v3/videos?key=" + API_KEY + "&fields=items(snippet(title,tags,channelTitle,publishedAt),statistics(viewCount))&part=snippet,statistics&id=" + videoId)
    json_data = response.json()
    title = json_data['items'][0]['snippet']['title']
    tags = json_data['items'][0]['snippet']['tags']
    view = json_data['items'][0]['statistics']['viewCount']
    title_column.append(title)
    tag_column.append(','.join(tags))
    view_column.append(view)
    return

store_videoId_list(channelID, API_KEY, pageToken)
for i in videoId_list:
    store_video_info(i)

print(title_column)
print(tag_column)
print(view_column)
print(len(title_column))
print(len(tag_column))
print(len(view_column))

# def video_crawling(videoId):
#     html = urlopen("https://www.youtube.com/watch?v="+videoId)
#     bsObj = BeautifulSoup(html, "html.parser")
#
#     title_html = bsObj.find("meta", {"name": "title"})
#     tag_html = bsObj.find("meta", {"name": "keywords"})
#     view_html = bsObj.find("meta", {"itemprop": "interactionCount"})
#
#     if (title_html['content'] is not None) and (tag_html['content'] is not None) and (view_html['content'] is not None):
#         title = title_html['content']
#         tag_list = tag_html['content']
#         view_count = view_html['content']
#
#         title_column.append(title)
#         tag_column.append(tag_list)
#         view_column.append(view_count)

    # date_html = bsObj.find("meta", {"itemprop": "uploadDate"})
    # date_count = date_html['content']
    #
    # like_html = bsObj.find("button", {"title": "이 동영상이 마음에 듭니다."})
    # like_count = re.findall("\d+", str(like_html['aria-label']))
    # like_count = "".join(like_count)

    # duration_html = bsObj.find("span", {"class": "ytp-time-duration"})
    # duration = duration_html

    # print(title)
    # print(tag_list)
    # print(view_count)
    # print(date_count)
    # print(like_count)
    # print(duration)

# video_crawling("https://www.youtube.com/watch?v=1RModyVxaQM")
# video_crawling("https://www.youtube.com/watch?v=uDUt5xx2WNk&t=3s")
# video_crawling("https://www.youtube.com/watch?v=sDrV9eyx4OI&t=6s")
# video_crawling("https://www.youtube.com/watch?v=080yWK_JHcc")
#
# print(tag_column)
# print(view_column)
