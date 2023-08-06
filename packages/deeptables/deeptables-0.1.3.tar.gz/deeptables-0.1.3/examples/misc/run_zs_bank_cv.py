# -*- coding:utf-8 -*-
__author__ = 'yangjian'
"""

"""

from deeptables.models.deeptable import DeepTable, ModelConfig
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score
import pandas as pd

import warnings
warnings.filterwarnings("ignore")

import logging

logging.basicConfig(level=logging.DEBUG)
data = pd.read_csv('datasets/zs_bank.csv', encoding='gb2312')
#datasets = datasets.head(1000)
data['TARGET'] = data['bad_rate'].apply(lambda x: 0 if x<=0 else 1)
data.drop(['No.','md5','bad_rate','ovdu_rate'],axis=1,inplace=True)
data['create_day'] = data['create_day'].astype('object')
data = data.astype('str')
data['TARGET'] = data['TARGET'].astype('int')
full_x = data.copy()
full_y = full_x.pop('TARGET')

df_train, df_test = train_test_split(data, test_size=0.2, random_state=100)

y = df_train.pop('TARGET')
X = df_train

y_test= df_test.pop('TARGET')

conf = ModelConfig(fixed_embedding_dim=False,
                   nets=['dnn_nets'],
                   embeddings_output_dim=4,
                   auto_discrete=True,
                   apply_class_weight=True,
                   apply_gbm_features=True,
                   dnn_units=((128, 0, False),))
#dnn_units = ((1024, 0, False), (256, 0, False), (128, 0, False)))

dt = DeepTable(config=conf)

modelset, oof_preds, test_preds = dt.fit_cross_validation(X, y,df_test, num_folds=5, epochs=2)
print(roc_auc_score(y,oof_preds))
print(roc_auc_score(y_test,test_preds))

