import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
from plotly.subplots import make_subplots
from pandasql import sqldf
import plotly.graph_objects as go
import streamlit as st



st.title('Superstore Analysis Presentation')

df = ('df2.csv')

#Will add @st.cache to prevent the app from loading the data each time an update is made
@st.cache
def load_data(nrows):
    data = pd.read_csv(df, nrows=nrows)
    return data

# Create a text element and let the reader know the data is loading.
data_load_state = st.text('Loading data...')
# Load 9800 rows of data into the dataframe.
data = load_data(9800)
# Notify the reader that the data was successfully loaded.
data_load_state.text("Done! (using st.cache)")

#Display the data
if st.checkbox('Show raw data'):
    st.subheader('Raw data')
    st.write(data)

st.subheader('Time Analysis')
st.text('We shall start our analysis by observing Sales between 2015-2018')


#TIME ANALYSIS
st.text('Questions')
st.markdown(
    """
    1.  What is the year, month and day with the highest sales

    2.  What is the sales trend between 2015 and 2018?

    3.  What is the order fulfillment period (Period between order and ship date)
    """
)

year_sales = pd.read_csv("year_sales.csv") #path folder of the data file
time = pd.read_csv("time.csv")
#st.write(year_sales)

#Lineplot
fig = plt.figure(figsize=(10, 4))
sns.lineplot(data=year_sales, x='order_year', y='Sales', ci=None)
plt.title('Lineplot showing Sales Orders Over The years')
st.pyplot(fig)


#Bar graph
fig = plt.figure(figsize=(15,15))
ax= plt.subplot(221)
ax=sns.barplot(data=year_sales, x='order_year',y='Sales')
ax=plt.title('Sales per Year')
st.pyplot(fig)

ax1=plt.subplot(222)
ax1=sns.barplot(data=time, x='order_month', y='Sales', hue='order_year')
ax1=plt.title('Monthly sales per year')
st.pyplot(fig)



#fig = make_subplots(rows=1, cols=2, start_cell="bottom-left",subplot_titles=("First Subplot","Second Subplot"))

#fig.add_trace(go.Bar(x=year_sales['order_year'], y=year_sales['Sales']),
#              row=1, col=1)

#fig.update_layout(height=500, width=700,
#                  title_text="Multiple Subplots with ")

#fig.add_trace(go.Bar(x=time['order_month'], y=time['Sales']),
#              row=1, col=2)

#st.plotly_chart(fig, use_container_width=True)


fig=plt.figure(figsize=(15,15))
sns.boxplot(data=data, x='delivery_duration', y='Ship Mode')
plt.title('Boxplot Showing Delivery Duration Distribution')
st.pyplot(fig)

st.markdown("""
From this analysis we can observe that

- There has been a steady increase in sales after a slight dip in 2016
- Sales generally start increasing from the month of September
- Depending on the mode of delivery, products are delivered on time
""")

#CATEGORY AND SEGMENT ANALYSIS
st.subheader(' Segment and Category Analysis')
st.markdown("""
Questions
1. Which segment has the highest sales?

2. Show sales in each segment by category

3. What is the highest selling sub-category and which sub-category sells the most
""")

seg_cat = pd.read_csv('seg_cat.csv')

#sunburst chart
fig = plt.figure(figsize=(10,10))
fig = px.sunburst(seg_cat, path=['Segment', 'Category'], values='Sales',)
#fig.show()
st.plotly_chart(fig, use_container_width=True)

#Icicle Chart
cat_sub = pd.read_csv('cat_sub.csv')

fig = px.icicle(cat_sub, path=[px.Constant('Total_Sales'), 'Category', 'Sub-Category'], values='Total_Sales', title='Sales by Category and Sub-Category')
fig.update_traces(root_color="lightgrey")
fig.update_layout(margin = dict(t=50, l=25, r=25, b=15))
st.plotly_chart(fig, use_container_width=True)

#Funnel Chart
fig = px.funnel(cat_sub, x='Total_Sales', y='Sub-Category', title="Sub-Category Sales Breakdown")
st.plotly_chart(fig, use_container_width=True)


#Category and Segment findings
st.markdown("""
We were able to observe
- Amongst the three segments, Consumer makes the most sales.
- There are three product categories with technology making the highest sales in each of the segment
- Phones, Chairs and Storage are the highest selling sub-categories
""")

#REGION ANALYSIS
st.subheader('Analysis by Region')

st.markdown("""
Questions
1. Best performing region
2. Customers in each region
3. Top selling states
4. Best selling products in each region
5. Top 10 selling cities in each region
""")

region = pd.read_csv('region.csv')
if st.checkbox("Show region data"):
    st.subheader('Region data')
    st.write(region)

fig = plt.figure(figsize=(3,3))
sns.barplot(data=region, x='Region', y='Sales', ci=None)
plt.title('Sales by Region')
st.pyplot(fig)

#Number of customers by region
cust_reg = pd.read_csv('cust_reg.csv')
fig = px.pie(cust_reg, values='Customer ID', names='Region',
             title='Number of Customers By Region',
             hover_data=['Sales'], labels={'Sales':'Total Sales'})

st.plotly_chart(fig, use_container_width=True)


#Choose Region
west_states = pd.read_csv('west.csv')
wsct= pd.read_csv('wsct.csv')
wscb= pd.read_csv('wscb.csv')

east_states = pd.read_csv('east.csv')
esct = pd.read_csv('esct.csv')
escb = pd.read_csv('escb.csv')

central_states = pd.read_csv('central.csv')
csct = pd.read_csv('csct.csv')
cscb = pd.read_csv('cscb.csv')

south_states = pd.read_csv('south.csv')
ssct = pd.read_csv('ssct.csv')
sscb = pd.read_csv('sscb.csv')



options = st.multiselect('Choose Region', ['West', 'East', 'South', 'Central'])

if 'West' in options:
    fig = px.bar(west_states, x='State', y='Sales', title='Sales by State in the West Region')
    st.plotly_chart(fig, use_container_width=True)

    fig=px.bar(wsct, x='City', y='Sales', title='Top Performing Cities in the West', height=400)
    st.plotly_chart(fig, use_container_width=True)

    fig=px.bar(wscb, x='City', y='Sales', title='Least Performing Cities in the West', height=400)
    st.plotly_chart(fig, use_container_width=True)


if 'East' in options:
    fig = px.bar(east_states, x='State', y='Sales', title='Sales by State in the East Region')
    st.plotly_chart(fig, use_container_width=True)

    fig=px.bar(esct, x='City', y='Sales', title='Top Performing Cities in the East', height=400)
    st.plotly_chart(fig, use_container_width=True)

    fig=px.bar(escb, x='City', y='Sales', title='LeastPerforming Cities in the East', height=400)
    st.plotly_chart(fig, use_container_width=True)


if 'Central' in options:
    fig = px.bar(central_states, x='State', y='Sales', title='Sales by State in the Central Region')
    st.plotly_chart(fig, use_container_width=True)

    fig=px.bar(csct, x='City', y='Sales', title='Top Performing Cities in the Central', height=400)
    st.plotly_chart(fig, use_container_width=True)

    fig=px.bar(cscb, x='City', y='Sales', title='Least Performing Cities in the Central', height=400)
    st.plotly_chart(fig, use_container_width=True)


if 'South' in options:
    fig = px.bar(south_states, x='State', y='Sales', title='Sales by State in the South Region')
    st.plotly_chart(fig, use_container_width=True)

    fig=px.bar(ssct, x='City', y='Sales', title='Top Performing Cities in the South', height=400)
    st.plotly_chart(fig, use_container_width=True)

    fig=px.bar(sscb, x='City', y='Sales', title='Least Performing Cities in the South', height=400)
    st.plotly_chart(fig, use_container_width=True)
    


