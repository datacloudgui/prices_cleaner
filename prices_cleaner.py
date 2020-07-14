import argparse
import logging
logging.basicConfig(level=logging.INFO)
import hashlib

import pandas as pd

logger = logging.getLogger(__name__)

def main(filename, today):
    
    logger.info('Starting cleaning process')

    df = _read_data(filename)
    df_nan=df.isnull().sum().sum()
    logger.info('NaN values {nans}'.format(nans=df_nan))

    if df_nan!=0:
        logger.info('Droping rows with NaN values')
        df = df.dropna()
    
    df = _add_articles_uid_column(df)

    logger.info('Droping rows with NaN values')
    df = df.drop_duplicates()
    df = _convert_price_to_number(df, today)
    df.to_csv('clean_'+filename[2::])

    return df


def _read_data(filename):
    logger.info('Reading file {}'.format(filename))

    return pd.read_csv(filename)

def _add_articles_uid_column(df):
    logger.info('Adding uniques IDs from link')
    uids = _calculate_uids_with_link(df)
    df['uid'] = uids

    return df.set_index('uid')

def _calculate_uids_with_link(df):
    return (df
            .apply(lambda row: hashlib.md5(bytes(row['link'].encode())), axis=1)
            .apply(lambda hash_object: hash_object.hexdigest())
            )

def _convert_price_to_number(df, today):
    logger.info('Converting column price to number')
    stripped_price = (df
                        .apply(lambda row: row[today], axis=1)
                        .apply(lambda precio: precio.replace('$',''))
                        .apply(lambda precio: precio.replace('.',''))
                        .apply(lambda precio: precio.strip())
                    )
    df[today]=stripped_price
    df[today]=pd.to_numeric(df[today])

    return df


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('filename',
                        help='The path to the dirty data',
                        type=str)
    parser.add_argument('today',
                        help='The date of the dirty file',
                        type=str)

    args = parser.parse_args()

    df = main(args.filename, args.today)

    logger.info('The final size of the data is {}'.format(df.shape[0]))