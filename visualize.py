import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

# خواندن داده‌های فایل اکسل
file_path = 'Samimi.xlsx'
df = pd.read_excel(file_path, sheet_name=None)

# نمایش نام شیت‌های اکسل
sheet_names = df.keys()
st.sidebar.title("Dashboard")
selected_sheet = st.sidebar.selectbox("Select a sheet", list(sheet_names))

# نمایش داده‌های شیت انتخابی
data = df[selected_sheet]
st.write(f"## Data from {selected_sheet} sheet")
st.dataframe(data)

# رسم نمودار پای
st.write("### Pie Chart")
pie_column = st.selectbox("Select column for Pie Chart", data.columns)
pie_data = data[pie_column].value_counts()
fig_pie = px.pie(values=pie_data.values, names=pie_data.index, title=f'Pie Chart of {pie_column}')
st.plotly_chart(fig_pie)

# رسم نمودار میله‌ای
st.write("### Bar Chart")
bar_column = st.selectbox("Select column for Bar Chart", data.columns)
bar_data = data[bar_column].value_counts()
fig_bar = px.bar(x=bar_data.index, y=bar_data.values, title=f'Bar Chart of {bar_column}')
st.plotly_chart(fig_bar)

# رسم نمودار خطی
st.write("### Line Chart")
line_column = st.selectbox("Select column for Line Chart", data.columns)
fig_line, ax = plt.subplots()
ax.plot(data[line_column])
ax.set_title(f'Line Chart of {line_column}')
st.pyplot(fig_line)
