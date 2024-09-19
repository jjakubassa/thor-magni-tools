import os
import logging
from typing import Dict
import pandas as pd

from thor_magni_tools.io import create_dir
from thor_magni_tools.data_tests.logger import CustomFormatter


LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
ch.setFormatter(CustomFormatter())
LOGGER.addHandler(ch)


class ActivitiesMerger:
    def __init__(self, activities_path: str, csv_path: str, out_dir: str) -> None:
        self.activities_df = pd.read_csv(activities_path, index_col=0)
        self.csv_path = csv_path
        self.out_dir = out_dir

    def merge_activities_trajectories(
        self,
        humans_trajectories_df: pd.DataFrame,
        file_activities: pd.DataFrame,
    ) -> pd.DataFrame:
        act_trajs_dfs = []
        activities_helmets = file_activities["ag_id"].unique()
        for helmet_id in activities_helmets:
            helmet_trajs_df = humans_trajectories_df[
                humans_trajectories_df["ag_id"] == helmet_id
            ]
            helmet_act_df = file_activities[file_activities.ag_id == helmet_id]
            merged_df = pd.merge_asof(
                helmet_trajs_df.sort_values("frame_id"),
                helmet_act_df[["file_name", "qtm_frame_act", "activity"]].sort_values(
                    "qtm_frame_act"
                ),
                left_on="frame_id",
                right_on="qtm_frame_act",
                direction="nearest",
                # tolerance=None,
            )
            act_trajs_dfs.append(merged_df)
        activities_trajs_merged = (
            pd.concat(act_trajs_dfs).set_index("Time").sort_index()
        )
        return activities_trajs_merged

    def run(self) -> Dict:
        split_path = self.csv_path.split("/")
        scenario_id, file_name = split_path[-2], split_path[-1]
        activities_df_fn = self.activities_df.groupby("file_name")
        if file_name not in activities_df_fn.groups.keys():
            return
        file_activities = activities_df_fn.get_group(file_name)
        if len(file_activities["ag_id"].unique()) == 0:
            return
        trajectories_df = pd.read_csv(self.csv_path)
        humans_trajectories_df = trajectories_df[
                    trajectories_df.ag_id.str.startswith("Helmet")
                ]
        activities_trajs_merged = self.merge_activities_trajectories(
            humans_trajectories_df=humans_trajectories_df,
            file_activities=file_activities,
        )
        create_dir(os.path.join(self.out_dir, scenario_id))
        activities_trajs_merged.to_csv(os.path.join(self.out_dir, scenario_id, file_name))
        LOGGER.info("%s merged and saved!", file_name)
