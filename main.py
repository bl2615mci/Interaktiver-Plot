import functions as f
import streamlit as st


df = f.read_my_csv("data/activity.csv")
wert = st.slider("Your max heart rate:", min_value=100, max_value=250, value=200, step=1)
st.write("You have selected:", wert)

f.Heart_Zone(df, wert)
zone_time_df = f.Zone_Time(df).reset_index()
zone_time_df.columns = ["Zone", "Estimated Time [ms]"]
average_power_by_zone = f.Average_Power_Zone(df, "PowerOriginal")



fig = f.make_plot_with_zones_and_power(df, wert, "HeartRate", "PowerOriginal")
st.plotly_chart(fig, use_container_width=True)

st.write("Average Power:", f.mittelwert(df, "PowerOriginal"))
st.write("Max Power:", f.maximalwert(df, "PowerOriginal"))

tab1, tab2 = st.tabs(["Zone Time", "Average Power by Zone"])

with tab1:
    st.subheader("Zone Time")
    st.table(zone_time_df[0:5][["Zone", "Estimated Time [ms]"]])

with tab2:
    st.subheader("Average Power by Zone")
    st.table(average_power_by_zone[1:5])
