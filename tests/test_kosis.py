from src import Kosis
from src.kosis import safe_classname
import pandas as pd

def test_kosis_class_name():
    o = Kosis()
    entries = dir(o.main)
    for entry in entries:
        print(entry)
        assert ' ' not in entry

def test_safe_classname():
    test_names = [
        '한글이름',
        '한 글 이 름',
        '1starts with number',
        'special/characters@',
    ]

    for test_name in test_names:
        safe_name = safe_classname(test_name)
        assert ' ' not in safe_name
        assert '/' not in safe_name
        assert '@' not in safe_name

def test_kosis():
    o = Kosis()
    data = o.main.금융.통화금융통계.통화_및_유동성지표.M2_광의통화_.M2_상품별구성내역_말잔_.M2_상품별_구성내역_말잔_계절조정계열_.data
    assert type(data) == pd.core.frame.DataFrame
    assert 'DT' in data.columns