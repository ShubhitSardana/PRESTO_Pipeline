# Pulsar Search Pipeline
This is a PRESTO pipeline to detect pulsars for the Giant Meterwave Radio Telescope developed by me for pc and server use, but you too can with some tweaks...

**INTRO to Repo**

This repository contains 4 files but for your machine (be it a server or pc)
1. organize.py
2. launch.py
3. config.txt
4. main.py

**Requirements:**
PRESTO installed on your machine and all the requirements should be satisfied

**_NOTE_: This pipeline doesnot uses rfifind to subsequently mask every file but uses rficlean**

**INSTRUCTIONS**

**Step 1:** If you want to use this pipeline copy all of these files of this repository in the folder containing filterbank files (.fil), after that change the name of main_server.py, main_pc.py depending on your machine file to main.py.

**Step 2:** Go through the code in main.py... It is very easy to understand, you might be required to change some of the things as I have made this for my pc and the server I use (the server that I use doesnot have TEMPO installed on it so to not cause any problems because of that I tweaked the code to not include barycenter, If you have the same situation you can also use it without much tweaking), make the required changes and you are done with all the tweakings needed. 

**Step 3:** Now run organize.py first. It executes quickly as it only organizes the files into subdirectories. After this you get a window to change the config.txt file present in each of the subdirectories (its is not a problem if you leave it as it is).

**Step 4:** After that execute launch.py file and it will sequentially execute main.py file in each of the subdiectories

Leave it and come after a week or so (depending upon your data maybe less maybe more). _**And you are done!!!**_


_**Feel free to share your suggestions and ask any questions. :)**_
