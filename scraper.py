import csv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime, timedelta
import time

def load_crop(file):
    c_data = {}
    with open(file, "r") as file:
        for l in file:
            line = l.strip()
            if line: 
                segments = line.split(", ")
                crop_name = segments[0]
