import time
import json
import pytest


def test_no_text_from_website(test_client, database):
    
    url = "http://www.yahoo.com"
    response = test_client.get("/api/v1/text", json={"url": url})

    assert response.status_code == 206
    assert response.json['message'] == "No text for this url"
    assert response.json['url'] == url


def test_get_text_task(database, f_celery, text):

    url = "http://www.google.com"
    task_name = "get_text"
    task = f_celery.send_task(task_name, args=[url], kwargs={})

    while not task.ready():
        time.sleep(1)

    res = f_celery.AsyncResult(task.task_id)
    assert res.state == "SUCCESS"
    
    textt = text.query.filter_by(url=url).first()
    assert textt.url == url
    assert textt.text != "" # powinienem sprawdzic czy tekst nie zawiera tagow html


@pytest.mark.parametrize(
    "url",
    ["http://www.bankier.pl",
    "http://www.bankierasd.apl"],
)
def test_fetch_text(test_client, database, url):

    # start fetching text
    response = test_client.post("/api/v1/text", json={"url": url})
    
    task_id = response.json["task_id"]
    task_url = response.json["check_task_status"]
    assert response.status_code == 202
    assert task_id != ""
    assert "api/v1/task/" in task_url

    # check status of fetch text
    status_url = 'api/v1/task/{}'.format(task_id)
    response = test_client.get(status_url)
    task_state = response.json["state"]

    assert task_state in ["SUCCESS","PENDING","FAILURE","ERROR"] # 

    # wait until result of fetch text is not ready
    while task_state == "PENDING":
        time.sleep(1)
        response = test_client.get(status_url)
        task_state = response.json["state"]

    # check result of fetch text
    if task_state == "SUCCESS":
        response = test_client.get("/api/v1/text", json={"url": url})

        assert response.status_code == 200
        assert response.json['task_id'] == task_id
        assert response.json['url'] == url
        assert response.json['text_from_website'] != ""

    if task_state == "ERROR":
        assert response.json["state"] == "ERROR"
        assert "ERROR" in response.json["message"]