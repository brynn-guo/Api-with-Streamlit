import streamlit as st
from pathlib import Path
import base64

# Initial page config

st.set_page_config(
     page_title='Streamlit组件清单',
     page_icon="📖",
     layout="wide",
     initial_sidebar_state="expanded",
)

def main():
    cs_sidebar()
    cs_body()
    return None

def img_to_bytes(img_path):
    img_bytes = Path(img_path).read_bytes()
    encoded = base64.b64encode(img_bytes).decode()
    return encoded

# sidebar
def cs_sidebar():
    st.sidebar.markdown('''[<img src='data:image/png;base64,{}' class='img-fluid' width=32 height=32>](https://streamlit.io/)'''.format(img_to_bytes("logomark_website.png")), unsafe_allow_html=True)
    st.sidebar.header('Streamlit组件清单')
    st.sidebar.markdown('''
<small>[Streamlit文档页界面](https://docs.streamlit.io/en/stable/api.html), | [Streamlit首页](https://www.streamlit.io/).</small>
    ''', unsafe_allow_html=True)
    st.sidebar.markdown('__安装及引用方法__')

    st.sidebar.code('pip install streamlit')

    st.sidebar.markdown('引入Streamlit后的简写方法')
    st.sidebar.code('import streamlit as st')

    st.sidebar.markdown('__给侧边栏添加组件__')
    st.sidebar.code('''
st.sidebar.<widget>
a = st.sidebar.radio(\'R:\',[1,2])
    ''')

    st.sidebar.markdown('__命令行__')
    st.sidebar.code('''
streamlit --help
streamlit run your_script.py
streamlit hello
streamlit config show
streamlit cache clear
streamlit docs
streamlit --version
    ''')

    st.sidebar.markdown('__尝鲜版安装方法__')
    st.sidebar.markdown('[Beta版和还在测试中功能](https://docs.streamlit.io/en/stable/api.html#beta-and-experimental-features)')
    st.sidebar.code('''
pip uninstall streamlit
pip install streamlit-nightly --upgrade
    ''')

    st.sidebar.markdown('''<small>[Streamlit组件清单v1.0.0](https://github.com/daniellewisDL/streamlit-cheat-sheet)  | Oct 2021</small>''', unsafe_allow_html=True)

    return None

##########################
# 主体部分
##########################

def cs_body():
    col1, col2, col3 = st.columns(3)
    col1.subheader('魔法命令')
    col1.code('''# 最简单的魔法命令 `st.write()`
\'\'\' _This_ is some __Markdown__ \'\'\'
a=3
'dataframe:', data
    ''')

    # Display text

    col1.subheader('显示文字')
    col1.code('''
st.text('固定宽度的文字')
st.markdown('_Markdown内容_') # see *
st.caption('Balloons. Hundreds of them...')
st.latex(r\'\'\' e^{i\pi} + 1 = 0 \'\'\')#嵌入公式
st.write('Most objects') # df, err, func, keras!
st.write(['st', 'is <', 3]) # see *
st.title('我的title')
st.header('我的标题')
st.subheader('我的副标题')
st.code('for i in range(8): foo()')

*可选参数 unsafe_allow_html = True

    ''')

    # Display data

    col1.subheader('显示数据')
    col1.code('''
st.dataframe(我的dataframe)
st.table(data.iloc[0:10])
st.json({'foo':'bar','fu':'ba'})
st.metric(label="Temp", value="273 K", delta="1.2 K")
    ''')

    # Display charts

    col1.subheader('显示各类图表')
    col1.code('''
st.line_chart(data)
st.area_chart(data)
st.bar_chart(data)
st.pyplot(fig)
st.altair_chart(data)
st.vega_lite_chart(data)
st.plotly_chart(data)
st.bokeh_chart(data)
st.pydeck_chart(data)
st.deck_gl_chart(data)
st.graphviz_chart(data)
st.map(data)
    ''')

    # Display media

    col1.subheader('显示媒体文件')
    col1.code('''
st.image('./header.png')
st.audio(data)
st.video(data)
    ''')

    # Display interactive widgets

    col2.subheader('交互类组件')
    col2.code('''
st.button('需要点我的时候就点我一下')
st.download_button('下载按钮', data)
st.checkbox('检查框')
st.radio('单选按钮', [1,2,3])
st.selectbox('下拉式单选', [1,2,3])
st.multiselect('多选框', [1,2,3])
st.slider('滑动选择器', min_value=0, max_value=10)
st.select_slider('滑动选择器', options=[1,'2'])
st.text_input('通过我可以输入一些文字')
st.number_input('Enter a number')
st.text_area('通过我可以输入多行文字')
st.date_input('日期选择框')
st.time_input('时间选择框')
st.file_uploader('File uploader', type=["csv","png","xlsx","json"])
st.color_picker('点我选择一种颜色')
    ''')
    col2.write('带返回值的组件:')
    col2.code('''
for i in range(int(st.number_input('Num:'))): foo()
if st.sidebar.selectbox('I:',['f']) == 'f': b()
my_slider_val = st.slider('Quinn Mallory', 1, 88)
st.write(slider_val)
    ''')

    # Control flow

    col2.subheader('控制流组件')
    col2.code('''
st.stop()
    ''')

    # Lay out your app

    col2.subheader('对你的APP进行布局')
    col2.code('''
st.form('表单定义组件')
st.form_submit_button('表单提交按钮')
st.container()
st.columns(这里放要分几列的数字)
col1, col2 = st.columns(2)
col1.subheader('Columnisation')
st.expander('展开')
with st.expander('点我进行展开'):
    st.write('次数可以写点什么')
    ''')

    col2.write('在表单中使用其他组件:')
    col2.code('''
with st.form(key='my_form'):
    text_input = st.text_input(label='Enter some text')
    submit_button = st.form_submit_button(label='Submit')
    ''')

    # Display code

    col2.subheader('显示代码')
    col2.code('''
st.echo()
with st.echo():
     st.write('代码将被执行并打印结果')
    ''')

    # Display progress and status

    col3.subheader('显示进度及状态')
    col3.code('''
st.progress(数字可以最大到100，意思是100%)
st.spinner()
with st.spinner(text='正在进行中'):
     time.sleep(5)
     st.success('完成')
st.balloons()
st.error('错误信息')
st.warning('警告信息')
st.info('通知信息')
st.success('成功信息')
st.exception(e)
    ''')

    # Placeholders, help, and options

    col3.subheader('预设内容, 帮助及操作选项')
    col3.code('''
st.empty()
my_placeholder = st.empty()
my_placeholder.text('替换完成!')
st.help(pandas.DataFrame)
st.get_option(key)
st.set_option(key, value)
st.set_page_config(page_title="streamlit", page_icon="", layout='wide')#设置页面模式
    ''')

    # Mutate data

    col3.subheader('表格数据操作方法')
    col3.code('''
DeltaGenerator.add_rows(data)
my_table = st.table(df1)
my_table.add_rows(df2)
my_chart = st.line_chart(df1)
my_chart.add_rows(df2)
    ''')

    # Optimize performance

    col3.subheader('优化性能方法')
    col3.code('''
@st.cache
... def fetch_and_clean_data(url):
...     # Mutate data at url
...     return data
# Executes d1 as first time
d1 = fetch_and_clean_data(ref1)
# Does not execute d1; returns cached value, d1==d2
d2 = fetch_and_clean_data(ref1)
# Different arg, so function d1 executes
d3 = fetch_and_clean_data(ref2)

    ''')

    col3.subheader('其他API查看链接')
    col3.markdown('''
<small>[State API](https://docs.streamlit.io/en/stable/session_state_api.html)</small><br>
<small>[Theme option reference](https://docs.streamlit.io/en/stable/theme_options.html)</small><br>
<small>[Components API reference](https://docs.streamlit.io/en/stable/develop_streamlit_components.html)</small><br>
<small>[API cheat sheet](https://share.streamlit.io/daniellewisdl/streamlit-cheat-sheet/app.py)</small><br>
    ''', unsafe_allow_html=True)

    return None


if __name__ == '__main__':
    main()