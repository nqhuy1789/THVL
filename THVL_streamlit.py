import pandas as pd
import streamlit as st
from itertools import cycle
from PIL import Image
import os
from underthesea import ner, word_tokenize


def preprocess_search_string(search_string):
    ner_results = ner(search_string + ".")
    NounPhrase = []
    Noun = []
    Others = []
    sPerson = ''
    sLocation = ''
    sNoun = ''
    for ner_result in ner_results:
        if ner_result[3] == 'B-PER':
            sPerson = ner_result[0]
        elif ner_result[3] == 'I-PER':
            sPerson += ' ' + ner_result[0]
        elif ner_result[3] == 'B-LOC':
            sLocation = ner_result[0]
        elif ner_result[3] == 'I-LOC':
            sLocation += ' ' + ner_result[0]
        elif ner_result[1] == 'Np':
            NounPhrase.append(ner_result[0])
        elif ner_result[1] == 'L':
            sNoun = ner_result[0]
        elif ner_result[1] == 'Nc':
            if sNoun: 
                sNoun += ' ' + ner_result[0]
            else:
                sNoun = ner_result[0]
        elif ner_result[1] == 'N': 
            if sNoun: sNoun += ' ' + ner_result[0]
            elif len(ner_result[0].split())>=2: Noun.append(ner_result[0].lower())
        else:
            if sPerson: 
                if (len(sPerson.split())>=2): NounPhrase.append(sPerson)
                sPerson = ''
            if sLocation:
                if (len(sLocation.split())>=2): NounPhrase.append(sLocation)
                sLocation = ''
            if sNoun and (len(sNoun.split()) >=2):
                Noun.append(sNoun.lower())
                sNoun = ''
            if ((ner_result[1] == 'A') or (ner_result[1] == 'V')) and (len(ner_result[0].split())>=2): Others.append(ner_result[0].lower())
    return(NounPhrase + Noun + Others)

def Search_string(search_string, source_string):
    result = [] 
    iCounter = 0
    for str in search_string:
        if str.lower() in source_string.lower(): 
            iCounter +=1
            result.append(str)
    return iCounter, result

def Load_Description(file_index, frame_index):
    # sPath = r'G:\My Drive\44 - AI\2 - Photo\THVL _ Phim t??i li???u_ Nam B??? x??a v?? nay - T???p '
    sPath = './THVL _ Phim t??i li???u_ Nam B??? x??a v?? nay - T???p '
    data = pd.read_csv(sPath + str(file_index) + '/' + 'THVL _ Phim t??i li???u_ Nam B??? x??a v?? nay - T???p '+ str(file_index) + '.csv')
    return data.iloc[frame_index]['Description']

def Load_Lexicon(file_index):
    iPosition = 1
    # sPath = r'G:\My Drive\44 - AI\2 - Photo\THVL _ Phim t??i li???u_ Nam B??? x??a v?? nay - T???p '
    sPath = './THVL _ Phim t??i li???u_ Nam B??? x??a v?? nay - T???p '
    data = pd.read_csv(sPath + str(file_index) + '/' + 'THVL _ Phim t??i li???u_ Nam B??? x??a v?? nay - T???p '+ str(file_index) + '.csv').dropna()
    for i in range(1,len(data)):
        scene_keywords = data.iloc[i]['Keywords']
        if (scene_keywords != ' '):
            keywords = scene_keywords.split(',')
            for keyword in keywords:
                words = word_tokenize(keyword.lower())
                for word in words:
                    if word not in lexicon:
                        lexicon[word] = []
                    lexicon[word].append((file_index, iPosition, data.iloc[i]['Start'], data.iloc[i]['End'], data.iloc[i]['Scene number']))
                    iPosition += 1
    return lexicon

def Load_listfile(list_file, file_index):
    # sPath = r'G:\My Drive\44 - AI\2 - Photo\THVL _ Phim t??i li???u_ Nam B??? x??a v?? nay - T???p ' + str(file_index)
    sPath = './THVL _ Phim t??i li???u_ Nam B??? x??a v?? nay - T???p ' + str(file_index)
    temp = []
    for path in os.scandir(sPath):
        if (path.is_file()) and (path.name[-4:]=='.jpg'):
            temp.append(sPath + '/' + path.name)
    list_file.append(temp)
    return list_file

def Search_thumbnail(search_string):
    words = word_tokenize(search_string.lower())
    num_words = len(words)
    results = []
    new_words = []
    for i in range(num_words):
        if words[i] in lexicon: 
            new_words.append((words[i],lexicon[words[i]]))
    num_words = len(new_words)
    if num_words==0: return []
    removeDuplicate = set()
    for i in range(num_words):
        for current_word in new_words[i][1]:
            search_result = new_words[i][0]
            full_word = current_word
            for j in range(i+1, num_words):
                for next_word in new_words[j][1]:
                    if (current_word[0] < next_word[0]) and (current_word[4] < next_word[4]): 
                        break
                    # if current_word[4] < next_word[4]: 
                    #     break
                    if current_word[1] == next_word[1]-1:
                        current_word = next_word
                        search_result += ' ' + new_words[j][0]
                    
            if (full_word[0],full_word[4]) not in removeDuplicate:
                removeDuplicate.add((full_word[0],full_word[4]))
                results.append((search_result, full_word))
                
    return results

  

import pickle
# # t???o d??? li???u t??m ki???m
# lexicon = {}
# lexicon = Load_Lexicon(lexicon, 1)
# lexicon = Load_Lexicon(lexicon, 2)
# lexicon = Load_Lexicon(lexicon, 3)
# lexicon = Load_Lexicon(lexicon, 4)
# lexicon = Load_Lexicon(lexicon, 5)
# lexicon = Load_Lexicon(lexicon, 6)
# lexicon = Load_Lexicon(lexicon, 7)
# pkl_file = open("lexicon.pkl", 'wb')
# pickle.dump(lexicon, pkl_file)
# pkl_file.close()
# list_file = []
# list_file = Load_listfile(list_file,1)
# list_file = Load_listfile(list_file,2)
# list_file = Load_listfile(list_file,3)
# list_file = Load_listfile(list_file,4)
# list_file = Load_listfile(list_file,5)
# list_file = Load_listfile(list_file,6)
# list_file = Load_listfile(list_file,7)
# pkl_file = open("listfile.pkl", 'wb')
# pickle.dump(list_file, pkl_file)
# pkl_file.close()

# ?????c d??? li???u t??m ki???m
lexicon = {}
pkl_file = open("lexicon.pkl", 'rb')
lexicon = pickle.load(pkl_file)
pkl_file.close()
list_file = []
pkl_file = open("listfile.pkl", 'rb')
list_file = pickle.load(pkl_file)
pkl_file.close()

# #test search
# results = Search_thumbnail('ch??a nguy???n')
# results.sort(key=lambda a: len(a[0]), reverse=True)
# for result in results:
#     # print(result[0], result[1])
#     print(result[0], list_file[result[1][0]-1][result[1][4]-1],result[1][2],result[1][3])


sLink = []
sLink.append("https://www.youtube.com/embed/xK6Eaq9KJXM")
sLink.append("https://www.youtube.com/embed/YPV2BBS2M7I")
sLink.append("https://www.youtube.com/embed/w-mS6zmy7ik")
sLink.append("https://www.youtube.com/embed/2GmEGs1e8Rg")
sLink.append("https://www.youtube.com/embed/njCVipzkqeU")
sLink.append("https://www.youtube.com/embed/JPbvvvDVwxw")
sLink.append("https://www.youtube.com/embed/eAuMur2aSDs")

# if bSearchBox:
if True:
    with st.sidebar.form(key ='Search'):
        search_string = st.text_input("T??m theo t??? kh??a", "")    
        submitted1 = st.form_submit_button(label = 'T??m ki???m ????')
    
    if submitted1:
        st.empty()
        results = Search_thumbnail(search_string)
        results.sort(key=lambda a: len(a[0]), reverse=True)
        for result in results:
            displayimage = Image.open(list_file[result[1][0]-1][result[1][4]-1])
            st.image(displayimage)
            scene_start = result[1][2]
            scene_end = result[1][3]
            start = int(scene_start[0:2]) * 3600 + int(scene_start[3:5]) * 60 + int(scene_start[6:8]) + int(scene_start[9:12]) // 1000
            end = int(scene_end[0:2]) * 3600 + int(scene_end[3:5]) * 60 + int(scene_end[6:8]) + int(scene_end[9:12]) // 1000 
            image_link = sLink[result[1][0]-1] + "?autoplay=1&" + 'start=' + str(start) + '&end=' + str(end)
            st.write("{} [link](%s)".format(result[0]) % image_link)
            st.write(Load_Description(result[1][0], result[1][4]))