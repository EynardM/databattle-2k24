# DataBattle 2K24 (IA Pau)

## Overview

This project evaluates various machine learning models for retrieving similar solutions based on text embeddings. The models compared include Fasttext, LASER, Camembert, Multilang_Bert, and Croissant. The project provides a web interface for interacting with the models and displaying results.

## Prerequisites

Before running the project, you need to install the required dependencies. Make sure you have Python installed (preferably Python 3.7 or higher). 

## Database Setup
Now let's setup the database.

1. **Install MySQL**

`sudo apt update`

`sudo apt install mysql-server`

2. **Start MySQL Service**

`sudo systemctl start mysql`

3. **Create Database and User: Log in to MySQL as root**

`sudo mysql -u root`

`CREATE DATABASE db_databattle;`

`USE db_databattle;`

`source ./db.sql;`

`CREATE USER 'user'@'localhost' IDENTIFIED BY '123';`

`GRANT ALL PRIVILEGES ON db_databattle.* TO 'user'@'localhost';`

`FLUSH PRIVILEGES;`

`EXIT;`

## Installation

Create a virtual environment (optional but recommended):
`python -m venv venv`

then activate it: `source venv/bin/activate  # On Windows use: venv\Scripts\activate`

Install the required packages: `pip install -r requirements.txt`

## Datasets 

Location : `Datasets`

The project utilizes several datasets to compare different models. These datasets are stored in CSV format and include precomputed embeddings for various text entries. Essentially, these embeddings are numerical representations of text that have been generated by different models to represent queries.

The datasets are organized into files named 0.csv through 22.csv. Each file contains columns for Solution_ID and Text. In cases where the dataset pertains to embeddings for a specific model, there is an additional column named Embedding, which includes the numerical values of the embeddings generated by that model. Rather than representing distinct solutions, these files correspond to various degrees of precision or granularity in the query embeddings. This setup allows for a comprehensive evaluation of model performance across different levels of detail.

## Embeddings
The following models are used to generate text embeddings:

- **Fasttext**: Provides word and sentence embeddings. 
  - **Note**: Due to the large size of the model, the `fasttext.pt` file is not included in this repository. Users need to download this file separately. Refer to the `emb_fasttext.py` file for the specific model used.
  
- **LASER**: Generates multilingual embeddings.

- **Camembert**: French language model for contextual embeddings.

- **Multilang_Bert**: Multilingual BERT model for embeddings.

- **Croissant**: Sentence Transformer for embeddings.
  - **Note**: The `model-00001-of-00002.safetensors` file is not included in this repository due to its large size. Users need to download this file separately. Refer to the `emb_croissant.py` file for the specific model used.


Each model's embeddings are compared to find the most similar solutions to a given query.

## Usage

To evaluate results based on the `Exemple de prompts.xlsx` file, run the following command:

`python evaluate.py`

To start the web interface for interacting with the models, use:

`streamlit run front.py`

Here is a demo :
![](demo.gif)

## Contributors
This project was developed by:

Sarah Chaabouni - Yann Langlo - Amaury Petersschmitt - Florian Bergere - Victoria Troubat - Maxime Eynard