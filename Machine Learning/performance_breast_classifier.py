import argparse
import pandas as pd
from joblib import load
from sklearn.preprocessing import LabelEncoder
import sklearn.metrics as metrics

parser = argparse.ArgumentParser(description='*** Breast cancer classification test ***')
parser.add_argument("--test", required=True, type=str, help="Test set name or path")
args = parser.parse_args()

dataset_test = pd.read_csv(args.test)
dataset_test = dataset_test.drop('id',1)
dataset_test = dataset_test.dropna()
    
test_x_ext = dataset_test
test_y_ext = test_x_ext.pop('diagnosis')

#Encoding categorical data values // B = 0, M = 1
test_y_ext = LabelEncoder().fit_transform(test_y_ext)

clf = load('breast_best_classifier.joblib')

pred_y = clf.predict(test_x_ext)

confusion_matrix = metrics.confusion_matrix(test_y_ext, pred_y)
print('Matrice di confusione:\n{}\n'.format(confusion_matrix))
rec_score = metrics.recall_score(test_y_ext, pred_y)
acc_score = metrics.accuracy_score(test_y_ext, pred_y)
print('Recall: {}%'.format(round(rec_score*100,2)))
print('Accuracy: {}%'.format(round(acc_score*100,2)))