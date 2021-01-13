import requests
import json
import sys
import unittest
from flask import Flask
from rabbit_api_server import app

url_issue = "http://127.0.0.1:5000/api/v1/resources/kanbans/issues"