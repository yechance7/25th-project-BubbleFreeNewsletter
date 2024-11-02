# 25th-project-BubbleFreeNewsletter
25기 신입기수 프로젝트 - 필터버블 해소를 위한 뉴스레터 <br />
Please refer to [필터버블 해소를 위한 뉴스레터](docs/project_final.pdf) for detailed project information.

## Prerequisites
 ```bash
- vessel server : 3090 GPU
- python==3.10
- pytorch==1.12.1
- CUDA==11.5
- transformers==4.44.0
 ```

## Directory
   ```bash
   ├── README.md
├── Ybigta.session.sql
├── be
│   ├── __pycache__
│   ├── api_upload.py
│   └── streamlit_demo.py
├── bub
│   ├── bin
│   ├── include
│   ├── lib
│   ├── lib64 -> lib
│   └── pyvenv.cfg
├── checkpoints
│   ├── model_epoch_3_val_loss_0.0895.pt
│   └── model_epoch_4_val_loss_0.1095.pt
├── db
│   ├── add_inference.py
│   ├── db.ini
│   ├── db_upload.py
│   ├── json
│   └── make_json.py
├── docs
│   ├── CONTRIBUTING.md
│   ├── MEETINGS.md
│   ├── PROJECT.pdf
│   └── TEAM.md
├── fe
│   ├── node_modules
│   ├── package-lock.json
│   ├── package.json
│   ├── public
│   └── src
├── imsuviiix.session.sql
├── kpfbert
│   ├── BERT-MediaNavi.pdf
│   ├── LICENSE
│   ├── README.md
│   ├── config.json
│   ├── pytorch_model.bin
│   ├── special_tokens_map.json
│   ├── tf_model.h5
│   ├── tokenizer.json
│   ├── tokenizer_config.json
│   └── vocab.txt
├── module
│   ├── __pycache__
│   ├── args.py
│   ├── bubble_free_BERT
│   ├── bubble_free_tokenizer
│   ├── config.yaml
│   ├── data_preprocessing.py
│   ├── dataset.py
│   ├── model_infer.py
│   ├── model_test.py
│   ├── model_train.py
│   ├── save_model.py
│   ├── split.py
│   ├── test_plot.py
│   └── view_data.py
├── real_time_scraper
│   ├── __pycache__
│   ├── db.ini
│   ├── db_upload.py
│   ├── dont_delete
│   ├── make_csv.py
│   ├── make_json.py
│   ├── new_data
│   ├── rt_main.py
│   ├── rt_scraper.py
│   ├── scrap.sh
│   ├── scrapers
│   └── update_inference.py
├── requirements.txt
└── src
    ├── article_data
    ├── data
    ├── preprocessing
    ├── raw_data
```
    

## Team Operation and Collaboration
- **Documentation**: <br>
For detailed team information, refer to [TEAM](docs/TEAM.md). <br>Our team meeting logs are available at [MEETINGS](docs/MEETINGS.md).
## Contributing

- **Cooperation**: <br>
For the cooperation rules, please review our [Collaboration Guidelines](docs/CONTRIBUTING.md) for details on how to participate.
