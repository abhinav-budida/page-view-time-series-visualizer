import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


# Import data
df = pd.read_csv(
    "fcc-forum-pageviews.csv",
    parse_dates=["date"],
    index_col="date"
)

# Clean data
df = df[
    (df["value"] >= df["value"].quantile(0.025))
    & (df["value"] <= df["value"].quantile(0.975))
]


def draw_line_plot():
    # Create a copy of the data
    df_line = df.copy()

    # Draw line plot
    fig, ax = plt.subplots(figsize=(15, 5))

    ax.plot(df_line.index, df_line["value"])

    ax.set_title(
        "Daily freeCodeCamp Forum Page Views 5/2016-12/2019"
    )

    ax.set_xlabel("Date")
    ax.set_ylabel("Page Views")

    # Save image and return figure
    fig.savefig("line_plot.png")
    return fig


def draw_bar_plot():
    # Create a copy of the data
    df_bar = df.copy()

    # Add year and month columns
    df_bar["year"] = df_bar.index.year
    df_bar["month"] = df_bar.index.month

    # Calculate average page views
    df_bar = (
        df_bar
        .groupby(["year", "month"])["value"]
        .mean()
        .unstack()
    )

    # Draw bar chart
    fig = df_bar.plot(
        kind="bar",
        figsize=(10, 6)
    ).figure

    ax = fig.axes[0]

    ax.set_xlabel("Years")
    ax.set_ylabel("Average Page Views")

    ax.legend(
        title="Months",
        labels=[
            "January",
            "February",
            "March",
            "April",
            "May",
            "June",
            "July",
            "August",
            "September",
            "October",
            "November",
            "December"
        ]
    )

    # Save image and return figure
    fig.savefig("bar_plot.png")
    return fig


def draw_box_plot():
    # Create a copy of the data
    df_box = df.copy()

    # Reset index
    df_box.reset_index(inplace=True)

    # Create year and month columns
    df_box["year"] = df_box["date"].dt.year

    df_box["month"] = df_box["date"].dt.strftime("%b")

    # Define correct month order
    month_order = [
        "Jan", "Feb", "Mar", "Apr",
        "May", "Jun", "Jul", "Aug",
        "Sep", "Oct", "Nov", "Dec"
    ]

    # Draw box plots
    fig, axes = plt.subplots(
        1, 2,
        figsize=(20, 6)
    )

    # Year-wise box plot
    sns.boxplot(
        data=df_box,
        x="year",
        y="value",
        ax=axes[0]
    )

    axes[0].set_title(
        "Year-wise Box Plot (Trend)"
    )

    axes[0].set_xlabel("Year")
    axes[0].set_ylabel("Page Views")

    # Month-wise box plot
    sns.boxplot(
        data=df_box,
        x="month",
        y="value",
        order=month_order,
        ax=axes[1]
    )

    axes[1].set_title(
        "Month-wise Box Plot (Seasonality)"
    )

    axes[1].set_xlabel("Month")
    axes[1].set_ylabel("Page Views")

    # Save image and return figure
    fig.savefig("box_plot.png")
    return fig
