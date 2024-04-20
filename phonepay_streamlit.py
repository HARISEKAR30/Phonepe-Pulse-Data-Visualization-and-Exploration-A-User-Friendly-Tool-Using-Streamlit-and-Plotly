import streamlit as st
from streamlit_option_menu import option_menu
import psycopg2
import pandas as pd
import plotly.express as px
import json
import requests
from PIL import Image

#dataframe creation

#sql connection
mydb=psycopg2.connect(host="127.0.0.1",
                user="postgres",
                password="hari",
                port="5432",
                database="phonephedata")

cursor=mydb.cursor()

#agg insurance df

cursor.execute("SELECT * FROM aggregated_insurance")
mydb.commit()
table1=cursor.fetchall()

Agg_insurance=pd.DataFrame(table1,columns=("States","Years","Quarters","Transaction_type","Transaction_count","Transaction_amount"))

#agg transa df

cursor.execute("SELECT * FROM aggregated_transaction")
mydb.commit()
table2=cursor.fetchall()

Agg_transaction=pd.DataFrame(table2,columns=("States","Years","Quarters","Transaction_type","Transaction_count","Transaction_amount"))

#agg user df

cursor.execute("SELECT * FROM aggregated_user")
mydb.commit()
table3=cursor.fetchall() 

Agg_user=pd.DataFrame(table3,columns=("States","Years","Quarters","Brands","Transaction_count","Percentage"))

#map user df

cursor.execute("SELECT * FROM map_user")
mydb.commit()
table4=cursor.fetchall() 

Map_user=pd.DataFrame(table4,columns=("States","Years","Quarters","District","RegisteredUsers","AppOpens"))

#map insurance df

cursor.execute("SELECT * FROM map_insurance")
mydb.commit()
table5=cursor.fetchall()

Map_insurance=pd.DataFrame(table5,columns=("States","Years","Quarters","District","Transaction_count","Transaction_amount"))

#map transa df

cursor.execute("SELECT * FROM map_transaction")
mydb.commit()
table6=cursor.fetchall()

Map_transaction=pd.DataFrame(table6,columns=("States","Years","Quarters","District","Transaction_count","Transaction_amount"))

#top insurance df

cursor.execute("SELECT * FROM top_insurance")
mydb.commit()
table7=cursor.fetchall()

Top_insurance=pd.DataFrame(table7,columns=("States","Years","Quarters","Pincode","Transaction_count","Transaction_amount"))

#top transa df

cursor.execute("SELECT * FROM top_transaction")
mydb.commit()
table8=cursor.fetchall()

Top_transaction=pd.DataFrame(table8,columns=("States","Years","Quarters","Pincode","Transaction_count","Transaction_amount"))

#top user df

cursor.execute("SELECT * FROM top_user")
mydb.commit()
table9=cursor.fetchall()

Top_user=pd.DataFrame(table9,columns=("States","Years","Quarters","Pincode","RegisteredUsers"))


def Transaction_amount_count_Y(df,year):
    tacy= df[df["Years"]==year]
    tacy.reset_index(drop=True,inplace=True)

    tacyg=tacy.groupby("States")[["Transaction_count","Transaction_amount"]].sum()
    tacyg.reset_index(inplace=True)
    
    col1,col2=st.columns(2)
    with col1:
        fig_amount=px.bar(tacyg,x="States",y="Transaction_amount",title=f"{year} TRANSACTION AMOUNT",
                        color_discrete_sequence=px.colors.sequential.Oranges_r,height=650,width=600)
        st.plotly_chart(fig_amount)
    
    with col2:
        fig_count=px.bar(tacyg,x="States",y="Transaction_count",title=f"{year} TRANSACTION COUNT",
                        color_discrete_sequence=px.colors.sequential.YlGnBu_r,height=650,width=600)
        st.plotly_chart(fig_count)
    
    
    col1,col2=st.columns(2)
    with col1:
        
        url="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
        response=requests.get(url)
        data1=json.loads(response.content)
        states_name=[]
        for feature in data1["features"]:
            states_name.append(feature["properties"]["ST_NM"])
        states_name.sort()
        
        fig_india_1=px.choropleth(tacyg,geojson=data1, locations="States",featureidkey="properties.ST_NM",
                                    color="Transaction_amount",color_continuous_scale="twilight",
                                    range_color= (tacyg["Transaction_amount"].min(), tacyg["Transaction_amount"].max()),
                                    hover_name="States", title= f"{year} TRANSACTION AMOUNT", fitbounds="locations",
                                    height=600,width=600)
        fig_india_1.update_geos(visible=False)
        st.plotly_chart(fig_india_1)
        
    with col2:
        
    
        fig_india_2=px.choropleth(tacyg,geojson=data1, locations="States",featureidkey="properties.ST_NM",
                                    color="Transaction_count",color_continuous_scale="twilight",
                                    range_color= (tacyg["Transaction_count"].min(), tacyg["Transaction_count"].max()),
                                    hover_name="States", title= f"{year} TRANSACTION COUNT", fitbounds="locations",
                                    height=600,width=600)
        fig_india_2.update_geos(visible=False)
        st.plotly_chart(fig_india_2)
    return tacy
    
def Transaction_amount_count_Y_Q(df,quarter):
    tacy= df[df["Quarters"]==quarter]
    tacy.reset_index(drop=True,inplace=True)

    tacyg=tacy.groupby("States")[["Transaction_count","Transaction_amount"]].sum()
    tacyg.reset_index(inplace=True)
    
    col1,col2=st.columns(2)
    with col1:
        fig_amount=px.bar(tacyg,x="States",y="Transaction_amount",title=f"{tacy['Years'].unique()[0]} YEAR {quarter} QUARTER TRANSACTION AMOUNT",
                    color_discrete_sequence=px.colors.sequential.Oranges_r,height=650,width=500)
        st.plotly_chart(fig_amount)

    with col2:
        fig_count=px.bar(tacyg,x="States",y="Transaction_count",title=f"{tacy['Years'].unique()[0]} YEAR {quarter} QUARTER TRANSACTION COUNT",
                        color_discrete_sequence=px.colors.sequential.YlGnBu_r,height=650,width=500)
        st.plotly_chart(fig_count)
        
    col1,col2=st.columns(2)
    with col1:
        url="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
        response=requests.get(url)
        data1=json.loads(response.content)
        states_name=[]
        for feature in data1["features"]:
            states_name.append(feature["properties"]["ST_NM"])
        states_name.sort()
            
        fig_india_1=px.choropleth(tacyg,geojson=data1, locations="States",featureidkey="properties.ST_NM",
                                    color="Transaction_amount",color_continuous_scale="twilight",
                                    range_color= (tacyg["Transaction_amount"].min(), tacyg["Transaction_amount"].max()),
                                    hover_name="States", title= f"{tacy['Years'].unique()[0]} YEAR {quarter} QUARTER TRANSACTION AMOUNT", fitbounds="locations",
                                    height=600,width=600)
        fig_india_1.update_geos(visible=False)
        st.plotly_chart(fig_india_1)
        
    with col2:
    
        fig_india_2=px.choropleth(tacyg,geojson=data1, locations="States",featureidkey="properties.ST_NM",
                                    color="Transaction_count",color_continuous_scale="twilight",
                                    range_color= (tacyg["Transaction_count"].min(), tacyg["Transaction_count"].max()),
                                    hover_name="States", title= f"{tacy['Years'].unique()[0]} YEAR {quarter} QUARTER TRANSACTION COUNT", fitbounds="locations",
                                    height=600,width=600)
        fig_india_2.update_geos(visible=False)
        st.plotly_chart(fig_india_2)
    
    return tacy
def Agg_Trans_Transaction_type(df,state):

    tacy= df[df["States"]==state]
    tacy.reset_index(drop=True,inplace=True)

    tacyg=tacy.groupby("Transaction_type")[["Transaction_count","Transaction_amount"]].sum()
    tacyg.reset_index(inplace=True)
    
    col1,col2=st.columns(2)
    with col1:

        fig_pie1=px.pie(data_frame=tacyg,names= "Transaction_type",values="Transaction_amount",
                    width=600,title=f"{state.upper()} TRANSACTION AMOUNT",hole=0.4)
        st.plotly_chart(fig_pie1)

    with col2:
        fig_pie2=px.pie(data_frame=tacyg,names= "Transaction_type",values="Transaction_count",
                    width=600,title=f"{state.upper()} TRANSACTION COUNT",hole=0.4)
        st.plotly_chart(fig_pie2)    

#Agg user analysis1
def Agg_Uer_Plot1(df,year):
    aguy=df[df["Years"]==year]
    aguy.reset_index(drop=True,inplace=True)
    aguyg=pd.DataFrame(aguy.groupby("Brands")["Transaction_count"].sum())
    aguyg.reset_index(inplace=True)

    fig_bar1=px.bar(aguyg,x="Brands",y="Transaction_count",title=f"{year}th BRANDS AND TRANSACTION COUNT",
                    width=1100,color_discrete_sequence=px.colors.sequential.Oranges_r, hover_name="Brands")
    st.plotly_chart(fig_bar1)
    
    return aguy

## Agg user analysis 2
def Agg_User_Plot2(df,quarter):
    aguyq=df[df["Quarters"]==quarter]
    aguyq.reset_index(drop=True,inplace=True)
    aguyqg=pd.DataFrame(aguyq.groupby("Brands")["Transaction_count"].sum())
    aguyqg.reset_index(inplace=True)

    fig_bar1=px.bar(aguyqg,x="Brands",y="Transaction_count",title=f"{quarter} QUARTER BRANDS AND TRANSACTION COUNT",
                        width=1100,color_discrete_sequence=px.colors.sequential.Oranges_r, hover_name="Brands")
    st.plotly_chart(fig_bar1)
    
    return aguyq

#Agg user analysis 3
def Agg_User_Plot3(df,state):
    auyqs=df[df["States"]==state]
    auyqs.reset_index(drop=True,inplace=True)

    fig_line_1=px.line(auyqs,x="Brands",y="Transaction_count",hover_data=["Percentage"],
                        title= f"{state.upper()} BRANDS VS PERCENTAGE & TRANSACTION COUNT",color_discrete_sequence=px.colors.sequential.Viridis_r,
                        width=1000,markers=True)
    st.plotly_chart(fig_line_1)
    
#map insurance district 
def Map_Insur_District(df,state):

    tacy= df[df["States"]==state]
    tacy.reset_index(drop=True,inplace=True)

    tacyg=tacy.groupby("District")[["Transaction_count","Transaction_amount"]].sum()
    tacyg.reset_index(inplace=True)
    
    col1,col2=st.columns(2)
    with col1:

        fig_bar1=px.bar(tacyg, x="Transaction_amount",y="District", orientation="h",height=600,
                        title= f"{state.upper()} DISTRICT's VS TRANSACTON AMOUNT",color_discrete_sequence=px.colors.sequential.Rainbow_r)
        st.plotly_chart(fig_bar1)

    with col2:
        fig_bar2=px.bar(tacyg, x="Transaction_count",y="District", orientation="h",height=600,
                        title= f"{state.upper()} DISTRICT's VS TRANSACTON COUNT",color_discrete_sequence=px.colors.sequential.Greens_r)
        st.plotly_chart(fig_bar2)
        
#map user plot1 
def Map_User_plot1(df,year):
    muy=df[df["Years"]==year]
    muy.reset_index(drop=True,inplace=True)
    muyg=muy.groupby("States")[["RegisteredUsers","AppOpens"]].sum()
    muyg.reset_index(inplace=True)

    fig_line_1=px.line(muyg,x="States",y=["RegisteredUsers","AppOpens"],
                            title=f"{year} STATE VS REGISTERED USERS & APP OPENS",color_discrete_sequence=px.colors.sequential.Viridis_r,
                            width=1000,height=800,markers=True)
    st.plotly_chart(fig_line_1)
    
    return muy

#map user plot2 
def Map_User_plot2(df,quarter):
    muyq=df[df["Quarters"]==quarter]
    muyq.reset_index(drop=True,inplace=True)
    muyqg=muyq.groupby("States")[["RegisteredUsers","AppOpens"]].sum()
    muyqg.reset_index(inplace=True)

    fig_line_1=px.line(muyqg,x="States",y=["RegisteredUsers","AppOpens"],
                            title=f"{df['Years'].min()} YEAR {quarter} QUARTER STATE VS REGISTERED USERS & APP OPENS",color_discrete_sequence=px.colors.sequential.Viridis_r,
                            width=1000,height=800,markers=True)
    st.plotly_chart(fig_line_1)
    
    return muyq

#Map user plot 3
def Map_User_plot3(df,state):
    muyqs=df[df["States"]==state]
    muyqs.reset_index(drop=True,inplace=True)
    
    col1,col2=st.columns(2)
    with col1:

        fig_map_userbar1=px.bar(muyqs,x="RegisteredUsers",y="District",orientation="h",title=f"{state.upper()} DISTRICT's Vs REGISTERED USERS",
                                height=800,color_discrete_sequence=px.colors.sequential.Greens_r)
        st.plotly_chart(fig_map_userbar1)
        
    with col2:

        fig_map_userbar2=px.bar(muyqs,x="AppOpens",y="District",orientation="h",title=f"{state.upper()} DISTRICT's VS APP OPENS",
                                height=800,color_discrete_sequence=px.colors.sequential.Reds_r)
        st.plotly_chart(fig_map_userbar2)

# top insurance plot 1
def Top_Insurance_plot1(df,state):   
    tiy=df[df["States"]==state]
    tiy.reset_index(drop=True,inplace=True)
    
    col1,col2=st.columns(2)
    with col1:

        fig_top_insurbar1=px.bar(tiy,x="Quarters",y="Transaction_amount", hover_data=["Pincode"],title="TRANSACTION AMOUNT VS QUATERS,PINCODE",
                                    height=800,width=650,color_discrete_sequence=px.colors.sequential.Greens_r)
        st.plotly_chart(fig_top_insurbar1)
    
    with col2:
    
        fig_top_insurbar2=px.bar(tiy,x="Quarters",y="Transaction_count", hover_data=["Pincode"],title="TRANSACTION COUNT VS  QUATERS,PINCODE",
                                    height=800,width=650,color_discrete_sequence=px.colors.sequential.Reds_r)
        st.plotly_chart(fig_top_insurbar2)

#top user plot1
def Top_User_plot1(df,year):
    tuy=df[df["Years"]==year]
    tuy.reset_index(drop=True,inplace=True)
    tuyg=pd.DataFrame(tuy.groupby(["States","Quarters"])["RegisteredUsers"].sum())
    tuyg.reset_index(inplace=True)


    fig_top_plot1=px.bar(tuyg,x="States",y="RegisteredUsers", color="Quarters",title=f"{year} YEAR STATES VS REGISTERED USERS",
                                height=800,width=600,color_discrete_sequence=px.colors.sequential.Greens_r,hover_name="States")
    st.plotly_chart(fig_top_plot1)
    
    return tuy 

#Top user plot 2   
def Top_User_plot2(df,state):
    tuys=df[df["States"]==state]
    tuys.reset_index(drop=True,inplace=True)

    fig_top_plot2=px.bar(tuys,x="Quarters",y="RegisteredUsers",title="REGISTERED USERS, PINCODES VS QUATERS",
                                    height=800,width=600,color="RegisteredUsers",color_continuous_scale=px.colors.sequential.Emrld_r,hover_data=["Pincode"])
    st.plotly_chart(fig_top_plot2)

        
def Top_Chart_Transaction_Amount(table_name):
        #sql connection
        mydb=psycopg2.connect(host="127.0.0.1",
                        user="postgres",
                        password="hari",
                        port="5432",
                        database="phonephedata")
        cursor=mydb.cursor()

        #plot 1 TOP 10 order
        query1=f'''SELECT states, SUM(transaction_amount) AS transaction_amount 
                FROM {table_name}
                GROUP BY states
                order by transaction_amount desc
                limit 10;'''
                
        cursor.execute(query1)
        table1=cursor.fetchall()
        mydb.commit()

        df1=pd.DataFrame(table1,columns=("states","transaction_amount"))

        col1,col2=st.columns(2)
        with col1:
            fig_amount1=px.bar(df1,x="states",y="transaction_amount",title="TOP 10 VALUES OF STATES VS TRANSACTION AMOUNT ",hover_name="states",
                            color_discrete_sequence=px.colors.sequential.Oranges_r,height=650,width=600)
            st.plotly_chart(fig_amount1)

        #plot 2 LEAT 10 order
        query2=f'''SELECT states, SUM(transaction_amount) AS transaction_amount 
                FROM {table_name}
                GROUP BY states
                order by transaction_amount
                limit 10;'''
                
        cursor.execute(query2)
        table2=cursor.fetchall()
        mydb.commit()

        df2=pd.DataFrame(table2,columns=("states","transaction_amount"))

        with col2:
            fig_amount2=px.bar(df2,x="states",y="transaction_amount",title=" LAST 10 VALUES OF STATES VS TRANSACTION AMOUNT ",hover_name="states",
                            color_discrete_sequence=px.colors.sequential.haline_r,height=650,width=600)
            st.plotly_chart(fig_amount2)


        #plot 3 avg 
        query3=f'''SELECT states, AVG(transaction_amount) AS avg_transaction_amount 
                FROM {table_name}
                GROUP BY states
                order by avg_transaction_amount;'''
                
        cursor.execute(query3)
        table3=cursor.fetchall()
        mydb.commit()

        df3=pd.DataFrame(table3,columns=("states","avg_transaction_amount"))

        fig_amount3=px.bar(df3,y="states",x="avg_transaction_amount",title=" AVERAGE VALUES OF  STATES VS TRANSACTION AMOUNT ",hover_name="states",orientation='h',
                        color_discrete_sequence=px.colors.sequential.Redor_r,height=800,width=1000)
        st.plotly_chart(fig_amount3)

        
def Top_Chart_Transaction_Count(table_name):
        #sql connection
        mydb=psycopg2.connect(host="127.0.0.1",
                        user="postgres",
                        password="hari",
                        port="5432",
                        database="phonephedata")
        cursor=mydb.cursor()

        #plot 1 TOP 10 order
        query1=f'''SELECT states, SUM(transaction_count) AS transaction_count 
                FROM {table_name}
                GROUP BY states
                order by transaction_count desc
                limit 10;'''
                
        cursor.execute(query1)
        table1=cursor.fetchall()
        mydb.commit()

        df1=pd.DataFrame(table1,columns=("states","transaction_count"))
        
        col1,col2=st.columns(2)
        with col1:

            fig_amount1=px.bar(df1,x="states",y="transaction_count",title="TOP 10 VALUES OF STATES VS TRANSACTION COUNT ",hover_name="states",
                            color_discrete_sequence=px.colors.sequential.Oranges_r,height=650,width=600)
            st.plotly_chart(fig_amount1)

        #plot 2 LEATS 10 order
        query2=f'''SELECT states, SUM(transaction_count) AS transaction_count 
                FROM {table_name}
                GROUP BY states
                order by transaction_count
                limit 10;'''
                
        cursor.execute(query2)
        table2=cursor.fetchall()
        mydb.commit()

        df2=pd.DataFrame(table2,columns=("states","transaction_count"))
        
        with col2:

            fig_amount2=px.bar(df2,x="states",y="transaction_count",title=" LAST 10 VALUES OF STATES VS TRANSACTION COUNT ",hover_name="states",
                            color_discrete_sequence=px.colors.sequential.haline_r,height=650,width=600)
            st.plotly_chart(fig_amount2)


        #plot 3 avg 
        query3=f'''SELECT states, AVG(transaction_count) AS avg_transaction_count 
                FROM {table_name}
                GROUP BY states
                order by avg_transaction_count;'''
                
        cursor.execute(query3)
        table3=cursor.fetchall()
        mydb.commit()

        df3=pd.DataFrame(table3,columns=("states","avg_transaction_count"))

        fig_amount3=px.bar(df3,y="states",x="avg_transaction_count",title=" AVERAGE VALUES OF  STATES VS TRANSACTION COUNT ",hover_name="states",orientation='h',
                        color_discrete_sequence=px.colors.sequential.Redor_r,height=800,width=1000)
        st.plotly_chart(fig_amount3)

def Top_Chart_RegisteredUsers(table_name,state):
    mydb=psycopg2.connect(host="127.0.0.1",
                        user="postgres",
                        password="hari",
                        port="5432",
                        database="phonephedata")
    cursor=mydb.cursor()

    #plot_1 top 10 
    query1= f'''SELECT districts, SUM(registeredusers) AS registeredusers
                FROM {table_name}
                WHERE states= '{state}'
                GROUP BY districts
                ORDER BY registeredusers DESC
                LIMIT 10;'''

    cursor.execute(query1)
    table1= cursor.fetchall()
    mydb.commit()

    df1= pd.DataFrame(table1, columns=("districts", "registeredusers"))

    col1,col2=st.columns(2)
    with col1:
        fig_ru1= px.bar(df1, x="districts", y="registeredusers", title="TOP 10 VALUES OF DISTRICTS VS REGISTERED USER", hover_name= "districts",
                            color_discrete_sequence=px.colors.sequential.Aggrnyl, height= 650,width= 600)
        st.plotly_chart(fig_ru1)

    #plot2 least 10 values
    query2= f'''SELECT districts, SUM(registeredusers) AS registeredusers
                FROM {table_name}
                WHERE states= '{state}'
                GROUP BY districts
                ORDER BY registeredusers 
                LIMIT 10;'''

    cursor.execute(query2)
    table2= cursor.fetchall()
    mydb.commit()

    df2= pd.DataFrame(table2, columns=("districts", "registeredusers"))

    with col2:
        fig_ru2= px.bar(df2, x="districts", y="registeredusers", title="LEAST 10 VALUES OF DISTRICTS VS REGISTERED USER", hover_name= "districts",
                            color_discrete_sequence=px.colors.sequential.Rainbow_r, height= 650,width= 600)
        st.plotly_chart(fig_ru2)

    #plot 3 avg values
    query3= f'''SELECT districts, AVG(registeredusers) AS avg_registeredusers
                FROM {table_name}
                WHERE states='{state}'
                GROUP BY districts
                ORDER BY avg_registeredusers 
                LIMIT 10;'''

    cursor.execute(query3)
    table3= cursor.fetchall()
    mydb.commit()

    df3= pd.DataFrame(table3, columns=("districts", "avg_registeredusers"))


    fig_ru3= px.bar(df3, y="districts", x="avg_registeredusers", title="AVG VALUES OF DISTRICTS VS REGISTERED USER",orientation='h' ,hover_name= "districts",
                        color_discrete_sequence=px.colors.sequential.Rainbow_r, height= 650,width= 600)
    st.plotly_chart(fig_ru3)

def Top_Chart_RegisteredUsers(table_name):
    mydb=psycopg2.connect(host="127.0.0.1",
                        user="postgres",
                        password="hari",
                        port="5432",
                        database="phonephedata")
    cursor=mydb.cursor()

    #plot_1 top 10 
    query1= f'''SELECT states, SUM(registeredusers) AS registeredusers
                FROM {table_name}
                GROUP BY states
                ORDER BY registeredusers DESC
                LIMIT 10;'''

    cursor.execute(query1)
    table1= cursor.fetchall()
    mydb.commit()

    df1= pd.DataFrame(table1, columns=("states", "registeredusers"))
    
    col1,col2=st.columns(2)
    with col1:

        fig_ru1= px.bar(df1, x="states", y="registeredusers", title="TOP 10 VALUES OF STATES VS REGISTERED USER", hover_name= "states",
                            color_discrete_sequence=px.colors.sequential.Aggrnyl, height= 650,width= 600)
        st.plotly_chart(fig_ru1)

    #plot2 least 10 values
    query2= f'''SELECT states, SUM(registeredusers) AS registeredusers
                FROM {table_name}
                GROUP BY states
                ORDER BY registeredusers 
                LIMIT 10;'''

    cursor.execute(query2)
    table2= cursor.fetchall()
    mydb.commit()

    df2= pd.DataFrame(table2, columns=("states", "registeredusers"))

    with col2:
        fig_ru2= px.bar(df2, x="states", y="registeredusers", title="LEAST 10 VALUES OF STATES VS REGISTERED USER", hover_name= "states",
                            color_discrete_sequence=px.colors.sequential.Rainbow_r, height= 650,width= 600)
        st.plotly_chart(fig_ru2)

    #plot 3 avg values
    query3= f'''SELECT states, AVG(registeredusers) AS avg_registeredusers
                FROM {table_name}
                GROUP BY states
                ORDER BY avg_registeredusers 
                LIMIT 10;'''

    cursor.execute(query3)
    table3= cursor.fetchall()
    mydb.commit()

    df3= pd.DataFrame(table3, columns=("states", "avg_registeredusers"))


    fig_ru3= px.bar(df3, y="states", x="avg_registeredusers", title="AVG VALUES OF STATES VS REGISTERED USER",orientation='h' ,hover_name= "states",
                        color_discrete_sequence=px.colors.sequential.Rainbow_r, height= 800,width= 1000)
    st.plotly_chart(fig_ru3)

def Top_Chart_Appopens(table_name, state):
    mydb=psycopg2.connect(host="127.0.0.1",
                        user="postgres",
                        password="hari",
                        port="5432",
                        database="phonephedata")
    cursor=mydb.cursor()

    #plot_1 TOP 10 
    query1= f'''SELECT districts, SUM(appopens) AS appopens
                FROM {table_name}
                WHERE states= '{state}'
                GROUP BY districts
                ORDER BY appopens DESC
                LIMIT 10;'''

    cursor.execute(query1)
    table1= cursor.fetchall()
    mydb.commit()

    df1= pd.DataFrame(table1, columns=("districts", "appopens"))

    col1,col2=st.columns(2)
    with col1:

        fig_apo= px.bar(df1, x="districts", y="appopens", title="TOP 10 VALUES OF APPOPENS VS DISTRICTS ", hover_name= "districts",
                            color_discrete_sequence=px.colors.sequential.Aggrnyl, height= 650,width= 600)
        st.plotly_chart(fig_apo)

    #plot_2 LEAST 10
    query2= f'''SELECT districts, SUM(appopens) AS appopens
                FROM {table_name}
                WHERE states= '{state}'
                GROUP BY districts
                ORDER BY appopens
                LIMIT 10;'''

    cursor.execute(query2)
    table2= cursor.fetchall()
    mydb.commit()

    df2= pd.DataFrame(table2, columns=("districts", "appopens"))

    with col2:

        fig_apo2= px.bar(df2, x="districts", y="appopens", title="LAST 10 VALUES OF APPOPENS VS DISTRICTS", hover_name= "districts",
                            color_discrete_sequence=px.colors.sequential.Aggrnyl_r, height= 650,width= 600)
        st.plotly_chart(fig_apo2)

    #plot_3 avg values
    query3= f'''SELECT districts, AVG(appopens) AS avg_appopens
                FROM {table_name}
                WHERE states= '{state}'
                GROUP BY districts
                ORDER BY avg_appopens;'''

    cursor.execute(query3)
    table3= cursor.fetchall()
    mydb.commit()

    df3= pd.DataFrame(table3, columns=("districts", "avg_appopens"))

    fig_apo3= px.bar(df3, y="districts", x="avg_appopens", title="AVERAGE VALUES OF APPOPENS VS DISTRICTS", hover_name= "districts", orientation= "h",
                        color_discrete_sequence=px.colors.sequential.Bluered_r, height= 800,width= 1000)
    st.plotly_chart(fig_apo3)


    
# Streamlit code

icon = Image.open(r"C:\Users\ADMIN\Desktop\download.png")
st.set_page_config(page_title= "PHONEPE PULSE ANALYSIS | By  HARI RAM",
                    page_icon= icon,
                    layout= "wide",
                    initial_sidebar_state= "expanded",
                    menu_items={'About': """# This app is created by *HARI RAM*"""})
st.title(":white[PHONEPE DATA VISUALIZATION AND EXPLORATION]")

with st.sidebar:
    
    select=option_menu("Main Menu",["HOME","DATA EXPLORATION","TOP CHARTS"],
                        icons=["house","bar-chart-steps","rainbow"],
                    default_index=0,
                    orientation="vertical",
                    styles={"container":{"background-color":"#6C22A6","size":"cover","width":"100%"},
                    "icon": {"color":"black","font-size":"20px"},
                    "nav-link": {"font-size":"20px","text-align":"left","margin":"-2px","--hover-color":"#FFA732"},
                    "nav-link-selected":{"background-color":"#A459D1"}})
    

page_bg_img = f"""
<style>
[data-testid="stAppViewContainer"] > .main {{
background-color: #6C22A6;
opacity: 0.9;
background-image: radial-gradient(circle at center center, #ffffff, #96E9C6), repeating-radial-gradient(circle at center center, #ffffff, #ffffff, 13px, transparent 26px, transparent 13px);
background-blend-mode: multiply;
}}

</style>
"""
st.markdown(page_bg_img, unsafe_allow_html=True)  
        
if select == "HOME":
    
    col1,col2= st.columns(2)

    with col1:
        st.header(":white[PHONEPE]")
        st.subheader(":red[INDIA'S BEST TRANSACTION APP]")
        st.markdown("PhonePe is a mobile payment platform using which you can transfer money using UPI, recharge phone numbers, pay utility bills, etc. PhonePe works on the Unified Payment Interface (UPI) system and all you need is to feed in your bank account details and create a UPI ID.")
        st.write("****AVAILABLE FEATURES THROUGH ONE CLICK****")
        st.write("****UPI Payments****")
        st.write("****Linking with Bank Accounts****")
        st.write("****Phonepe Wallet****")
        st.write("****Pay all your Bills****")
        st.write("Insurance")
        st.download_button("DOWNLOAD THE APP NOW", "https://www.phonepe.com/app-download/")
    
    with col2:
        video_path = r"C:\Users\ADMIN\Downloads\phone.mp4"
        st.video(video_path)
    
    col3,col4=st.columns(2)    
    with col3:
        video_path = r"C:\Users\ADMIN\Downloads\phone2.mp4"
        st.video(video_path)
    
    with col4:
        st.image(Image.open(r"C:\Users\ADMIN\Desktop\download.jpeg"),width=700)
    
        
elif select == "DATA EXPLORATION":
    
    tab1, tab2, tab3=st.tabs(["Aggregated Analysis","Map Analysis","Top Analysis"])
    
    with tab1:
        method=st.radio("Select the Analysis",["Insurance Analysis","Transaction Analysis","User Analysis"])
        
        if method=="Insurance Analysis":
            
            col1,col2=st.columns(2)
            with col1:
                years= st.slider("Select the Years",Agg_insurance["Years"].min(),Agg_insurance["Years"].max(),Agg_insurance["Years"].min())
            tacy_Y=Transaction_amount_count_Y(Agg_insurance,years)
            
            col1,col2=st.columns(2)
            with col1:
                quarters= st.slider("Select the Quaters",tacy_Y["Quarters"].min(),tacy_Y["Quarters"].max(),tacy_Y["Quarters"].min())
            Transaction_amount_count_Y_Q(tacy_Y,quarters)
            
        
        
        elif method=="Transaction Analysis":
            
            col1,col2=st.columns(2)
            with col1:
                years= st.slider("Select the Years",Agg_transaction["Years"].min(),Agg_transaction["Years"].max(),Agg_transaction["Years"].min())
            Agg_tran_tac_Y=Transaction_amount_count_Y(Agg_transaction,years)
        
            col1,col2=st.columns(2)
            with col1:
                states=st.selectbox("Select the states", Agg_tran_tac_Y["States"].unique())
        
            Agg_Trans_Transaction_type(Agg_tran_tac_Y,states)
            
            col1,col2=st.columns(2)
            with col1:
                quarters= st.slider("Select the Quaters",Agg_tran_tac_Y["Quarters"].min(),Agg_tran_tac_Y["Quarters"].max(),Agg_tran_tac_Y["Quarters"].min())
            Agg_tran_tac_Y_Q= Transaction_amount_count_Y_Q(Agg_tran_tac_Y,quarters)
            
            
            col1,col2=st.columns(2)
            with col1:
                states=st.selectbox("Select the states_ty", Agg_tran_tac_Y_Q["States"].unique())
        
            Agg_Trans_Transaction_type(Agg_tran_tac_Y_Q,states)
            
            
        elif method=="User Analysis":
            
            col1,col2=st.columns(2)
            with col1:
                years= st.slider("Select the Years",Agg_user["Years"].min(),Agg_user["Years"].max(),Agg_user["Years"].min())
            Agg_user_Y=Agg_Uer_Plot1(Agg_user,years)

            col1,col2=st.columns(2)
            with col1:
                quarters= st.slider("Select the Quaters",Agg_user_Y["Quarters"].min(),Agg_user_Y["Quarters"].max(),Agg_user_Y["Quarters"].min())
            Agg_user_Y_Q= Agg_User_Plot2(Agg_user_Y,quarters)
            
            
            col1,col2=st.columns(2)
            with col1:
                states=st.selectbox("Select the states", Agg_user_Y_Q["States"].unique())
        
            Agg_User_Plot3(Agg_user_Y_Q,states)
            

    with tab2:
        method2=st.radio("Select the Analysis",["Map Insurance","Map Transaction","Map User"])
        
        if method2=="Map Insurance":
            
            col1,col2=st.columns(2)
            with col1:
                years= st.slider("Select the Years",Map_insurance["Years"].min(),Map_insurance["Years"].max(),Map_insurance["Years"].min())
            Map_Insur_tac_Y=Transaction_amount_count_Y(Map_insurance,years)
        
            col1,col2=st.columns(2)
            with col1:
                states=st.selectbox("Select the states_mi", Map_Insur_tac_Y["States"].unique())
        
            Map_Insur_District(Map_Insur_tac_Y,states)
            
            col1,col2=st.columns(2)
            with col1:
                quarters= st.slider("Select the Quaters_MI",Map_Insur_tac_Y["Quarters"].min(),Map_Insur_tac_Y["Quarters"].max(),Map_Insur_tac_Y["Quarters"].min())
            Map_Insur_tac_Y_Q= Transaction_amount_count_Y_Q(Map_Insur_tac_Y,quarters)
        
            col1,col2=st.columns(2)
            with col1:
                states=st.selectbox("Select the States_", Map_Insur_tac_Y_Q["States"].unique())
        
            Map_Insur_District(Map_Insur_tac_Y_Q,states)   
        
        elif method2=="Map Transaction":
            col1,col2=st.columns(2)
            with col1:
                years= st.slider("Select the Years MT",Map_transaction["Years"].min(),Map_transaction["Years"].max(),Map_transaction["Years"].min())
            Map_Trans_tac_Y=Transaction_amount_count_Y(Map_transaction,years)
            
            col1,col2=st.columns(2)
            with col1:
                states=st.selectbox("Select the states_mi", Map_Trans_tac_Y["States"].unique())
        
            Map_Insur_District(Map_Trans_tac_Y,states)
            
            col1,col2=st.columns(2)
            with col1:
                quarters= st.slider("Select the Quaters_MI",Map_Trans_tac_Y["Quarters"].min(),Map_Trans_tac_Y["Quarters"].max(),Map_Trans_tac_Y["Quarters"].min())
            Map_Trans_tac_Y_Q= Transaction_amount_count_Y_Q(Map_Trans_tac_Y,quarters)
        
            col1,col2=st.columns(2)
            with col1:
                states=st.selectbox("Select the States_", Map_Trans_tac_Y_Q["States"].unique())
        
            Map_Insur_District(Map_Trans_tac_Y_Q,states)  
            
        elif method2=="Map User":
            col1,col2=st.columns(2)
            with col1:
                years= st.slider("Select the Years MU",Map_user["Years"].min(),Map_user["Years"].max(),Map_user["Years"].min())
            Map_User_Y=Map_User_plot1(Map_user,years)
            
            col1,col2=st.columns(2)
            with col1:
                quarters= st.slider("Select the Quaters_MU",Map_User_Y["Quarters"].min(),Map_User_Y["Quarters"].max(),Map_User_Y["Quarters"].min())
            Map_User_Y_Q= Map_User_plot2(Map_User_Y,quarters)
            
            col1,col2=st.columns(2)
            with col1:
                states=st.selectbox("Select the States_MU", Map_User_Y_Q["States"].unique())
        
            Map_User_plot3(Map_User_Y_Q,states)  
        
    with tab3:
        method3=st.radio("Select the Analysis",["Top Insurance","Top Transaction","Top User"])
        
        if method3=="Top Insurance":
            
            col1,col2=st.columns(2)
            with col1:
                years= st.slider("Select the Years TI",Top_insurance["Years"].min(),Top_insurance["Years"].max(),Top_insurance["Years"].min())
            Top_Insur_tac_Y=Transaction_amount_count_Y(Top_insurance,years)

            col1,col2=st.columns(2)
            with col1:
                states=st.selectbox("Select the States_TI", Top_Insur_tac_Y["States"].unique())
        
            Top_Insurance_plot1(Top_Insur_tac_Y,states)  
            
            col1,col2=st.columns(2)
            with col1:
                quarters= st.slider("Select the Quaters_TI",Top_Insur_tac_Y["Quarters"].min(),Top_Insur_tac_Y["Quarters"].max(),Top_Insur_tac_Y["Quarters"].min())
            Top_Insur_tac_Y_Q= Transaction_amount_count_Y_Q(Top_Insur_tac_Y,quarters)
            
        elif method3=="Top Transaction":
            
            col1,col2=st.columns(2)
            with col1:
                years= st.slider("Select the Years TT",Top_transaction["Years"].min(),Top_transaction["Years"].max(),Top_transaction["Years"].min())
            Top_Trans_tac_Y=Transaction_amount_count_Y(Top_transaction,years)

            col1,col2=st.columns(2)
            with col1:
                states=st.selectbox("Select the States_TT", Top_Trans_tac_Y["States"].unique())
        
            Top_Insurance_plot1(Top_Trans_tac_Y,states)  
            
            col1,col2=st.columns(2)
            with col1:
                quarters= st.slider("Select the Quaters_TI",Top_Trans_tac_Y["Quarters"].min(),Top_Trans_tac_Y["Quarters"].max(),Top_Trans_tac_Y["Quarters"].min())
            Top_Trans_tac_Y_Q= Transaction_amount_count_Y_Q(Top_Trans_tac_Y,quarters)
        
        elif method3=="Top User":
            col1,col2=st.columns(2)
            with col1:
                years= st.slider("Select the Years TU",Top_user["Years"].min(),Top_user["Years"].max(),Top_user["Years"].min())
            Top_User_Y=Top_User_plot1(Top_user,years)    
            
            col1,col2=st.columns(2)
            with col1:
                states=st.selectbox("Select the States_TU", Top_User_Y["States"].unique())
        
            Top_User_plot2(Top_User_Y,states)  
            

elif select == "TOP CHARTS":
    query=st.selectbox("Choose the query",["1. Transaction Amount and Count of Aggregated Insurance",
                                            "2. Transaction Amount and Count of Map Insurance",
                                            "3. Transaction Amount and Count of Top Insurance",
                                            "4. Transaction Amount and Count of Aggregated Transaction",
                                            "5. Transaction Amount and Count of Map Transaction",
                                            "6. Transaction Amount and Count of Top Transaction",
                                            "7. Transaction Count of Aggregated User",
                                            "8. Registered users of Map User",
                                            "9. App opens of Map User",
                                            "10. Registered users of Top User",])
    
    if query=="1. Transaction Amount and Count of Aggregated Insurance":
        select=st.selectbox("SELECT THE ANALYSIS",("TRANSACTION AMOUNT","TRANSACTION COUNT"))
        if select=="TRANSACTION AMOUNT":
                st.subheader("TRANSACTION AMOUNT")
                Top_Chart_Transaction_Amount("aggregated_insurance")
        
        if select=="TRANSACTION COUNT":
                st.subheader("TRANSACTION COUNT")
                Top_Chart_Transaction_Count("aggregated_insurance")

    
    elif query=="2. Transaction Amount and Count of Map Insurance":
        select=st.selectbox("SELECT THE ANALYSIS",("TRANSACTION AMOUNT","TRANSACTION COUNT"))
        if select=="TRANSACTION AMOUNT":
                st.subheader("TRANSACTION AMOUNT")
                Top_Chart_Transaction_Amount("map_insurance")
        
        if select=="TRANSACTION COUNT":
                st.subheader("TRANSACTION COUNT")
                Top_Chart_Transaction_Count("map_insurance")
                
    
    elif query=="3. Transaction Amount and Count of Top Insurance":
        select=st.selectbox("SELECT THE ANALYSIS",("TRANSACTION AMOUNT","TRANSACTION COUNT"))
        if select=="TRANSACTION AMOUNT":
                st.subheader("TRANSACTION AMOUNT")
                Top_Chart_Transaction_Amount("top_insurance")
        
        if select=="TRANSACTION COUNT":
                st.subheader("TRANSACTION COUNT")
                Top_Chart_Transaction_Count("top_insurance")
                
    elif query=="4. Transaction Amount and Count of Aggregated Transaction":
        select=st.selectbox("SELECT THE ANALYSIS",("TRANSACTION AMOUNT","TRANSACTION COUNT"))
        if select=="TRANSACTION AMOUNT":
                st.subheader("TRANSACTION AMOUNT")
                Top_Chart_Transaction_Amount("aggregated_transaction")
        
        if select=="TRANSACTION COUNT":
                st.subheader("TRANSACTION COUNT")
                Top_Chart_Transaction_Count("aggregated_transaction")
    
    elif query=="5. Transaction Amount and Count of Map Transaction":
        select=st.selectbox("SELECT THE ANALYSIS",("TRANSACTION AMOUNT","TRANSACTION COUNT"))
        if select=="TRANSACTION AMOUNT":
                st.subheader(":blue[TRANSACTION AMOUNT]")
                Top_Chart_Transaction_Amount("map_transaction")
        
        if select=="TRANSACTION COUNT":
                st.subheader(":blue[TRANSACTION COUNT]")
                Top_Chart_Transaction_Count("map_transaction")
                
    
    elif query=="6. Transaction Amount and Count of Top Transaction":
        select=st.selectbox("SELECT THE ANALYSIS",("TRANSACTION AMOUNT","TRANSACTION COUNT"))
        if select=="TRANSACTION AMOUNT":
                st.subheader(":blue[TRANSACTION AMOUNT]")
                Top_Chart_Transaction_Amount("top_transaction")
        
        if select=="TRANSACTION COUNT":
                st.subheader(":blue[TRANSACTION COUNT]")
                Top_Chart_Transaction_Count("top_transaction")
                
    elif query=="7. Transaction Count of Aggregated User":
                st.subheader(":blue[TRANSACTION COUNT]")
                Top_Chart_Transaction_Count("aggregated_user")
    
    elif query=="8. Registered users of Map User":
                states= st.selectbox("Select the State", Map_user["States"].unique())   
                st.subheader(":blue[REGISTERED USERS]")
                Top_Chart_RegisteredUsers("map_user", states)
                
    elif query=="9. App opens of Map User":
                states= st.selectbox("Select the State", Map_user["States"].unique())   
                st.subheader(":blue[APPOPENS]")
                Top_Chart_Appopens("map_user", states)
    
    elif query=="10. Registered users of Top User":
                st.subheader(":blue[REGISTERED USERS]")
                Top_Chart_RegisteredUsers("top_user")