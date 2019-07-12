import time
import json
import pytest

def test_no_image_from_website(test_client, database):
    
    url = "http://www.yahoo.com"
    response = test_client.get("/api/v1/images", json={"url": url})

    assert response.status_code == 206
    assert response.json['message'] == "No images for this url"
    assert response.json['url'] == url


def test_get_images_task(database, f_celery, image):
    
    url = "http://www.bankier.pl"
    task_name = "get_images"
    task = f_celery.send_task(task_name, args=[url], kwargs={})

    while not task.ready():
        time.sleep(1)

    res = f_celery.AsyncResult(task.task_id)
    assert res.state == "SUCCESS"
    
    # images saved in db ?
    images = image.query.filter_by(url=url).all()
    assert len(images) != 0
    
    # not null content of first image ?
    img = images[0]
    assert img.url == url
    assert img.name != ""
    assert img.source_url != ""
    assert img.data != b""


@pytest.mark.parametrize(
    "url",
    ["http://www.onet.pl",
    "http://www.onet.apl"],
)
def test_fetch_images(test_client, database, url):

    # start fetching text
    response = test_client.post("/api/v1/images", json={"url": url})
    
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
        response = test_client.get("/api/v1/images", json={"url": url})

        assert response.status_code == 200
        assert response.data != b''
        assert response.data != b'PK'

    if task_state == "ERROR":
        assert response.json["state"] == "ERROR"
        assert "ERROR" in response.json["message"]