#! ./venv/bin/activate

import pandas as pd
import xgboost as xgb
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error
from sklearn.datasets import load_boston
from sklearn.model_selection import train_test_split

from app.helpers import gen_df

df = gen_df(asset_name='ethereum', days=30)

for asset_name in ['bitcoin', 'sdefi']:
    temp_df = gen_df(asset_name=asset_name, days=30)
    df = pd.merge(df, temp_df, on="date")

print(df)
print(df.info(verbose=True))
quit()

boston = load_boston()

data = pd.DataFrame(boston.data)
data.columns = boston.feature_names
data['PRICE'] = boston.target

X, y = data.iloc[:, :-1], data.iloc[:, -1]

data_matrix = xgb.DMatrix(data=X, label=y)

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=123)

xg_reg = xgb.XGBRegressor(objective='reg:linear', colsample_bytree=0.3,
                          learning_rate=0.1, max_depth=5, alpha=10,
                          n_estimators=10)

xg_reg.fit(X_train, y_train)

preds = xg_reg.predict(X_test)
print('> X_test:', X_test)
print('> Preds:', preds)
print('> Len:', len(preds))
print('> Y Test:', y_test)
rmse = np.sqrt(mean_squared_error(y_test, preds))
print('> RMSE:', rmse)

params = {
    "objective": "reg:linear",
    "colsample_bytree": 0.3,
    "learning_rate": 0.1,
    "max_depth": 5,
    "alpha": 10
}

cv_results = xgb.cv(dtrain=data_matrix, params=params, nfold=3,
                    num_boost_round=50, early_stopping_rounds=10,
                    metrics="rmse", as_pandas=True, seed=123)

print(cv_results.head())
print('> Last boosting metric', (cv_results["test-rmse-mean"]).tail(1))

xg_reg = xgb.train(params=params, dtrain=data_matrix, num_boost_round=10)

xgb.plot_tree(xg_reg, num_trees=0)
plt.rcParams["figure.figsize"] = [100, 20]
plt.show()

xgb.plot_importance(xg_reg)
plt.rcParams["figure.figsize"] = [5, 5]
plt.show()
