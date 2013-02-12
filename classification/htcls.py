#@tag 

import os
import glob
import random


from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.naive_bayes import MultinomialNB, GaussianNB, BernoulliNB



def split_dataset(nzfiles, nonnzfiles):
    """ Split the dataset into test/train partitions.

    Returns a dictionary keyed to:
        'train_nz'
        'train_nonnz'
        'test_nz'
        'test_nonnz', 
    each of which yield an iterable over filepaths.

    """

    sets = {}

    random.shuffle(nzfiles)
    random.shuffle(nonnzfiles)

    h_nz = len(nzfiles) / 2
    h_nonnz = len(nonnzfiles) /2

    sets['train_nz'] = nzfiles[h_nz:]
    sets['test_nz'] = nzfiles[:h_nz]
    sets['train_nonnz'] = nonnzfiles[h_nonnz:]
    sets['test_nonnz'] = nonnzfiles[:h_nonnz]

    return sets



if __name__ == "__main__":

    datapath = 'data/'

    nzfiles =  glob.glob(datapath + 'nz/*')
    nonnzfiles = glob.glob(datapath + 'nonnz/*')

    sets = split_dataset(nzfiles, nonnzfiles)
   
    train_nz = sets['train_nz']
    train_nonnz = sets['train_nonnz']   
    training_set = train_nz + train_nonnz 
    training_labels = ['nz']*len(train_nz) + ['nonnz']*len(train_nonnz)

    test_nz = sets['test_nz']
    test_nonnz = sets['test_nonnz']
    testing_set = test_nz + test_nonnz
    testing_labels = ['nz']*len(test_nz) + ['nonnz']*len(test_nonnz)

    cv = CountVectorizer(input='filename', stop_words='english')
    train_X = cv.fit_transform(training_set)
    test_X = cv.transform(testing_set)

    # t = TfidfTransformer(use_idf=True, smooth_idf=True, sublinear_tf=True)
    # train_X = t.fit_transform(train_X)
    # test_X = t.fit_transform(test_X)

    mnb = MultinomialNB()
    mnb.fit(train_X, training_labels)

    print "Mean accuracy: "
    print "     train_X: {0}".format(mnb.score(train_X, training_labels))
    print "     test_X:  {0}".format(mnb.score(test_X, testing_labels))



