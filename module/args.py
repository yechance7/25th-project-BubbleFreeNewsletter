from argparse import ArgumentParser

def get_args(args=None):
    parser = ArgumentParser(description='Bubble_free_news_by_BERT')
    parser.add_argument("--model_path", required=False, default="kpfbert", type=str)
    parser.add_argument("--data_path", required=False, default='src/article_data/train_articles.csv', type=str)
    parser.add_argument("--train_data_path", required=False, default='', type=str)
    parser.add_argument("--out_dir", required=False, default='', type=str)
    parser.add_argument("--num_classes", required=False, default='2', type=int)
    parser.add_argument("--max_len", required=False, default='512', type=int)
    parser.add_argument("--lr", required=False, default='1e-5', type=float)
    parser.add_argument("--batch_size", required=False, default='32', type=int)
    parser.add_argument("--epoch", required=False, default='5', type=int)
    
    if args is None:
        params = parser.parse_args()
    else:
        params = parser.parse_args(args)


    return params