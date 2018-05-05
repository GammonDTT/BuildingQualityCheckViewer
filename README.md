# BuildingQualityCheckViewer
(Recommends Python version 3.5 or later)

## Install relevant Python modules
    pip3 install python-telegram-bot

## Add the required files to the directory
- _parameters.txt_ which contains the telegram bot token
- Tableau image printouts should be named in the following format: TEAM_TOWER#_FLOOR##_FLAT#.jpg, where
  - TEAM: **Internal**, **SPU** or **"External**
  - Tower: **Tower** and a **one digit number** with no space in between
  - Floor: **Floor** and  **two digit number** with no space in between
  - Flat: **Flat** with a **single capital letter** flat number with no space in between
  - Each part is separated by a single underscore **_**
  - e.g. **Internal_Tower1_Floor01_FlatA.jpg**
