##### Super Bowl Squares Streamlit App #####

import streamlit as st
import pandas as pd
import numpy as np
from streamlit_extras.metric_cards import style_metric_cards
import plotly.express as px
import plotly.graph_objects as go


# Set the page to wide mode
st.set_page_config(layout="wide")


### Define functions 

# Load data using Lee Sharpe's games data file
nfl_scores = pd.read_csv("NFL Game Scores.csv")

# Function to calculate probabilities from NFL scores
def calculate_probabilities(nfl_scores):
    nfl_scores['home_score_last_digit'] = nfl_scores['home_score'] % 10
    nfl_scores['away_score_last_digit'] = nfl_scores['away_score'] % 10
    score_combinations = nfl_scores.groupby(['home_score_last_digit', 'away_score_last_digit']).size().unstack(fill_value=0)
    total_games = nfl_scores.shape[0]
    score_probabilities = score_combinations / total_games
    return score_probabilities

# Function to create a Plotly heatmap
def create_heatmap(score_probabilities):

    fig = px.imshow(
        score_probabilities,
        labels=dict(x="Away Team", y="Home Team", color="Probability"),
        x=score_probabilities.columns,
        y=score_probabilities.index,
        aspect="auto",
        color_continuous_scale='dense'  # You can choose a color scale that fits your preference
    )

    # Adding annotations (percentage values) to each cell
    for y in range(score_probabilities.shape[0]):
        for x in range(score_probabilities.shape[1]):
            fig.add_annotation(
                x=score_probabilities.columns[x],
                y=score_probabilities.index[y],
                text=f"{score_probabilities.iloc[y, x]*100:.1f}%",  
                showarrow=False,
                font=dict(color="white")
            )

    fig.update_xaxes(side="top", tickvals=list(range(10)), ticktext=[str(i) for i in range(10)])
    fig.update_yaxes(tickvals=list(range(10)), ticktext=[str(i) for i in range(10)])

    fig.update_layout(
        title="",
        xaxis_nticks=10,
        yaxis_nticks=10,
        height=700,  # Set the height of the figure
        coloraxis_showscale=False  # Hide the color bar/legend
    )
    return fig

# Function to calculate frequency distribution of the last digit of scores
def calculate_score_frequencies(nfl_scores, team_type):
    if team_type == "Home":
        scores = nfl_scores['home_score'] % 10
    else:
        scores = nfl_scores['away_score'] % 10

    frequencies = scores.value_counts().sort_index()
    return frequencies


#### Define Mainpage UI ####

# Display NFL logo image
logo_path_or_url = '/Users/Stephan/Desktop/Python/Super-Bowl-Squares/Super_Bowl_LVIII_logo.png'
st.image(logo_path_or_url, width=100)  # Adjust width as needed

# Title of your app
st.title('Super Bowl Squares')

# Description or introduction
st.markdown(""" 
Welcome to the NFL Super Bowl Squares app. Use this to explore unique NFL game scores! A **Between The Pipes** app by [Stephan Teodosescu](https://stephanteodosescu.com/).
""")

"---"

# ---- Sidebar ----

# Sidebar for odds type selection and moneyline + bet amount inputs

st.sidebar.header('Selections')
bet_amount = st.sidebar.number_input('Wager/Square ($)', value=10, min_value=0)
away_square = st.sidebar.number_input('Away Square', value=3, min_value=1)
home_square = st.sidebar.number_input('Home Square', value=7, min_value=1)


# Calculate the total payout, profit, and expected value
# win_probability = to_win(bet_amount, odds if odds_type == "American" else american_odds)
# profit = total_payout - bet_amount
# expected_value = (profit * (implied_probability/100)) - (1-(implied_probability/100) * bet_amount)


# ---- KPIs Section ----

# Bet payouts and expected value KPIs
col1, col2, col3 = st.columns(3)

#col1.metric("To Win", value = "$100")
col1.metric(label="Win Probability", value=f"5.6%")
col2.metric("Profit (Earnings)", value=f"$80")
col3.metric("Expected Return", value=f"$100")

style_metric_cards(border_color = '#CCC',
                   border_left_color = '#AA0000')

"---"

# --- Tabs ---
tab1, tab2, tab3, tab4 = st.tabs(["📈 Squares", "📊 Common Numbers", "📊 All Scores", "🗃 About"])

# ---- Plotly Heatmap ----

# Create a full-width container
with tab1:
    tab1.subheader("Squares Heatmap")
    tab1.text('Investigate different odds systems and their implied probability conversions')

    # Calculate probabilities
    probabilities = calculate_probabilities(nfl_scores)

    # Create and display heatmap
    heatmap = create_heatmap(probabilities)

    # Update layout height and remove the legend
    st.plotly_chart(heatmap, use_container_width=True)


# Display the DataFrame as a table
with tab2:  
    st.write('Most common digits')
    
    # Radio button for selecting team type
    team_type = st.radio("Home or Away?", ("Home", "Away"))

    # Calculate and display score frequencies
    frequencies = calculate_score_frequencies(nfl_scores, team_type)
    fig = px.bar(frequencies, labels={'index': 'Last Digit of Score', 'value': 'Frequency'},
                 title=f"Frequency of Last Digit of {team_type} Team Scores")
    st.plotly_chart(fig)

with tab3:
    st.write('All NFL game scores since 2015')
    st.dataframe(nfl_scores)

with tab4:
    st.subheader('About')
    st.markdown(""" 
    **What is Super Bowl Squares?**
                
    The goal of Super Bowl Squares is to match the last digit of each team’s score at the end of each quarter and end of the game. 
    For example, if the 1st quarter ends Chiefs 14, 49ers 7, the individual who bought the square intersecting Chiefs-4 and 49ers-7
    will win money. The most common payout is one winner for each of the first 3 quarters and a 4th winner for the final score. 
    The payouts can be equal or they can increase each quarter. For example, if each square is sold for 10 dollars, then each winner would 
    receive 250 dollars in the equal payout scenario. Alternatively the payout structure could look like: 1st Quarter 100 dollars; 
    2nd Quarter 175 dollars; 3rd Quarter 275 dollars; Final Score 450 dollars.
                
    For more check out my [NFL Analytics website](https://steodose.github.io/NFL/NFL-Summary-Report.html).
    """)



