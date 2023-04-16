### KOSIS api

## Installing

```
pip install kosis
```

## Using kosis

- Get API Key from kosis.kr
https://kosis.kr/openapi/serviceUse/serviceUseUnityReg_01Detail.jsp

- Export environment variable KOSIS_API_KEY
export KOSIS_API_KEY={your key}

### Using ipython's autocompletion for easy navigation
```
from kosis import Kosis
ks = Kosis()
# press tab after typing "ks.main." to see the top most list.
# You can navigate every statistics data using autocompletion
ks.main.금융
```
### Using dir() to navigate items
```
from kosis import Kosis
ks = Kosis()
dir(ks.main)
dir(ks.main.금융)
```

### Getting statics data

```
from kosis import Kosis
ks = Kosis()
ks.main.금융.통화금융통계.통화_및_유동성지표.M2_광의통화_.M2_상품별구성내역_말잔_.M2_상품별_구성내역_말잔_계절조정계열_.data
```

output
```
                    TBL_NM              PRD_DE      TBL_ID                  ITM_NM                    ITM_NM_ENG          ITM_ID           UNIT_NM ORG_ID  UNIT_NM_ENG   C1_OBJ_NM    C1_OBJ_NM_ENG              DT PRD_SE            C1                      C1_NM                  C1_NM_ENG
0   M2 상품별 구성내역(말잔 계절조정계열)  202212  DT_101Y001  M2 상품별 구성내역(말잔 계절조정계열)  M2 By Type (End of SA)  13103134693999     십억원    301     Bil.Won     계정항목별       ACCOUNT      3750603.4      M       13102134693ACC_ITEM.BBGS00  M2(말잔 계절조정계열)   M2(End Of period SA)
1   M2 상품별 구성내역(말잔 계절조정계열)  202301  DT_101Y001  M2 상품별 구성내역(말잔 계절조정계열)  M2 By Type (End of SA)  13103134693999     십억원    301     Bil.Won     계정항목별       ACCOUNT      3795354.4      M       13102134693ACC_ITEM.BBGS00  M2(말잔 계절조정계열)   M2(End Of period SA)
2   M2 상품별 구성내역(말잔 계절조정계열)  202302  DT_101Y001  M2 상품별 구성내역(말잔 계절조정계열)  M2 By Type (End of SA)  13103134693999     십억원    301     Bil.Won     계정항목별       ACCOUNT      3802737.3      M       13102134693ACC_ITEM.BBGS00  M2(말잔 계절조정계열)   M2(End Of period SA)
3   M2 상품별 구성내역(말잔 계절조정계열)  202212  DT_101Y001  M2 상품별 구성내역(말잔 계절조정계열)  M2 By Type (End of SA)  13103134693999     십억원    301     Bil.Won     계정항목별       ACCOUNT       163052.4      M       13102134693ACC_ITEM.BBGS01           현금통화      Currency in Circulation
4   M2 상품별 구성내역(말잔 계절조정계열)  202301  DT_101Y001  M2 상품별 구성내역(말잔 계절조정계열)  M2 By Type (End of SA)  13103134693999     십억원    301     Bil.Won     계정항목별       ACCOUNT       161895.8      M       13102134693ACC_ITEM.BBGS01           현금통화      Currency in Circulation
5   M2 상품별 구성내역(말잔 계절조정계열)  202302  DT_101Y001  M2 상품별 구성내역(말잔 계절조정계열)  M2 By Type (End of SA)  13103134693999     십억원    301     Bil.Won     계정항목별       ACCOUNT       163942.1      M       13102134693ACC_ITEM.BBGS01           현금통화      Currency in Circulation
...

```

