import pandas as pd
import plotly.express as px
import plotly.graph_objects as go




def read_my_csv(file_path):
    # Einlesen eines Dataframes
    ## "," steht für das Trennzeichen in der csv-Datei
    df = pd.read_csv(file_path, sep=",", header=None)

    # Setzt die Columnnames im Dataframe
    df.columns = ["Duration","Distance","OriginalPace","HeartRate","Cadence","PowerOriginal","CalculatedPace","CalculatedStrideLength","CalculatedAerobicEfficiencyPace","CalculatedAerobicEfficiencyPower","CalculatedEfficiencyIndex","0"]
    df.drop("0", axis=1, inplace=True)
    
    # Konvertiere alle Spalten in numerische Werte
    df = df.apply(pd.to_numeric, errors="coerce")
    
    # Gibt den geladen Dataframe zurück
    return df

def mittelwert(df, column_name):
    for c in df.columns:
        df[c] = pd.to_numeric(df[c], errors="coerce")
    return df[column_name].mean(numeric_only=True)

def maximalwert(df, column_name):
    for c in df.columns:
        df[c] = pd.to_numeric(df[c], errors="coerce")
    return df[column_name].max(numeric_only=True)


def make_plot(df, column_name):

    fig = px.line(df, x= df.index, y=column_name, title=f"{column_name} over Time", labels={"index": "Time [ms]", column_name: f"{column_name} [bpm]"})
    return fig

def Zone(df, heart_rate, wert):
    # NaN-Werte handhaben und Strings in Zahlen umwandeln
    heart_rate = pd.to_numeric(heart_rate, errors="coerce")
    if pd.isna(heart_rate):
        return None
    
    if heart_rate >= 0.5*wert and heart_rate < 0.6*wert:
        return "Zone 1"
    elif heart_rate >= 0.6*wert and heart_rate < 0.7*wert:
        return "Zone 2"
    elif heart_rate >= 0.7*wert and heart_rate < 0.8*wert:
        return "Zone 3"
    elif heart_rate >= 0.8*wert and heart_rate < 0.9*wert:
        return "Zone 4"
    elif heart_rate >= 0.9*wert and heart_rate <= wert:
        return "Zone 5"
    elif heart_rate < 0.5*wert:
        return "Zone 0"
    else:
        return None

def Heart_Zone(df, wert, column_name="HeartRate"):
    df["Zone"] = df[column_name].apply(lambda hr: Zone(df, hr, wert))

def Zone_Percentage(df):
    zone_counts = df["Zone"].value_counts(normalize=True) * 100
    return zone_counts

def Zone_Time(df):
    zone_order = ["Zone 5", "Zone 4", "Zone 3", "Zone 2", "Zone 1", "Zone 0"]
    zone_time = df["Zone"].value_counts().reindex(zone_order, fill_value=0)
    return zone_time * (df["Duration"].mean())

def Average_Power_Zone(df, power):
    # Calculate the average power for each zone
    avg_power_by_zone = df.groupby("Zone")[power].mean()
    return avg_power_by_zone



def make_plot_with_zones_and_power(df, max_hr, heart_rate_column="HeartRate", power_column="PowerOriginal"):

    fig = go.Figure()

    # background
    zones_info = [
        (0, 0.5, "Zone 0", "rgba(255, 255, 255, 0.2)"),
        (0.5, 0.6, "Zone 1", "rgba(50, 200, 255, 0.2)"),
        (0.6, 0.7, "Zone 2", "rgba(0, 150, 255, 0.2)"),
        (0.7, 0.8, "Zone 3", "rgba(255, 200, 0, 0.2)"),
        (0.8, 0.9, "Zone 4", "rgba(255, 100, 0, 0.2)"),
        (0.9, 1.0, "Zone 5", "rgba(255, 0, 0, 0.2)")
    ]

    for low, high, zone_name, color in zones_info:
        fig.add_hrect(y0=low * max_hr, y1=high * max_hr,
                      fillcolor=color, layer="below", line_width=0,
                      annotation_text=zone_name, annotation_position="top left")

    # Heart rate line on primary y-axis
    fig.add_trace(go.Scatter(
        x=df.index,
        y=df[heart_rate_column],
        mode='lines',
        name='HeartRate',
        line=dict(color='red', width=2),
        yaxis='y1'
    ))

    # Power line on secondary y-axis
    fig.add_trace(go.Scatter(
        x=df.index,
        y=df[power_column],
        mode='lines',
        name='Power',
        line=dict(color='orange', width=1.5),
        yaxis='y2'
    ))

    fig.update_layout(
        title=f"{heart_rate_column} and {power_column} over Time with Zones",
        xaxis=dict(title="Time [ms]"),
        yaxis=dict(title=f"{heart_rate_column} [bpm]", side='left'),
        yaxis2=dict(title=f"{power_column} [W]", overlaying='y', side='right'),
        legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1),
        hovermode='x unified'
    )

    return fig