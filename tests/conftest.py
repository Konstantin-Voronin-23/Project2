import pytest
from src.HH_API import HeadHunterAPI


@pytest.fixture
def hh_api():
    return HeadHunterAPI()