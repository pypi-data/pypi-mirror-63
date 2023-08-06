from bess.bess import PdasLm, PdasLogistic
import numpy as np
import pandas as pd
np.random.seed(123)   # fix seed to get the same result

# ### PdasLm sample
# # Data information
# train_X = np.random.normal(0, 1, 10 * 5).reshape((10, 5))     # train_x
# train_y = np.random.normal(0, 1, 10)                          # train_y
# test_X = np.random.normal(0, 1, 10 * 5).reshape((10, 5))      # test_x
#
# # path_type="seq", sequence:搜索的稀疏度列表
# model = PdasLm(path_type="seq", sequence=[3])
# model.fit(X=train_X, y=train_y)
# print(model.predict(test_X))
# print(model.beta_out)
#
#
# ### PdasLogistic sample
# # Data information
# train_X = np.random.normal(0, 1, 10 * 5).reshape((10, 5))     # train_x
# train_y = np.random.randint(0, 2, 10)                         # train_y
# test_X = np.random.normal(0, 1, 10 * 5).reshape((10, 5))      # test_x
#
# # path_type="seq", sequence:搜索的稀疏度列表
# model = PdasLogistic(path_type="seq", sequence=[3])
# model.fit(X=train_X, y=train_y)
# print(model.predict(test_X))
# print(model.beta_out)

# X = np.random.normal(0, 1, 5 * 3).reshape((5, 3))
# print(X)
# # beta = np.hstack((np.array([1 , -1, -1, -1, -1]), np.zeros(5)))
# beta = np.array([1, -1, 0])
# print(beta)
# xbeta = np.matmul(X, beta)
# print(xbeta)
# p = np.exp(xbeta)/(1+np.exp(xbeta))
# print(p)
# y = np.random.binomial(1, p)
# print(y)

data = pd.read_csv("dat.csv", header=None)
print(data)
X = data.iloc[:, 0:10]
y = data.iloc[:, 10]
model = PdasLogistic(path_type="seq", sequence=[5])
model.fit(X=X, y=y)
print(model.beta_out)

# np.random.seed(123)
# train_x = np.random.normal(0, 1, 100 * 200).reshape((100, 200))
# beta = np.hstack((np.ones(5), -1 * np.ones(5) , np.zeros(190)))
# np.random.seed(1234)
# e = np.random.normal(0, 1, 100)
# train_y = np.matmul(train_x, beta) + e
# model = PdasLm(path_type = "seq", sequence = [10])
# model.fit(X = train_x, y = train_y)
# print(model.beta_out)



