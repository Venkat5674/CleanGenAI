import pandas as pd
from env.observation import Observation
from env.actions import Action
from typing import Tuple, Dict, Any


class DataCleaningEnv:
    def __init__(self, task: str = "easy", df: pd.DataFrame = None):
        self.task = task
        self.initial_df = df
        self.df = pd.DataFrame()
        self.steps = 0
        self.max_steps = 10

    async def reset(self) -> Observation:
        if self.initial_df is not None:
            self.df = self.initial_df.copy()
        else:
            self.df = pd.read_csv(f"data/raw_{self.task}.csv")
        self.steps = 0
        return self.state()

    async def step(
        self, action: Action
    ) -> Tuple[Observation, float, bool, Dict[str, Any]]:
        self.steps += 1
        reward = 0.0
        error = None

        try:
            # Force df copy to avoid SettingWithCopyWarning
            self.df = self.df.copy()
            if action.action_type == "remove_duplicates":
                self.df = self.df.drop_duplicates()
            elif action.action_type == "fill_nulls" and action.column:
                if "date" in action.column.lower():
                    error = "Cannot fill nulls in date column. Try stop_cleaning."
                else:
                    self.df.loc[:, action.column] = self.df[action.column].fillna(action.value)
            elif action.action_type == "convert_date" and action.column:
                self.df.loc[:, action.column] = pd.to_datetime(
                    self.df[action.column], format="mixed", errors="coerce"
                ).dt.strftime("%Y-%m-%d")
            elif action.action_type == "drop_column" and action.column:
                self.df = self.df.drop(columns=[action.column])
            elif action.action_type == "drop_row":
                if action.column is not None and action.value is not None:
                    # Drop rows where a specific column equals a specific value
                    self.df = self.df[self.df[action.column] != action.value]
                else:
                    # Just drop rows containing nulls globally if no column/value given
                    self.df = self.df.dropna()
            elif action.action_type == "stop_cleaning":
                pass # Nothing to mutate, just let "done" logic handle it below
            else:
                error = "Invalid action parameters"
        except Exception as e:
            error = str(e)

        reward = self._compute_reward()
        done = self.steps >= self.max_steps or reward >= 0.99 or action.action_type == "stop_cleaning"

        return self.state(), reward, done, {"error": error} if error else {}

    def state(self) -> Observation:
        if self.df is None or self.df.empty:
            return Observation(
                table_preview=[],
                num_missing=0,
                num_duplicates=0,
                data_schema={},
                steps_taken=self.steps,
            )
        return Observation(
            table_preview=self.df.head().to_dict(orient="records"),
            num_missing=int(self.df.isnull().sum().sum()),
            num_duplicates=int(self.df.duplicated().sum()),
            data_schema={col: str(dtype) for col, dtype in self.df.dtypes.items()},
            steps_taken=self.steps,
        )

    def _compute_reward(self) -> float:
        if self.df is None or self.df.empty:
            return 0.001
        total_cells = max(1, len(self.df) * len(self.df.columns))
        missing_score = 1 - (self.df.isnull().sum().sum() / total_cells)
        duplicate_score = 1 - (self.df.duplicated().sum() / max(1, len(self.df)))
        return float(max(0.001, min(0.999, 0.5 * missing_score + 0.5 * duplicate_score)))


