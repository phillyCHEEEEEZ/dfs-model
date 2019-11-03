timeout 5
python "c:\dev\Python\Repos\dfs-model\nba\scripts\python\archive\scrape actuals.py"
timeout 5
python "c:\dev\Python\Repos\dfs-model\nba\scripts\python\archive\append data to master aggregate.py"
timeout 5
exit