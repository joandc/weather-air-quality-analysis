from pathlib import Path

import pandas as pd
import streamlit as st
from scipy import stats


st.set_page_config(
    page_title="Weather and Air Quality | Toronto vs Vancouver",
    layout="wide",
    initial_sidebar_state="expanded",
)


st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

h1, h2, h3,
[data-testid="stMarkdownContainer"] h1,
[data-testid="stMarkdownContainer"] h2,
[data-testid="stMarkdownContainer"] h3 {
    color: #0f172a !important;
}

[data-testid="stCaptionContainer"] p {
    font-size: 1.2rem !important;
}

[data-testid="stMarkdownContainer"] p,
[data-testid="stMarkdownContainer"] li {
    color: #334155;
}

[data-testid="stSidebar"] {
    background: #0f172a !important;
    border-right: 1px solid #1e293b !important;
}

[data-testid="stSidebar"] * {
    color: #cbd5e1 !important;
}

[data-testid="stSidebar"] input {
    color: #0f172a !important;
    -webkit-text-fill-color: #0f172a !important;
}

[data-testid="stSidebar"] [data-baseweb="input"] input {
    color: #0f172a !important;
    -webkit-text-fill-color: #0f172a !important;
}

[data-testid="stSidebar"] [data-baseweb="input"] {
    background: #ffffff !important;
}

[data-testid="metric-container"] {
    background: #1e293b !important;
    border: 1px solid #334155 !important;
    border-radius: 12px !important;
    padding: 1rem 1.2rem !important;
}

[data-testid="stMetricLabel"] {
    font-size: 1.2rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.05em !important;
    text-transform: uppercase !important;
    color: #34d399;
}

[data-testid="stMetricValue"] {
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 1.45rem !important;
}

.hero-wrap {
    background: linear-gradient(135deg, #0f172a 0%, #0c2340 60%, #0d3a6e 100%);
    border: 1px solid #1e3a5f;
    border-radius: 18px;
    padding: 2.5rem 2.5rem 2rem 2.5rem;
    margin-bottom: 1.75rem;
}

.hero-grid {
    display: grid;
    grid-template-columns: minmax(0, 1.9fr) minmax(150px, 0.9fr);
    gap: 1.5rem;
    align-items: center;
}

.hero-copy {
    min-width: 0;
}

.hero-tag {
    display: inline-block;
    background: rgba(56, 189, 248, 0.12);
    border: 1px solid rgba(56, 189, 248, 0.25);
    color: #7dd3fc;
    font-size: 0.72rem;
    font-weight: 700;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    padding: 0.28rem 0.85rem;
    border-radius: 999px;
    margin-bottom: 1rem;
}

.hero-title {
    font-size: 2.3rem;
    font-weight: 700;
    color: #f8fafc;
    line-height: 1.18;
    margin-bottom: 0.8rem;
}

.hero-title span {
    color: #38bdf8;
}

.hero-sub {
    color: #cbd5e1;
    font-size: 1.1rem;
    line-height: 1.75;
    max-width: 760px;
    margin-bottom: 1.25rem;
}

.pill-wrap {
    display: flex;
    gap: 0.6rem;
    flex-wrap: wrap;
}

.pill {
    background: rgba(255, 255, 255, 0.06);
    border: 1px solid #334155;
    color: #cbd5e1;
    padding: 0.3rem 0.85rem;
    border-radius: 999px;
    font-size: 0.76rem;
    font-weight: 500;
}

.hero-logo-wrap {
    display: flex;
    align-items: center;
    justify-content: center;
    min-height: 100%;
    padding: 0.25rem 0;
}

.hero-logo-wrap svg {
    width: 175px;
    max-width: 100%;
    height: auto;
    filter: drop-shadow(0 14px 28px rgba(15, 23, 42, 0.22));
}

.section-head {
    display: flex;
    align-items: center;
    gap: 0.85rem;
    margin: 2.25rem 0 1rem 0;
}

.section-num {
    width: 34px;
    height: 34px;
    border-radius: 10px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: 700;
    font-size: 1.3rem;
    flex-shrink: 0;
}

.section-title {
    font-size: 2rem;
    font-weight: 650;
    color: #0f172a;
}

.section-line {
    flex: 1;
    height: 1px;
    background: linear-gradient(90deg, #334155, transparent);
}

.story-card,
.table-card,
.test-card,
.reflection-card {
    background: #1e293b;
    border: 1px solid #334155;
    border-radius: 14px;
}

.story-card,
.story-card p,
.story-card li,
.story-card code,
.reflection-card,
.reflection-card li,
.test-card,
.test-card p,
.test-card li {
    color: #e2e8f0 !important;
}

.story-card,
.reflection-card {
    padding: 1.2rem 1.35rem;
}

.table-card,
.test-card {
    padding: 1.3rem 1.45rem;
    margin-bottom: 1rem;
}

.card-title {
    font-size: 0.98rem;
    font-weight: 700;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: #94a3b8;
    margin-bottom: 0.85rem;
}

.lead {
    color: #cbd5e1;
    font-size: 1.1rem;
    line-height: 1.8;
}

.story-list {
    margin: 0;
    padding-left: 1.1rem;
    color: #cbd5e1;
    line-height: 1.8;
    font-size: 1.2rem;
}

.story-list li {
    margin-bottom: 0.45rem;
}

.story-card code {
    background: rgba(255, 255, 255, 0.12);
    border-radius: 6px;
    padding: 0.1rem 0.35rem;
    font-size: 0.95em;
}

.tbl {
    width: 100%;
    border-collapse: collapse;
    font-size: 0.85rem;
    border-radius: 10px;
    overflow: hidden;
}

.table-scroll {
    width: 100%;
    overflow-x: auto;
    overflow-y: hidden;
}

.table-scroll .tbl {
    min-width: max-content;
}

.tbl th {
    background: #0f172a;
    color: #94a3b8;
    padding: 9px 12px;
    text-align: left;
    font-weight: 600;
    font-size: 1rem;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    border-bottom: 1px solid #334155;
}

.tbl td {
    padding: 8px 12px;
    color: #cbd5e1;
    border-bottom: 1px solid #1e293b;
}

.tbl-blue th { background: #0f172a; color: #94a3b8; }
.tbl-blue tr:nth-child(odd) { background: #1e293b; }
.tbl-blue tr:nth-child(even) { background: #233876; }
.tbl-blue td { color: #cbd5e1; border-bottom: 1px solid #1e293b; }

.tbl-green th { background: #0f172a; color: #94a3b8; }
.tbl-green tr:nth-child(odd) { background: #1e293b; }
.tbl-green tr:nth-child(even) { background: #0f3d2e; }
.tbl-green td { color: #cbd5e1; border-bottom: 1px solid #1e293b; }

.tbl-purple th { background: #0f172a; color: #94a3b8; }
.tbl-purple tr:nth-child(odd) { background: #1e293b; }
.tbl-purple tr:nth-child(even) { background: #134e4a; }
.tbl-purple td { color: #cbd5e1; border-bottom: 1px solid #1e293b; }

.bridge {
    color: #475569;
    font-size: 1.1rem;
    line-height: 1.75;
    margin: 0.25rem 0 1rem 0;
}

.chart-label {
    color: #0f172a;
    font-size: 1.2rem;
    font-weight: 700;
    line-height: 1.4;
    margin: 0 0 0.25rem 0;
}

.note {
    color: #94a3b8;
    font-size: 1.19rem;
    line-height: 1.7;
}

[data-testid="stAlert"] {
    color: #0f172a !important;
    font-size: 1.2rem;
}

[data-testid="stAlert"] * {
    color: #0f172a !important;
    font-size: 1.1rem;
}

.hypothesis-box {
    background: #0f172a;
    border-left: 3px solid #38bdf8;
    border-radius: 0 8px 8px 0;
    padding: 0.85rem 1rem;
    font-size: 1rem;
    color: #cbd5e1;
    line-height: 1.7;
    margin-bottom: 1rem;
}

.chips {
    display: flex;
    gap: 0.7rem;
    flex-wrap: wrap;
    margin-bottom: 0.9rem;
}

.chip {
    background: #0f172a;
    border: 1px solid #334155;
    border-radius: 9px;
    padding: 0.55rem 0.9rem;
    font-family: 'JetBrains Mono', monospace;
    font-size: 1rem;
    color: #e2e8f0;
}

.chip small {
    display: block;
    font-family: 'Inter', sans-serif;
    font-size: 0.8rem;
    color: #64748b;
    margin-bottom: 0.18rem;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}

.verdict-pass {
    background: #052e16;
    border: 1px solid #166534;
    border-radius: 9px;
    padding: 0.8rem 1rem;
    color: #86efac;
    font-size: 1rem;
    line-height: 1.6;
}

.verdict-warn {
    background: #1c1400;
    border: 1px solid #854d0e;
    border-radius: 9px;
    padding: 0.8rem 1rem;
    color: #fcd34d;
    font-size: 1rem;
    line-height: 1.6;
}

.test-caveat {
    color: #94a3b8;
    font-size: 1.1rem;
    line-height: 1.6;
    margin-top: 0.75rem;
    font-style: italic;
}

.reflection-card ul {
    margin: 0;
    padding-left: 1.1rem;
    color: #cbd5e1;
    line-height: 1.8;
    font-size: 1rem;
}
</style>
""",
    unsafe_allow_html=True,
)


@st.cache_data
def load_data():
    df = pd.read_csv("data/gold/weather_air_quality_daily.csv", parse_dates=["date"])

    if "is_holiday" not in df.columns:
        df["is_holiday"] = False
    else:
        df["is_holiday"] = df["is_holiday"].fillna(False).astype(bool)

    if "rainy_day" not in df.columns:
        df["rainy_day"] = df["precipitation_sum"].fillna(0) > 0
    else:
        df["rainy_day"] = df["rainy_day"].fillna(False).astype(bool)

    if "bad_air_day" not in df.columns:
        df["bad_air_day"] = df["pm25_mean"] > 15
    else:
        df["bad_air_day"] = df["bad_air_day"].fillna(False).astype(bool)

    return df.sort_values(["date", "city"]).reset_index(drop=True)


def section_header(number, title, badge_bg, badge_fg):
    st.markdown(
        f"""
        <div class="section-head">
          <div class="section-num" style="background:{badge_bg};color:{badge_fg};">{number}</div>
          <div class="section-title">{title}</div>
          <div class="section-line"></div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def chips_html(pairs):
    html = '<div class="chips">'
    for label, value in pairs:
        html += f'<div class="chip"><small>{label}</small>{value}</div>'
    html += "</div>"
    return html


def verdict_html(p_value, success_text, neutral_text):
    css_class = "verdict-pass" if p_value < 0.05 else "verdict-warn"
    text = success_text if p_value < 0.05 else neutral_text
    return f'<div class="{css_class}">{text}</div>'


def render_test_card(
    label,
    method,
    question,
    variables,
    hypotheses_html,
    why_text,
    chips,
    p_value,
    success_text,
    neutral_text,
    caveat,
):
    st.markdown(
        f"""
        <div class="test-card">
          <div class="card-title">{label} | {method}</div>
          <div style="font-size:1rem;font-weight:600;color:#f8fafc;margin-bottom:0.85rem;">{question}</div>
          <div class="note" style="margin-bottom:0.85rem;"><b style="color:#e2e8f0;">Variables:</b> {variables}</div>
          <div class="hypothesis-box">{hypotheses_html}<br><b style="color:#e2e8f0;">Why this method fits:</b> {why_text}</div>
          {chips_html(chips)}
          {verdict_html(p_value, success_text, neutral_text)}
          <div class="test-caveat">{caveat}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_hero(filtered_df, selected_city):
    date_start = filtered_df["date"].min().strftime("%Y-%m-%d")
    date_end = filtered_df["date"].max().strftime("%Y-%m-%d")
    focus_label = (
        "Toronto and Vancouver together" if selected_city == "Both" else selected_city
    )
    logo_path = Path(__file__).parent / "assets" / "atmoscope_logo.svg"
    logo_svg = logo_path.read_text(encoding="utf-8") if logo_path.exists() else ""

    logo_html = f'<div class="hero-logo-wrap">{logo_svg}</div>' if logo_svg else ""
    st.markdown(
        f"""
        <div class="hero-wrap">
          <div class="hero-grid">
            <div class="hero-copy">
              <div class="hero-tag">Assignment 4 | Statistical Analysis Story</div>
              <div class="hero-title">Weather and air quality in <span>Toronto and Vancouver</span></div>
              <div class="hero-sub">
                This app follows one analytical question from context to conclusion:
                how do weather conditions and holidays relate to air quality in Toronto and Vancouver,
                and which patterns are strong enough to support formal statistical testing?
              </div>
              <div class="pill-wrap">
                <span class="pill">Focus: {focus_label}</span>
                <span class="pill">Date range: {date_start} to {date_end}</span>
                <span class="pill">Source: Open-Meteo</span>
                <span class="pill">External source: Nager.Date</span>
                <span class="pill">5 hypothesis tests</span>
              </div>
            </div>
            {logo_html}
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_project_story():
    section_header("01", "Project Overview and Data Story", "#172554", "#38bdf8")
    st.markdown(
        """
        <div class="bridge">
          The story starts with where the dataset came from, what was added in Assignment 4,
          and how those choices shape the analysis that follows.
        </div>
        """,
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns(2)
    with col1:
        st.markdown(
            """
            <div class="story-card">
              <div class="card-title">What changed from Assignment 3</div>
              <ul class="story-list">
                <li>Original dataset: daily weather and air-quality measures for Toronto and Vancouver from Open-Meteo.</li>
                <li>New external source: the Nager.Date holiday API, added to identify Canadian statutory holidays.</li>
                <li>Core merge: weather and air quality are joined on <code>date</code> and <code>city</code>.</li>
                <li>Holiday enrichment: the holiday flag is joined by <code>date</code> to extend the Gold dataset.</li>
              </ul>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with col2:
        st.markdown(
            """
            <div class="story-card">
              <div class="card-title">Main analytical question</div>
              <div class="lead">
                How do weather conditions and holidays relate to air quality in Toronto and Vancouver,
                and which of those visible patterns are strong enough to justify formal hypothesis tests?
              </div>
              <div class="lead" style="margin-top:0.8rem;">
                This page is intentionally ordered as a guided argument:
                first the data foundation, then the visual evidence, then the tests,
                and finally the limits on what the results can claim.
              </div>
            </div>
            """,
            unsafe_allow_html=True,
        )


def render_data_foundations(filtered_df):
    section_header("02", "Data Foundations", "#052e16", "#34d399")
    st.markdown(
        """
        <div class="bridge">
          Before making claims, we need to show what is in the final Gold dataset,
          what variables were derived, and why those fields matter for the later tests.
        </div>
        """,
        unsafe_allow_html=True,
    )

    total_rows = len(filtered_df)
    mean_aqi = filtered_df["aqi_max"].mean()
    mean_pm25 = filtered_df["pm25_mean"].mean()
    rainy_share = filtered_df["rainy_day"].mean() * 100
    holiday_rows = int(filtered_df["is_holiday"].sum())

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Rows in focus", f"{total_rows:,}")
    m2.metric("Mean AQI", f"{mean_aqi:.1f}")
    m3.metric("Mean PM2.5", f"{mean_pm25:.2f} ug/m3")
    m4.metric("Holiday rows", f"{holiday_rows:,}", delta=f"{rainy_share:.1f}% rainy")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown(
            """
            <div class="table-card">
              <div class="card-title">Derived variables used in the tests</div>
            """,
            unsafe_allow_html=True,
        )
        derived = pd.DataFrame(
            {
                "Column": ["is_holiday", "bad_air_day", "rainy_day"],
                "Type": ["bool", "bool", "bool"],
                "Why it matters": [
                    "Creates the holiday vs regular-day comparison",
                    "Turns PM2.5 into a categorical air-quality outcome",
                    "Creates the rainy vs non-rainy comparison",
                ],
            }
        )
        st.markdown(
            f'<div class="table-scroll">{derived.to_html(classes="tbl tbl-blue", index=False)}</div>',
            unsafe_allow_html=True,
        )
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown(
            """
            <div class="table-card">
              <div class="card-title">How the visuals lead into the tests</div>
            """,
            unsafe_allow_html=True,
        )
        test_map = pd.DataFrame(
            {
                "Visual pattern": [
                    "AQI versus benchmark over time",
                    "PM2.5 by rainy-day group",
                    "Bad-air counts by holiday flag",
                    "PM2.5 spread by holiday flag",
                    "Temperature against PM2.5",
                ],
                "Formal test": [
                    "One-sample t-test",
                    "Welch two-sample t-test",
                    "Chi-square test",
                    "Levene's test",
                    "Pearson correlation",
                ],
            }
        )
        st.markdown(
            f'<div class="table-scroll">{test_map.to_html(classes="tbl tbl-green", index=False)}</div>',
            unsafe_allow_html=True,
        )
        st.markdown("</div>", unsafe_allow_html=True)

    col3, col4 = st.columns([1.2, 1])
    with col3:
        st.markdown(
            """
            <div class="table-card">
              <div class="card-title">Preview of the final dataset</div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown(
            f'<div class="table-scroll">{filtered_df.head(15).to_html(classes="tbl tbl-blue", index=False)}</div>',
            unsafe_allow_html=True,
        )
        st.markdown("</div>", unsafe_allow_html=True)
    with col4:
        st.markdown(
            """
            <div class="table-card">
              <div class="card-title">Summary statistics</div>
            """,
            unsafe_allow_html=True,
        )
        summary = (
            filtered_df.select_dtypes(include="number")
            .describe()
            .round(2)
            .reset_index()
        )
        st.markdown(
            f'<div class="table-scroll">{summary.to_html(classes="tbl tbl-purple", index=False)}</div>',
            unsafe_allow_html=True,
        )
        st.markdown("</div>", unsafe_allow_html=True)

    descriptions = pd.DataFrame(
        {
            "Column": [
                "date",
                "city",
                "temp_max",
                "temp_min",
                "precipitation_sum",
                "pm25_mean",
                "pm10_mean",
                "aqi_max",
                "rainy_day",
                "is_holiday",
                "bad_air_day",
            ],
            "Description": [
                "Calendar date",
                "Toronto or Vancouver",
                "Daily maximum temperature (C)",
                "Daily minimum temperature (C)",
                "Total daily precipitation (mm)",
                "Mean daily PM2.5 (ug/m3)",
                "Mean daily PM10 (ug/m3)",
                "Maximum daily US AQI",
                "True when precipitation is greater than 0",
                "True when the date is a statutory holiday",
                "True when PM2.5 is greater than 15 ug/m3",
            ],
        }
    )
    st.markdown(
        """
        <div class="table-card">
          <div class="card-title">Column descriptions</div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown(
        f'<div class="table-scroll">{descriptions.to_html(classes="tbl tbl-blue", index=False)}</div>',
        unsafe_allow_html=True,
    )
    st.markdown("</div>", unsafe_allow_html=True)


def render_visual_story(filtered_df):
    section_header("03", "Visual Evidence", "#2e1065", "#a78bfa")
    st.markdown(
        """
        <div class="bridge">
          The charts below are ordered to build the argument.
          Each one highlights a pattern that motivates a specific statistical test in the next section.
        </div>
        """,
        unsafe_allow_html=True,
    )

    try:
        import plotly.express as px
    except ImportError:
        st.warning(
            "Plotly is not installed. Run `uv add plotly statsmodels` to render the charts."
        )
        return

    colors = {"Toronto": "#38bdf8", "Vancouver": "#34d399"}
    layout = dict(
        paper_bgcolor="#1e293b",
        plot_bgcolor="#0f172a",
        font=dict(family="Inter", color="#cbd5e1", size=12),
        title=dict(font=dict(size=18, color="#f8fafc")),
        margin=dict(t=40, b=30, l=20, r=20),
        legend=dict(
            orientation="h",
            y=1.03,
            x=0.001,
            font=dict(size=12, color="#e2e8f0"),
            title=dict(text="City", font=dict(size=12, color="#e2e8f0")),
        ),
        xaxis=dict(gridcolor="#1e3a5f", linecolor="#334155"),
        yaxis=dict(gridcolor="#1e3a5f", linecolor="#334155"),
    )

    st.markdown(
        '<div class="chart-label">1. AQI over time</div>', unsafe_allow_html=True
    )
    st.caption(
        "This establishes the baseline question: Does average daily AQI sit meaningfully away from the benchmark value of 15?"
    )
    fig1 = px.line(
        filtered_df,
        x="date",
        y="aqi_max",
        color="city",
        color_discrete_map=colors,
        title="Daily maximum AQI over time",
    )
    fig1.add_hline(
        y=15,
        line_dash="dash",
        line_color="#ef4444",
        annotation_text="Benchmark = 15",
        annotation_font_color="#ef4444",
        annotation_font_size=11,
    )
    fig1.update_layout(**layout)
    fig1.for_each_trace(lambda trace: trace.update(name=str(trace.name).title()))
    st.plotly_chart(fig1, use_container_width=True)

    left, right = st.columns(2)
    with left:
        st.markdown(
            '<div class="chart-label">2. PM2.5 by rainy-day group</div>',
            unsafe_allow_html=True,
        )
        st.caption(
            "This checks whether rainfall appears to separate PM2.5 into two group means, which is why a two-sample t-test comes next."
        )
        fig2 = px.box(
            filtered_df,
            x="rainy_day",
            y="pm25_mean",
            color="city",
            color_discrete_map=colors,
            labels={"rainy_day": "Rainy day", "pm25_mean": "PM2.5 (ug/m3)"},
            title="PM2.5 on rainy versus non-rainy days",
        )
        fig2.update_layout(**layout)
        st.plotly_chart(fig2, use_container_width=True)

    with right:
        st.markdown(
            '<div class="chart-label">3. Bad-air counts by holiday flag</div>',
            unsafe_allow_html=True,
        )
        st.caption(
            "This reframes air quality as a categorical outcome and motivates a test of association rather than a test of means."
        )
        counts = (
            filtered_df.groupby(["is_holiday", "bad_air_day"])
            .size()
            .reset_index(name="count")
        )
        counts["is_holiday"] = counts["is_holiday"].map(
            {True: "Holiday", False: "Regular day"}
        )
        counts["bad_air_day"] = counts["bad_air_day"].map(
            {True: "Bad air day", False: "Clean air day"}
        )
        fig3 = px.bar(
            counts,
            x="is_holiday",
            y="count",
            color="bad_air_day",
            barmode="stack",
            color_discrete_map={"Bad air day": "#ef4444", "Clean air day": "#34d399"},
            title="Bad-air day counts by holiday flag",
        )
        fig3.update_layout(**layout)
        st.plotly_chart(fig3, use_container_width=True)

    left, right = st.columns(2)
    with left:
        st.markdown(
            '<div class="chart-label">4. PM2.5 spread on holidays versus regular days</div>',
            unsafe_allow_html=True,
        )
        st.caption(
            "The mean is not the only story. This chart checks whether the spread itself changes, which motivates Levene's test."
        )
        fig4 = px.box(
            filtered_df,
            x="is_holiday",
            y="pm25_mean",
            color="city",
            color_discrete_map=colors,
            labels={"is_holiday": "Holiday", "pm25_mean": "PM2.5 (ug/m3)"},
            title="PM2.5 variability by holiday flag",
        )
        fig4.update_layout(**layout)
        st.plotly_chart(fig4, use_container_width=True)

    with right:
        st.markdown(
            '<div class="chart-label">5. Temperature versus PM2.5</div>',
            unsafe_allow_html=True,
        )
        st.caption(
            "A scatterplot with a fitted trend line checks whether a linear relationship is visible before using Pearson correlation."
        )
        fig5 = px.scatter(
            filtered_df,
            x="temp_max",
            y="pm25_mean",
            color="city",
            trendline="ols",
            color_discrete_map=colors,
            labels={
                "temp_max": "Maximum temperature (C)",
                "pm25_mean": "PM2.5 (ug/m3)",
            },
            title="Temperature versus PM2.5 concentration",
        )
        fig5.update_layout(**layout)
        st.plotly_chart(fig5, use_container_width=True)


def render_hypothesis_tests(filtered_df, selected_city):
    section_header("04", "Formal Hypothesis Tests", "#431407", "#fb923c")
    scope = (
        "The current focus pools Toronto and Vancouver together. Read these results as combined evidence, not city-specific inference."
        if selected_city == "Both"
        else f"The current focus is {selected_city} only, so each result applies to that city subset."
    )
    st.markdown(
        """
        <div class="bridge">
          The visual patterns above now move into formal tests.
          Each result states the hypotheses, the fitting method, and a plain-language interpretation.
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.info(scope)

    aqi = filtered_df["aqi_max"].dropna()
    if len(aqi) >= 2:
        t1, p1 = stats.ttest_1samp(aqi, popmean=15)
        render_test_card(
            label="Test 1",
            method="One-sample t-test",
            question="Is mean daily AQI different from the benchmark value of 15?",
            variables="aqi_max versus the benchmark 15",
            hypotheses_html="<b style='color:#e2e8f0;'>H0:</b> mean AQI = 15 &nbsp; | &nbsp; <b style='color:#e2e8f0;'>H1:</b> mean AQI != 15",
            why_text="There is one sample of AQI values and one fixed benchmark value.",
            chips=[
                ("t-statistic", f"{t1:.3f}"),
                ("p-value", f"{p1:.4f}"),
                ("Sample mean", f"{aqi.mean():.1f}"),
                ("Benchmark", "15.0"),
            ],
            p_value=p1,
            success_text=f"p = {p1:.4f} < 0.05, so the mean AQI is statistically different from 15 in the current focus.",
            neutral_text=f"p = {p1:.4f} >= 0.05, so the current data do not show a statistically significant difference from 15.",
            caveat="AQI-related measures can be skewed by spikes. Large samples help, but distribution shape still matters.",
        )
    else:
        st.warning(
            "Test 1 is unavailable because the filtered sample does not contain enough AQI values."
        )

    rainy = filtered_df.loc[filtered_df["rainy_day"], "pm25_mean"].dropna()
    dry = filtered_df.loc[~filtered_df["rainy_day"], "pm25_mean"].dropna()
    if len(rainy) >= 2 and len(dry) >= 2:
        t2, p2 = stats.ttest_ind(rainy, dry, equal_var=False)
        render_test_card(
            label="Test 2",
            method="Welch two-sample t-test",
            question="Do PM2.5 levels differ on rainy versus non-rainy days?",
            variables="pm25_mean grouped by rainy_day",
            hypotheses_html="<b style='color:#e2e8f0;'>H0:</b> mean PM2.5 is the same on rainy and non-rainy days &nbsp; | &nbsp; <b style='color:#e2e8f0;'>H1:</b> the means differ",
            why_text="The question compares the means of two independent groups, and Welch's version avoids assuming equal variance.",
            chips=[
                ("t-statistic", f"{t2:.3f}"),
                ("p-value", f"{p2:.4f}"),
                ("Rainy mean", f"{rainy.mean():.2f} ug/m3"),
                ("Dry mean", f"{dry.mean():.2f} ug/m3"),
            ],
            p_value=p2,
            success_text=f"p = {p2:.4f} < 0.05, so rainy and non-rainy days show a statistically significant PM2.5 difference.",
            neutral_text=f"p = {p2:.4f} >= 0.05, so the current sample does not show a statistically significant PM2.5 difference by rainfall group.",
            caveat="Rainfall can also reflect season and temperature, so this should be read as association rather than causation.",
        )
    else:
        st.warning(
            "Test 2 is unavailable because the current filters do not leave enough rainy and dry observations."
        )

    bad_air = pd.Categorical(filtered_df["bad_air_day"], categories=[False, True])
    holiday = pd.Categorical(filtered_df["is_holiday"], categories=[False, True])
    contingency = pd.crosstab(bad_air, holiday)
    if (
        contingency.to_numpy().sum() > 0
        and (contingency.sum(axis=0) > 0).all()
        and (contingency.sum(axis=1) > 0).all()
    ):
        chi2, p3, dof, _ = stats.chi2_contingency(contingency)
        render_test_card(
            label="Test 3",
            method="Chi-square test",
            question="Is a bad-air day associated with the holiday flag?",
            variables="bad_air_day and is_holiday",
            hypotheses_html="<b style='color:#e2e8f0;'>H0:</b> bad_air_day and is_holiday are independent &nbsp; | &nbsp; <b style='color:#e2e8f0;'>H1:</b> they are associated",
            why_text="Both variables are categorical, so the question is about association in counts rather than differences in means.",
            chips=[
                ("Chi-square", f"{chi2:.3f}"),
                ("p-value", f"{p3:.4f}"),
                ("Degrees of freedom", f"{dof}"),
                ("Rows in table", f"{int(contingency.to_numpy().sum())}"),
            ],
            p_value=p3,
            success_text=f"p = {p3:.4f} < 0.05, so the bad-air indicator and holiday flag are statistically associated in this sample.",
            neutral_text=f"p = {p3:.4f} >= 0.05, so the data do not show a statistically significant association between the two flags.",
            caveat="Holiday counts are small, so expected cell counts may limit the stability of this result.",
        )
    else:
        st.warning(
            "Test 3 is unavailable because the filtered data do not contain both categories for each variable."
        )

    holiday_pm = filtered_df.loc[filtered_df["is_holiday"], "pm25_mean"].dropna()
    regular_pm = filtered_df.loc[~filtered_df["is_holiday"], "pm25_mean"].dropna()
    if len(holiday_pm) >= 2 and len(regular_pm) >= 2:
        lev, p4 = stats.levene(holiday_pm, regular_pm)
        render_test_card(
            label="Test 4",
            method="Levene's test",
            question="Is PM2.5 variability different on holidays versus regular days?",
            variables="pm25_mean grouped by is_holiday",
            hypotheses_html="<b style='color:#e2e8f0;'>H0:</b> PM2.5 variance is equal on holidays and regular days &nbsp; | &nbsp; <b style='color:#e2e8f0;'>H1:</b> the variances differ",
            why_text="This question is about spread rather than means, and Levene's test is more robust than a raw F-test under non-normal data.",
            chips=[
                ("Levene stat", f"{lev:.3f}"),
                ("p-value", f"{p4:.4f}"),
                ("Holiday SD", f"{holiday_pm.std():.2f}"),
                ("Regular SD", f"{regular_pm.std():.2f}"),
            ],
            p_value=p4,
            success_text=f"p = {p4:.4f} < 0.05, so PM2.5 variability differs significantly between holidays and regular days.",
            neutral_text=f"p = {p4:.4f} >= 0.05, so the current sample does not show a statistically significant difference in PM2.5 spread.",
            caveat="This comparison usually has low power because the holiday group is much smaller than the regular-day group.",
        )
    else:
        st.warning(
            "Test 4 is unavailable because there are not enough holiday and regular-day PM2.5 values after filtering."
        )

    clean = filtered_df[["temp_max", "pm25_mean"]].dropna()
    if (
        len(clean) >= 3
        and clean["temp_max"].nunique() > 1
        and clean["pm25_mean"].nunique() > 1
    ):
        r_value, p5 = stats.pearsonr(clean["temp_max"], clean["pm25_mean"])
        direction = "positive" if r_value > 0 else "negative"
        render_test_card(
            label="Test 5",
            method="Pearson correlation",
            question="Is temperature linearly associated with PM2.5 concentration?",
            variables="temp_max and pm25_mean",
            hypotheses_html="<b style='color:#e2e8f0;'>H0:</b> r = 0 (no linear association) &nbsp; | &nbsp; <b style='color:#e2e8f0;'>H1:</b> r != 0",
            why_text="Both variables are continuous, and the visual question is whether a linear relationship is present.",
            chips=[
                ("Pearson r", f"{r_value:.3f}"),
                ("p-value", f"{p5:.4f}"),
                ("Observations", f"{len(clean):,}"),
                ("Direction", direction),
            ],
            p_value=p5,
            success_text=f"p = {p5:.4f} < 0.05, so the data show a statistically significant {direction} linear relationship between temperature and PM2.5.",
            neutral_text=f"p = {p5:.4f} >= 0.05, so the current sample does not show a statistically significant linear relationship.",
            caveat="Pearson assumes linearity. If the scatterplot bends or clusters, Spearman would be a better follow-up.",
        )
    else:
        st.warning(
            "Test 5 is unavailable because the filtered sample does not contain enough variation for correlation."
        )


def render_reflection():
    section_header("05", "Reflection and Limitations", "#1e293b", "#94a3b8")
    st.markdown(
        """
        <div class="bridge">
          This final section narrows the claims from the tests above.
          Statistical significance does not remove assumptions, data limitations, or join risks.
        </div>
        """,
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns(2)
    with col1:
        st.markdown(
            """
            <div class="reflection-card">
              <div class="card-title">Test assumptions</div>
              <ul>
                <li>T-tests assume approximate stability in the sampling distribution of the mean, even if PM2.5 itself is right-skewed.</li>
                <li>Chi-square needs enough expected counts in each cell, which becomes harder when the holiday subset is small.</li>
                <li>Pearson correlation assumes a roughly linear relationship between temperature and PM2.5.</li>
              </ul>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with col2:
        st.markdown(
            """
            <div class="reflection-card">
              <div class="card-title">Data limitations</div>
              <ul>
                <li>The dataset only covers two cities over about two years, so the findings should not be generalized too broadly.</li>
                <li>Open-Meteo air-quality values are model-based estimates, not direct sensor readings.</li>
                <li>A national holiday calendar cannot capture every provincial, municipal, or local behavior change.</li>
              </ul>
            </div>
            """,
            unsafe_allow_html=True,
        )

    col3, col4 = st.columns(2)
    with col3:
        st.markdown(
            """
            <div class="reflection-card">
              <div class="card-title">Join issues</div>
              <ul>
                <li>Weather and air quality are merged on date and city, but the holiday flag is joined by date only.</li>
                <li>The Gold build uses an inner join, so dates missing from either cleaned source drop out of the final dataset.</li>
                <li>Those join choices are reasonable for the assignment, but they still shape what questions the data can answer well.</li>
              </ul>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with col4:
        st.markdown(
            """
            <div class="reflection-card">
              <div class="card-title">What significance does not mean</div>
              <ul>
                <li>A small p-value suggests a pattern is unlikely to be due to random noise alone.</li>
                <li>It does not automatically mean the effect is large, important, or useful in practice.</li>
                <li>It also does not prove causation, especially when rainfall, season, city, and temperature can move together.</li>
              </ul>
            </div>
            """,
            unsafe_allow_html=True,
        )


df = load_data()

st.sidebar.markdown("## Focus Controls")
selected_city = st.sidebar.radio(
    "City focus", ["Both", "Toronto", "Vancouver"], index=0
)

min_date = df["date"].min().date()
max_date = df["date"].max().date()
selected_dates = st.sidebar.date_input(
    "Date range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date,
)

st.sidebar.markdown("---")
st.sidebar.markdown(
    """
    <div style="font-size:0.92rem;line-height:1.7;">
      <b>How to read this page</b><br>
      Start at the top and move down. The visuals are placed in the same order as the tests they motivate.
    </div>
    """,
    unsafe_allow_html=True,
)
st.sidebar.markdown("<div style='height:0.75rem;'></div>", unsafe_allow_html=True)
st.sidebar.markdown(
    """
    <div style="font-size:0.88rem;line-height:1.7;color:#94a3b8;">
      Sources:<br>
      Open-Meteo Historical Weather<br>
      Open-Meteo Air Quality<br>
      Nager.Date Holiday API
    </div>
    """,
    unsafe_allow_html=True,
)

filtered_df = df.copy()
if selected_city != "Both":
    filtered_df = filtered_df[filtered_df["city"] == selected_city]

if isinstance(selected_dates, tuple) and len(selected_dates) == 2:
    start_date, end_date = selected_dates
    filtered_df = filtered_df[
        (filtered_df["date"].dt.date >= start_date)
        & (filtered_df["date"].dt.date <= end_date)
    ]

filtered_df = filtered_df.sort_values(["date", "city"]).reset_index(drop=True)

if filtered_df.empty:
    st.warning(
        "No data matched the selected focus controls. Adjust the city or date range and try again."
    )
    st.stop()

render_hero(filtered_df, selected_city)
render_project_story()
render_data_foundations(filtered_df)
render_visual_story(filtered_df)
render_hypothesis_tests(filtered_df, selected_city)
render_reflection()
