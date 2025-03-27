# E2E_DeepLearning_MLFlow_DVC_CICD
End to End Kidney Disease Classification

## Workflows
1. Update config.yaml
2. Update secrets.yaml [Optional]
3. Update params.yaml
4. Update the entity
5. Update the configuration manager in src config
6. Update the components
7. Update the pipeline
8. Update the main.py
9. Update the dvc.yaml
10. Create the app.py

# How to run?

### STEPS:
Clone the repository

```bash
https://github.com/tripathivishwadeepak/E2E_DeepLearning_MLFlow_DVC_CICD
```

### Step 01 - Create an conda environment after opening the repository

```bash
conda create -n cnnClassifier python=3.9.12 -y
````

```bash
conda activate cnnClassifier
```

### Step 02 - Install the requirements.txt 

```bash
pip install -r requirements.txt
```

### Step 03[Optional] - To avoid everytime data downloading, made following changes in stage_01_data_ingestion file under pipeline directory.

```bash
# Only download if the file doesn't exist
if not os.path.exists(data_ingestion_config.local_data_file):
    data_ingestion.download_file()
        
# Only extract if the directory is empty
if not os.listdir(data_ingestion_config.unzip_dir):
    data_ingestion.extract_zip_file()
```

### Step 04[Optional] - Since Model Training is usually heavy both on resources and time on normal system to avoid everytime running the model training do the add following line inside your *params.yaml* file and and then use the code of component folder.

```bash
TRAINING:
  SHOULD_TRAIN: False  # Set to True when you want to train
```


### Step 05 (MLFLOW) -
[Documentation](https://mlflow.org/docs/latest/index.html)

##### cmd
- mlflow ui

### dagshub
[dagshub](https://dagshub.com/)

```
MLFLOW_TRACKING_URI =
"https://dagshub.com/tripathivishwadeepak/E2E_DeepLearning_MLFlow_DVC_CICD.mlflow"
```
```
MLFLOW_TRACKING_USERNAME = "tripathivishwadeepak"
```
```
MLFLOW_TRACKING_PASSWORD = "c5e1c9532cc301ea889416e189cae21fc1cceb7b"
```
python script.py

Run this to set as env variables:
```bash
set MLFLOW_TRACKING_URI=https://dagshub.com/tripathivishwadeepak/E2E_DeepLearning_MLFlow_DVC_CICD.mlflow
set MLFLOW_TRACKING_USERNAME=tripathivishwadeepak
set MLFLOW_TRACKING_PASSWORD=c5e1c9532cc301ea889416e189cae21fc1cceb7b
```