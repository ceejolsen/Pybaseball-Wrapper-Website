# Pybaseball-Wrapper-Website
Pybaseball Wrapper:

This Flask web app uses the pybaseball library to look up batting statistics for MLB players. Users can filter players by a minimum number of plate appearances the current or most recent year. After selecting a player, the app displays their batting statistics depending on the relevant checkboxes selected, along with a player image and colors depending on what team or teams a player has played for in the relevant year. 

Dependencies
1. Navigate to the root directory of the project in your terminal.
2. Install the required libraries using pip or conda (or whatever preferred method:
   pip install Flask pybaseball pandas

How to run/use this
1. Save the provided file in the same directory, structured in the zip file. 
2. Open your terminal or command prompt.
3. Navigate to the directory where you saved the files, probably by using "cd {relevant directory}"
4. Run the Flask application using the command:
   python baseball.py
5. Open your web browser and go to the address displayed in the terminal, which should be http://127.0.0.1:5000/

What outputs to expect:
- Home Page (default.html):
  - A form to enter a minimum number of plate appearances to filter players.
  - A dropdown list of players matching the criteria for the current season (or previous season if the current season has no data, likely due to being run before that year's season has started).
  - Checkbox options to "Show Advanced Stats" and "Show Detailed Stats"
  - A "Filter Players" button to apply the PA filter
  - A "Get Player Info" button to view selected player's details

- Player Information Page (info_display.html):
  - The player's name and the season for which data is displayed.
  - A headshot image of the player (if available, other a default grey baseball player).
  - A table of their batting statistics, which can include different stats depending on what's chosen on the home screen.
  - Team colors are applied to the display elements based on the player's team, or generic MLB colors if there's any issues there.
  - An error message will be displayed if a player's information cannot be retrieved.
  - A button to go back to the home page.

Any setup instructions or limitations:
- The application relies on the `pybaseball` library to fetch data from Fangraphs/MLB's API. Data availability is dependent those working properly. 
- Player images are fetched from MLB's content servers using MLB IDs obtained via `playerid_lookup`. There are be instances where a player's MLB ID cannot be found or their image is not available, resulting in a generic headshot.
- Team colors are hardcoded for current MLB teams and may not be accurate for historical team affiliations or if team codes change, like Montreal Expo's "MTL" code. Having both "ATH" and "OAK" work for the A's is the only current case like this though and it has been handled. 
- The `min_pa` filter on the home page, if left blank, will fetch data for "qualified" hitters, which is 3.1 PAs per team game played.

For a brief explanation of relevant baseball terminology for this document: 
PA refers to Plate Appearances, which is the number of times a batter comes to the plate, no matter the outcomes. In order to be a qualified hitter, a player must have 3.1 PAs for every 1 game their team has played, for instance, if a team has played 100 games each qualified hitter on their team must have at least 310 PAs.
