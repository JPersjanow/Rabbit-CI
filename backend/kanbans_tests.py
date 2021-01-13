import requests
import json
import sys
import unittest
from flask import Flask
from rabbit_api_server import app

url = "http://127.0.0.1:5000" # The root url of the flask app
url_kanaban = "http://127.0.0.1:5000/api/v1/resources/kanbans/"


class AConnectionTest(unittest.TestCase):
    def test_conn_ok(self):
        r = requests.get(url+"/api/v1/") 
        self.assertEqual(r.status_code, 200)
    def test_conn_fail(self):
        r = requests.get(url)
        self.assertEqual(r.status_code, 404)

class BPOSTKanbans(unittest.TestCase):
    def test_post_kanban_ok(self):
        r = requests.post(url_kanaban,data=json.dumps({"name": "test", "description": "test2"})) 
        self.assertEqual(r.status_code, 201)
        self.assertTrue("New kanban board with id" in r.text)
    def test_post_kanban_spaces(self):
        r = requests.post(url_kanaban,data=json.dumps({"name": "test ", "description": " test"})) 
        self.assertEqual(r.status_code, 201)
        self.assertTrue("New kanban board with id" in r.text)
    def test_post_kanban_empty_desc(self):
        r = requests.post(url_kanaban,data=json.dumps({"name": "test", "description": ""})) 
        self.assertEqual(r.status_code, 201)
        self.assertTrue("New kanban board with id" in r.text)
    def test_post_kanban_special_characters(self):
        r = requests.post(url_kanaban,data=json.dumps({"name": "!@#$%^&*()_+,", "description": "!@#$%^&*()_+,"})) 
        self.assertEqual(r.status_code, 201)
        self.assertTrue("New kanban board with id" in r.text)
    def test_post_kanban_numbers_only(self):
        r = requests.post(url_kanaban,data=json.dumps({"name": "1234567890", "description": "1234567890"})) 
        self.assertEqual(r.status_code, 201)
        self.assertTrue("New kanban board with id" in r.text)
    def test_post_kanban_whitespaces(self):
        r = requests.post(url_kanaban,data=json.dumps({"name": "", "description": "   "})) 
        self.assertEqual(r.status_code, 400)
        self.assertTrue("Name cannot be null or whitespaces only" in r.text)
    def test_post_kanban_whitespaces_2(self):
        r = requests.post(url_kanaban,data=json.dumps({"name": "", "description": "test"})) 
        self.assertEqual(r.status_code, 400)
        self.assertTrue("Name cannot be null or whitespaces only" in r.text)

class CDELETEkanban(unittest.TestCase):
    def test_delete_existing(self):
        r = requests.delete(url_kanaban + "3")
        self.assertEqual(r.status_code, 204)
    def test_delete_not_existing(self):
        r = requests.delete(url_kanaban + "300")
        self.assertEqual(r.status_code, 400)
        self.assertTrue("Kanban id not found" in r.text)
    def test_delete_no_id(self): #We need to change this response code to 400/404!
        r = requests.delete(url_kanaban + "")
        self.assertEqual(r.status_code, 405)


class DGETKanbans(unittest.TestCase):
     def test_get_list(self):
        r = requests.get(url_kanaban) 
        self.assertEqual(r.status_code, 200)   

class EGETKanbans(unittest.TestCase):
     def test_get_existing_id(self):
        r = requests.get(url_kanaban + "1") 
        self.assertEqual(r.status_code, 200)
     def test_get_not_existing_id(self):
        r = requests.get(url_kanaban + "100") 
        self.assertEqual(r.status_code, 400)
        self.assertTrue("Kanban id not found" in r.text)




if __name__ == "__main__":
    unittest.main()
