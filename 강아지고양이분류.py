# -*- coding: utf-8 -*-
"""
Created on Sun Jun 26 15:20:37 2022

@author: hsh97
"""

from keras.applications import vgg16
from tensorflow.keras.utils import img_to_array
from tensorflow.keras.preprocessing.image import load_img
from keras.models import Model
from keras.applications.imagenet_utils import preprocess_input
from PIL import Image
import os
import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import random


imgs_path = "/content/drive/MyDrive/abc/"  #이미지 경로 (용량 작은))

imgs_model_width, imgs_model_height = 224, 224 #크기 전부 224,224로 변경 

vgg_model = vgg16.VGG16(weights='imagenet') #VGG16

# 예측대신에 -> 비슷한애들 추출하기 위해 마지막 레이어를 제거
feat_extractor = Model(inputs=vgg_model.input, outputs=vgg_model.get_layer("fc2").output)

# CNN 레이어 갯수 추출
feat_extractor.summary()


files = [imgs_path + x for x in os.listdir(imgs_path) if "jpg" in x] #파일추출 ->jpg지정

print("파일 갯수 :",len(files))


original = load_img(files[0], target_size=(imgs_model_width, imgs_model_height))



#이 순서는 path순인 것 같은데......
plt.imshow(original)
plt.show()
print("이미지 가져오기 성공!")


 
numpy_image_original = img_to_array(original) #이미지를 넘파이 형태로.

# 이미지 변경/ 배치포멧으로 변경하기
# 데이터 형태를 (batchsize, height, width, channels) 로 바꿀거고
# 차원하나를 추가해야하기때문에 axis=  0

image_batch_original = np.expand_dims(numpy_image_original, axis=0)

print('image batch size', image_batch_original.shape)

# VGG모델을 위한 이미지 준비하기


processed_image_original = preprocess_input(image_batch_original.copy())
img_features_original = feat_extractor.predict(processed_image_original)


print("VGG모델 성공!")
print("이미지 특성의 갯수 :",img_features_original.size)

img_features_original #array 형태

importedImages_original = []


#모든 file 안에 돌려서 array만들기. 특성 변경하기.
for f in files:
    filename = f
    original = load_img(filename, target_size=(224, 224))
    numpy_image_original = img_to_array(original)
    image_batch_original = np.expand_dims(numpy_image_original, axis=0)
    
    importedImages_original.append(image_batch_original)


images = np.vstack(importedImages_original)

processed_imgs = preprocess_input(images.copy())

imgs_features = feat_extractor.predict(processed_imgs) #특성추출에 시간이 좀 걸림. 
print("특성 추출 성공!")
imgs_features.shape 


cosSimilarities = cosine_similarity(imgs_features)

# 데이터프레임형태로 만들기.

cos_similarities_df = pd.DataFrame(cosSimilarities, columns=files, index=files)
cos_similarities_df.head()

# df 분리하기
# 고양이 분리
import re
이쁜고양이 = []
for A in cos_similarities_df.columns:
  if bool(re.search('catpick', A)):
    이쁜고양이.append(A)

유기묘 = []
잠시 = []
for B in cos_similarities_df.index:
    if bool(re.search('cat', B)):
      잠시.append(B)
for j in 잠시:
  if bool(re.search('catpick', j)):
    pass
  else:
    유기묘.append(j)

# 고양이df 만들기
고양이 = cos_similarities_df[이쁜고양이]
고양이 = 고양이.loc[유기묘]



# 강아지 분리
이쁜강아지 = []
for A in cos_similarities_df.columns:
  if bool(re.search('dogpick', A)):
    이쁜강아지.append(A)

유기견 = []
잠시 = []
for B in cos_similarities_df.index:
    if bool(re.search('dog', B)):
      잠시.append(B)
for j in 잠시:
  if bool(re.search('dogpick', j)):
    pass
  else:
    유기견.append(j)

# 강아지df만들기
강아지 = cos_similarities_df[이쁜강아지]
강아지 = 강아지.loc[유기견]



nb_closest_images = 3 #개 뽑기

#####################################################
# 내가 선택한 동물 사진 출력
#####################################################
## 고양이 분류기
def retrieve_most_similar_products_cat_img(given_img):

    original = load_img(given_img, target_size=(imgs_model_width, imgs_model_height))
    plt.imshow(original)
    plt.show()

    print("-----------------------------------------------------------------------")
    print("비슷한 친구:")

    closest_imgs = 고양이[given_img].sort_values(ascending=False)[1:nb_closest_images+1].index
    closest_imgs_scores = 고양이[given_img].sort_values(ascending=False)[1:nb_closest_images+1]

    for i in range(0,len(closest_imgs)):
        original = load_img(closest_imgs[i], target_size=(imgs_model_width, imgs_model_height))
        plt.imshow(original)
        plt.show()
        print(i+1,"번유사도 점수 : ",round(closest_imgs_scores[i]*150,2))
        print(closest_imgs[i])

# 고양이 택 후 사진 출력
my_pick = ['catpick2.jpg', 'catpick18.jpg', 'catpick22.jpg']
for a in my_pick:
    print("-----------------------------------------------------------------------")
    print("선택한 친구 :",a)
    for C in 이쁜고양이:
      if bool(re.search(a, C)): 
        retrieve_most_similar_products_cat_img(C)


## 강아지 분류기
def retrieve_most_similar_products_dog_img(given_img):

    original = load_img(given_img, target_size=(imgs_model_width, imgs_model_height))
    plt.imshow(original)
    plt.show()

    print("-----------------------------------------------------------------------")
    print("비슷한 친구:")

    closest_imgs = 강아지[given_img].sort_values(ascending=False)[1:nb_closest_images+1].index
    closest_imgs_scores = 강아지[given_img].sort_values(ascending=False)[1:nb_closest_images+1]

    for i in range(0,len(closest_imgs)):
        original = load_img(closest_imgs[i], target_size=(imgs_model_width, imgs_model_height))
        plt.imshow(original)
        plt.show()
        print(i+1,"번유사도 점수 : ",round(closest_imgs_scores[i]*150,2))
        print(closest_imgs[i])

my_pick = ['dogpick25.jpg', 'dogpick36.jpg', 'dogpick44.jpg']
for a in my_pick:
    print("-----------------------------------------------------------------------")
    print("선택한 친구 :",a)
    for C in 이쁜강아지:
      if bool(re.search(a, C)): 
        retrieve_most_similar_products_dog_img(C)


############################################################
## 연동된 csv 파일 정보 가져오기
############################################################
cat = pd.read_csv(r'/content/drive/MyDrive/유기묘최종크롤링.csv', encoding = 'utf-8')
dog = pd.read_csv(r'/content/drive/MyDrive/유기견최종크롤링.csv', encoding = 'utf-8')

# 고양이 분류기
def retrieve_most_similar_products_cat_csv(given_img):

    print("-----------------------------------------------------------------------")
    print("비슷한 친구:")

    closest_imgs = 고양이[given_img].sort_values(ascending=False)[1:nb_closest_images+1].index
    closest_imgs_scores = 고양이[given_img].sort_values(ascending=False)[1:nb_closest_images+1]

    for i in range(0,len(closest_imgs)):
      n = closest_imgs[i][30:-len('.jpg')]
      ns = int(n)-1
      print(cat.loc[ns])
      print(i+1,"번유사도 점수 : ",round(closest_imgs_scores[i]*150,2))
      print(closest_imgs[i])

# csv 파일 호출
my_pick = ['catpick2.jpg', 'catpick18.jpg', 'catpick22.jpg']
for a in my_pick:
    print("-----------------------------------------------------------------------")
    print("선택한 친구 :",a)
    for C in 이쁜고양이:
      if bool(re.search(a, C)): 
        retrieve_most_similar_products_cat_csv(C)



# 강아지 분류기
def retrieve_most_similar_products_dog_csv(given_img):

    print("-----------------------------------------------------------------------")
    print("비슷한 친구:")

    closest_imgs = 강아지[given_img].sort_values(ascending=False)[1:nb_closest_images+1].index
    closest_imgs_scores = 강아지[given_img].sort_values(ascending=False)[1:nb_closest_images+1]

    for i in range(0,len(closest_imgs)):
      n = closest_imgs[i][30:-len('.jpg')]
      ns = int(n)-1
      print(dog.loc[ns])
      print(i+1,"번유사도 점수 : ",round(closest_imgs_scores[i]*150,2))
      print(closest_imgs[i])

# csv 파일 호출
my_pick = ['dogpick25.jpg', 'dogpick36.jpg', 'dogpick44.jpg']
for a in my_pick:
    print("-----------------------------------------------------------------------")
    print("선택한 친구 :",a)
    for C in 이쁜강아지:
      if bool(re.search(a, C)): 
        retrieve_most_similar_products_dog_csv(C)