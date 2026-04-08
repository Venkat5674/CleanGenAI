---
title: CleanGen AI
emoji: 🧹
colorFrom: blue
colorTo: green
sdk: streamlit
app_file: app.py
pinned: false
---

# 🧹 AI-Powered Data Cleaning Agent using OpenEnv

## 📖 Project Title
**AI-Powered Data Cleaning Agent** - An autonomous workflow built using the **OpenEnv** framework.

## ⚠️ Problem Statement and Gap Identified
In modern data science, cleaning messy datasets is often the most tedious, manual, and time-consuming part of the traditional ETL pipeline. Data engineers and analysts spend countless hours fixing formatting issues, filling missing values, dropping irrelevant columns, and removing duplicate rows. 
The major gap is the lack of completely autonomous systems that can figure out these cleaning rules on the fly, without needing a human to write custom Pandas scripts for every single new dirty dataset.

## 💡 Our Approach to solve that problem using OpenEnv
We built this project using **OpenEnv**, an environment framework that lets us treat data cleaning as a Reinforcement Learning (RL) problem. Think of it like a video game where the Large Language Model (LLM) is the player, the messy dataset is the level, and the goal is to get a perfect score by fixing all the errors.

Here is how this loop works in detail:

### 1. Observation (The "Eyes" of the Agent)
If we send an entire dataset with a million rows to an AI, it will crash or forget information. Instead, the environment generates a **highly summarized snapshot** (the observation) of the data's current state. At every step, the LLM looks at:
* **The Schema:** A list of all column names and their data types (e.g., knowing that 'Age' is numbers and 'Name' is text).
* **Error Counts:** Exactly how many missing values (nulls) and exact duplicate rows currently exist in the whole dataset.
* **Data Preview:** A tiny 5-row preview of the actual data to give the LLM context of what the information actually looks like.
This snapshot gives the LLM the exact context it needs to figure out what is wrong to plan its next move.

### 2. Action Space (The "Hands" of the Agent)
To prevent the AI from making wild guesses or writing broken code, we restrict it to a specific "menu" of approved moves. It must reply in a strict structure. The LLM can choose to:
* `remove_duplicates`: Delete rows that are exact copies of another row.
* `fill_nulls`: Target a specific column and replace missing holes with a logical value.
* `convert_date`: Look for weird date formats and standardize them (e.g., converting "Jan-1-2020" to "2020-01-01").
* `drop_column` or `drop_row`: Delete completely useless data.
* `stop_cleaning`: Tell the system it thinks the dataset is finally perfect.
By forcing the AI to use these specific structured actions, we guarantee the cleaning process is safe and bug-free.

### 3. Reward Function (The "Scoreboard")
How does the AI know if it made a good decision or a bad one? After every single action, the environment calculates a **Reward Score** between 0.0 and 1.0. 
* If the AI removes duplicates or successfully fills missing values, the score goes up. 
* If the AI does something useless, the score stays the same.
* If it breaks a rule (like trying to fill a date column with text), the environment feeds back an error message.
This creates an iterative **feedback loop**. The agent takes an action, gets a score and feedback, looks at the new "Observation", and repeats the process step-by-step until the dataset is perfectly clean!

## 🏗️ Architecture Diagram of how project works

<a href="https://ibb.co/p66wW32v"><img src="https://i.ibb.co/Y44QDt27/mermaid-diagram.png" alt="mermaid diagram" border="0"></a>

## 🎯 Main Task of the project
The ultimate goal of this project is to eliminate the need for manual data cleaning by providing a **purely autonomous, zero-code AI agent**. Instead of a human writing one-off Python scripts to clean every new dataset, this system handles the entire process end-to-end.

Here is the frictionless workflow we have built:
1. **Upload the Mess:** The user simply uploads a raw, messy CSV or Excel file containing duplicates, missing values, or inconsistent data formats. No technical knowledge is required.
2. **AI Diagnosis:** The agent instantly scans the dataset to figure out exactly what is wrong without needing instructions or rules from the user.
3. **Autonomous Execution:** Behind the scenes, the agent acts like a tireless Data Engineer. It selects and applies the correct `pandas` fixes (like dropping bad rows or standardizing dates) step-by-step until the data is mathematically pristine.
4. **Download Perfection:** The system presents the final, standardized, and error-free dataset back to the user, ready to be downloaded and used for machine learning, analysis, or dashboards.

In short: **You provide the dirty data, and the AI hands you back the clean result.**

## 💻 Tech Stack
This project leverages modern data science and AI tools to create a seamless experience:
*   **Core Language:** Python 3.10+
*   **Web Interface:** Streamlit (For the interactive, real-time frontend)
*   **Data Engine:** Pandas & NumPy (For fast, under-the-hood data manipulation)
*   **LLM Provider:** Groq API (For lightning-fast reasoning and action generation)
*   **Data Validation:** Pydantic (To strictly enforce the LLM's structured JSON outputs)
*   **RL Framework:** OpenEnv (The structural backbone for the reinforcement learning loop)
*   **Deployment:** Docker (For consistent, isolated environment execution)

## 🛠️ Installation Commands from scratch to end
To run this project on your local machine, follow these steps:

```bash
# 1. Clone the repository
git clone https://github.com/your-repo/OpenEnv-Data-Cleaner.git
cd OpenEnv-Data-Cleaner

# 2. Setup a local Python Virtual Environment
python -m venv .venv

# 3. Activate the environment (Windows)
.venv\Scripts\activate
# (For Mac/Linux: source .venv/bin/activate)

# 4. Install dependencies
pip install -r requirements.txt

# 5. Provide your GROQ API Key 
# Create a .env file and add your key:
echo "GROQ_API_KEY=gsk_your_api_key_here" > .env

# Optional: Run with Docker
docker build -t openenv-cleaner .
docker run -it --env-file .env openenv-cleaner
```

## 🚀 Running commands
Launch the interactive web interface to upload files and watch the agent work:
```bash
streamlit run app.py
```
Run the automated test suite to evaluate the agent on standard tasks:
```bash
python evaluate.py
```
Run the agent in the terminal without a UI:
```bash
python inference.py
```

## 🌐 Deploying to Hugging Face Spaces
Since this project uses a Streamlit web interface (`app.py`), it needs to run as a **Streamlit** Space. It looks like you created a **Gradio** space, but don't worry! We have added a configuration block at the top of this `README.md` file that will automatically switch your space to Streamlit when you upload it.

To deploy your existing code to your new space (`venkatesh509/CleanGen_AI`), run these commands in your terminal:

```bash
# 1. Initialize git if you haven't already
git init

# 2. Add the Hugging Face space as your remote origin (Use HTTPS)
git remote add huggingface https://huggingface.co/spaces/CleanGenAI/CleanGen_AI

# 3. Add all your project files
git add .

# 4. Commit your files
git commit -m "Deploying Streamlit Data Cleaning Agent to Hugging Face"

# 5. Ensure your local branch is named 'main'
git branch -M main

# 6. Push to Hugging Face
git push huggingface main -f
```

**Crucial Final Step (Adding the API Key):** 
Once the upload finishes, go to your Space's **Settings** tab on the Hugging Face website. Scroll down to **Variables and secrets** and create a new **Secret**:
* **Name:** `GROQ_API_KEY`
* **Value:** *(paste your Groq API key here)*

Your space will automatically build and launch!

## 📂 Project Structure
```text
Openenv/
 ├── data/
 │   ├── expected_easy.csv
 │   ├── raw_easy.csv
 │   └── ... (medium, hard)
 ├── env/
 │   ├── actions.py
 │   ├── environment.py
 │   ├── grader.py
 │   ├── observation.py
 │   └── tasks.py
 ├── app.py
 ├── Dockerfile
 ├── evaluate.py
 ├── inference.py
 ├── openenv.yaml
 ├── requirements.txt
 └── README.md
```

## 📝 Explanation of Each File in the project

### `app.py`
1. This is the main web interface for the project, built using Streamlit.
2. It provides an intuitive UI for users to upload messy CSV or Excel files.
3. It displays a preview of the raw, uncleaned dataset upon upload.
4. It manages the background asynchronous execution of the LLM via `inference.py`.
5. It tracks the agent's progress, logging every single action chosen.
6. It dynamically updates a dashboard showing exactly how many duplicates and nulls are left.
7. It gracefully catches and skips bad lines in uploaded CSVs without crashing.
8. It maintains user session state so the UI doesn't reset unexpectedly during cleaning.
9. It presents the final, perfectly cleaned dataset on the screen once the agent is finished.
10. It provides convenient "Download as CSV/Excel" buttons for the final result.

### `evaluate.py`
1. This script serves as our automated benchmarking and testing suite.
2. It tests the agent's capabilities across three difficulty levels: easy, medium, and hard.
3. For each level, it automatically loads the messy `raw_...csv` data into the environment.
4. It triggers the `get_action_from_llm` loop to let the agent clean the file.
5. It tracks the step-by-step choices the agent makes during the terminal output.
6. Once the agent finishes, it loads the perfect golden-standard `expected_...csv` file.
7. It calls the grader module to compare the agent's resulting dataset against the expected dataset.
8. It handles unexpected parsing errors gracefully to keep the evaluation loop running.
9. It calculates a final percentage score based on how perfectly the agent cleaned the data.
10. It outputs an easily readable summary of the evaluation runs to the console.

### `inference.py`
1. This is the core logic connecting our environment to the Groq LLM API.
2. It securely loads the `GROQ_API_KEY` from the `.env` file using the `dotenv` library.
3. It contains the primary system prompt telling the LLM how to act as a data cleaner.
4. It feeds the LLM the current "Observation" (the state of the dataframe).
5. It strictly instructs the LLM to reply only in a specified JSON form.
6. It uses a regular expression to extract the JSON, making it resilient to "chatty" LLMs.
7. It parses the JSON securely using the `Action` Pydantic model to ensure it is valid.
8. It has a fallback mechanism to default to `remove_duplicates` if the LLM output is malformed.
9. It includes a standalone `run()` function to test the agent plainly in the terminal.
10. It prints out exactly what actions the agent takes and what reward it receives.

### `openenv.yaml`
1. This is the main configuration file for the OpenEnv benchmark framework.
2. It explicitly declares the name of our project as `data-cleaning-env`.
3. It keeps a clean structure that defines exactly what simulation we are running.
4. It specifies which standard LLM models (like `gpt-4o-mini`) this benchmark typically runs best on.
5. It catalogs the three default tasks included in this benchmark: `easy`, `medium`, and `hard`.
6. It formally lists the entire action space available to the agent.
7. Actions listed include `remove_duplicates`, `fill_nulls`, `convert_date`, and `drop_column`.
8. It serves as standard metadata so other benchmarking tools can automatically discover this project.
9. It utilizes simple, standard YAML syntax making it universally readable.
10. It represents the structural backbone required for any OpenEnv deployment.

### `Dockerfile`
1. This file provides the exact instructions needed to build a Docker container.
2. It uses `python:3.10-slim` as the base image to keep the overall download size small.
3. It sets the working directory to `/app` inside the isolated container.
4. It copies the `requirements.txt` file separately first to leverage Docker's layer caching.
5. It installs all Python dependencies safely without storing cache data to save space.
6. It then copies the rest of the application code into the container.
7. It guarantees the app will run identically on Windows, Mac, or Linux systems.
8. It isolates the environment to prevent version conflicts with other local software.
9. It eliminates the "it works on my machine" problem for developers.
10. By default, it runs `inference.py` when the container starts.

### `requirements.txt`
1. This standard text file tracks every single Python package required to run the project.
2. It includes `pandas`, which is the engine of the entire application for data processing.
3. It requires `pydantic` to securely validate the LLM's JSON formatting.
4. It includes `streamlit` to power the interactive web frontend dashboard.
5. It utilizes `openai` and `groq` to communicate with the language model API.
6. It ensures `python-dotenv` is installed to parse local secret keys.
7. It uses `numpy` as a backend mathematics dependency required by pandas.
8. It allows simple one-command installation of the entire project structure.
9. It tells hosting platforms exactly what to download before running the app.
10. It freezes dependencies making sure future updates won't arbitrarily break the app.

### `env/actions.py`
1. This file defines the exact actions the LLM is legally allowed to take.
2. It relies on the Pydantic library to easily enforce strict data validation.
3. It outlines the `Action` class, acting as the primary contract for the LLM.
4. It enforces `action_type` to be a string representing what Pandas fix to apply.
5. It includes an optional `column` field, letting the agent specify the target column.
6. It includes an optional `value` field, letting the agent specify what to impute or drop.
7. It defines the allowed action types clearly, such as `stop_cleaning` and `convert_date`.
8. It provides a robust safety net—if the LLM hallucinates an action, Pydantic catches the error.
9. This structural check prevents `environment.py` from crashing due to bad string values.
10. It fundamentally bridges raw LLM text generation to executable Python commands.

### `env/environment.py`
1. This script is the heartbeat of our Reinforcement Learning setup.
2. It defines the `DataCleaningEnv` class which holds the current Pandas dataframe in memory.
3. The `reset()` function safely loads the messy dataset and sets the step counter to zero.
4. The `step()` function executes the action the LLM chose on the actual dataframe.
5. It cleanly handles dropping duplicate rows and missing values using native Pandas.
6. It prevents illogical moves, like trying to fill missing values inside a date column.
7. It avoids endless looping by enforcing a maximum step count (default 10 steps).
8. It calls `_compute_reward()` after every action to assess the dataset's cleanliness.
9. It returns execution errors back to the LLM so it can learn from its mistakes and pivot.
10. It outputs the new Observation state, the numerical reward, and whether the task is finished.

### `env/grader.py`
1. This file is strictly responsible for grading how well the agent performed its task.
2. It takes the agent's final cleaned DataFrame and compares it to the "expected" DataFrame.
3. It immediately handles edge cases, scoring a 0.0 if either dataset was wiped out completely.
4. To prevent ordering bugs, it automatically sorts both datasets before doing any cell comparisons.
5. It checks cell-by-cell to see if the AI matched exactly what the golden standard dataset has.
6. It elegantly handles missing values (`NaN`) by treating them as matches if they exist in both.
7. It calculates a final score by dividing perfect matched cells by total expected cells.
8. It returns a straightforward fraction (like 0.95 for a 95% match) back to the evaluation script.
9. It keeps the evaluation purely objective, ensuring no subjective bias in scoring the benchmark.
10. It is heavily utilized by `evaluate.py` to print final accuracy metrics for each difficulty level.

### `env/observation.py`
1. This script defines what the LLM "sees" at the start of every step.
2. It uses Pydantic to ensure the environment's observation payload always stays perfectly formatted.
3. It bundles a small 5-row preview of the dataframe, converted into a list of dictionaries.
4. It dynamically calculates and stores exactly how many missing values currently remain in the data.
5. It tracks how many duplicated rows are present so the agent prioritizes fixing them.
6. It lists the schema (column names and their data types) so the agent knows strings from numbers.
7. It includes the `steps_taken` counter so the agent knows how close to the step limit it is.
8. This model ensures the LLM's prompt stays small and lightweight instead of feeding it huge files.
9. It acts as the literal "eyes" of the agent, delivering the exact context needed.
10. It cleanly standardizes how state data is sent to the LLM across any uploaded dataset.

### `env/tasks.py`
1. This is a lightweight configuration catalog used by the benchmark framework.
2. It simply returns a Python dictionary mapping the different testing difficulty levels.
3. It describes the "easy" task as solely removing duplicate rows from the dataset.
4. It maps the "medium" task to handling missing data points and basic formatting issues.
5. It scales up to the "hard" task, which represents a complete, messy ETL data pipeline.
6. It formally dictates the "eval_metrics" (like Accuracy) so the runner knows how to grade it.
7. It acts as a central location to add completely new tasks (e.g., "expert") in the future.
8. It keeps these literal string descriptions neatly organized outside of the main loop logic.
9. It allows automated runner scripts to easily iterate through task difficulties.
10. It is a cleanly written dictionary index ensuring strong software architecture.

### `data/` *(Directory containing CSV Files)*
1. This folder simply acts as the static storage for all of our evaluation test cases.
2. It cleanly separates the messy, real-world data from the application code.
3. The `raw_...csv` files represent dirty inputs full of errors, duplicates, and nulls.
4. The `expected_...csv` files represent the mathematically perfect, fully cleaned output versions.
5. The "easy" dataset checks if the model can easily handle duplicated lines.
6. The "medium" dataset introduces harder null value replacements and inconsistencies.
7. The "hard" dataset requires the agent to blend dropping, formatting, and filling data.
8. This clear separation allows users to safely tweak the CSV data without touching Python logic.
9. It provides the literal ground truth utilized by `grader.py` to calculate accuracy.
10. It guarantees that anyone who clones the repository can instantly run the evaluation benchmarks.

## 🎖️ About Rewards, Evaluations, and Graders
The OpenEnv simulation dynamically scores the agent without human intervention:
- **Grader (`grader.py`)**: Compares the AI's final dataset row-by-row and column-by-column against a golden-standard `expected` CSV. It outputs an exact percentage match, serving as the benchmark's true accuracy score.
- **Reward Algorithm**: As the agent cleans data, the environment's `step()` function gives the agent an immediate fractional score between 0.0 and 1.0. This score favors reducing duplicate rows and minimizing nulls, acting as "breadcrumbs" letting the AI know if it's doing a good job.
- **Evaluation Loop (`evaluate.py`)**: A purely automated testing script that runs the agent across easy, medium, and hard tasks, comparing outputs to expected datasets and printing out final percentage grades for developers.

## 👤 Developed By
Developed to automate away the most tedious parts of tabular data work, letting engineers focus on analysis rather than repetitive, rigid cleaning scripts. Built natively on top of the generic OpenEnv reinforcement learning framework.

## 📜 MIT License
Copyright (c) 2026

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
