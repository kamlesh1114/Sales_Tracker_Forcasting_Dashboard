
import pandas as pd
import streamlit as st
import datetime as dt
from datetime import datetime
from io import BytesIO
import xlsxwriter
import streamlit_authenticator as stauth

from deta import Deta
# import streamlit as st
# load  the environment


## Read excel and define df as required
st.set_page_config(page_title='DSA-DASHBOARD', page_icon=":bar_chart:", layout="wide", initial_sidebar_state="auto",menu_items={'Get help':"https://www.kreditbee.in",'Report a bug': "https://www.kreditbee.in",'About': "# This is a header. This is an *extremely* cool app!"})
st.sidebar.image("kblogo.png", use_column_width=True)

# deta = Deta(st.secrets["key_auth"])
# db = deta.Base("users_db")
# # users=db.fetch().items
# users = db.fetch().items

# # the code mentioned above
# usernames = [user["key"] for user in users]
# names = [user["name"] for user in users]
# hashed_passwords = [user["password"] for user in users]
# credentials = {"usernames":{}}
# for un, name, pw in zip(usernames, names,hashed_passwords):
#     user_dict = {"name":name,"password":pw}
#     credentials["usernames"].update({un:user_dict})


# # usernames=[user["key"] for user in users]
# # names=[name["name"] for name in users]
# # hashed_passwords=[password["password"] for password in users]

# authenticator=stauth.Authenticate(credentials,"dsa_dashboard","xyzab",cookie_expiry_days=1)

# name,authentication_status, username=authenticator.login("Login","sidebar")

# if authentication_status== False:
#     st.error("Username/Password is Incorrect")
# if authentication_status== None:
#     st.warning("Please Enter Your Usernames and Password")

# if authentication_status==True:
#     if st.session_state["authentication_status"]==True:
#         st.sidebar.write(f' **Mr. {st.session_state["name"]}**')
#         authenticator.logout('Logout', 'sidebar')
#         # st.title('Some content')

month=datetime.today().strftime('%B')
### 31 days Months list
list1=['January', 'March', 'May', 'July', 'August', 'October','December']

### 30 days Months list
list2=['November', 'April', 'June','September']

# all_months=['January','February','March','April','May','June','July','August','September','October','November','December']

#     all_months=[12,11,10,9,8,7,6,5,4,3,2,1]

all_months=[5,4,3,2,1,6,7,8,9,10,11,12]

#     all_months=all_months_l.reverse()

list1_2=[1, 3, 5, 7, 8, 10,12]  ## 31 days
list2_1=[11, 4, 6,9]  ## 30 days
list3_1=[2]


all_year=[2023,2022]
# using now() to get current time 
current_time = dt.datetime.now()
t=current_time.day
m=current_time.month

option_year = st.sidebar.selectbox(
'Select Year:',
(all_year))

if option_year==option_year:

    year_selected=option_year
option_month = st.sidebar.selectbox(
    'Select Month:',
    (all_months))
# st.sidebar.write('You selected:', option_month)
months_list=option_month

if option_month in list2_1:
    kk=30
    months_list=option_month
    if months_list==m:
        if 1<t<10:           #### Updated on 29-04-2023
            kk=t-1
        else:
            kk=t-1                 
elif option_month in list3_1:
    kk=28
    months_list=option_month
    if months_list==m:
        if 1<t<10:
            kk=t-1
        else:
            kk=t-1

elif option_month in list1_2:
    kk=31
    months_list=option_month
    if months_list==m:
        if 1<t<10:
            kk=t-1
        else:
            kk=t-1

date_list=[]
for i in range(kk+1):
    if i<=8:
        opt_list1=(f"{year_selected}-{months_list}-{0}{1+i}")
        date_list.append(opt_list1)
    elif i>=10:
        opt_list2=(f"{year_selected}-{months_list}-{i}")
        date_list.append(opt_list2)

# st.header('DSA Live Tracker Dashboard')

dsa_wise=pd.read_excel(f'Report_New_{kk}_{months_list}_{year_selected}.xlsx',sheet_name=0,index_col=False)    
bdm_wise=pd.read_excel(f'Report_New_{kk}_{months_list}_{year_selected}.xlsx',sheet_name=1)
loan_leads=pd.read_excel(f'Report_New_{kk}_{months_list}_{year_selected}.xlsx',sheet_name=2)
user_counts=pd.read_excel(f'Report_New_{kk}_{months_list}_{year_selected}.xlsx',sheet_name=3)
#         reg_leads=pd.read_excel(f'Report_New_{kk}_{months_list}_{year_selected}.xlsx',sheet_name=4)


dsa_reg_list=user_counts['current_attributed_channel'].unique()

# loan_leads.drop(['mobile'],axis=1,inplace=True)
# user_counts.drop(['mobile'],axis=1,inplace=True)

## Daywise latest loans and gmv df

daywise1=bdm_wise.T
daywise2=daywise1.drop(['BDM']).drop(daywise1.columns[[0,1,2,3]],axis=1).T
daywise=daywise2.drop(daywise2.iloc[:,4::],axis=1)


## Counts and sum of required infor (i.e information in card)
reg_list=[]
for g in range(len(dsa_reg_list)):
    reg_df=(user_counts[user_counts['current_attributed_channel'].isin([dsa_reg_list[g]])].groupby('registration_date')['uid'].count()).astype(int)
    reg_list.append(reg_df)

## making final df of registrations for visualization

##particular date wise filter

date1=[]
for d in range(kk):
    date1.append(1+d)

date_option1=st.selectbox(
        'Select Date:',['All']+(date1))

if date_option1=='All':
    final_date=date_list
else:
    final_date=[date_list[date_option1-1]]

final_reg_df=pd.DataFrame(reg_list,columns=final_date,index=dsa_reg_list)

#   common df for loans and gmv counts

common_df=loan_leads[loan_leads['first_loan_taken_date'].isin(final_date)]

final_reg_df.loc["Total"]=final_reg_df.sum(numeric_only=False)
final_reg_df["Total"]=final_reg_df.sum(numeric_only=True,axis=1)

all_reg_count=user_counts[user_counts['registration_date'].isin(final_date)]['uid'].count()

all_loan_count=common_df['uid'].count()
all_gmv=common_df['first_loan_gmv'].sum()

all_se_count=common_df[common_df['product_name'].isin(['MLA-X'])]['uid'].count()
all_se_gmv=common_df[common_df['product_name'].isin(['MLA-X'])]['first_loan_gmv'].sum()

all_sa_count=common_df[common_df['product_name'].isin(['PK-SA'])]['uid'].count()
all_sa_gmv=common_df[common_df['product_name'].isin(['PK-SA'])]['first_loan_gmv'].sum()

all_ats=round(all_gmv/all_loan_count)


## Selectbox execution data in sidebar
option = st.sidebar.selectbox(
    'Select Here:',
    ('Summary','BDM WISE', 'DSA WISE'))


## Report downloading dataframe

# st.sidebar.write(f'Report Upto: {kk}-{months_list}-{year_selected}')
# #         def to_excel(df):
# output = BytesIO()
# writer = pd.ExcelWriter(output, engine='xlsxwriter')
# dsa_wise.to_excel(writer, index=False, sheet_name='dsa')
# bdm_wise.to_excel(writer, index=False, sheet_name='bdm')
# loan_leads.to_excel(writer, index=False, sheet_name='loan_leads')
# user_counts.to_excel(writer, index=False, sheet_name='user_counts')
# #             reg_leads.to_excel(writer, index=False, sheet_name='New_Registration_dump')
# writer.save()
# processed_data = output.getvalue()
# #             return processed_data

# #         df_xlsx = to_excel(processed_data)
# st.sidebar.download_button(label='📥 Download Report',
#                                 data=processed_data ,
#                                 file_name= f"Report_New_{kk}_{months_list}_{year_selected}.xlsx")


## Card design and data inserting
import hydralit_components as hc

if option=='BDM WISE':
    """
    #### BDM WISE SALES:
    """
    st.write(bdm_wise)

elif option=='DSA WISE':
    """
    #### DSA WISE SALES:
    """
    st.write(dsa_wise)

elif option=='Summary':
    expander7 = st.expander("Latest Counts Here")
    expander7.table(daywise)

    #can apply customisation to almost all the properties of the card, including the progress bar
#     color_library=[533483,E94560,   used now  FB2576,3F0071, 524A4E]

    ## Target Condition (all gmv loans,reg etc) should be month wise

    ### added on 3-12-2022

    target_2023={'Jan-2022':75000000,'Feb-2022':82500000,'March-2022':110000000,'Apr-2022':105000000,'May-2022':135000000
                ,'June-2022':500000000,'July-2022':550000000,'August-2022':53000000,'Sep-2022':71000000
                ,'October-2022':65000000,'November-2022':33000000,'Dec-2022':40000000}

    reg_target_2023={'Jan-2023':30000,'Feb-2023':35000,'March-2023':35000,'Apr-2023':50000,'May-2023':50000,
                        'June-2023':35000,'July-2023':35000,'August-2023':35000,'Sep-2023':35000
                        ,'October-2023':35000,'November-2023':35000,'Dec-2023':35000}
    
    reg_target_list=list(reg_target_2023.values())     
    reg_target=reg_target_list[months_list-1]
    reg_achieve=(all_reg_count/reg_target)*100
    
# Gmv Target
    target_list=list(target_2023.values())
    target=target_list[months_list-1]
    gmv_achieve=(all_gmv/target)*100
    """
    ##### Business Done Till Selected Month/Day

    """
    col1, col2, col3,col4= st.columns(4)
    col1.metric("Overall GMV", str(f'{round((all_gmv/10000000),2)} Cr'),(f'Achieved : {round(gmv_achieve)}%'))
    col2.metric('Overall Loans',all_loan_count)
    col3.metric('Average Ticket Size',str(f'{(all_ats)}'))
    col4.metric("Overall Registration",str(f'{(all_reg_count)}'), (f'Achieved: {round(reg_achieve)}%'))

    col5,col6,col7,col8= st.columns(4)
    col5.metric("Salary Advance GMV", str(f'{round((all_sa_gmv/10000000),2)} Cr'))
    col6.metric('SA Loans',all_sa_count)
    col7.metric('Self Employed GMV', str(f'{round((all_se_gmv/10000000),2)} Cr'))
    col8.metric("SE Loans",str(f'{(all_se_count)}'))

    """ 
    ##### Expected Business In Current Month

    """
    #Always current months data
    
    year_current=2023
    exp_loan_leads=pd.read_excel(f'Report_New_{t-1}_{m}_{year_current}.xlsx',sheet_name=2)
    exp_all_gmv=exp_loan_leads['first_loan_gmv'].sum()
    exp_all_loans=exp_loan_leads['uid'].count()

    # Updated on 30-DEC-2022
    list1_2=[1, 3, 5, 7,8,10,12]  ## 31 days
    list2_1=[11,4,6,9]  ## 30 days
    list3_1=[2]
    
    if m in list1_2:
        m_value=31
    elif m in list3_1:    # Feb months list
        m_value=28  
    elif m in list2_1:
        m_value=30
        
        
    
    #GMV EXPECETD ------------------------------------------------
    exp_gmv=round(((exp_all_gmv/(t-1))*m_value),2)
    exp_target=target_list[m-1]
    exp_gmv_achieve=(exp_gmv/exp_target)*100
    daily_avg_gmv=round(exp_all_gmv/(t-1))
    daily_gmv_rqd=round(exp_target/m_value)
    lag_by=daily_avg_gmv-daily_gmv_rqd
    
    
    
    #REMAINING GMV TO ACHIEVE DAILY

    gmv_df_for_remainig=loan_leads[loan_leads['first_loan_taken_date'].isin(date_list)]
    remaining_gmv=gmv_df_for_remainig['first_loan_gmv'].sum()
    remain_days=m_value-kk
    remain_daily_gmv=(target-remaining_gmv)/remain_days
    # """
    # Here i made a df for specially gmv remaining 
    # calculations above
    # """

    col9,col10,col11,col12= st.columns(4)
    col9.metric("Expected Overall GMV", str(f'{round(((exp_all_gmv/(t-1))*m_value/10000000),2)} Cr'),(f'Expected : {round(exp_gmv_achieve)}%'))
#             col10.metric("Expected Overall Loans",str(f'{round((exp_all_loans/(t-1))*m_value)}'))
    col10.metric("Remaining GMV Daily",str(f'{round(remain_daily_gmv)}'))

    
    col11.metric("Running Average GMV",str(f'{round(exp_all_gmv/(t-1))}'),delta=str(lag_by))
    col12.metric("Target Average GMV",str(f'{round(exp_target/m_value)}'))
    
    #Registrations EXPECETD -----------------------------------------------
    year_current=2023
    reg_user_counts=pd.read_excel(f'Report_New_{t-1}_{m}_{year_current}.xlsx',sheet_name=4)
    
    # Registrations Target
    exp_df_reg_count=reg_user_counts['uid'].count()
    reg_target_list=list(reg_target_2023.values())     
    reg_target=reg_target_list[m-1]
#           reg_achieve_till_now=(exp_df_reg_count/reg_target)
    avg_reg=exp_df_reg_count/(t-1)
    exp_overall_regis=avg_reg*m_value
    exp_reg_achieve=(exp_overall_regis/reg_target)*100
    exp_daily_required=round(reg_target/m_value)
#             exp_reg_achieve=exp_reg_achieve/
    
    col13,col14,col15,col16= st.columns(4)
    col13.metric("Registration Target",str(f'{reg_target}'))
    col14.metric("Expected Overall Registration",(f'{round(exp_overall_regis)}'),(f'Expected:{round(exp_reg_achieve)}%'))
    col15.metric("Daily Average Registration",str(f'{round(avg_reg)}'),delta=round(avg_reg-exp_daily_required))
    col16.metric("Daily Required Registration",str(f'{round(exp_daily_required)}'))


if date_option1=='All':
    comment=(f'Till  {kk}-{months_list}')
else:
    comment=(f'{date_list[date_option1-1]}')

st.sidebar.write('You Selected Date :',comment)

expander1 = st.expander("Top5 DSA See Here")
expander1.table(dsa_wise.sort_values(by=['TOTAL_GMV'],ascending=False).head(6).dropna(axis=0).drop(dsa_wise.iloc[:,8::], axis=1).drop('BDM',axis=1))


import time

dtcus_df_reg_dsa=user_counts[user_counts['registration_date'].isin(final_date)]
dsawise_reg_date=dtcus_df_reg_dsa.groupby('registration_date')['current_attributed_channel'].count()

dsa_loans_datewise=common_df.groupby('current_attributed_channel')['uid'].count()
dsa_gmv_datewise=common_df.groupby('current_attributed_channel')['first_loan_gmv'].sum()

datewise_gmv_all=common_df.groupby('first_loan_taken_date')['first_loan_gmv'].sum()
datewise_loans_all=common_df.groupby('first_loan_taken_date')['uid'].count()

## Added this on 3-12-2022
expander8 = st.expander("Date-Wise gmv")
expander8.area_chart(datewise_gmv_all)

expander9 = st.expander("Date-Wise loans")
expander9.area_chart(datewise_loans_all)
#----------------------------------------------

expander2 = st.expander("GMV DSA-Wise on Selected Date")
expander2.bar_chart(dsa_gmv_datewise)

expander3 = st.expander("Loans DSA-Wise on Selected Date")
expander3.bar_chart(dsa_loans_datewise)


if date_option1=='All':

    expander4 = st.expander("Date Wise Registrations on selected date")
    expander4.area_chart(dsawise_reg_date)
else:
    pass

expander5 = st.expander("DSA Wise Registrations on selected date")

dtcus_df_reg_dsa=user_counts[user_counts['registration_date'].isin(final_date)]
dsawise_reg=dtcus_df_reg_dsa.groupby('current_attributed_channel')['registration_date'].count()

expander5.bar_chart(dsawise_reg)

# final_reg_df.sort_values(['Total'])

final_reg_df.sort_values(by=['Total'],ascending=False)
final_reg_df = final_reg_df.style.highlight_null(props="color:Transparent;")  # hide NaNs
# final_reg_df.round(decimals =0)

expander6 = st.expander("Registrations Table on Selected Date")
expander6.write(final_reg_df)

# Expander used till now 
# drop total column


import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk

chart_data = pd.DataFrame(
   np.random.randn(1000, 2) / [50, 50] + [37.76, -122.4],
   columns=['lat', 'lon'])

st.pydeck_chart(pdk.Deck(
    map_style=None,
    initial_view_state=pdk.ViewState(
        latitude=37.76,
        longitude=-122.4,
        zoom=11,
        pitch=50,
    ),
    layers=[
        pdk.Layer(
           'HexagonLayer',
           data=chart_data,
           get_position='[lon, lat]',
           radius=200,
           elevation_scale=4,
           elevation_range=[0, 1000],
           pickable=True,
           extruded=True,
        ),
        pdk.Layer(
            'ScatterplotLayer',
            data=chart_data,
            get_position='[lon, lat]',
            get_color='[200, 30, 0, 160]',
            get_radius=200,
        ),
    ],
))


