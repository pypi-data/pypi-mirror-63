# -*- coding:utf-8 -*-
__author__ = 'yangjian'
"""

"""
import pandas as pd
import os
from deeptables.utils import dt_logging

logger = dt_logging.get_logger(__name__)
basedir = os.path.dirname(__file__)


def load_cat_in_the_dat_ii_kaggle():
    print(f'Base dir:{basedir}')
    train = pd.read_csv(f'{basedir}/cat-in-the-dat-ii/train.csv')
    test = pd.read_csv(f'{basedir}/cat-in-the-dat-ii/test.csv')
    submission = pd.read_csv(f'{basedir}/cat-in-the-dat/sample_submission.csv')
    print(f'train shape:{train.shape}')
    print(f'test shape:{test.shape}')
    print(f'submission shape:{submission.shape}')
    return train, test, submission


def load_cat_in_the_dat_kaggle():
    print(f'Base dir:{basedir}')
    train = pd.read_csv(f'{basedir}/cat-in-the-dat/train.csv')
    test = pd.read_csv(f'{basedir}/cat-in-the-dat/test.csv')
    submission = pd.read_csv(f'{basedir}/cat-in-the-dat/sample_submission.csv')
    print(f'train shape:{train.shape}')
    print(f'test shape:{test.shape}')
    print(f'submission shape:{submission.shape}')
    return train, test, submission


def load_heart_disease_uci():
    print(f'Base dir:{basedir}')
    data = pd.read_csv(f'{basedir}/heart-disease-uci.csv')
    logger.info(f'data shape:{data.shape}')
    return data


def load_adult():
    print(f'Base dir:{basedir}')
    data = pd.read_csv(f'{basedir}/adult.csv', header=None)
    logger.info(f'data shape:{data.shape}')
    return data


def load_glass_uci():
    print(f'Base dir:{basedir}')
    data = pd.read_csv(f'{basedir}/glass_uci.csv', header=None)
    logger.info(f'data shape:{data.shape}')
    return data


def load_bank():
    logger.info(f'Base dir:{os.getcwd()}')
    data = pd.read_csv(f'{basedir}/bank.csv')
    logger.info(f'data shape:{data.shape}')
    return data


def load_home_credit_app():
    logger.info(f'Base dir:{os.getcwd()}')
    df_train = pd.read_csv(f'{basedir}/home-credit-default-risk/application_train.csv')
    df_test = pd.read_csv(f'{basedir}/home-credit-default-risk/application_test.csv')
    logger.info(f'df_train shape:{df_train.shape}, df_test shape:{df_test.shape}')

    return df_train, df_test
