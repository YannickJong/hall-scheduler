import pandas as pd
from constants import TEAM_MAP

def get_mapped(team):
    return TEAM_MAP[team]


def get_primordial_genome(input_file: str) -> str:
    """Builds the primordial genome from the available hall space
      and the number of times the teams practice"""
    # Load the files/dataframes
    hall_space: pd.DataFrame = pd.read_excel(input_file, sheet_name=0).set_index("Day")
    teams: pd.DataFrame = pd.read_excel(input_file, sheet_name=2).set_index("Name")

    # Check if hall space is used efficiently
    total_hall_space: int = hall_space.sum().sum()
    total_n_practices: float = teams["N practices"].sum()
    if total_hall_space != total_n_practices:
        if total_hall_space > total_n_practices:
            print(f"WARNING: Inefficient scheduling, more hall space ({total_hall_space}) than practices ({total_n_practices})")
        else:
            raise Exception(f"More practices ({total_n_practices}) than hall space ({total_hall_space})!")

    # Check the rotational teams
    rotational_teams: pd.DataFrame = teams[teams["N practices"] * 2 % 2 == 1]
    rotational_teams_count: pd.Series = rotational_teams.groupby("N practices")["N practices"].count()
    num_rotational_slots: int = int(rotational_teams_count.sum() / 2)

    rotational_longer_teams = teams.loc[rotational_teams.index][(teams["N longer"] != 0)]
    # TODO fix the lower case letters, indicating 2 hour practices
    primordial_genome_regular: str = ((teams["N practices"].astype(int)-teams["N longer"].astype(int)) * teams.index.map(TEAM_MAP)).sum() 
    primordial_genome_longer: str = ((teams["N longer"].astype(int)) * teams.index.map(TEAM_MAP).astype(str)).sum().lower()
    primordial_genome_rotation: str = (num_rotational_slots - rotational_longer_teams["N longer"].sum().astype(int)) * TEAM_MAP["Rot"]
    primordial_genome_rotation_longer: str = rotational_longer_teams["N longer"].sum().astype(int) * TEAM_MAP["Rot"].lower()

    primordial_genome: str = "".join(sorted(primordial_genome_regular + primordial_genome_longer + primordial_genome_rotation + primordial_genome_rotation_longer, key=lambda L: (L.lower(), L)))
    print(primordial_genome)

    # Change primordial genome to account for longer practices
    teams_longer_practice: pd.DataFrame = teams[teams["N longer"] != 0]
    # print(teams_longer_practice)



def cleanup(input_file: str):
    # Load the files/dataframes
    hall_space: pd.DataFrame = pd.read_excel(input_file, sheet_name=0).set_index("Day")
    time_slots: pd.DataFrame = pd.read_excel(input_file, sheet_name=1).set_index("Slot")
    teams: pd.DataFrame = pd.read_excel(input_file, sheet_name=2).set_index("Name")
    users: pd.DataFrame = pd.read_excel(input_file, sheet_name=3).set_index("Name")



filename = "input_files/input.xlsx"
get_primordial_genome(filename)
