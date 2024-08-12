from sklearn.utils import resample
import re
import pandas as pd
import os
from args import get_args

def clean_text(text):
    # 이메일 주소 제거
    text = re.sub(r'\S+@\S+\.\S+', '', text)
    # 특정 기호로 시작하는 패턴 제거 (예: ⓒ뉴시스)
    text = re.sub(r'ⓒ\S+', '', text)
    # 기자 이름 제거 (예: 000 기자)
    text = re.sub(r'\w+ 기자', '', text)
    # 기타 불필요한 텍스트 제거
    text = re.sub(r'크게보기', '', text)
    # 괄호로 감싸진 문자열 제거
    text = re.sub(r'\(.*?\)', '', text) # 소괄호 ()
    text = re.sub(r'<[a-zA-Z][^>]*>', '', text) #html tag 제거 
    return text

def downsampling(df):

  df_majority = df[df['label'] == 0]
  df_minority = df[df['label'] == 1]

  df_majority_downsampled = resample(df_majority,
                                     replace=False,
                                     n_samples=len(df_minority),
                                     random_state=42)
  df_downsampled = pd.concat([df_majority_downsampled, df_minority])
  return df_downsampled


if __name__ == '__main__':
    #train dataset 경로와 저장 경로 설정
    args = ["--data_path", "src/article_data/train_articles.csv","--out_dir", "src/article_data/"]
    arg = get_args(args)

    filepath = arg.data_path
    output_dir = arg.out_dir    

    df = pd.read_csv(filepath, encoding='utf-8')
    df.dropna(inplace=True)
    df.drop_duplicates(inplace=True)
    df['Article'] = df['Article'].apply(clean_text)
    df.to_csv(os.path.join(output_dir,'trian_articles_processed.csv'), index=False)

    down_df = downsampling(df)

    label_counts = down_df['label'].value_counts()
    print(label_counts)