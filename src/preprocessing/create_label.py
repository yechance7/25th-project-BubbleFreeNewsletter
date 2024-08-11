import os
import pandas as pd

def process_csv_files(directory):
    all_dataframes = []
    
    for filename in os.listdir(directory):
        if filename.endswith(".csv"):
            # 파일 경로
            file_path = os.path.join(directory, filename)
            
            # CSV 파일 읽기
            df = pd.read_csv(file_path)
            
            # 'url' 컬럼 제거
            if 'URL' in df.columns:
                df = df.drop(columns=['URL'])
            
            # 'label' 컬럼 추가, 파일명에서 확장자를 제거하고 label로 사용
            label = os.path.splitext(filename)[0]
            if label in ['chosun_article', 'donga_article', 'joongang_article']:
                df['label'] = 0
            else:
                df['label'] = 1
            
            # 데이터프레임 리스트에 추가
            all_dataframes.append(df)
    
    # 모든 데이터프레임을 하나로 합치기
    combined_df = pd.concat(all_dataframes, ignore_index=True)
    
    return combined_df

# 지정한 디렉토리 경로
directory_path = 'src/article_data'

# 함수 실행 및 결과 반환
result_df = process_csv_files(directory_path)

# 합쳐진 데이터프레임을 새로운 CSV로 저장
result_df.to_csv(os.path.join(directory_path, 'train_article.csv'), index=False)

print("All CSV files processed and combined into 'train_article.csv'")
