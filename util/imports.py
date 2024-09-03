# imports.py
import mysql.connector

from html import unescape
from bs4 import BeautifulSoup
from typing import List, Tuple
import pandas as pd
import itertools
import os
from transformers import CamembertModel, CamembertTokenizer
import torch
from tqdm import tqdm
from codecarbon import EmissionsTracker
from sentence_transformers import SentenceTransformer
import fasttext
from huggingface_hub import hf_hub_download
from transformers import AutoModelForCausalLM, AutoTokenizer
from laserembeddings import Laser
from transformers import BertTokenizer, BertModel
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import streamlit as st
from laserembeddings import Laser

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import math

import pandas as pd
from sqlalchemy import create_engine
import math
import math
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sqlalchemy import create_engine

import pandas as pd
import numpy as np
import plotly.graph_objects as go
from collections import defaultdict

