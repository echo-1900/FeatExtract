# coding: utf-8

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_score,train_test_split
import pandas as pd
import numpy as np

all_data = pd.read_csv("test.csv",index_col=0)
label = all_data.iloc[:,-1]
feat = all_data.iloc[:,:-1]

xtrain,xtest,ytrain,ytest = train_test_split(feat,label,test_size=0.3)
clf = RandomForestClassifier(n_estimators=10)
clf.fit(xtrain,ytrain)
score = clf.score(xtest,ytest)

result = clf.feature_importances_

# cross_score = cross_val_score(clf,feat,label,cv=10)