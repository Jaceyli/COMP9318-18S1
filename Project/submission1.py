import math

import numpy as np
from sklearn import svm
from sklearn.feature_extraction.text import  CountVectorizer, TfidfVectorizer,TfidfTransformer
from sklearn.model_selection import GridSearchCV

import helper

'''
Version 5: 

1.Compute weight: CountVectorizer
2.Get the best parameters with grid search 
3.Train SVM with the best parameters
3.Modfiy test sample according to clf.coef
'''

def fool_classifier(test_data):  ## Please do not change the function defination...
    strategy_instance = helper.strategy()
    parameters = {}

    parameters['C'] = 1
    parameters['kernel'] = 'linear'
    parameters['degree'] = 3
    parameters['gamma'] = 'auto'
    parameters['coef0'] = 0

    vec = CountVectorizer(tokenizer = lambda x:x.split())
    # tfidf = TfidfVectorizer()
    data = []

    for line in strategy_instance.class0:
        data.append(' '.join(i for i in line))
    for line in strategy_instance.class1:
        data.append(' '.join(i for i in line))

    TFID = TfidfTransformer()
    X = TFID.fit_transform(vec.fit_transform(data))

    y = [0] * len(strategy_instance.class0) + [1] * len(strategy_instance.class1)

    clf = svm.SVC(kernel='linear', C=1)
    # clf = svm.SVC(kernel='linear', C=0.030999999999999996, class_weight="balanced")
    clf.fit(X,y)
    # print(clf.coef_)

    coef_dict = dict()
    coef = clf.coef_[0]
    for i in range(len(coef.indices)):
        coef_dict[coef.indices[i]] = coef.data[i]

    coef_pos = [i for i in coef_dict.items() if i[1] > 0]
    coef_neg = [i for i in coef_dict.items() if i[1] < 0]
    coef_pos = sorted(coef_pos, key=lambda x: x[1], reverse=True)
    coef_neg = sorted(coef_neg, key=lambda x: x[1], reverse=False)


    # delete:word_pos
    word_pos = [j[0] for i in coef_pos for j in vec.vocabulary_.items() if j[1] == i[0]][:1000]
    # add:word_neg
    word_neg = [j[0] for i in coef_neg for j in vec.vocabulary_.items() if j[1] == i[0]]


    # modify
    modified_data = './modified_data.txt'
    # modify operation
    with open(test_data, 'r') as test_file:
        with open(modified_data, 'w') as modified_file:
            for line in test_file:
                use_add = []
                use_dele = []
                words = line.strip().split(' ')
                words = list(set(words))
                dele = [i for i in word_pos if i in words]
                # print('d', len(dele), dele)
                count = 0
                for i in dele :


                    words.remove(dele[count])
                    use_dele.append(dele[count])
                    count += 1
                    if count==10:
                        break

                add_new = [i for i in word_neg if i not in words]

                for i in range(20 -  count):
                    words.append(add_new[i])
                    use_add.append(add_new[i])
               ## print(use_dele)
               ## print(use_add)

                use_dele=[]
                use_add=[]
                line = ' '.join(i for i in words)

                modified_file.write(line + '\n')
    modified_file.close()

    # predict test
    with open(test_data, 'r') as file1:
        data1 = [line.strip().split(' ') for line in file1]
    testdata = []
    for line in data1:
        testdata.append(' '.join(i for i in line))

    X_test = vec.transform(testdata)
    # X_test = tfidf.transform(testdata)
    y1 = clf.predict(X_test)
    ##print(y1)
    result = sum(y1) * 100 / 200  # test_data是1的概率
    ##print('Success = {}%'.format(result))

    # predict modify
    with open(modified_data, 'r') as file2:
        data2 = [line.strip().split(' ') for line in file2]
    testdata2 = []
    for line in data2:
        testdata2.append(' '.join(i for i in line))

    X_test2 = vec.transform(testdata2)
    # X_test2 = tfidf.transform(testdata2)
    ##print(X_test2.shape)
    # print(X_test.toarray())
    y2 = clf.predict(X_test2)
    ##print(y2)
    result2 = sum(y2) * 100 / 200  # test_data是1的概率
    ##print('Success = {}%'.format(result2))

    assert strategy_instance.check_data(test_data, modified_data)
    return strategy_instance  ## NOTE: You are required to return the instance of this class.

test_data='./test_data.txt'
fool_classifier(test_data)