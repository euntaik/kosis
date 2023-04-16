import requests
import pandas as pd
import plotly.express as px
import os
import json
import ast
import re
import logging
import inspect

API_KEY = os.environ['KOSIS_API_KEY']

# Configure logging level and format
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def is_valid_class_name(name):
    class_definition = f'class {name}: pass'
    try:
        ast.parse(class_definition)
    except Exception as e:
        return False
    return True

def safe_classname(name):
    safe_name = name.strip()
    # add _ to a name if it starts with numbers
    safe_name = f'_{safe_name}' if safe_name[0].isdigit() else safe_name

    # replace all non alpha numeric characters
    safe_name = safe_name.replace('ㆍ', '_')
    safe_name = re.sub('[\W_]+', '_', safe_name, flags=re.UNICODE)
    if False: # is_valid_class_name() sometimes works and sometimes doesn't
        if is_valid_class_name(safe_name):
            return safe_name
        raise Exception(f'Invalid class name : {safe_name}')
    else:
        return safe_name

class KosisEntry:
    def __init__(self, kosis, name, attrs: dict):
        self.class_name = safe_classname(name)
        self.__class__.__name__ = self.class_name
        self.kosis = kosis
        if 'LIST_NM' in attrs:
            self.id = attrs['LIST_ID']
            self.type = 'LIST_NM'
        elif 'TBL_NM' in attrs:
            self.id = attrs['TBL_ID']
            self.type = 'TBL_NM'
        else:
            self.id = ''
            self.type = 'LIST_NM'
        self.name = name

        for k,v in attrs.items():
            setattr(self, k, v)
            
    def __dir__(self):
        logging.debug(inspect.currentframe().f_back.f_code.co_name)
        if hasattr(self, 'init'):
            logging.debug('init already done')
        else:
            logging.debug('kosis get')
            # retreive list/table for the current entry.
            self.get(self)
        return super().__dir__()

    def __getattr__(self, key):
        logging.debug(f'{inspect.currentframe().f_back.f_code.co_name} {key}')
        self.get(self)
        return self.__getattribute__(key)
        
    def get(self, instance):
        self.kosis.get(instance)
    
    def set_dataframe(self, df):
        self.data = df
        self.data['DT'] = self.data['DT'].apply(pd.to_numeric)

    def graph(self, x_item='PRD_DE', y_item='DT', width=None, height=800):
        import plotly.graph_objs as go
        df = self.data
        show_scatter = False
        fig = px.area(df,  x=x_item, y=y_item)
        fig.for_each_trace(lambda trace: trace.update(line=dict(width=0.5, color='rgba(75,0,130,1)'), fillcolor = 'rgba(75,0,130,0.2)'))
        
        if False:
            fig.update_layout(
                plot_bgcolor='white',
                showlegend = True,
                hovermode  = 'x',
                
            )
            fig.update_xaxes(
                mirror=True,
                ticks='outside',
                showline=True,
                linecolor='lightgrey',
                gridcolor='rgba(240,240,240,240)',
                showspikes = True,
                spikemode  = 'across',
                spikesnap = 'cursor',
                showgrid=False,
                tickangle=-60
            )
            fig.update_yaxes(
                mirror=True,
                ticks='outside',
                showline=True,
                linecolor='lightgrey',
                gridcolor='rgba(245,245,245,255)',
                showspikes = True,
                dtick = 10000,
            )
            
        fig.show()

class Kosis():
    def __init__(self, api_key=API_KEY):
        self.kosis = self
        self.api_key = api_key
        self.main = KosisEntry(self, 'main', {})

        self.get(self.main)


    def _get(self, url) -> dict:
        return requests.get(url).json()

    def _get_as_df(self, url) -> pd.DataFrame:
        return pd.DataFrame.from_dict(self._get(url))
    
    def _get_list(self, parentListId):
        parent = f'&parentListId={parentListId}' if parentListId else ''
        return self._get(f'https://kosis.kr/openapi/statisticsList.do?method=getList&apiKey={API_KEY}&vwCd=MT_ZTITLE{parent}&format=json&jsonVD=Y')

    def get_table(self, orgId, tblId, itmId='all', objL1='all', objL2='', objL3='', objL4='', objL5='', objL6='', objL7='', objL8='', prdSe='M', newEstPrdCnt=3) -> pd.DataFrame:
        return self._get_as_df(f'https://kosis.kr/openapi/Param/statisticsParameterData.do?method=getList&apiKey={API_KEY}'
                        f'&vwCd=MT_ZTITLE'
                        f'&orgId={orgId}'
                        f'&tblId={tblId}'
                        f'&itmId={itmId}'
                        f'&objL1={objL1}'
                        f'&objL2={objL2}'
                        f'&objL3={objL3}'
                        f'&objL4={objL4}'
                        f'&objL5={objL5}'
                        f'&objL6={objL6}'
                        f'&objL7={objL7}'
                        f'&objL8={objL8}'
                        f'&prdSe={prdSe}'
                        f'&newEstPrdCnt={newEstPrdCnt}'
                        f'&format=json&jsonVD=Y')
    

    def get_list(self, list_id):
        """ get list with name keyname """
        parent = f'&parentListId={list_id}' if list_id else ''
        return self._get(f'https://kosis.kr/openapi/statisticsList.do?method=getList&apiKey={API_KEY}&vwCd=MT_ZTITLE{parent}&format=json&jsonVD=Y')


    def get(self, instance):
        # called from child instance
        if instance.type == 'LIST_NM':
            # get list and create KosisEntry for each item
            entries = self.get_list(instance.id)
            logging.debug(entries)
            for entry in entries:
                #    def __init__(self, kosis, name, id, id_type):
                if 'LIST_NM' in entry:
                    item = KosisEntry(self, entry['LIST_NM'], entry)
                elif 'TBL_NM' in entry:
                    item = KosisEntry(self, entry['TBL_NM'], entry)
                elif 'errMsg' in entry:
                    logging.error(f'Error : {entry}')
                    continue
                else:
                    logging.error(f'Unexpected entry data: {entry}')
                    continue

                setattr(instance, item.class_name, item)
            setattr(instance, 'init', True)
        elif instance.type == 'TBL_NM':
            # get table and create KosisEntry
            data = self.get_table(instance.ORG_ID, instance.TBL_ID)
            instance.set_dataframe(data)
