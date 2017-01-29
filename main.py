#!/usr/local/env python

# ============== CONFIG PARAMETERS
from config import NAME, SNOOZE_TIME, READING_TIME, BED_TIME, NORMAL_TIME, DOW
# ============== INTERNAL LIBRARIES
# ============== EXTERNAL LIBRARIES
from flask import Flask

app = Flask(__name__)
