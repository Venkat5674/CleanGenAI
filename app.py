import asyncio
import streamlit as st
import pandas as pd
from env.environment import DataCleaningEnv
from inference import get_action_from_llm
import io

st.set_page_config(page_title="AI Data Cleaner", layout="wide")
st.title("🧹 AI-Powered Data Cleaning Agent")

st.markdown("""
Upload a messy dataset (CSV or Excel) and let our LLM agent clean it autonomously! 
It iteratively applies data cleaning actions (remove duplicates, fill missing values, etc.) and evaluates a reward function.
""")

uploaded_file = st.file_uploader("Upload uncleaned Data (CSV or Excel)", type=["csv", "xlsx", "xls"])

if "cleaned_df" not in st.session_state:
    st.session_state.cleaned_df = None
if "history" not in st.session_state:
    st.session_state.history = []

async def run_cleaning(df):
    env = DataCleaningEnv(df=df)
    obs = await env.reset()
    
    st.write("### 🛠️ Cleaning Process Log")
    log_container = st.empty()
    
    done = False
    reward = 0.0
    history = []
    
    while not done:
        with st.spinner("LLM is analyzing the data and deciding next action..."):
            action = await get_action_from_llm(obs)
            
        pre_missing = obs.num_missing
        pre_duplicates = obs.num_duplicates
        step_num = obs.steps_taken + 1
        
        obs, reward, done, info = await env.step(action)
        
        if action.action_type == "remove_duplicates":
            action_desc = "Removed duplicate rows"
        elif action.action_type == "fill_nulls":
            action_desc = f"Filled missing values in '{action.column}' with '{action.value}'"
        elif action.action_type == "drop_column":
            action_desc = f"Dropped column '{action.column}'"
        elif action.action_type == "convert_date":
            action_desc = f"Converted '{action.column}' to Date format"
        elif action.action_type == "drop_row":
            if action.column:
                action_desc = f"Dropped rows where '{action.column}' is '{action.value}'"
            else:
                action_desc = "Dropped all rows containing missing values"
        elif action.action_type == "stop_cleaning":
            action_desc = "Finished! Data marked clean."
        else:
            action_desc = str(action.action_type)

        history.append({
            "Step": step_num,
            "Action Summary": action_desc,
            "Action Type": action.action_type,
            "Target Column": action.column,
            "Values Fixed": action.value,
            "Missing Left": obs.num_missing,
            "Missing Diff": pre_missing - obs.num_missing,
            "Duplicates Left": obs.num_duplicates,
            "Duplicates Diff": pre_duplicates - obs.num_duplicates,
            "Reward Score": round(reward, 4),
            "Error": info.get("error", None)
        })

        # Update log on screen
        log_df = pd.DataFrame(history)
        log_container.dataframe(log_df, use_container_width=True)
        
    return env.df, history, reward

if uploaded_file is not None:
    st.write("### 📄 Original Dataset Preview")
    
    try:
        if uploaded_file.name.endswith(".csv"):
            original_df = pd.read_csv(uploaded_file)
        else:
            original_df = pd.read_excel(uploaded_file)
    except pd.errors.ParserError:
        # Reset file pointer and try again while skipping bad lines, or try different separator
        uploaded_file.seek(0)
        original_df = pd.read_csv(uploaded_file, on_bad_lines='skip', engine='python')
        st.warning("⚠️ Some rows in the uploaded CSV had irregular columns and had to be skipped.")
    except Exception as e:
        st.error(f"Error loading file: {e}")
        st.stop()

    st.dataframe(original_df.head(10))

    if st.button("Start Cleaning 🚀"):
        st.session_state.history = [] # reset
        with st.spinner("Cleaning in progress..."):
            cleaned_df, history, final_reward = asyncio.run(run_cleaning(original_df))
            st.session_state.cleaned_df = cleaned_df
            st.session_state.history = history

if st.session_state.cleaned_df is not None:
    st.success("Data Cleaning Complete!")
    st.write("### ✨ Cleaned Dataset")
    st.dataframe(st.session_state.cleaned_df)
    
    # Download logic
    csv = st.session_state.cleaned_df.to_csv(index=False)
    
    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
        st.session_state.cleaned_df.to_excel(writer, index=False, sheet_name='Cleaned')
        
    col1, col2 = st.columns(2)
    with col1:
        st.download_button(
            label="Download as CSV ⬇️",
            data=csv,
            file_name="cleaned_data.csv",
            mime="text/csv",
        )
    with col2:
        st.download_button(
            label="Download as Excel ⬇️",
            data=buffer,
            file_name="cleaned_data.xlsx",
            mime="application/vnd.ms-excel",
        )
