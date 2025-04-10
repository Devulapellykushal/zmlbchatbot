# import pandas as pd
# from sklearn.linear_model import LogisticRegression
# from sklearn.preprocessing import LabelEncoder
# import warnings

# warnings.filterwarnings('ignore')

# def load_health_logs(filepath):
#     df = pd.read_csv(filepath, parse_dates=['date'])
#     df.sort_values('date', inplace=True)
#     return df

# def train_mood_model(df):
#     if 'mood' not in df.columns:
#         return None, None

#     le = LabelEncoder()
#     df['mood_encoded'] = le.fit_transform(df['mood'])

#     features = [col for col in ['sleep_hours', 'hydration_ml', 'steps'] if col in df.columns]
#     if not features:
#         return None, None

#     X = df[features]
#     y = df['mood_encoded']

#     model = LogisticRegression()
#     model.fit(X, y)
#     return model, le

# def analyze_hydration(df):
#     if 'hydration_ml' not in df.columns:
#         return None
#     low_hydration_days = df[df['hydration_ml'] < 2200]
#     if len(low_hydration_days) >= 3:
#         return "🚰 Your hydration has been low for 3 or more days. Increase water intake."
#     return None

# def analyze_sleep(df):
#     if 'sleep_hours' not in df.columns:
#         return None
#     low_sleep_days = df[df['sleep_hours'] < 6]
#     if len(low_sleep_days) >= 3:
#         return "😴 Your sleep has been below 6 hours for multiple days. Aim for 7–8 hours of rest."
#     return None

# def analyze_steps(df):
#     if 'steps' not in df.columns:
#         return None
#     avg_steps = df['steps'].mean()
#     if avg_steps < 5000:
#         return f"🚶‍♂️ Your average steps ({int(avg_steps)}) are lower than the healthy range. Try to stay more active."
#     return None

# def analyze_mood_with_ml(df, model, le):
#     if model is None or le is None:
#         return None
#     features = [col for col in ['sleep_hours', 'hydration_ml', 'steps'] if col in df.columns]
#     if not features:
#         return None
#     df['predicted_mood'] = le.inverse_transform(model.predict(df[features]))
#     sad_days = df[df['predicted_mood'] == 'sad']
#     if len(sad_days) >= 3:
#         return "🧠 Mood patterns suggest fatigue or stress. Consider self-care, better sleep, and hydration."
#     return None

# def generate_combined_insights(df):
#     insights = []

#     model, le = train_mood_model(df)

#     for fn in [analyze_hydration, analyze_sleep, analyze_steps]:
#         msg = fn(df)
#         if msg:
#             insights.append(msg)

#     mood_msg = analyze_mood_with_ml(df, model, le)
#     if mood_msg:
#         insights.append(mood_msg)

#     if not insights:
#         insights.append("✅ No issues detected from the uploaded data.")

#     return insights

# if __name__ == "__main__":
#     df = load_health_logs("data/mock_health_logs.csv")
#     insights = generate_combined_insights(df)

#     print("\n💡 Health Insights Summary:")
#     for insight in insights:
#         print(f"- {insight}")


import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import LabelEncoder
import warnings

warnings.filterwarnings('ignore')

def load_health_logs(filepath):
    df = pd.read_csv(filepath, parse_dates=['date'])
    df.sort_values('date', inplace=True)
    return df

def train_mood_model(df):
    if 'mood' not in df.columns:
        return None, None

    le = LabelEncoder()
    df['mood_encoded'] = le.fit_transform(df['mood'])

    features = [col for col in ['sleep_hours', 'hydration_ml', 'steps'] if col in df.columns]
    if not features:
        return None, None

    X = df[features]
    y = df['mood_encoded']

    model = LogisticRegression()
    model.fit(X, y)
    return model, le

def analyze_hydration(df):
    if 'hydration_ml' not in df.columns:
        return "⚠️ 'hydration_ml' column missing. Hydration analysis skipped."
    low_hydration_days = df[df['hydration_ml'] < 2200]
    if len(low_hydration_days) >= 3:
        return "🚰 Your hydration has been low for 3 or more days. Increase water intake."
    return None

def analyze_sleep(df):
    if 'sleep_hours' not in df.columns:
        return "⚠️ 'sleep_hours' column missing. Sleep analysis skipped."
    low_sleep_days = df[df['sleep_hours'] < 6]
    if len(low_sleep_days) >= 3:
        return "😴 Your sleep has been below 6 hours for multiple days. Aim for 7–8 hours of rest."
    return None

def analyze_steps(df):
    if 'steps' not in df.columns:
        return "⚠️ 'steps' column missing. Steps analysis skipped."
    avg_steps = df['steps'].mean()
    if avg_steps < 5000:
        return f"🚶‍♂️ Your average steps ({int(avg_steps)}) are lower than the healthy range. Try to stay more active."
    return None

def analyze_mood_with_ml(df, model, le):
    if model is None or le is None:
        return "⚠️ Mood prediction skipped due to missing required columns."
    features = [col for col in ['sleep_hours', 'hydration_ml', 'steps'] if col in df.columns]
    if not features:
        return "⚠️ Insufficient features for mood prediction."
    df['predicted_mood'] = le.inverse_transform(model.predict(df[features]))
    sad_days = df[df['predicted_mood'] == 'sad']
    if len(sad_days) >= 3:
        return "🧠 Mood patterns suggest fatigue or stress. Consider self-care, better sleep, and hydration."
    return None

def generate_combined_insights(df):
    insights = []

    model, le = train_mood_model(df)

    for fn in [analyze_hydration, analyze_sleep, analyze_steps]:
        msg = fn(df)
        if msg:
            insights.append(msg)

    mood_msg = analyze_mood_with_ml(df, model, le)
    if mood_msg:
        insights.append(mood_msg)

    if not insights:
        insights.append("✅ No issues detected from the uploaded data.")

    return insights

if __name__ == "__main__":
    df = load_health_logs("data/mock_health_logs.csv")
    insights = generate_combined_insights(df)

    print("\n💡 Health Insights Summary:")
    for insight in insights:
        print(f"- {insight}")
