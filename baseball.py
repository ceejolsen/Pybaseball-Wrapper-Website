# -*- coding: utf-8 -*-
"""
Created on Fri May 16 00:05:19 2025

@author: cjols
"""

from flask import Flask, render_template, request, redirect, url_for
from pybaseball import cache
import datetime
import pandas as pd

import pyball_fxns as pybf

app = Flask(__name__)

# enable pybaseball cache, not sure if this is bad form?
cache.enable()

GLOBAL_YEAR = datetime.datetime.now().year


#decorator for home page
@app.route('/', methods=['GET', 'POST'])
def home():
    year_to_fetch = GLOBAL_YEAR
    players_data = []
    
    min_pa_val = None
    if request.method == 'POST':
        min_pa_form = request.form.get('min_pa')
        if min_pa_form:
            if min_pa_form.isdigit():
                min_pa_val = int(min_pa_form)
            else:
                min_pa_val = None
        else:
            min_pa_val = None
    players_data = pybf.get_all_players_data(year_to_fetch, min_pa_val)
    while len(players_data) == 0 and year_to_fetch > 2024:
        year_to_fetch -= 1
        players_data = pybf.get_all_players_data(year_to_fetch, min_pa_val)

    return render_template('default.html', players=players_data, year=year_to_fetch, current_min_pa=min_pa_val)


#decorator for info_display
@app.route('/player_info', methods=['POST'])
def player_info():
    selected_player_idfg = request.form.get('player_idfg')
    current_year = GLOBAL_YEAR

    if not selected_player_idfg:
        return render_template('info_display.html', error_message="No player selected.", team_colors=pybf.mlb_colors)

    player_details = None
    year_of_data_found = str(current_year)
    
    temp_year = current_year
    # written 6-4-25, there is a full season of data in 2024
    while temp_year >= 2024:
        player_details = pybf.get_player_details(selected_player_idfg, temp_year)
        if player_details:
            year_of_data_found = str(temp_year)
            break
        temp_year -= 1

    if player_details:
        show_advanced = 'show_advanced_stats' in request.form
        show_detailed = 'show_detailed_stats' in request.form
        
        display_cols = pybf.required_cols.copy()
        
        if show_detailed:
            display_cols.extend(pybf.addl_cols)
        
        if show_advanced:
            display_cols.extend(pybf.advanced_cols)

        display_details = {
            'Name': player_details.get('Name'),
            'player_image_url': player_details.get('player_image_url'),
            'Season': player_details.get('Season', year_of_data_found)
        }

        for col in display_cols:
            if col in player_details and col not in ['Name', 'IDfg']:
                display_details[col] = player_details[col]

        #coerce data into forms that I want it in...
        three_decimal_cols = ['AVG', 'OBP', 'SLG', 'wOBA', 'ISO', 'BABIP'] #Example: 0.250 instead of 0.25
        percentage_cols = ['BB%', 'K%'] #Example: 44% instead of 0.44

        for k, v in display_details.items():
            if k in three_decimal_cols:
                display_details[k] = f"{float(v):.3f}"
            elif k in percentage_cols:
                display_details[k] = f"{float(v) * 100:.0f}%" # convert to percentage   
        display_details["wRC+"] = int(float(display_details["wRC+"])) #manually change wRC+ to an int

        #used to fetch color scheme
        team_abbr = player_details.get('Team', 'MLB')
        team_colors_tuple = pybf.team_colors.get(team_abbr, pybf.mlb_colors) #having both gets return the same tuple is redundant but provides additional layer of protection

        return render_template('info_display.html', 
                               player=display_details,
                               team_colors=team_colors_tuple, 
                               year=year_of_data_found)
    else:
        error_msg = f"Could not find statistics for player ID {selected_player_idfg} in recent seasons. "
        return render_template('info_display.html', error_message=error_msg, team_colors=pybf.mlb_colors)

if __name__ == '__main__':
    app.run(debug=True)