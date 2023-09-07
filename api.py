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


#网页设置
st.set_page_config(
     page_title="实验数据访问平台",
     page_icon="🧊",
     layout="wide",    # 'wide' or 'centered'
     initial_sidebar_state="expanded",
 )

# 取数部分
def get_data_from_database():
    URL = f'sqlite:///{"D:/data/waveforms.db"}'
    LIMIT = 1000

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
    df['tag1'] = df['tag2'] = df['tag3'] = df['tag4'] = ''
    return df

df = get_data_from_database()
df = df.applymap(lambda df: np.real(df))

# 显示表格
def display_table():
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

    gb.configure_side_bar()


    gb.configure_pagination(enabled=True,
                            paginationAutoPageSize=False,
                            paginationPageSize=5)


    editable_columns = ['Tags', 'tag1', 'tag2', 'tag3', 'tag4']
    for column in df.columns:
        if column in editable_columns:
            gb.configure_column(column, editable=True)  # 使特定列可编辑
        else:
            gb.configure_column(column, editable=False)  # 使其他列变为只读

    gridOptions = gb.build()


    AgGrid(
        df,
        gridOptions = gridOptions,
        fit_columns_on_grid_load=True,
        update_mode=GridUpdateMode.MODEL_CHANGED
        # height=300
    )

display_table()

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
        import plotly.express as px
        fig = px.line(x=x,
                      y=y,
                      markers=True,
                      title = f'Experiment name: {experiment}',
                      width = 30)
        st.plotly_chart(fig,
                        theme="streamlit",
                        use_container_width=True)
        
    with col2:
        if st.button('normalization'):
            order = 'normalization'
        option = st.selectbox('Select:', ('Trigonometric fitting', 'e exponential fitting', 'Peak finding'))

        st.button("Reset", type="primary")
    

    with col3:
        st.write('Why hello there')



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


















# with tab1:
#     col1, col2, col3 = st.columns([3,1,3])
#     with col1:

#         if selected_ID:
#             #selected_ID = int(selected_ID)
#             # experiment = df.loc[df['ID'] == selected_ID]['App'].values[0]
#             # st.write('Experiment name: ', experiment)

#             selected_ID = str(selected_ID)
#             rec = get_record_by_id(selected_ID)
#             experiment = rec.key
#             name = list(get_record_by_id(selected_ID).data.keys())[-1]

#             x = pd.DataFrame(list(rec.data['index'].values())[0].tolist()[:15], columns=['x'])
#             y = pd.DataFrame(rec.data[name])
#             y = y.applymap(lambda y: np.real(y))
            
#             #plotly
#             import plotly.express as px
#             fig = px.line(y,
#                         markers=True,
#                         title = f'Experiment name: {experiment}',
#                         width = 30)
#             st.plotly_chart(fig,
#                             theme="streamlit",
#                             use_container_width=True)
#         else:
#             st.text('The line chart will be shown here ')
            
#     with col2:
        
#         if st.button('Say hello'):
#             st.write('Why hello there')
#         option = st.selectbox('Select:', ('Email', 'Home phone', 'Mobile phone'))
#         st.button("Reset", type="primary")
        

#     with col3:
#         st.write('Why hello there')

# with tab2:
#    st.header("A dog")
#    st.image("https://static.streamlit.io/examples/dog.jpg", width=200)

# with tab3:
#    st.header("An owl")
#    st.image("https://static.streamlit.io/examples/owl.jpg", width=200)
    


# #
