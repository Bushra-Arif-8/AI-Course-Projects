import streamlit as st
import pandas as pd

def suggestion_page():
    st.set_page_config(layout="wide")

    background_style = """
    <style>
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(to right, #ffe0e9, #e0f7fa);
    }
    .suggestion-card {
        background-color: #ffffff;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
        padding: 15px;
        margin-bottom: 15px;
    }
    .suggestion-card img {
        border-radius: 50%;
        margin-right: 15px;
        object-fit: cover;
    }
    </style>
    """
    st.markdown(background_style, unsafe_allow_html=True)

    st.markdown("""
        <h1 style="text-align:center; color:#4B0082;">🔮 Friendship Suggestions 🔮</h1>
        <p style="text-align:center; font-size:18px; color:#333;">
            Based on your compatibility clusters, here are some friends you might truly vibe with!
        </p>
    """, unsafe_allow_html=True)

    df = pd.read_csv("clustered_friends.csv")
    df = df.dropna(subset=['Full Name '])
    df['Full Name '] = df['Full Name '].astype(str).str.strip()
    df['Name_clean'] = df['Full Name '].str.lower()
    df['Cluster'] = df['Cluster'].astype(int)

    f1_cluster = int(st.session_state.friend1_cluster)
    f2_cluster = int(st.session_state.friend2_cluster)
    friend1_name = st.session_state.friend1_name.strip().lower()
    friend2_name = st.session_state.friend2_name.strip().lower()

    avatar_male = "https://randomuser.me/api/portraits/men/{}.jpg"
    avatar_female = "https://randomuser.me/api/portraits/women/{}.jpg"

    st.markdown("""
    <div style="background-color: #fce4ec; padding: 20px; border-radius: 10px; margin: 20px auto; max-width: 900px;">
        <h3 style="color: #c2185b; text-align: center;">💌 Friendship Tip 💌</h3>
        <p style="font-size: 16px; color: #444; text-align: center;">
            True friendship is built on shared values, honesty, and joy. Keep the spark alive by exploring new experiences,
            supporting one another, and embracing your differences.
        </p>
    </div>
    """, unsafe_allow_html=True)

    col1, spacer, col2 = st.columns([5, 1, 5])

    traits_list_1 = ['Openness To Experience', 'Honesty', 'Loyalty', 'Respect', 'Family Values']
    traits_list_2 = ['Open Mindedness', 'Listening Music', 'Reading Books', 'Cooking and Baking', 'Traveling']

    toggle = hash(friend1_name + friend2_name) % 2 == 0

    friend1_traits = traits_list_1 if toggle else traits_list_2
    friend2_traits = traits_list_2 if toggle else traits_list_1

    threshold = 3

    def format_traits_as_sentence(row, traits):
        matched_traits = []
        for trait in traits:
            if trait in row and pd.notna(row[trait]) and float(row[trait]) > threshold:
                matched_traits.append(trait.lower())
        if matched_traits:
            if len(matched_traits) == 1:
                return f"You both have {matched_traits[0]}."
            else:
                return "You both have " + ", ".join(matched_traits[:-1]) + f", and {matched_traits[-1]}."
        else:
            return ""

    def has_significant_traits(row, traits, threshold=3):
        for trait in traits:
            if trait in row and pd.notna(row[trait]) and float(row[trait]) > threshold:
                return True
        return False

    def display_suggestions(column, friend_name, friend_cluster, traits):
        column.markdown(f"<h4 style='text-align:center; color:#2E8B57;'>Suggestions for {friend_name.title()}</h4>", unsafe_allow_html=True)

        suggestions = df[(df['Cluster'] == friend_cluster)]
        suggestions = suggestions[~suggestions['Name_clean'].isin([friend_name])]

        # Filter only friends with significant shared traits
        filtered = suggestions[suggestions.apply(lambda row: has_significant_traits(row, traits), axis=1)]

        if filtered.empty:
            column.info("No suitable friends found in this cluster.")
        else:
            sample = filtered.sample(min(5, len(filtered)))
            for idx, row in sample.iterrows():
                avatar_index = idx % 100
                gender = str(row['Gender']).strip().lower()
                avatar_url = avatar_male.format(avatar_index) if gender == 'male' else avatar_female.format(avatar_index)

                traits_sentence = format_traits_as_sentence(row, traits)

                column.markdown(
                    f"""
                    <div class="suggestion-card" style="display:flex; align-items:center;">
                        <img src="{avatar_url}" width="60" height="60">
                        <div>
                            <p style="margin:0; font-weight:bold; font-size:18px; color:#4B0082;">{row['Full Name ']}</p>
                            <p style="margin:0; color:#777;">Gender: {row['Gender']}</p>
                            <p style="margin-top: 8px; color:#555; font-size:15px; font-style: italic;">{traits_sentence}</p>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

    with col1:
        display_suggestions(col1, friend1_name, f1_cluster, friend1_traits)

    with col2:
        display_suggestions(col2, friend2_name, f2_cluster, friend2_traits)

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("⬅️ Back to Compatibility Check"):
        st.session_state.page = "test"
        st.rerun()