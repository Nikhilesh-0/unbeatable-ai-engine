import streamlit as st
import math
from game_engine import TicTacToe, minimax

# --- PAGE CONFIG ---
st.set_page_config(page_title="Unbeatable AI", page_icon="🤖")

# --- CUSTOM CSS ---
st.markdown("""
    <style>
    /* 1. Hide Menu & Footer */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* 2. Compact Layout */
    .block-container {
        padding-top: 0.5rem; /* Ultra-tight top padding */
        padding-bottom: 0rem;
    }
    
    /* 3. Button Styling - SMALLER HEIGHT */
    div.stButton > button {
        height: 80px;  /* Reduced from 100px -> 80px */
        width: 100%;
        font-size: 28px; /* Slightly smaller font */
        margin: 0px;
    }
    
    /* 4. Reduce Gap between Title and Board */
    div[data-testid="stMarkdownContainer"] > h1 {
        padding-top: 0rem;
        margin-bottom: 0rem;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🤖 Unbeatable AI")
st.write("Engine: **Minimax Algorithm** | Optimization: **Alpha-Beta Pruning**")

# --- INITIALIZE STATE ---
if 'game' not in st.session_state:
    st.session_state.game = TicTacToe()
if 'winner' not in st.session_state:
    st.session_state.winner = None

# --- GAME LOGIC ---
def handle_click(i):
    if st.session_state.game.board[i] == ' ' and not st.session_state.winner:
        st.session_state.game.make_move(i, 'X')
        
        if st.session_state.game.current_winner:
            st.session_state.winner = 'X'
        elif not st.session_state.game.empty_squares():
            st.session_state.winner = 'Draw'
        else:
            with st.spinner("Thinking..."):
                ai_move = minimax(st.session_state.game, 0, -math.inf, math.inf, True)['position']
                st.session_state.game.make_move(ai_move, 'O')
                
                if st.session_state.game.current_winner:
                    st.session_state.winner = 'O'
                elif not st.session_state.game.empty_squares():
                    st.session_state.winner = 'Draw'

# --- UI LAYOUT ---
col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    # 1. The Board
    for row in range(3):
        cols = st.columns(3)
        for col in range(3):
            i = row * 3 + col
            disabled = (st.session_state.winner is not None)
            
            if cols[col].button(
                st.session_state.game.board[i], 
                key=i, 
                disabled=disabled,
                use_container_width=True
            ):
                handle_click(i)
                st.rerun()

    # 2. Result Area
    if st.session_state.winner:
        st.write("") 
        if st.session_state.winner == 'O':
            st.error("💀 AI Wins!")
        elif st.session_state.winner == 'X':
            st.success("🎉 You Won!")
        else:
            st.info("🤝 It's a Draw!")
        
        if st.button("Play Again", type="primary", use_container_width=True):
            del st.session_state.game
            del st.session_state.winner
            st.rerun()