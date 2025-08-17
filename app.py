import streamlit as st
import pandas as pd
import plotly.express as px


df = pd.read_csv("total.csv", encoding="utf-8")
version_info = pd.read_csv("versioninfo.csv", encoding="utf-8")

st.title("캐릭터 별 나선 픽률 📊")

st.sidebar.header("캐릭터 선택")

if st.sidebar.button("전체 선택 해제"):
    for key in list(st.session_state.keys()):
        if key in df["이름"].unique():
            st.session_state[key] = False

selected_names = []

for group, group_df in df.groupby("속성"):
    with st.sidebar.expander(group, expanded=False):
        for name in group_df["이름"].unique():
            cols = st.columns([3])
            with cols[0]:
                checked = st.checkbox(name, value=st.session_state.get(name, False), key=name)
                if checked:
                    selected_names.append(name)


filtered_df = df[df["이름"].isin(selected_names)]

fig = px.line(filtered_df,
    x="기간",
    y="사용률",
    color="이름",
    line_group="이름",
    markers=True,
    hover_data=["버전"]
)

fig.update_xaxes(
    tickformat="%y-%-m-%-d"
)

fig.update_layout(
    showlegend=False
)


for name in selected_names:
    person_df = filtered_df[filtered_df["이름"] == name].sort_values("기간")
    if len(person_df) == 0:
        continue

    last_row = person_df.iloc[-1]
    x_val, y_val = last_row["기간"], last_row["사용률"]

    fig.add_annotation(
        x=x_val,
        y=y_val,
        text=name,
        showarrow=False,
        xanchor="left",
        yanchor="bottom"
    )


vline_dates = version_info["start_date"].values.tolist()
vline_texts = version_info["version"].values.tolist()

for date_str, label in zip(vline_dates, vline_texts):
    date = pd.to_datetime(date_str)
    
    fig.add_vline(
        x=date,
        line=dict(color="#777777", width=0.3, dash="dash"),
    )
    
    fig.add_annotation(
        x=date,
        y=df["사용률"].max()+2,
        text=label,
        showarrow=False,
        xanchor="left",
        yanchor="bottom"
    )

st.plotly_chart(fig, use_container_width=True)