import unittest
import requests
import json


url = "http://127.0.0.1:5000"  # The root url of the flask app
url_kanaban = "http://127.0.0.1:5000/api/v1/resources/kanbans/"

# Kanbans unit tests:


class AConnectionTest(unittest.TestCase):
    def test_conn_ok(self):
        r = requests.get(url+"/api/v1/")
        self.assertEqual(r.status_code, 200)

    def test_conn_fail(self):
        r = requests.get(url)
        self.assertEqual(r.status_code, 404)


class BPOSTKanbans(unittest.TestCase):
    def test_post_kanban_ok(self):
        r = requests.post(url_kanaban, json={
                          "name": "test", "description": "test2"})
        self.assertEqual(r.status_code, 201)
        self.assertTrue("New kanban board with id" in r.text)

    def test_post_kanban_spaces(self):
        r = requests.post(url_kanaban, json={
                          "name": "test ", "description": " test"})
        self.assertEqual(r.status_code, 201)
        self.assertTrue("New kanban board with id" in r.text)

    def test_post_kanban_empty_desc(self):
        r = requests.post(url_kanaban, json={
                          "name": "test", "description": ""})
        self.assertEqual(r.status_code, 201)
        self.assertTrue("New kanban board with id" in r.text)

    def test_post_kanban_special_characters(self):
        r = requests.post(url_kanaban, json={
                          "name": "!@#$%^", "description": "&*()_+,"})
        self.assertEqual(r.status_code, 201)
        self.assertTrue("New kanban board with id" in r.text)

    def test_post_kanban_numbers_only(self):
        r = requests.post(url_kanaban, json={
                          "name": "1234567890", "description": "1234567890"})
        self.assertEqual(r.status_code, 201)
        self.assertTrue("New kanban board with id" in r.text)

    def test_post_kanban_whitespaces(self):
        r = requests.post(url_kanaban, json={"name": "", "description": "   "})
        self.assertEqual(r.status_code, 400)
        self.assertTrue("Name cannot be null or whitespaces only" in r.text)

    def test_post_kanban_whitespaces_2(self):
        r = requests.post(url_kanaban, json={
                          "name": "", "description": "test"})
        self.assertEqual(r.status_code, 400)
        self.assertTrue("Name cannot be null or whitespaces only" in r.text)

    def test_post_kanban_no_name_body(self):
        r = requests.post(url_kanaban, json={"description": "test"})
        self.assertEqual(r.status_code, 400)

    def test_post_kanban_no_desc_body(self):
        r = requests.post(url_kanaban, json={"name": "test"})
        self.assertEqual(r.status_code, 400)

    def test_post_kanban_no_body(self):
        r = requests.post(url_kanaban, json={})
        self.assertEqual(r.status_code, 400)


class CDELETEkanban(unittest.TestCase):
    def test_delete_existing(self):
        r = requests.delete(url_kanaban + "3")
        self.assertEqual(r.status_code, 204)

    def test_delete_not_existing(self):
        r = requests.delete(url_kanaban + "300")
        self.assertEqual(r.status_code, 400)
        self.assertTrue("Kanban id not found" in r.text)

    def test_delete_no_id(self):
        r = requests.delete(url_kanaban + "")
        self.assertEqual(r.status_code, 400)


class DGETKanbans(unittest.TestCase):
    def test_get_list(self):
        r = requests.get(url_kanaban)
        self.assertEqual(r.status_code, 200)


class EGETKanban(unittest.TestCase):
    def test_get_existing_id(self):
        r = requests.get(url_kanaban + "1")
        self.assertEqual(r.status_code, 200)

    def test_get_not_existing_id(self):
        r = requests.get(url_kanaban + "100")
        self.assertEqual(r.status_code, 400)
        self.assertTrue("Kanban id not found" in r.text)


class FPUTKanbans(unittest.TestCase):
    def test_put_not_existing(self):
        r = requests.put(url_kanaban + "1000",
                         json={"name": "put test", "description": "put test 2"})
        self.assertEqual(r.status_code, 404)

    def test_put_existing(self):
        r = requests.put(url_kanaban + "1",
                         json={"name": "put", "description": "put test 2"})
        self.assertEqual(r.status_code, 204)

    def test_put_no_name(self):
        r = requests.put(url_kanaban + "2",
                         json={"name": "", "description": "test"})
        self.assertEqual(r.status_code, 400)

    def test_put_no_desc(self):
        r = requests.put(url_kanaban + "2",
                         json={"name": "test", "description": ""})
        self.assertEqual(r.status_code, 204)

    def test_put_empty(self):
        r = requests.put(url_kanaban + "4",
                         json={"name": "test", "description": ""})
        self.assertEqual(r.status_code, 204)

    def test_put_special(self):
        r = requests.put(url_kanaban + "5",
                         json={"name": "!@#$%^", "description": "&*()_+,"})
        self.assertEqual(r.status_code, 204)

# Issues unit tests:


class GPOSTIssues(unittest.TestCase):
    def test_post_existing_kanban(self):
        r = requests.post(url_kanaban + "1"+"/issues",
                          json={"name": "issue 1", "description": "desc", "creator": "julia"})
        self.assertEqual(r.status_code, 201)

    def test_post_not_existing_kanban(self):
        r = requests.post(url_kanaban + "1000"+"/issues",
                          json={"name": "issue 1", "description": "desc", "creator": "julia"})
        self.assertEqual(r.status_code, 400)
        self.assertTrue("Kanban id not found" in r.text)

    def test_post_no_desc(self):
        r = requests.post(url_kanaban + "2"+"/issues",
                          json={"name": "issue 1", "description": "", "creator": "julia"})
        self.assertEqual(r.status_code, 201)

    def test_post_no_creator(self):
        r = requests.post(url_kanaban + "2"+"/issues",
                          json={"name": "issue 1", "description": "test", "creator": ""})
        self.assertEqual(r.status_code, 400)
        self.assertTrue(
            "Name/creator cannot be null or whitespaces only" in r.text)

    def test_post_no_name(self):
        r = requests.post(url_kanaban + "4"+"/issues",
                          json={"name": "", "description": "test", "creator": "test"})
        self.assertEqual(r.status_code, 400)
        self.assertTrue(
            "Name/creator cannot be null or whitespaces only" in r.text)

    def test_post_no_body(self):
        r = requests.post(url_kanaban + "4"+"/issues", json={})
        self.assertEqual(r.status_code, 400)

    def test_post_only_name(self):
        r = requests.post(url_kanaban + "4"+"/issues", json={"name": "test"})
        self.assertEqual(r.status_code, 400)

    def test_post_only_desc(self):
        r = requests.post(url_kanaban + "4"+"/issues",
                          json={"description": "test"})
        self.assertEqual(r.status_code, 400)

    def test_post_only_creator(self):
        r = requests.post(url_kanaban + "4"+"/issues",
                          json={"creator": "test"})
        self.assertEqual(r.status_code, 400)

    def test_post_only_numbers(self):
        r = requests.post(url_kanaban + "4"+"/issues",
                          json={"name": "1234567", "description": "8907", "creator": "12390"})
        self.assertEqual(r.status_code, 201)


class HGETKanbanIssues(unittest.TestCase):
    def test_get_existing_id(self):
        r = requests.get(url_kanaban + "4"+"/issues")
        self.assertEqual(r.status_code, 200)

    def test_get_not_existing_id(self):
        r = requests.get(url_kanaban + "4000"+"/issues")
        self.assertEqual(r.status_code, 400)
        self.assertTrue("Kanban id not found" in r.text)


class IPUTissues(unittest.TestCase):
    def test_put_not_existing_kanban(self):
        r = requests.put(url_kanaban + "4000"+"/issues/" + "1",
                         json={"name": "issue 2", "description": "desc", "creator": "julia"})
        self.assertEqual(r.status_code, 400)
        self.assertTrue("Kanban id not found" in r.text)

    def test_put_not_existing_issue(self):
        r = requests.put(url_kanaban + "1"+"/issues/" + "1000",
                         json={"name": "issue 3", "description": "desc", "creator": "julia"})
        self.assertEqual(r.status_code, 400)
        self.assertTrue("Issue id not found" in r.text)

    def test_put_existing(self):
        r = requests.put(url_kanaban + "1"+"/issues/" + "1",
                         json={"name": "issue 2", "description": "desc", "creator": "julia"})
        self.assertEqual(r.status_code, 204)

    def test_put_no_name(self):
        r = requests.put(url_kanaban + "1"+"/issues/" + "1",
                         json={"name": "", "description": "desc", "creator": "julia"})
        self.assertEqual(r.status_code, 400)

    def test_put_no_desc(self):
        r = requests.put(url_kanaban + "1"+"/issues/" + "1",
                         json={"name": "", "description": "", "creator": "julia"})
        self.assertEqual(r.status_code, 204)

    def test_put_no_creator(self):
        r = requests.put(url_kanaban + "1"+"/issues/" + "1",
                         json={"name": "", "description": "", "creator": ""})
        self.assertEqual(r.status_code, 400)

    def test_put_special(self):
        r = requests.put(url_kanaban + "1"+"/issues/" + "1",
                         json={"name": "!@#$%^", "description": "&*()_+,", "creator": "&*()_+"})
        self.assertEqual(r.status_code, 204)

    def test_put_no_body(self):
        r = requests.put(url_kanaban + "1"+"/issues/" + "1",
                         json={})
        self.assertEqual(r.status_code, 400)


class JGETKanbanIssueId(unittest.TestCase):
    def test_get_existing_id(self):
        r = requests.get(url_kanaban + "1"+"/issues/" + "1")
        self.assertEqual(r.status_code, 200)

    def test_get_not_existing_id_issue(self):
        r = requests.get(url_kanaban + "1"+"/issues/" + "1000")
        self.assertEqual(r.status_code, 400)
        self.assertTrue("Issue id not found" in r.text)

    def test_get_not_existing_id_kanban(self):
        r = requests.get(url_kanaban + "1000"+"/issues/" + "1")
        self.assertEqual(r.status_code, 400)
        self.assertTrue("Kanban id not found" in r.text)


class KDELETEIssue(unittest.TestCase):
    def test_delete_existing(self):
        r = requests.delete(url_kanaban + "1"+"/issues/" + "1")
        self.assertEqual(r.status_code, 200)

    def test_delete_not_existing_issue(self):
        r = requests.delete(url_kanaban + "1"+"/issues/" + "10000")
        self.assertEqual(r.status_code, 400)
        self.assertTrue("Issue id not found" in r.text)

    def test_delete_not_existing_kanban(self):
        r = requests.delete(url_kanaban + "1000"+"/issues/" + "1")
        self.assertEqual(r.status_code, 400)
        self.assertTrue("Kanban id not found" in r.text)

    def test_delete_no_id(self):
        r = requests.delete(url_kanaban + "1"+"/issues/" + "")
        self.assertEqual(r.status_code, 404)


# Stages unit tests:
class LPUTStage(unittest.TestCase):
    def test_put_existing_todo(self):
        r = requests.put(url_kanaban + "/4"+"/issues/" + "1/stage",
                         json={"stage": "todo"})
        self.assertEqual(r.status_code, 200)

    def test_put_existing_doing(self):
        r = requests.put(url_kanaban + "/4"+"/issues/" + "1/stage",
                         json={"stage": "doing"})
        self.assertEqual(r.status_code, 200)

    def test_put_existing_done(self):
        r = requests.put(url_kanaban + "/4"+"/issues/" + "1/stage",
                         json={"stage": "done"})
        self.assertEqual(r.status_code, 200)

    def test_put_not_existing_stage(self):
        r = requests.put(url_kanaban + "/4"+"/issues/" + "1/stage",
                         json={"stage": "test"})
        self.assertEqual(r.status_code, 400)
        self.assertTrue(
            "Stage cannot be anything other than todo, done or doing" in r.text)

    def test_put_empty_stage(self):
        r = requests.put(url_kanaban + "/4"+"/issues/" + "1/stage",
                         json={"stage": ""})
        self.assertEqual(r.status_code, 400)
        self.assertTrue("Stage cannot be null or whitespaces only" in r.text)

    def test_put_not_existing_kanban(self):
        r = requests.put(url_kanaban + "/4000"+"/issues/" + "1/stage",
                         json={"stage": "doing"})
        self.assertEqual(r.status_code, 400)

    def test_put_not_existing_issue(self):
        r = requests.put(url_kanaban + "/4"+"/issues/" + "1000/stage",
                         json={"stage": "doing"})
        self.assertEqual(r.status_code, 400)

    def test_put_no_body(self):
        r = requests.put(url_kanaban + "/4"+"/issues/" + "1/stage",
                         json={})
        self.assertEqual(r.status_code, 400)


class MGETstage(unittest.TestCase):
    def test_get_existing_id(self):
        r = requests.get(url_kanaban + "4"+"/issues/" + "1/stage")
        self.assertEqual(r.status_code, 200)

    def test_get_not_existing_id_issue(self):
        r = requests.get(url_kanaban + "1"+"/issues/" + "1000/stage")
        self.assertEqual(r.status_code, 400)
        self.assertTrue("Issue id not found" in r.text)

    def test_get_not_existing_id_kanban(self):
        r = requests.get(url_kanaban + "1000"+"/issues/" + "1/stage")
        self.assertEqual(r.status_code, 400)
        self.assertTrue("Kanban id not found" in r.text)


if __name__ == "__main__":
    unittest.main()
