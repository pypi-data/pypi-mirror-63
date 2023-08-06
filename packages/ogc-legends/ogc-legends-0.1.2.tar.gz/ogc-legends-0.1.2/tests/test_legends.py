import json
import pytest
import ogc_legends


def test_get_legends():

    url = "https://demo.mapserver.org/cgi-bin/wms?"
    legends = ogc_legends.get_legends(url, "./images")
    print(json.dumps(legends, indent=4))
    assert "cities" in legends


def test_get_legends_1_1_1():

    url = "https://demo.mapserver.org/cgi-bin/wms?"
    legends = ogc_legends.get_legends(url, "./images", False, "1.1.1")
    print(json.dumps(legends, indent=4))
    assert "cities" in legends


def run_tests():
    pytest.main(["tests/test_legends.py", "-vv"])


if __name__ == '__main__':
    run_tests()
    # test_get_legends()
    print("Done!")
