from rt_scraper import RTScraper
import os
import shutil

"""
    빅카인즈에서 엑셀 파일 다운로드 후 현재 디렉토리 new_data 폴더에 저장하는 코드
"""

if __name__ == "__main__":
    test = RTScraper()
    test.scrap()
    
    # 다운로드 폴더에서 엑셀파일을 가져오는 코드
    download_dir = os.path.join(os.path.expanduser('~'), 'Downloads')  # Default download folder
    current_dir = os.getcwd()  # Current working directory
    new_data_dir = os.path.join(current_dir, 'new_data')  # new_data folder within the current directory

    # Create the new_data directory if it doesn't exist
    if not os.path.exists(new_data_dir):
        os.makedirs(new_data_dir)

    # Find the latest downloaded file in the download folder
    files = os.listdir(download_dir)
    paths = [os.path.join(download_dir, file) for file in files if os.path.isfile(os.path.join(download_dir, file))]
    latest_file = max(paths, key=os.path.getctime)  # Find the most recently created/modified file
    destination_path = os.path.join(new_data_dir, os.path.basename(latest_file))

    # Remove the existing file if it exists
    if os.path.exists(destination_path):
        os.remove(destination_path)

    # Move the file to the new_data directory
    shutil.move(latest_file, new_data_dir)

    print(f"Moved {os.path.basename(latest_file)} to {new_data_dir}")
    