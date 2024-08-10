# Animal Image Scrape and Predict

This repository showcases a full pipeline from web scraping images of animals to building and training a Convolutional Neural Network (CNN) model to predict the type of animal in an image. 

## Table of Contents

- [Introduction](#introduction)
- [Installation and Setup](#installation-and-setup)
- [Step 1: Scrape Animal Images](#step-1-scrape-animal-images)
- [Step 2: Convert Images to Vectors](#step-2-convert-images-to-vectors)
- [Step 3: Train a CNN Model](#step-3-train-a-cnn-model)

## Introduction

This project is designed to scrape animal images from the web, preprocess them, and use them to train a CNN model for image classification. It's a practical demonstration of integrating web scraping with machine learning.

## Installation and Setup

To get started, you'll need to clone the repository and install the required dependencies. Here's how:

### 1. Clone the Repository

```bash
git clone https://github.com/Stevealila/Animal-Image-Scrape-Predict.git
cd Animal-Image-Scrape-Predict
```

### 2. Set Up a Virtual Environment

It's recommended to use a virtual environment to manage dependencies. Create and activate a virtual environment as follows:

```bash
# Create a virtual environment
python3 -m venv venv

# Activate the virtual environment
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate

```

### 3. Install Dependencies

Install the required Python packages:

```bash
pip install -r requirements.txt
```

## Step 1: Scrape Animal Images

The first step involves scraping images of different animals from the web. This step uses Selenium to automate the browser and requests to download images.

### Key Libraries:

- **Selenium**: Automates browser tasks.
- **requests**: Handles HTTP requests.
- **Python-dotenv**: Manages environment variables.

### Running the Scraping Script

The `animal_image_scrape.py` script scrapes images of cats, dogs, monkeys, cows, and birds from Pexels and stores them in the `datasets/animal_images` directory.

```bash
python animal_image_scrape.py
```

This script sets up a Selenium WebDriver with proxy authentication, navigates to the Pexels website, and downloads images for each animal type.

## Step 2: Convert Images to Vectors

Once the images are scraped, the next step is to convert them into numerical vectors that can be used for training the model.

### Key Libraries:

- **pathlib**: Manages file paths in an intuitive and OS-independent way.

- **OpenCV**: Handles image resizing and conversion to numpy arrays. 

- **PIL**: Handles image file operations such as opening images. 

### Processing the Images

In the `animal_image_predict.ipynb` notebook, OpenCV is used to resize the images to a standard size (150x150) and convert them into numpy arrays. Each image is labeled according to its class (e.g., cat, dog).

```python
# Example of converting an image to a vector
img = imread(img_path)
img_resized = resize(img, (150, 150))
```

## Step 3: Train a CNN Model

With the images converted into vectors, the final step is to train a CNN model using TensorFlow.

### Key Libraries:

- **TensorFlow**: Builds and trains the CNN model.
- **Scikit-learn**: Splits the data into training and testing sets.

### Training the Model

The CNN model is built with layers for feature extraction and classification.  `softmax` layer is used to predict the class of each image.

```python
cnn.fit(X_train, y_train, epochs=10)
```

Finally, the model is used to predict the classes of the last 8 images in the testing dataset.

***Note***: Given the small number of training images, the model may perform better on the training dataset than on the testing dataset. To address potential overfitting, data augmentation might be necessary.
