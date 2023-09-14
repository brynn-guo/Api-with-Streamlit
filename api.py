# import部分
import h5py
import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder
from pathlib import Path
import matplotlib.image as mim
import matplotlib.pyplot as plt
import numpy as np
from storage.crud.record import query_record, update_tags
from storage.utils import session
from home.hkxu.tools import lookup, get_record_by_id
from st_aggrid.shared import GridUpdateMode
from picture import data_view
import plotly.express as px
from qos_tools.analyzer.tools import get_normalization
from fit import exponential_fit


#网页设置
st.set_page_config(
     page_title="实验数据访问平台",
     page_icon="🧊",
     layout="wide",    # 'wide' or 'centered'
     initial_sidebar_state="expanded",
 )

# 取数部分 用query_record将数据完整的以dataframe的形式取出
@st.cache_data
def load_data_from_database():
    URL = f'sqlite:///{"D:/data/waveforms.db"}'
    LIMIT = 100000
    db = session(url=URL)
    page = 2
    app = None
    tags = []
    before =None
    after = None
    total, apps, table = query_record(db,
                                        offset=(page-1)*LIMIT,
                                        limit=LIMIT,
                                        app=app,
                                        tags=tags,
                                        before=before,
                                        after=after)
    df = pd.DataFrame(table['body'], columns=table['header'])
    df.rename(columns={'tags': 'Tags'}, inplace=True)
    df = df.applymap(lambda df: np.real(df)) #将数据都变为实数，方便绘图
    return df

load_data = load_data_from_database()
# df1['tag1'] = df1['tag2'] = df1['tag3'] = df1['tag4'] = ''

def data_tag(load_data): #将数据库中的数据和标签tag连在一起，返回显示在web界面上的dataframe
    tags = pd.read_csv('Tags.csv')
    df = pd.concat([load_data,tags.iloc[:,-4:]], axis = 1, sort = False)
    return df

# 显示表格
def display_table(load_data):
    df = data_tag(load_data)
    enable_enterprise_modules=True #启用企业版
    gb = GridOptionsBuilder.from_dataframe(
        df,
        enableRowGroup=True,
        enableValue=True,
        enablePivot=True,
        enable_Pagination = True)
    gb.configure_default_column(min_column_width=3)
    selection_mode = 'multiple'
    gb.configure_selection(
        selection_mode,
        use_checkbox = True
    )
    # gb.configure_side_bar()
    gb.configure_pagination(enabled=True,
                            paginationAutoPageSize=False,
                            paginationPageSize=5)
    editable_columns = ['tag1', 'tag2', 'tag3', 'tag4', 'Tags']
    for column in df.columns:
        if column in editable_columns:
            gb.configure_column(column, editable=True)  # 使特定列可编辑
        else:
            gb.configure_column(column, editable=False)  # 使其他列变为只读

    gridOptions = gb.build()
    grid_return = AgGrid(
        df,
        gridOptions = gridOptions,
        fit_columns_on_grid_load=True,
        update_mode=GridUpdateMode.MODEL_CHANGED,
        reload_data = False
    )
    return grid_return

with st.form(key='my_form'):
    grid_return = display_table(load_data)
    new_df = grid_return['data']
    submitted = st.form_submit_button("Submit")
    if submitted:
        tags = pd.concat([load_data['ID'], new_df.iloc[:,-4:]], axis=1) 
        # st.table(df.columns)
        tags.to_csv("Tags.csv", index=False)




# 画图，分析
def plot_and_analyze(selected_ID, qubits, i):
    col1, col2, col3 = st.columns([3,1,3])
    with col1:
        selected_ID = str(selected_ID)
        rec = get_record_by_id(selected_ID)
        experiment = rec.key
        name = list(get_record_by_id(selected_ID).data.keys())[-1]

        x = list(rec.data['index'].values())[i]
        y = rec.data[name][:,i]

        #plotly
        
        fig = px.line(x=x,
                      y=y,
                      markers=True,
                      title = f'Experiment name: {experiment}',
                    #   width = 560
                      )
        st.plotly_chart(fig,
                        # theme="streamlit",
                        theme = None,
                        use_container_width=True
                        )
        
    with col2:
        choose = {}
        choose['normalize'] = st.checkbox('normalize', key = f'normalize{i}')

        choose['option'] = st.selectbox('Select a function:', 
                                        ('exponential fitting', 'Trigonometric fitting', 'peak searching', 'FFT', 'Linear fitting'), 
                                        key = f'option{i}')

    with col3:
        if choose['normalize']:
            y=get_normalization(np.abs(y))

        if choose['option'] == 'exponential fitting':
            y1 = exponential_fit(x,y) 
            plot_y = [y,y1]

        fig = px.line(x=x,
                      y=plot_y,
                      labels = {'raw','fitted'},
                      markers=True,
                      title = f'Experiment name: {experiment}',
                    #   width = 560
                      )
        fig.update_layout(legend=dict(
            yanchor="top",  # y轴顶部
            y=0.99,
            xanchor="right",  # x轴靠左
            x=0.99
            ))
        st.plotly_chart(fig,
                        # theme = "streamlit",
                        theme = None,
                        use_container_width=True
                        )

selected_ID = st.number_input("Select an ID",
                              min_value = 0,
                              step = 1)

if selected_ID:
    selected_ID = str(selected_ID)
    rec = get_record_by_id(selected_ID)
    experiment = rec.key
    qubits = list(rec.data['index'].keys())
    tags = []
    for i in qubits:
        tag = f"tag{i}"
        tags.append(tag)
    tags = st.tabs(qubits)
    for i in range(len(qubits)):
        with tags[i]:
            plot_and_analyze(selected_ID, qubits, i)













