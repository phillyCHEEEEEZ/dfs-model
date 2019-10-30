timeout 5
CALL "c:\dev\Python\Repos\dfs-model\nba\scripts\batch\02 - Scrape Projections.bat"
timeout 5
CALL "c:\dev\Python\Repos\dfs-model\nba\scripts\batch\03 - Prep Data for Analysis.bat"
REM timeout 5
REM CALL "c:\dev\Python\Repos\dfs-model\nba\scripts\batch\04 - Predictive Models.bat"
timeout 5
CALL "c:\dev\Python\Repos\dfs-model\nba\scripts\batch\05 - Upload Projections to FC.bat"
timeout 5
CALL "c:\dev\Python\Repos\dfs-model\nba\scripts\batch\06 - Archive and Append Dates.bat"
timeout 5
exit

