import re
import string

import numpy as np
import pandas as pd
from sklearn.externals import joblib
from sklearn.feature_extraction import text
import sklearn.preprocessing as sk_prep

from .base import BaseTransformer


class WordListFilter(BaseTransformer):
    def __init__(self, word_list_filepath):
        self.word_set = self._read_data(word_list_filepath)

    def transform(self, X):
        X = self._transform(X)
        return {'X': X}

    def _transform(self, X):
        X = pd.DataFrame(X, columns=['text']).astype(str)
        X['text'] = X['text'].apply(self._filter_words)
        return X['text'].values

    def _filter_words(self, x):
        x = x.lower()
        x = ' '.join([w for w in x.split() if w in self.word_set])
        return x

    def _read_data(self, filepath):
        with open(filepath, 'r+') as f:
            data = f.read()
        return set(data.split('\n'))

    def load(self, filepath):
        return self

    def save(self, filepath):
        joblib.dump({}, filepath)


class TextCleaner(BaseTransformer):
    def __init__(self, drop_punctuation, drop_newline, drop_multispaces,
                 all_lower_case, fill_na_with, deduplication_threshold):
        self.drop_punctuation = drop_punctuation
        self.drop_newline = drop_newline
        self.drop_multispaces = drop_multispaces
        self.all_lower_case = all_lower_case
        self.fill_na_with = fill_na_with
        self.deduplication_threshold = deduplication_threshold

    def transform(self, X):
        X = pd.DataFrame(X, columns=['text']).astype(str)
        X['text'] = X['text'].apply(self._transform)
        if self.fill_na_with:
            X['text'] = X['text'].fillna(self.fill_na_with).values
        return {'X': X['text'].values}

    def _transform(self, x):
        if self.all_lower_case:
            x = self._lower(x)
        if self.drop_punctuation:
            x = self._remove_punctuation(x)
        if self.drop_newline:
            x = self._remove_newline(x)
        if self.drop_multispaces:
            x = self._substitute_multiple_spaces(x)
        if self.deduplication_threshold is not None:
            x = self._deduplicate(x)
        return x

    def _lower(self, x):
        return x.lower()

    def _remove_punctuation(self, x):
        return re.sub(r'[^\w\s]', ' ', x)

    def _remove_newline(self, x):
        x = x.replace('\n', ' ')
        x = x.replace('\n\n', ' ')
        return x

    def _substitute_multiple_spaces(self, x):
        return ' '.join(x.split())

    def _deduplicate(self,x):
        word_list = x.split()
        num_words = len(word_list)
        if num_words ==0:
            return x
        else:
            num_unique_words = len(set(word_list))
            unique_ratio = num_words/num_unique_words
            if unique_ratio > self.deduplication_threshold:
                x = ' '.join(x.split()[:num_unique_words])
            return x

    def load(self, filepath):
        params = joblib.load(filepath)
        self.drop_punctuation = params['drop_punctuation']
        self.all_lower_case = params['all_lower_case']
        self.fill_na_with = params['fill_na_with']
        return self

    def save(self, filepath):
        params = {'drop_punctuation': self.drop_punctuation,
                  'all_lower_case': self.all_lower_case,
                  'fill_na_with': self.fill_na_with,
                  }
        joblib.dump(params, filepath)


class XYSplit(BaseTransformer):
    def __init__(self, x_columns, y_columns):
        self.x_columns = x_columns
        self.y_columns = y_columns

    def transform(self, meta, train_mode):
        X = meta[self.x_columns].values
        if train_mode:
            y = meta[self.y_columns].values
        else:
            y = None

        return {'X': X,
                'y': y}

    def load(self, filepath):
        params = joblib.load(filepath)
        self.columns_to_get = params['x_columns']
        self.target_columns = params['y_columns']
        return self

    def save(self, filepath):
        params = {'x_columns': self.x_columns,
                  'y_columns': self.y_columns
                  }
        joblib.dump(params, filepath)


class TfidfVectorizer(BaseTransformer):
    def __init__(self, **kwargs):
        self.vectorizer = text.TfidfVectorizer(**kwargs)

    def fit(self, text):
        self.vectorizer.fit(text)
        return self

    def transform(self, text):
        return {'features': self.vectorizer.transform(text)}

    def load(self, filepath):
        self.vectorizer = joblib.load(filepath)
        return self

    def save(self, filepath):
        joblib.dump(self.vectorizer, filepath)


class TextCounter(BaseTransformer):
    def transform(self, X):
        X = pd.DataFrame(X, columns=['text']).astype(str)
        X = X['text'].apply(self._transform)
        X['caps_vs_length'] = X.apply(lambda row: float(row['upper_case_count']) / float(row['char_count']), axis=1)
        X['num_symbols'] = X['text'].apply(lambda comment: sum(comment.count(w) for w in '*&$%'))
        X['num_words'] = X['text'].apply(lambda comment: len(comment.split()))
        X['num_unique_words'] = X['text'].apply(lambda comment: len(set(w for w in comment.split())))
        X['words_vs_unique'] = X['num_unique_words'] / X['num_words']
        X['mean_word_len'] = X['text'].apply(lambda x: np.mean([len(w) for w in str(x).split()]))
        X.drop('text', axis=1, inplace=True)
        X.fillna(0.0, inplace=True)
        return {'X': X}

    def _transform(self, x):
        features = {}
        features['text'] = x
        features['char_count'] = char_count(x)
        features['word_count'] = word_count(x)
        features['punctuation_count'] = punctuation_count(x)
        features['upper_case_count'] = upper_case_count(x)
        features['lower_case_count'] = lower_case_count(x)
        features['digit_count'] = digit_count(x)
        features['space_count'] = space_count(x)
        features['newline_count'] = newline_count(x)
        return pd.Series(features)

    def load(self, filepath):
        return self

    def save(self, filepath):
        joblib.dump({}, filepath)


class Normalizer(BaseTransformer):
    def __init__(self):
        self.normalizer = sk_prep.Normalizer()

    def fit(self, X):
        self.normalizer.fit(X)
        return self

    def transform(self, X):
        X = self.normalizer.transform(X)
        return {'X': X}

    def load(self, filepath):
        self.normalizer = joblib.load(filepath)
        return self

    def save(self, filepath):
        joblib.dump(self.normalizer, filepath)


def char_count(x):
    return len(x)


def word_count(x):
    return len(x.split())


def newline_count(x):
    return x.count('\n')


def upper_case_count(x):
    return sum(c.isupper() for c in x)


def lower_case_count(x):
    return sum(c.islower() for c in x)


def digit_count(x):
    return sum(c.isdigit() for c in x)


def space_count(x):
    return sum(c.isspace() for c in x)


def punctuation_count(x):
    return occurence(x, string.punctuation)


def occurence(s1, s2):
    return sum([1 for x in s1 if x in s2])
