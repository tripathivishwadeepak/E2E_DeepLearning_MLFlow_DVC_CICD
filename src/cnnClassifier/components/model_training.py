import os
import urllib.request as request
import tensorflow as tf
import time
from zipfile import ZipFile
from cnnClassifier.utils.common import read_yaml
from cnnClassifier.constants import PARAMS_FILE_PATH
from pathlib import Path
from cnnClassifier.entity.config_entity import ModelTrainingConfig

class Model_Training:
    def __init__(self, config: ModelTrainingConfig):
        self.config = config
        self.train_generator = None
        self.valid_generator = None
        self.model = None
        
        # Read params from the standard params file
        try:
            self.params = read_yaml(PARAMS_FILE_PATH)
            # Check training flag, default to True if not specified
            self.should_train = self.params.get('TRAINING', {}).get('SHOULD_TRAIN', True)
        except Exception as e:
            print(f"Error reading params file: {e}")
            self.params = {}
            self.should_train = True

    def get_base_model(self):
        self.model = tf.keras.models.load_model(
            self.config.updated_base_model_path
        )

    def train_valid_generator(self):
        datagenerator_kwargs = dict(
            rescale = 1./255,
            validation_split = 0.20
        )

        dataflow_kwargs = dict(
            target_size = self.config.params_image_size[:-1],
            batch_size = self.config.params_batch_size,
            interpolation = "bilinear"
        )

        valid_datagenerator = tf.keras.preprocessing.image.ImageDataGenerator(
            **datagenerator_kwargs
        )

        self.valid_generator = valid_datagenerator.flow_from_directory(
            directory = self.config.training_data,
            subset = "validation",
            shuffle = False,
            **dataflow_kwargs
        )

        if self.config.params_is_augmentation:
            train_datagenerator = tf.keras.preprocessing.image.ImageDataGenerator(
                rotation_range = 40,
                horizontal_flip = True,
                width_shift_range = 0.2,
                height_shift_range = 0.2,
                shear_range = 0.2,
                zoom_range = 0.2,
                **datagenerator_kwargs
            )
        else:
            train_datagenerator = valid_datagenerator

        self.train_generator = train_datagenerator.flow_from_directory(
            directory = self.config.training_data,
            subset = 'training',
            shuffle = True,
            **dataflow_kwargs
        )

    def train(self, callback_list: list = None):
        # Check if training is disabled
        if not self.should_train:
            print("Training is disabled. Attempting to load existing model.")
            
            # Check if a trained model already exists
            if os.path.exists(self.config.training_model_path):
                print(f"Loading existing model from {self.config.training_model_path}")
                return tf.keras.models.load_model(self.config.training_model_path)
            
            raise ValueError("Training is disabled and no existing model found.")

        # Ensure base model and generators are loaded
        if self.model is None:
            self.get_base_model()
        
        if self.train_generator is None or self.valid_generator is None:
            self.train_valid_generator()

        # Calculate steps
        self.steps_per_epoch = self.train_generator.samples // self.train_generator.batch_size
        self.validation_steps = self.valid_generator.samples // self.valid_generator.batch_size

        # Prepare callbacks (if any)
        callbacks = callback_list or []

        # Perform training
        self.model.fit(
            self.train_generator,
            epochs = self.config.params_epochs,
            steps_per_epoch = self.steps_per_epoch,
            validation_steps = self.validation_steps,
            validation_data = self.valid_generator,
            callbacks = callbacks
        )

        # Save the trained model
        self.save_model(
            path = self.config.training_model_path,
            model = self.model
        )

        return self.model

    @staticmethod
    def save_model(path: Path, model: tf.keras.Model):
        model.save(path)