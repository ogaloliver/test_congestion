#%%
import pandas as pd
import streamlit as st
import numpy as np
from plotly import graph_objects as go
#%%
train=pd.read_csv(r"D:\预测拥堵\train.csv")
test=pd.read_csv(r"D:\预测拥堵\test.csv")
#%%
def fe(data):
    data['time']=pd.to_datetime(data['time'])
    data['weekday']=data['time'].dt.weekday
    data['hour']=data['time'].dt.hour
    data['minute'] = data['time'].dt.minute
    data['dayofyear']=data['time'].dt.dayofyear
    return data
#%%
train=fe(train)
test=fe(test)


#%%
st.subheader('时间聚合分析')
x_opt=st.sidebar.radio('x_axis',[0,1,2,'none'])
y_opt=st.sidebar.radio('y_axis',[0,1,2,3,'none'])
direction_opt=st.sidebar.selectbox('direction',['NB','SB','EB','WB','NE','NW','SE','SW','none'])



#%%
selected_list=[[0,1,2],[0,1,2,3],['NB','SB','EB','WB','NE','NW','SE','SW']]
for i,r in enumerate([x_opt,y_opt,direction_opt]):
    if r!='none':
        selected_list[i]=[r]


#%%
for_time_df=train[(train['x'].isin(selected_list[0]))&(train['y'].isin(selected_list[1]))&(train['direction'].isin(selected_list[2]))]


#%%
time_mode_opt=st.sidebar.selectbox('time_mode',['weekday','hour','minute'])
plot_time_df=for_time_df.groupby(time_mode_opt).congestion.median()


#%%
trace=go.Bar(x=plot_time_df.index,y=plot_time_df.values,opacity=0.7,marker={'color':'lightgreen'})
fig=go.Figure(trace,layout={'xaxis':{'gridcolor':'grey'},'yaxis':{'gridcolor':'grey','range':[0,100]}})
st.plotly_chart(fig,use_container_width=True)


#%%
st.subheader('时间序列分析')
day_num = st.sidebar.number_input('day_of_year',91,273,273)
temp_train=train[(train['x']==x_opt)&(train['y']==y_opt)&
                 (train['direction']==direction_opt)&
                 (train['dayofyear']==day_num)&
                 (train['hour']>=12)]

#%%
trace_day_series=go.Scatter(x=temp_train['time'],y=temp_train['congestion'],mode='lines',marker={'color':'gold'})
fig_day_series=go.Figure(trace_day_series,layout={'xaxis':{'gridcolor':'grey'},'yaxis':{'gridcolor':'grey','range':[0,100]}})
st.plotly_chart(fig_day_series,use_container_width=True)

#%%
# train.head()
# temp=train.groupby(['x','y','time']).congestion.sum().reset_index()
# temp1=temp[(temp['x']==x_opt)&(temp['y']==y_opt)]
# trace1=go.Scatter(x=temp1['time'],y=temp1['congestion'],mode='lines',marker={'color':'lightblue'})
# fig1=go.Figure(trace1,layout={'xaxis':{'gridcolor':'grey'},'yaxis':{'gridcolor':'grey'}})
# st.plotly_chart(fig1,use_container_width=True)
#%%
result=pd.read_csv(r"D:\预测拥堵\pre_sub.csv")
new_test=pd.concat([test,result],axis=1)
new_select_test=new_test[(new_test['x']==x_opt)&(new_test['y']==y_opt)&(new_test['direction']==direction_opt)]
trace2=go.Scatter(x=new_select_test['time'],y=new_select_test['congestion'],mode='lines',marker={'color':'pink'})
fig2=go.Figure(trace2,layout={'xaxis':{'gridcolor':'grey'},'yaxis':{'gridcolor':'grey','range':[0,100]}})
st.plotly_chart(fig2,use_container_width=True)
#%%
train.head()