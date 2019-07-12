def test_init_text(text):
    
    textt = text("http://www.google.com", "1234", "Wyszukiwarka Google")
    assert textt.url == "http://www.google.com"
    assert textt.task_id == "1234"
    assert textt.text == "Wyszukiwarka Google"


def test_init_image(image):

    imagee = image("http://www.google.com", "1234", 
        "photo", "http://www.google.com/photo", b"12345")

    assert imagee.url == "http://www.google.com"
    assert imagee.task_id == "1234"
    assert imagee.name == "photo"
    assert imagee.source_url == "http://www.google.com/photo"
    assert imagee.data == b"12345"
