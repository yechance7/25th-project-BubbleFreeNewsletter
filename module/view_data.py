
import pandas as pd

def view_data(file_path):
    try:
        train_df = pd.read_csv(f'{file_path}/train.csv')
        val_df = pd.read_csv(f'{file_path}/valid.csv')
        test_df = pd.read_csv(f'{file_path}/test.csv')
    except Exception as e:
        print(f"Can't not open the file: {e}")

    # Check label balance for each dataset
    print("Label Distribution in the Training Set:")
    print(train_df['label'].value_counts(normalize=False))
    print()
    
    print("Label Distribution in the Validation Set:")
    print(val_df['label'].value_counts(normalize=False))
    print()
    
    print("Label Distribution in the Test Set:")
    print(test_df['label'].value_counts(normalize=False))
    print()


if __name__ == "__main__":
    file_path = 'src/data'
    view_data(file_path)