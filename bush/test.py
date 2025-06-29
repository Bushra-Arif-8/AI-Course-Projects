import streamlit as st  # Streamlit for building web apps
import pandas as pd  # Pandas for data manipulation
import json  # JSON for loading and parsing JSON files
import joblib  # Joblib for loading saved models and scalers
import numpy as np  # NumPy for numerical operations
from sklearn.metrics.pairwise import cosine_similarity  # Cosine similarity from sklearn for compatibility scoring

# Main function to render the prediction page
def prediction_page():
    st.set_page_config(layout="wide")  # Set Streamlit page layout to wide

    # 🌈 Custom Background
    page_bg = """
    <style>
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(to right, #ffecd2, #fcb69f);
    }
    </style>
    """
    st.markdown(page_bg, unsafe_allow_html=True)  # Apply custom background gradient

    # 🎉 Welcome Header
    st.markdown("""
        <h1 style="text-align: center; color: #FF69B4; font-size: 48px;">
            💞 Welcome to <span style="color:#8A2BE2;"> AI-POWERED Match Minds</span> 💞
        </h1>
    """, unsafe_allow_html=True)  # Display main header

    # 📜 Redesigned Intro Box with Image Side-by-Side
    st.markdown("""
        <div style="
            display: flex;
            align-items: center;
            background-color: #f0f8ff;
            padding: 20px;
            border-radius: 15px;
            max-width: 900px;
            margin: 0 auto 30px auto;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        ">
            <img src="https://static.vecteezy.com/system/resources/previews/003/209/711/original/friendship-compatibility-and-relationship-vector.jpg"
                 alt="Friendship Image"
                 style="border-radius: 15px; margin-right: 25px; width: 150px; height: 150px; object-fit: cover;">
            <div style="font-size: 18px; color: #333;">
                <p><strong>Discover how compatible you are with potential friends through our engaging quiz!</strong></p>
                <p>This fun and insightful journey will help you understand your friendships better and find those who share similar values and interests.</p>
                <ul>
                    <li>Answer questions about your lifestyle and personality</li>
                    <li>Explore your thoughts on friendships and social interactions</li>
                    <li>Receive a compatibility score that can help you find your ideal friend match!</li>
                </ul>
            </div>
        </div>
    """, unsafe_allow_html=True)  # Intro box with an image and text

    # 📂 Load Session Data
    if "df" not in st.session_state:
        st.session_state.df = pd.read_csv("clustered_friends.csv")  # Load clustered friends data

    if "expected_features" not in st.session_state:
        with open("expected_features.json") as f:
            st.session_state.expected_features = [feat.strip().lower() for feat in json.load(f)]  # Load expected features

    if "kmeans" not in st.session_state:
        st.session_state.kmeans = joblib.load("kmeans_model.joblib")  # Load trained KMeans model

    if "scaler" not in st.session_state:
        st.session_state.scaler = joblib.load("scaler.joblib")  # Load the feature scaler

    if "question_bank" not in st.session_state:
        questions_df = pd.read_csv("questionnaire.csv", encoding='cp1252')  # Load questions from CSV
        qb = {}
        for _, row in questions_df.iterrows():
            feature = str(row["Feature"]).strip().lower()  # Extract and clean feature name
            question = str(row["Question"]).strip()  # Extract question
            options = [opt.strip() for opt in str(row["Options"]).split(",")] if "Options" in row else []  # Extract options
            labels = [int(label.strip()) for label in str(row["Labels"]).split(",")] if "Labels" in row else []  # Extract labels
            qb[feature] = {"question": question, "options": options, "labels": labels}  # Store in question bank
        st.session_state.question_bank = qb  # Save to session state

    # 👤 Friend 1
    st.markdown("---")  # Horizontal rule
    st.markdown("<h3 style='color: #2e8b57;'>📝 Please answer these questions:</h3>", unsafe_allow_html=True)  # Section header

    friend1_name = st.text_input("Enter Friend 1 Name", value="", placeholder="Please enter your name", key="f1_name")  # Input for Friend 1 name
    friend1_scores = {}  # Dictionary to store Friend 1's answers

    if friend1_name.strip():
        friend1_age = st.number_input("Enter Friend 1 Age", min_value=0, step=1, key="f1_age")  # Friend 1 age input
        friend1_scores['age'] = friend1_age  # Store age

        if friend1_age > 0:
            st.markdown(f"<h4 style='color: #4169e1; text-align: center;'>💬 Answer for {friend1_name}</h4>", unsafe_allow_html=True)  # Show question header
            for feature in st.session_state.expected_features:
                if feature == 'age':
                    continue  # Skip age (already handled)
                if feature in st.session_state.question_bank:
                    q = st.session_state.question_bank[feature]  # Retrieve question for feature

                    st.markdown(f"""<div style="background: linear-gradient(135deg, #f6d365 0%, #fda085 100%); border-radius: 15px; padding: 25px; margin: 15px auto; max-width: 700px; font-weight: bold; font-size: 22px; text-align: center; color: #333;">{q['question']}</div>""", unsafe_allow_html=True)  # Styled question

                    options = q["options"]
                    labels = q["labels"]
                    selected_key = f"f1_{feature}"  # Unique key

                    col1, col2, col3 = st.columns([1, 2, 1])  # Centered input
                    with col2:
                        selected_option = st.radio("", options=options, index=0, key=selected_key, label_visibility="collapsed")  # Answer options

                    friend1_scores[feature] = labels[options.index(selected_option)]  # Map option to label
                else:
                    friend1_scores[feature] = st.number_input(f"{friend1_name} - {feature}", 0, 10, 5, key=f"f1_num_{feature}")  # Input for unlisted features

    # 👥 Friend 2
    st.markdown("<hr style='border: 4px solid black; margin: 30px 0;'>", unsafe_allow_html=True)  # Separator
    friend2_scores = {}  # Friend 2 answers
    friend2_name = ""  # Placeholder name
    friend2_age = 0  # Placeholder age

    if friend1_name.strip() and friend1_scores.get('age', 0) > 0 and len(friend1_scores) == len(st.session_state.expected_features):
        friend2_name = st.text_input("Enter Friend 2 Name", value="", placeholder="Please enter Friend 2 name", key="f2_name")  # Friend 2 name input
        if friend2_name.strip():
            friend2_age = st.number_input("Enter Friend 2 Age", min_value=0, step=1, key="f2_age")  # Friend 2 age input
            friend2_scores['age'] = friend2_age

            if friend2_age > 0:
                st.markdown(f"<h4 style='color: #ff4500; text-align: center;'>💬 Answer for {friend2_name}</h4>", unsafe_allow_html=True)  # Question heading
                for feature in st.session_state.expected_features:
                    if feature == 'age':
                        continue  # Skip age
                    if feature in st.session_state.question_bank:
                        q = st.session_state.question_bank[feature]  # Get question

                        st.markdown(f"""<div style="background: linear-gradient(135deg, #ff9a9e 0%, #fad0c4 100%); border-radius: 15px; padding: 25px; margin: 15px auto; max-width: 700px; font-weight: bold; font-size: 22px; text-align: center; color: #333;">{q['question']}</div>""", unsafe_allow_html=True)  # Styled question box

                        options = q["options"]
                        labels = q["labels"]
                        selected_key = f"f2_{feature}"  # Unique key

                        col1, col2, col3 = st.columns([1, 2, 1])  # Layout
                        with col2:
                            selected_option = st.radio("", options=options, index=0, key=selected_key, label_visibility="collapsed")  # Select option

                        friend2_scores[feature] = labels[options.index(selected_option)]  # Get score
                    else:
                        friend2_scores[feature] = st.number_input(f"{friend2_name} - {feature}", 0, 10, 5, key=f"f2_num_{feature}")  # Input for unlisted features

    # 🔍 Compatibility Calculation
    if friend1_scores.get('age', 0) > 0 and friend2_scores.get('age', 0) > 0 and \
       len(friend1_scores) == len(st.session_state.expected_features) and \
       len(friend2_scores) == len(st.session_state.expected_features):

        if st.button("Check Compatibility 💖"):  # Button to calculate compatibility
            df = st.session_state.df
            kmeans = st.session_state.kmeans
            scaler = st.session_state.scaler

            f1_df = pd.DataFrame([friend1_scores])  # DataFrame for Friend 1
            f2_df = pd.DataFrame([friend2_scores])  # DataFrame for Friend 2

            # Mapping lowercase to original column names
            mapping = {
                'age': 'Age',
                'openness to experience': 'Openness To Experience',
                'extraversion': 'Extraversion',
                'neuroticism': 'Neuroticism',
                'honesty': 'Honesty',
                'loyality': 'Loyality',
                'respect': 'Respect',
                'family values': 'Family Values',
                'open mindedness': 'Open Mindedness',
                'listen music': 'Listen Music',
                'reading books': 'Reading Books',
                'playing or watching sports': 'Playing or Watching Sports',
                'watching movies and tv series': 'Watching Movies and TV Series',
                'traveling': 'Traveling',
                'cooking and baking': 'Cooking and Baking',
                'video gaming': 'Video Gaming',
                'drawing or painting': 'Drawing or Painting',
                'coding and working with technology': 'Coding and Working with Technology',
                'hanging out with friends': 'Hanging Out With Friends',
                'writing or journaling': 'Writing or Journaling',
                'yoga or meditation': 'Yoga or Meditation',
                'solving puzzles or brain games': 'Solving Puzzles or Brain Games',
                'photography': 'Photography',
                'hangout routine': 'Hangout Routine',
                'use ofsocial media': 'Use ofsocial Media',
                'public speaking': 'Public Speaking',
                'friendhip initiations': 'Friendhip Initiations'
            }

            original_features = list(scaler.feature_names_in_)  # Get feature order
            f1_df.rename(columns=mapping, inplace=True)  # Rename Friend 1 columns
            f2_df.rename(columns=mapping, inplace=True)  # Rename Friend 2 columns
            f1_df = f1_df.reindex(columns=original_features, fill_value=0)  # Reorder features
            f2_df = f2_df.reindex(columns=original_features, fill_value=0)

            f1_scaled = scaler.transform(f1_df)  # Scale Friend 1 features
            f2_scaled = scaler.transform(f2_df)  # Scale Friend 2 features
            f1_cluster = kmeans.predict(f1_scaled)[0]  # Predict cluster
            f2_cluster = kmeans.predict(f2_scaled)[0]

            st.session_state.friend1_cluster = f1_cluster  # Save cluster
            st.session_state.friend2_cluster = f2_cluster
            st.session_state.friend1_name = friend1_name  # Save names
            st.session_state.friend2_name = friend2_name

            centroid_sim = cosine_similarity(
                kmeans.cluster_centers_[f1_cluster].reshape(1, -1),
                kmeans.cluster_centers_[f2_cluster].reshape(1, -1)
            )[0][0]  # Similarity between clusters

            friend_sim = cosine_similarity(f1_scaled, f2_scaled)[0][0]  # Individual similarity
            compatibility_score = 0.6 * friend_sim + 0.4 * centroid_sim  # Weighted score
            compatibility_percentage = round(compatibility_score * 100, 2)  # Percentage score

            # 🎁 Compatibility Display
            st.markdown(f"""<div style="margin-top: 40px; padding: 30px; border-radius: 20px; background-color: #FFF0F5; max-width: 600px; margin-left: auto; margin-right: auto; box-shadow: 0 6px 10px rgba(255,105,180,0.3); text-align: center;"><h2 style="color: #db1492;">Compatibility between <span style="color:#ff1493;">{friend1_name}</span> and <span style="color:#ff69b4;">{friend2_name}</span></h2><p style="font-size: 48px; font-weight: bold; color: #FF69B4;">{compatibility_percentage}%</p></div>""", unsafe_allow_html=True)  # Result display

            # 🎯 Compatibility Category
            if compatibility_percentage > 80:
                category = "Highly Compatible"
                quote = "“A true friend is one soul in two bodies.” – Aristotle"
                funny_comment = "😄 You guys are practically two peas in a pod!"
                color = "#2e8b57"
            elif compatibility_percentage > 70:
                category = "Compatible"
                quote = "“Friendship is the only cement that will ever hold the world together.” – Woodrow Wilson"
                funny_comment = "🙂 Great potential for an awesome friendship!"
                color = "#6a5acd"
            elif compatibility_percentage > 40:
                category = "Somewhat Compatible"
                quote = "“A friend may well be reckoned the masterpiece of nature.” – Ralph Waldo Emerson"
                funny_comment = "😅 You’ll have fun, but expect some quirks!"
                color = "#ffa500"
            else:
                category = "Less Compatible"
                quote = "“Friendship is unnecessary, like philosophy, like art... It has no survival value; rather it is one of those things which give value to survival.” – C.S. Lewis"
                funny_comment = "😬 Opposites attract, but brace yourself!"
                color = "#b22222"

            st.markdown(f"""<div style="margin-top: 25px; padding: 20px; border-radius: 15px; background-color: {color}; color: white; max-width: 600px; margin-left: auto; margin-right: auto;"><h3>{category}</h3><blockquote style="font-size: 18px; font-style: italic;">{quote}</blockquote><p style="font-size: 20px;">{funny_comment}</p></div>""", unsafe_allow_html=True)  # Category result

    # ➡️ Friend Suggestions Button
    if st.button("See Friend Suggestions"):  # Button to go to suggestion page
        if "friend1_cluster" in st.session_state and "friend2_cluster" in st.session_state:
            st.session_state.page = "suggestion"
            st.rerun()  # Navigate to suggestion page
        else:
            st.warning("🚨 Please enter both friends' details and check compatibility first!")  # Warning if conditions not met

# Entry point for the app
if __name__ == "__main__":
    prediction_page()
