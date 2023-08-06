from bess.bess import PdasLm, PdasLogistic
import numpy as np
np.random.seed(123)   # fix seed to get the same result

### PdasLm sample
# Data information
train_X = np.random.normal(0, 1, 10 * 5).reshape((10, 5))     # train_x
train_y = np.random.normal(0, 1, 10)                          # train_y
test_X = np.random.normal(0, 1, 10 * 5).reshape((10, 5))      # test_x

# Default:path_type="seq", sequence=[1,2,...,X.shape[1]]
model = PdasLm()
model.fit(X=train_X, y=train_y)
print(model.predict(test_X))

# path_type="gs", Default:s_min=1, s_max=X.shape[1], K_max = int(math.log(p, 2/(math.sqrt(5) - 1)))
model = PdasLm(path_type="gs")
model.fit(X=train_X, y=train_y)
print(model.predict(test_X))


### PdasLogistic sample
# Data information
train_X = np.random.normal(0, 1, 10 * 5).reshape((10, 5))     # train_x
train_y = np.random.randint(0, 2, 10)                         # train_y
test_X = np.random.normal(0, 1, 10 * 5).reshape((10, 5))      # test_x

# Default:path_type="seq", sequence=[1,2,...,X.shape[1]]
model = PdasLogistic()
model.fit(X=train_X, y=train_y)
print(model.predict(test_X))

# path_type="gs", Default:s_min=1, s_max=X.shape[1], K_max = int(math.log(p, 2/(math.sqrt(5) - 1)))
model = PdasLogistic(path_type="gs")
model.fit(X=train_X, y=train_y)
print(model.predict(test_X))

