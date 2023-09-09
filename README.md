# PRESTO_Pipeline
This is a PRESTO pipeline for the Giant Meterwave Radio Telescope to detect pulsars developed by me for pc and server use

**INTRO to Repo**

This repository contains 5 files but for your machine (be it a server or pc) you will be requiring only 4
1. organize.py
2. launch.py
3. config.txt
4. main.py (personal_computer/server)

**INSTRUCTIONS**

**Step 1:** Now if you want to use this pipeline fork this rep[o and copy all of these files in the folder containing filterbank files (.fil), after that change the name of main_server.py, main_pc.py file to main.py.

**Step 2:** Now run organize.py first. It executes quickly as it only organizes the files into subdirectories. After this you get a window to change the config.txt file present in each of the subdirectories (its is not a problem if you leave it as it is).

**Step 3:** After that execute launch.py file and it will sequentially execute main.py file in each of the subdiectories

Leave it and come after a week or so (depending upon your data maybe less maybe more). _**And you are done!!!**_
