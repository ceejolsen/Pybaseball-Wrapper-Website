# -*- coding: utf-8 -*-
"""
Created on Fri May 16 00:05:19 2025

@author: cjols
"""
from pybaseball import batting_stats, playerid_lookup
import pandas as pd

#the info that will always display for a player
required_cols = ['Name', 'Age', 'Team', 'G', 'PA', 'AB', 'H', 'HR', 'RBI', 'SB', 'AVG', 'OBP', 'SLG', 'wOBA', 'wRC+', 'IDfg']
#will be displayed if the "Additional" checkbox is checked
addl_cols = [ 'BB%', 'K%', 'ISO', 'BABIP']
#will be displayed if the "Advanced" checkbox is checked
advanced_cols = ['BsR', 'Off', 'Def', 'WAR']

# Team colors, alphabetical in division order (AL -> NL, East -> West)
#not future or past proofed, team codes changing or adding future functionality to display more player info from
#older teams will end up with default MLB colors
team_colors = {
    "MLB": ("#002D62", "#D50032", "#FFFFFF"),

    "BAL": ("#DF4601", "#000000", "#FFFFFF"),
    "BOS": ("#0C2340", "#BD3039", "#FFFFFF"),
    "TBR": ("#00285D", "#8FBCE6", "#F5D130"),
    "TOR": ("#134A8E", "#1D2D5C", "#E8291C"),
    "NYY": ("#003087", "#C4CED3", "#FFFFFF"),

    "CHW": ("#000000", "#C4CED3", "#FFFFFF"),
    "CLE": ("#002B5C", "#E31937", "#FFFFFF"),
    "DET": ("#0C2340", "#FA4616", "#FFFFFF"),
    "KCR": ("#004687", "#BD9B60", "#74B4FA"),
    "MIN": ("#002B5C", "#D31145", "#FFFFFF"),

    #Has both OAK and ATH bc of the 2025 relocation
    "HOU": ("#002D62", "#EB6E1F", "#FFFFFF"),
    "LAA": ("#BA0021", "#003263", "#FFFFFF"),
    "OAK": ("#003831", "#EFB21E", "#a2aaad"),
    "ATH": ("#003831", "#EFB21E", "#a2aaad"),
    "SEA": ("#0C2C56", "#005C5C", "#C4CED3"),
    "TEX": ("#003278", "#C0111F", "#FFFFFF"),

    "ATL": ("#13274F", "#CE1141", "#FFFFFF"),
    "MIA": ("#00A3E0", "#000000", "#EF3340"),
    "NYM": ("#002D72", "#FF5910", "#FFFFFF"),
    "PHI": ("#E81828", "#002D72", "#FFFFFF"),
    "WSN": ("#AB0003", "#14224B", "#FFFFFF"),

    "CHC": ("#0E3386", "#CC3433", "#FFFFFF"),
    "CIN": ("#D50032", "#000000", "#FFFFFF"),
    "MIL": ("#12284B", "#FFC52F", "#1F437F"),
    "PIT": ("#FDB827", "#000000", "#FFFFFF"),
    "STL": ("#C41E3A", "#0C2340", "#FEDB00"),

    "ARI": ("#A71930", "#E3D4AD", "#000000"),
    "COL": ("#33006F", "#C4CED3", "#000000"),
    "LAD": ("#005A9C", "#FFFFFF", "#EF3E42"),
    "SDP": ("#2F241D", "#FFC425", "#FFFFFF"),
    "SFG": ("#FD5A1E", "#000000", "#EFD19F"),
}

mlb_colors = ("#002D62", "#D50032", "#FFFFFF")

#gets all players who fit criteria for dropdown menu display, using pybaseball batting_stats feature
# @input year - the year to get data for
# @input min_pa - the minimum number of plate appearances to filter the player list by, defaults to None which returns
# qualified players
# @return a dict of all players who meet the criteria of the input, sorted alphabetically
def get_all_players_data(year, min_pa=None):
    batters_df = pd.DataFrame()

    try:
        if min_pa is not None:
            batters_df = batting_stats(year, qual=min_pa)
        else:
            batters_df = batting_stats(year)
    except Exception as e:
        return []

    if batters_df.empty and min_pa is not None and min_pa > 0:
        try:
            any_players_df = batting_stats(year, qual=0)
            if not any_players_df.empty:
                return []
            else:
                return []
        except:
            return []

    if batters_df.empty:
        return []

    if 'IDfg' in batters_df.columns:
        batters_df['IDfg'] = batters_df['IDfg'].astype(str)
    else:
        return []

    available_cols = [col for col in required_cols if col in batters_df.columns]
    players_df = batters_df[available_cols].sort_values(by='Name')
    return players_df.to_dict(orient='records')

#gets data for specific player who is selected to send to info_display, including an image url
# @input player_idfg_str - a player's fangraphs id in string for
# for example: https://www.fangraphs.com/players/aaron-judge/15640/stats?position=OF
# Aaron's Judge's is 15640, as seen in the url
# @input year - the year to find data for
# @output - a dictionary created by dictionary comprehension of the inputted player with the desired stats depending on 
# the year and what checkboxes were selected
def get_player_details(player_idfg_str, year):
    try:
        all_player_stats_for_year_df = batting_stats(year, qual=0)

        if all_player_stats_for_year_df.empty:
            return None

        if 'IDfg' not in all_player_stats_for_year_df.columns or \
           'Team' not in all_player_stats_for_year_df.columns:
            return None

        all_player_stats_for_year_df['IDfg'] = all_player_stats_for_year_df['IDfg'].astype(str)
        player_season_stats_df = all_player_stats_for_year_df[all_player_stats_for_year_df['IDfg'] == player_idfg_str]

        if player_season_stats_df.empty:
            return None

        #focues on a row of player data that refers to multiple teams played on in a season, instead of ending up with only
        #a player's data on one team
        tot_row_df = player_season_stats_df[player_season_stats_df['Team'] == 'TOT']
        
        details_dict_raw = None
        if not tot_row_df.empty:
            details_dict_raw = tot_row_df.iloc[0].to_dict()
        elif not player_season_stats_df.empty:
            details_dict_raw = player_season_stats_df.iloc[0].to_dict()
        else:
            return None
        
        details_dict = {k: str(v) for k, v in details_dict_raw.items()}

        if 'Season' not in details_dict or pd.isna(details_dict.get('Season')) or details_dict.get('Season') == 'nan':
             details_dict['Season'] = str(year)
        
        # Fetch MLB ID for player image
        lookup_name = details_dict.get('Name')
        mlb_id = None
        if lookup_name:
            name_parts = lookup_name.split(' ')
            first_name = name_parts[0]
            #for players with names that are longer than just "First Last", so the first name is presumably counted as 
            # "First + Middle"
            if len(name_parts) > 2:
                first_name = first_name + name_parts[1]
            else:   
                last_name = name_parts[len(name_parts)-1]

            if last_name:
                try:
                    player_id_df = playerid_lookup(last_name, first_name)
                    if not player_id_df.empty:
                        valid_entries = player_id_df[pd.notna(player_id_df['key_mlbam'])].copy()
                        if not valid_entries.empty:
                            if 'mlb_played_last' in valid_entries.columns:
                                valid_entries['mlb_played_last'] = pd.to_numeric(valid_entries['mlb_played_last'], errors='coerce')
                                valid_entries = valid_entries.sort_values(by='mlb_played_last', ascending=False, na_position='last')
                            
                            mlb_id = valid_entries['key_mlbam'].iloc[0]
                            mlb_id = str(int(mlb_id))
                except Exception as e:
                    print("Error during playerid_lookup " + e) 
        #fetches player image from MLB API if mlb_id is valid
        if mlb_id:
            details_dict['player_image_url'] = f"https://img.mlbstatic.com/mlb-photos/image/upload/w_213,d_people:generic:headshot:silo:current.png,q_auto:best,f_auto/v1/people/{mlb_id}/headshot/67/current"
        #otherwise provides a generic image for players who don't have proper mlb ids or if something goes wrong with the call
        else:
            details_dict['player_image_url'] = "https://img.mlbstatic.com/mlb-photos/image/upload/w_213,d_people:generic:headshot:silo:current.png,q_auto:best,f_auto/v1/people/0/headshot/67/current"
        return details_dict

    except Exception as e:
        return None