import pandas as pd
import matplotlib.pyplot as plt

plt.style.use('ggplot')

def load_health_logs(filepath):
    df = pd.read_csv(filepath, parse_dates=['date'])
    df.sort_values('date', inplace=True)
    
    mood_map = {'sad': 0, 'neutral': 1, 'happy': 2}   #we need to encode numericallly for the graphs
    df['mood_score'] = df['mood'].map(mood_map)
    
    return df

def plot_health_trends(df):

    mood_map = {'sad': 0, 'neutral': 1, 'happy': 2}
    df['mood_score'] = df['mood'].map(mood_map)
    dates = df['date']

    plt.figure(figsize=(12, 8))

    plt.subplot(2, 2, 1)
    plt.plot(dates, df['sleep_hours'], marker='o')
    plt.title('Sleep Duration (hrs)')
    plt.xlabel('Date')
    plt.ylabel('Hours')

    plt.subplot(2, 2, 2)
    plt.plot(dates, df['mood_score'], marker='o', color='orange')
    plt.title('Mood Score (0=Sad, 1=Neutral, 2=Happy)')
    plt.xlabel('Date')
    plt.ylabel('Mood Score')

    plt.subplot(2, 2, 3)
    plt.plot(dates, df['hydration_ml'], marker='o', color='blue')
    plt.title('Hydration (ml)')
    plt.xlabel('Date')
    plt.ylabel('ml')

    plt.subplot(2, 2, 4)
    plt.plot(dates, df['steps'], marker='o', color='green')
    plt.title('Steps Count')
    plt.xlabel('Date')
    plt.ylabel('Steps')

    plt.tight_layout()
    plt.show()


# if __name__ == "__main__":
#     df = load_health_logs("data/mock_health_logs.csv")
#     plot_health_trends(df)
