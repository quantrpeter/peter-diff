def test_greet():
    assert greet("world") == "Hi there, world!"

def test_greet_empty():
    assert greet("") == "Hi there, !"
