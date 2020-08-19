# 추천시스템
############ 잠재요인 협업필터링 - 행렬분해svd
import os
import pandas as pd 
import numpy as np

from sklearn.decomposition import TruncatedSVD

os.chdir('C:/Users/etotm/Desktop/refer')

rating = pd.read_csv('ratings.csv')
movie = pd.read_csv('datasets_4010_6264_movies.csv')

rating.head()
movie.head()

# 아래 변수들은 '잠재요인 기반 협업 필터링 추천시스템'에서는 필요없음 
del rating['timestamp']
del movie['genres']

user_movie = pd.merge(rating, movie , on='movieId')  
user_movie.head()  # 유저가 영화에 평점을 매겼을때 제목이 무엇인지 알 수 있음. 

# 피벗화 
user_movie_rating = user_movie.pivot_table('rating', index='userId', columns='title').fillna(0)
user_movie_rating.head()
# 특정영화와 비슷한 영화를 추천해보자
movie_user_rating = user_movie_rating.T

# SVD 
SVD = TruncatedSVD(n_components=12)
matrix = SVD.fit_transform(movie_user_rating)
matrix.shape

corr = np.corrcoef(matrix)
corr.shape
# 이 상관계수를 기반으로 하여 특정영화와 관련하여 값이 높은 영화를 추출
movie_title = user_movie_rating.columns
movie_title_list = list(movie_title)
coffey_hands = movie_title_list.index("Guardians of the Galaxy (2014)")

corr_coffey_hands = corr[coffey_hands]
list(movie_title[(corr_coffey_hands >= 0.9)])[:50]
len(list(movie_title[(corr_coffey_hands >= 0.9)]))

 - 이때의 문제점은 개인에게 맞춤형 추천이 아닌, 특정영화와 비슷한 영화를 추천 


##############
import os
import pandas as pd 
import numpy as np

from sklearn.decomposition import TruncatedSVD
from scipy.sparse.linalg import svds
os.chdir('C:/Users/etotm/Desktop/refer')

rating = pd.read_csv('ratings.csv')
movie = pd.read_csv('datasets_4010_6264_movies.csv')

user_movie_rating = rating.pivot(index='userId', columns='movieId', values='rating').fillna(0)
user_movie_rating.head() # N명의 사용자와 M개의 영화

matrix = user_movie_rating.values
user_rating_mean = np.mean(matrix, axis=1) # 사용자의 평균평점
matrix_user_mean = matrix - user_rating_mean.reshape(-1,1) # 사용자-영화 에 대해 평균평점을 뺀것
pd.DataFrame(matrix_user_mean, columns=user_movie_rating.columns) # N명의 사용자가 M개의 영화에 rating


U, sigma, Vt = svds(matrix_user_mean, k=12)
U.shape
sigma.shape  # 0이 아닌값만 1차원 행렬로 표현된 상태 -> 0이 포함된 대칭행렬로 변환시 np의 diag를 사용
Vt.shape

sigma = np.diag(sigma)


svd_user_predicted_ratings = np.dot(np.dot(U, sigma), Vt) + user_rating_mean.reshape(-1,1)
df_svd_preds = pd.DataFrame(svd_user_predicted_ratings, columns= user_movie_rating.columns)
df_svd_preds.head()

def recommend_movies(svd_preds, )


