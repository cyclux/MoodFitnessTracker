import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


Y_LABELS = {
    "sleep": "Schlafzeit [h]",
    "bodybattery": "Body Battery [%]",
    "steps": "Schritte [absolut]",
    "body": "Körpergefühl [0-6]",
    "psyche": "Psychegefühl [0-6]",
    "dizzy": "Schwindel Häufigkeit [absolut]",
}


def _concat_columns(df: pd.DataFrame, cols: list[str], new_col_name: str) -> pd.Series:
    bodybattery = pd.concat(
        [
            df[cols[0]],
            df[cols[1]],
        ]
    )
    bodybattery.name = new_col_name
    return bodybattery


def _merge_pd_series(col1: pd.Series, col2: pd.Series) -> pd.DataFrame:
    return pd.DataFrame({f"{col1.name}": col1, f"{col2.name}": col2})


def run_interval_plots(df: pd.DataFrame) -> None:
    x_label = "Zeitintervall"

    # Sleep
    st.write("### Schlafzeit")
    plot_sleep = sns.boxplot(y=df["sleep"], x=df["date_interval"])
    plot_sleep.set_ylabel(Y_LABELS["sleep"])
    st.pyplot(plot_sleep.get_figure())
    plt.clf()

    # Body Battery
    st.write("### Body Battery Min / Max")
    plot_bodybattery = sns.stripplot(
        x=df["date_interval"], y="bodybattery_min", data=df, jitter=True
    )
    plot_bodybattery = sns.pointplot(
        x=df["date_interval"],
        y="bodybattery_min",
        data=df,
        linestyle="none",
        capsize=0.2,
        color="black",
    )
    plot_bodybattery = sns.stripplot(
        x=df["date_interval"], y="bodybattery_max", data=df, jitter=True
    )
    plot_bodybattery = sns.pointplot(
        x=df["date_interval"],
        y="bodybattery_max",
        data=df,
        linestyle="none",
        capsize=0.2,
        color="black",
    )
    plot_bodybattery.set_ylabel(Y_LABELS["bodybattery"])
    st.pyplot(plot_bodybattery.get_figure())
    plt.clf()

    # Body Battery (violin)
    st.write("### Body Battery Min/Max (Violin)")
    series_bodybattery = _concat_columns(
        df, ["bodybattery_min", "bodybattery_max"], "bodybattery"
    )

    series_date_interval = _concat_columns(
        df, ["date_interval", "date_interval"], "date_interval"
    )

    df_bodybattery_min_max_merged = _merge_pd_series(
        series_bodybattery, series_date_interval
    )

    plot_bodybattery_violin = sns.violinplot(
        x="date_interval", y="bodybattery", data=df_bodybattery_min_max_merged
    )
    plot_bodybattery_violin.set_ylabel(Y_LABELS["bodybattery"])
    st.pyplot(plot_bodybattery_violin.get_figure())
    plt.clf()

    # Steps
    st.write("### Schritte")
    plot_steps = sns.boxplot(y=df["steps"], x=df["date_interval"])
    plot_steps.set_ylabel(Y_LABELS["steps"])
    st.pyplot(plot_steps.get_figure())
    plt.clf()

    # Body
    st.write("### Körpergefühl")
    plot_body = sns.boxplot(y=df["body"], x=df["date_interval"])
    plot_body.set_ylabel(Y_LABELS["body"])
    st.pyplot(plot_body.get_figure())
    plt.clf()

    # Psyche
    st.write("### Psychegefühl")
    plot_psyche = sns.boxplot(y=df["psyche"], x=df["date_interval"])
    plot_psyche.set_ylabel(Y_LABELS["psyche"])
    st.pyplot(plot_psyche.get_figure())
    plt.clf()

    # Dizzy: Plus / Minus Balkendiagramm
    # Prepare data
    df_dizzy = df.groupby("date_interval")["dizzy"].value_counts().reset_index()

    df_dizzy["count"] = df_dizzy.apply(
        lambda x: -x["count"] if x["dizzy"] is True else x["count"], axis=1
    )

    st.write("### Schwindel")
    # hue_order = ["Ja", "Nein"]
    plot_dizzy = sns.barplot(
        x="date_interval",
        y="count",
        hue="dizzy",
        data=df_dizzy,
        dodge=False,
        hue_order=[True, False],
    )
    plot_dizzy.set_label("Schwindel")

    # Set the labels of the legend
    new_labels = ["Ja", "Nein"]
    for t, label in zip(plot_dizzy.legend().texts, new_labels):
        t.set_text(label)

    plot_dizzy.set_ylabel(Y_LABELS["dizzy"])
    # Adjusting the plot to make it more readable
    plt.axhline(0, color="black", linewidth=0.8)

    st.pyplot(plot_dizzy.get_figure())
    plt.clf()


def run_daily_plots(df: pd.DataFrame) -> None:
    # Sleep
    st.write("### Schlafzeit")
    plot_sleep = sns.lineplot(y="sleep", x="date_interval", data=df)
    plot_sleep.set_ylabel(Y_LABELS["sleep"])
    st.pyplot(plot_sleep.get_figure())
    plt.clf()

    st.write("### Schlafzeit | Regression")
    plot_sleep_reg = sns.regplot(x="date_interval", y="sleep", order=3, data=df)
    plot_sleep_reg.set_ylabel(Y_LABELS["sleep"])
    st.pyplot(plot_sleep_reg.get_figure())
    plt.clf()

    st.write("### Schlafzeit | Barplot")
    plot_sleep_bar = sns.barplot(x="date_interval", y="sleep", data=df)
    plot_sleep_bar.set_xticks(range(0, len(df["date_interval"]), 20))
    plot_sleep_bar.set_ylabel(Y_LABELS["sleep"])
    st.pyplot(plot_sleep_bar.get_figure())
    plt.clf()

    # Body Battery
    st.write("### Body Battery Min / Max")

    plot_bodybattery = sns.regplot(
        x="date_interval", y="bodybattery_min", order=3, data=df
    )
    plot_bodybattery = sns.regplot(
        x="date_interval", y="bodybattery_max", order=3, data=df
    )

    plot_bodybattery.set_ylabel(Y_LABELS["bodybattery"])
    st.pyplot(plot_bodybattery.get_figure())
    plt.clf()

    # Steps
    st.write("### Schritte")
    plot_steps = sns.regplot(y="steps", x="date_interval", data=df)
    plot_steps.set_ylabel(Y_LABELS["steps"])
    st.pyplot(plot_steps.get_figure())
    plt.clf()

    # Body
    st.write("### Körpergefühl")
    plot_body = sns.regplot(y="body", x="date_interval", data=df)
    plot_body.set_ylabel(Y_LABELS["body"])
    st.pyplot(plot_body.get_figure())
    plt.clf()

    # Psyche
    st.write("### Psychegefühl")
    plot_psyche = sns.regplot(y="psyche", x="date_interval", data=df)
    plot_psyche.set_ylabel(Y_LABELS["psyche"])
    st.pyplot(plot_psyche.get_figure())
    plt.clf()

    # Dizzy: Plus / Minus Balkendiagramm
    # Prepare data
    df_dizzy = df.groupby("date_interval")["dizzy"].value_counts().reset_index()

    df_dizzy["count"] = df_dizzy.apply(
        lambda x: -x["count"] if x["dizzy"] is True else x["count"], axis=1
    )

    st.write("### Schwindel")
    plot_dizzy = sns.barplot(
        x="date_interval", y="count", hue="dizzy", data=df_dizzy, dodge=False
    )
    plot_dizzy.set_ylabel(Y_LABELS["dizzy"])
    plot_dizzy.set_xticks(range(0, len(df_dizzy["date_interval"]), 20))
    # Adjusting the plot to make it more readable
    plt.axhline(0, color="black", linewidth=0.8)

    st.pyplot(plot_dizzy.get_figure())
    plt.clf()


def create_plots(df: pd.DataFrame, interval: str) -> None:
    if interval == "daily":
        run_daily_plots(df)
    else:
        run_interval_plots(df)
