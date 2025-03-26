import os
from pathlib import Path
from cnnClassifier.config.configuration import ConfigurationManager
from cnnClassifier.components.data_ingestion import DataIngestion
from cnnClassifier import logger

STAGE_NAME = "Data Ingestion Stage"

class DataIngestionTrainingPipeline:
    def __init__(self):
        pass

    def main(self):
        # config = ConfigurationManager()
        # data_ingestion_config = config.get_data_ingestion_config()
        # data_ingestion = DataIngestion(config = data_ingestion_config)
        # data_ingestion.download_file()
        # data_ingestion.extract_zip_file()


        config = ConfigurationManager()
        data_ingestion_config = config.get_data_ingestion_config()
        data_ingestion = DataIngestion(config=data_ingestion_config)
        
        # Only download if the file doesn't exist
        if not os.path.exists(data_ingestion_config.local_data_file):
            data_ingestion.download_file()
        
        # Only extract if the directory is empty
        if not os.listdir(data_ingestion_config.unzip_dir):
            data_ingestion.extract_zip_file()

if __name__ == '__main__':
    try:
        logger.info(f">>>>> stage {STAGE_NAME} started <<<<<")
        obj = DataIngestionTrainingPipeline()
        obj.main()
        logger.info(f">>>>> stage {STAGE_NAME} completed <<<<< \n\n x===============x")
    except Exception as e:
        logger.exception(e)
        raise e