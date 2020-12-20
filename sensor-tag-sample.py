# -*- coding: utf-8 -*-
#By Jonathan Williams, October 2020
import pandas as pd
import numpy as np
from sklearn import svm
from sklearn.metrics import accuracy_score, confusion_matrix
from sklearn.linear_model import  LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier


from sklearn.svm import SVC

def csv_data(filename):
    df = pd.read_csv(filename)
    #data = df.as_matrix(columns = ['Ambiant Temp C', 'Object Temp C'])
    #data = df.as_matrix(columns = [ 'Object Temp C'])
    #data = df.as_matrix(columns = ['Brightness']) 
    data = df[["Brightness"]].values
    return data

def compute_accuracy(clf, data, target):
    y = clf.predict(data)
    score = accuracy_score(target, y)
    return score

def print_accuracy(clf, data1, target1, data2, target2):
    print("- Training set", compute_accuracy(clf, data1, target1))
    print("- Testing set", compute_accuracy(clf, data2, target2))

def print_gridsearch_summary(clf, parameters):
    print("parameters:")
    print(parameters)
    print("Best parameters set:")
    best_parameters = clf.best_estimator_.get_params()
    for param_name in sorted(parameters.keys()):
        print("\t%s: %r" % (param_name, best_parameters[param_name]))


def tune_svm_lin(data, target, rseed=42, verbose=1):
    print("")
    print("Tuning Linear SVM ...")
    print("--------------------------------------------------------------------------------")
    parameters = {
                  'C': [0.1, 1, 10, 100]
    }

    classifier = SVC(kernel='linear', random_state=rseed)
    clf = GridSearchCV(classifier, parameters, verbose=verbose)
    clf.fit(data, target)

    print_gridsearch_summary(clf, parameters)

    return clf

def tune_knn(data, target, rseed=42, verbose=1):
    print("")
    print("Tuning K-NN ")
    print("--------------------------------------------------------------------------------")
    parameters = {
                    'n_neighbors': [1,2,5,10]
    }
    classifier = KNeighborsClassifier()
    clf = GridSearchCV(classifier, parameters, verbose=verbose)
    clf.fit(data, target)

    print_gridsearch_summary(clf, parameters)
    
    return clf

def tune_decision_tree(data, target, rseed=42, verbose=1):
    print("")
    print("Tuning Decision Tree ")
    print("--------------------------------------------------------------------------------")
    parameters = {
                'max_depth': [1, 10, 100],
                'max_features': ['auto', 1, 3, 30]
    }
    classifier = DecisionTreeClassifier()
    clf = GridSearchCV(classifier, parameters, verbose=verbose)
    clf.fit(data, target)

    print_gridsearch_summary(clf, parameters)
    
    return clf

def tune_random_forest(data, target, rseed=42, verbose=1):
    print("")
    print("Tuning Random Forest ")
    print("--------------------------------------------------------------------------------")
    parameters = {
                'max_depth': [1, 10, 100],
                'max_features': ['auto', 1, 3, 30],
                'n_estimators': [2, 10, 100]
    }
    classifier = RandomForestClassifier()
    clf = GridSearchCV(classifier, parameters, verbose=verbose)
    clf.fit(data, target)

    print_gridsearch_summary(clf, parameters)
    
    return clf

if __name__ == "__main__":

    # Make binary data from two reading files

	#Obtain the brightness samples obtained at the bright location
    X_bright = csv_data('record-bright.csv') 
    y_bright = np.ones(X_bright.shape[0])

	#Obtain the brightness samples obtained at the dark location
    X_dark = csv_data('record-dark.csv')
    y_dark = np.zeros(X_dark.shape[0])

    X = np.concatenate((X_bright, X_dark), axis=0)
    y = np.concatenate((y_bright, y_dark), axis=0)
    data1, data2, target1, target2 = train_test_split(X, \
                                                      y, \
                                                      test_size=0.8, \
                                                      random_state=42)
    # Train classifiers
    verbosity = 1
    
    clf_svm_lin = tune_svm_lin(data1, target1, verbose=verbosity)
    clf_knn = tune_knn(data1, target1, verbose=verbosity)
    clf_decision_tree = tune_decision_tree(data1, target1, verbose=verbosity)
    clf_random_forest = tune_random_forest(data1, target1, verbose=verbosity)
	
    # Print performance
    print("")
    print("Classifier Performance")
    print("--------------------------------------------------------------------------------")
    print("")

    print("")
    print("Accuracy with linear SVM and parameter tuning:")
    print_accuracy(clf_svm_lin, data1, target1, data2, target2)
    print("")
    print("Accuracy with k-nn classifier with  parameter tuning:")
    print_accuracy(clf_knn, data1, target1, data2, target2)
    print("")
    print("Accuracy with a decision tree and parameter tuning:")
    print_accuracy(clf_decision_tree, data1, target1, data2, target2)
    print("")
    print("Accuracy with a random forest and parameter tuning:")
    print_accuracy(clf_random_forest, data1, target1, data2, target2)
    

    
