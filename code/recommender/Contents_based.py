import numpy as np
import pandas as pd

# csv파일을 읽어서 리스트로 반환
def read_csv():
    data = pd.read_csv("./dataset.csv", encoding="cp949")
    return data

# 리스트 내의 문자열의 공백 제거 후 반환
def delete_blank(list):
    result = []
    for i in list:
        result.append(i.replace(' ', ''))
    return result

# tag_count : 해당 태그 나온 횟수
# tag_view : 해당 태그가 포함된 영상의 조회수들의 합
# data_num : 전체 영상 수
# idf = ln(전체 영상 수/해당 태그를 갖고있는 영상의 수)
# (idf x 해당 태그가 포함된 영상의 조회수들의 합)으로 내림차순 출력
def calculate_idf(data):
    # print(data)
    data_num = len(data)
    tag_view = {}
    tag_count = {}
    idf = {}
    
    # 태그들을 '/' 기준으로 토큰화 하고, 토큰화 된 태그와 해당 태그가 포함된 영상의 조회수를 딕셔너리에 저장
    for i in data.keys():
        temp = i.split("/")
        for k in temp:
            if k in tag_view:
                tag_view[k] = int(tag_view[k]) + int(data[i])
            else :
                tag_view[k] = int(data[i])

    # 태그들을 '/' 기준으로 토큰화 하고, 토큰화 된 태그와 해당 태그가 포함된 영상의 수를 딕셔너리에 저장
    for i in data.keys():
        temp = i.split("/")
        for k in temp:
            if k in tag_count:
                tag_count[k] = int(tag_count[k]) + 1
            else :
                tag_count[k] = 1
    # print(tag_view)
    # print(len(tag_view))
    # print(tag_count)
    # print(len(tag_count))

    # 토큰화된 각 태그들의 idf를 계산 후 해당 태그가 포함된 영상의 조회수들의 합을 곱셈
    for i in tag_view.keys():
        idf[i] = np.log(data_num/tag_count[i]) * tag_view[i]

    rank = sorted(idf.items(), key=lambda x: x[1], reverse=True)
    max_tag = rank[0][0]
    print(max_tag)
    print(rank)

    # 가장 순위가 높은 태그가 포함된 영상들로 n회차 수행
    next_data = {}
    for i in data.keys():
        if max_tag in i:
            next_data[i] = data[i]
    # print(two_temp)
    if len(next_data) > 1:
        calculate_idf(next_data)

    # print(max(idf, key=idf.get))
    # print(idf['빅헤드오버워치'])

data = read_csv()
tag_column = delete_blank(data['태그'].tolist())
view_column = data['조회수'].tolist()
tagView_dict = dict(zip(tag_column, view_column))
calculate_idf(tagView_dict)