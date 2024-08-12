from sklearn.utils import resample
import re
import pandas as pd
import os
from args import get_args
from sklearn.model_selection import train_test_split

def downsampling(df, total_samples=54370): # original dataset: 54372 samples
    # adjust to minority
    df_majority = df[df['label'] == 0]
    df_minority = df[df['label'] == 1]

    # balancing
    num_samples_per_class = total_samples // 2

    df_majority= resample(df_majority,
                          replace=False,
                          n_samples=num_samples_per_class,
                          random_state=42)

    df_minority = resample(df_minority,
                           replace=False,
                           n_samples=num_samples_per_class,
                           random_state=42)

    df_downsampled = pd.concat([df_majority, df_minority])
    
    return df_downsampled


if __name__ == '__main__':
    #dataset 경로와 저장 경로 설정
    args = ["--data_path", "../src/article_data/trian_articles_processed.csv","--out_dir", "../src/data/"]
    arg = get_args(args)

    filepath = arg.data_path
    output_dir = arg.out_dir    

    # read data
    try:
        df = pd.read_csv(filepath, encoding='utf-8')
    except Exception as e:
        print(f"Can't not open the file: {e}")

    # down_sampling
    df = downsampling(df)

    # Split the dataset into train, validation, and test sets
    train_df, temp_df = train_test_split(df, test_size=0.2, random_state=42, stratify=df['label'])
    valid_df, test_df = train_test_split(temp_df, test_size=0.5, random_state=42, stratify=temp_df['label'])

    # check directory, if does not exists, create
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    #save to directory
    train_df.to_csv(os.path.join(output_dir, 'train.csv'), index=False)
    valid_df.to_csv(os.path.join(output_dir, 'valid.csv'), index=False)
    test_df.to_csv(os.path.join(output_dir, 'test.csv'), index=False)