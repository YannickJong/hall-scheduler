# import numpy as np
import pandas as pd

from constants import TEAM_MAP


class Hall_Scheduler:
    def __init__(self, input_dir: str):
        self.input_dir: str = input_dir
        self.hall_space: pd.DataFrame = pd.read_csv(
            f"{self.input_dir}/hall_space.csv"
        ).set_index("Day")
        self.time_slots: pd.DataFrame = pd.read_csv(
            f"{self.input_dir}/time_slots.csv"
        ).set_index("Slot")
        self.teams: pd.DataFrame = pd.read_csv(f"{self.input_dir}/teams.csv").set_index(
            "Name"
        )
        self.users: pd.DataFrame = pd.read_csv(f"{self.input_dir}/users.csv").set_index(
            "Name"
        )
        self.primordial_genome: str = self.get_primordial_genome()

    def get_primordial_genome(self) -> str:
        """Builds the primordial genome from the available hall space
        and the number of times the teams practice"""
        # Check if hall space is used efficiently
        total_hall_space: int = self.hall_space.sum().sum()
        total_n_practices: float = self.teams["N practices"].sum()
        if total_hall_space != total_n_practices:
            if total_hall_space > total_n_practices:
                print(
                    f"WARNING: Inefficient scheduling, more hall space ({total_hall_space}) than practices ({total_n_practices})"
                )
            else:
                raise ValueError(
                    f"More practices ({total_n_practices}) than hall space ({total_hall_space})!"
                )

        # Check the rotational teams
        rotational_teams: pd.DataFrame = self.teams[
            self.teams["N practices"] * 2 % 2 == 1
        ]
        rotational_teams_count: pd.Series = rotational_teams.groupby("N practices")[
            "N practices"
        ].count()
        num_rotational_slots: int = int(rotational_teams_count.sum() / 2)
        rotational_longer_teams = self.teams.loc[rotational_teams.index][
            rotational_teams["N longer"] != 0
        ]

        primordial_genome_regular: str = (
            (self.teams["N practices"].astype(int) - self.teams["N longer"].astype(int))
            * self.teams.index.map(TEAM_MAP)
        ).sum()
        primordial_genome_longer: str = (
            (
                (self.teams["N longer"].astype(int))
                * self.teams.index.map(TEAM_MAP).astype(str)
            )
            .sum()
            .lower()
        )
        primordial_genome_rotation: str = (
            num_rotational_slots - rotational_longer_teams["N longer"].sum().astype(int)
        ) * TEAM_MAP["Rot"]
        primordial_genome_rotation_longer: str = (
            rotational_longer_teams["N longer"].sum().astype(int)
            * TEAM_MAP["Rot"].lower()
        )

        primordial_genome: str = "".join(
            sorted(
                primordial_genome_regular
                + primordial_genome_longer
                + primordial_genome_rotation
                + primordial_genome_rotation_longer,
                key=lambda L: (L.lower(), L),
            )
        )
        return primordial_genome

    def genome_to_schedule(genome: str):
        pass


scheduler = Hall_Scheduler("input_files")
print(scheduler.primordial_genome)
