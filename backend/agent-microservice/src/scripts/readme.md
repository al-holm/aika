### Running scripts

If you want to run the run_queries.py script, you should run it in the src directory, not the scripts directory, using the following command in a terminal "python -m scripts.run_queries"

Otherwise you may get problems like ModuleNotFoundError due to a nested directory structure.



To run tests cd to the 'src' dir and run "python -m scripts.run_test", default option - only txt report with branch coverage for each py file. You can uncomment html report creation to see more details! 