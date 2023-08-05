# wt-mgr
Webex Teams manager

## Description
Webex Teams manager (`wt-mgr`) helps with setting up or migrating Teams, Rooms and account Memberships on Cisco Webex Teams.  
It allows to import Teams, Rooms and Membership information from CSV files.  
It has been developed to quickly set up Webex Teams orgs for multiple schools, in the context of the COVID-19, in order to allow students to attend classes remotely, but it's useful in all cases where there's the need to quickly create multiple similar organizations.


## Installation
Tested with Python 3.7+.  
It's recommended to install the package in a virtual environment.

* Easiest way:  
  `pip install wt-mgr`
* Download the `tar.gz` package and install using `pip`:  
  `pip install wt-mgr-<version>.tar.gz`
* Clone the git repo and run the `setup.py`:  
  `python setup.py install`

## Usage
* Obtain a Webex Teams API token and set the `WEBEX_TEAMS_ACCESS_TOKEN` environment variable using the token value:  
  `export WEBEX_TEAMS_ACCESS_TOKEN=XXXXXXXXXXX`

  See https://webexteamssdk.readthedocs.io/en/latest/user/quickstart.html#get-your-webex-teams-access-token for more details about how to get and use the access token.

* Initialize a working directory as follows:  
  `wt-mgr -wd <work_dir-path> --init`

  This creates the directory and it populates it with the required CSV config files:  
  ```
  % wt-mgr -wd ~/scripts/wteams/test_org/ --init
  2020-03-08 01:01:55,307 - wt_mgr.wt_mgr - INFO - Initializing WT API
  2020-03-08 01:01:56,443 - wt_mgr.wt_mgr - INFO - Initializing work dir: /Users/flovison/scripts/wteams/test_org/
  2020-03-08 01:01:56,443 - wt_mgr.wt_mgr - INFO - Creating file: /Users/flovison/scripts/wteams/test_org/teams.csv
  2020-03-08 01:01:56,444 - wt_mgr.wt_mgr - INFO - Creating file: /Users/flovison/scripts/wteams/test_org/rooms.csv
  2020-03-08 01:01:56,445 - wt_mgr.wt_mgr - INFO - Creating file: /Users/flovison/scripts/wteams/test_org/teams_users.csv
  ``` 

* Full help with `wt-mgr --help`:  
    ```
    % wt-mgr --help                          
    2020-03-08 00:40:37,281 - wt_mgr.wt_mgr - INFO - Initializing WT API
    usage: wt-mgr [-h] -wd WORK_DIR [--init] [-tf TEAMS_FILE] [-rf ROOMS_FILE] [-tu TEAMS_USERS_FILE] [-tc] [-td] [-rc] [-rd] [-ua] [-ur] [-ea] [-er] [-ts] [-rs] [-us] [-gm] [-dm] [-du] [-sa] [-ia] [-ii] [-oi] [-sd]
                  [-ic] [-fa] [--team-filter TEAM_FILTER] [--room-filter ROOM_FILTER] [--mail-filter MAIL_FILTER]

    optional arguments:
      -h, --help            show this help message and exit
      -wd WORK_DIR, --work-dir WORK_DIR
                            Set work directory
      --init                Initialize work directory with CSV templates
      -tf TEAMS_FILE, --teams-file TEAMS_FILE
                            Override the path or name of the Teams definition CSV file
      -rf ROOMS_FILE, --rooms-file ROOMS_FILE
                            Override the path or name of the Rooms definition CSV file
      -tu TEAMS_USERS_FILE, --teams-users-file TEAMS_USERS_FILE
                            Override the path or name of the Teams Users definition CSV file
      -tc, --create-teams   Create Teams as defined on CSV file
      -td, --delete-teams   Delete Teams as defined on CSV file
      -rc, --create-rooms   Create Rooms as defined on CSV file
      -rd, --delete-rooms   Delete Rooms as defined on CSV file
      -ua, --assign-users   Assign users to teams as defined on CSV file
      -ur, --remove-users   Remove users from teams as defined on CSV file
      -ea, --add-eurl       Add the EURL bot to the Teams rooms
      -er, --remove-eurl    Add the EURL bot to the Teams rooms
      -ts, --show-teams     Show Teams
      -rs, --show-rooms     Show Rooms
      -us, --show-users     Show Users
      -gm, --get-members
      -dm, --dump-members
      -du, --dump-urls
      -sa, --show-all
      -ia, --include-active
      -ii, --include-inactive
      -oi, --only-inactive
      -sd, --skip-dump      If selected, CSV files are NOT updated with live data.
      -ic, --import-current
                            Import existing teams/spaces/users from the WT account in use.
      -fa, --force-active   Used to mark existing teams/spaces to be imported in active state.
      --team-filter TEAM_FILTER
      --room-filter ROOM_FILTER
      --mail-filter MAIL_FILTER
    ```

## Config files
### Teams
* Add one row for each Team in the `teams.csv` file, setting the team name on the `team_name` column.  
* Also set the `is_active` status to `True` for the "active" teams.  

The tool by default only processes entries tagged as `is_active`, although this behavior can be overridden with the following CLI options:  
```
    -ii, --include-inactive
    -oi, --only-inactive
```

The `team_id` field is automatically updated upon the first successful connection.  

#### Create Teams
Use the `-tc` or `--create-teams` CLI option, e.g.:  
`wt-mgr -wd <work_dir_path> -tc`

#### Delete Teams
Use the `-td` or `--delete-teams` CLI option, e.g.:  
`wt-mgr -wd <work_dir_path> -td`  
__Note__ : by default the tool processes entries with `is_active` is set to `True`.  
If you want to delete only inactive teams, add the `--only-inactive` CLI option.  
If you want to delete all teams, add the `--include-inactive` CLI option. 

#### Show Teams
Use the `-ts` or `--show-teams` CLI option, e.g.:  
`wt-mgr -wd <work_dir_path> -ts`  
__Note__ : by default the tool processes entries with `is_active` is set to `True`.  
If you want to show only inactive teams, add the `--only-inactive` CLI option.  
If you want to show all teams, add the `--include-inactive` CLI option. 

### Rooms
* Add one row for each Room (also called "Space") in the `rooms.csv` file.  
* Specify the Room name(s) on the `room_name` column; if this field is left blank, it assumes this is the `General` room.  
* For each room specify the Team it belongs to using the `team_name` column; if this field is left blank, it will expand to **all** the configured teams in the `teams.csv` file.  
It's possible to specify multiple Teams in a comma-separated value, e.g.:  `Team1,Team2`.  This will be automatically expanded upon processing.
* Specify `True` under the `is_active` field to mark the active rooms.

#### Create Rooms
Use the `-rc` or `--create-rooms` CLI option, e.g.:  
`wt-mgr -wd <work_dir_path> -rc`

#### Delete Rooms
Use the `-rd` or `--delete-rooms` CLI option, e.g.:  
`wt-mgr -wd <work_dir_path> -rd`  
__Note__ : by default the tool processes entries with `is_active` is set to `True`.  
If you want to delete only inactive rooms, add the `--only-inactive` CLI option.  
If you want to delete all rooms, add the `--include-inactive` CLI option. 

#### Show Rooms
Use the `-rs` or `--show-rooms` CLI option, e.g.:  
`wt-mgr -wd <work_dir_path> -rs`  
__Note__ : by default the tool processes entries with `is_active` is set to `True`.  
If you want to show only inactive rooms, add the `--only-inactive` CLI option.  
If you want to show all rooms, add the `--include-inactive` CLI option. 

### Teams users
* Specify the following fields in order to be able to map the users to the Teams:  
  * `member_mail`: e-mail address of the user
  * `member_name` (optional): name of the user
  * `team_name`: Team a given user should be member of
  * `is_active`: set to `True` to activate a user

Using the `--dump-members` option will scan existing users on the configured teams and it will update the CSV file.

### Import existing teams/rooms/members from WT account
In order to dump all the Teams, Rooms and Members from the WT account in use (identified by the token in use), please proceed as follows:  
* Initialize a new "org" work directory:  
  `wt-mgr -wd <path/to/my-new-org> --init`
* Import data:  
  `wt-mgr -wd <path/to/my-new-org> --import-current --include-inactive`  
  The `--include-inactive` options is needed as imported entries are considered disabled by deafult.  
* To import existing entities and mark them as active, use the `--force-active` option:  
  `wt-mgr -wd <path/to/my-new-org> --import-current --force-active`

Once done, validate the CSV files in the work directory before using this data for additional operations or to import this to a different org.  

### Eurl Bot
#### Add the Eurl bot
Use the `-ea` or `--add-eurl` CLI option to add the bot to all active Teams.  
__Note__: by default the tool adds the EURL bot only to the `General` room of each team.  
Make sure you have an entry in the `rooms.csv` file with an empty `room_name` for this to work.  
To cover all `General` rooms in one go, add a row to the `rooms.csv` file with just `is_active` set to `True` as in this case, the empty `team_name` will be automatically expanded to all configured and active Teams, whereas the empty `room_name` will be interpreted as the default/`General` room.

Adding the EURL bot also configures the room as follows:
* `list off`: to remove the room from the EURL directory
* `internal off`: to allow anyone to join this room using the URL

#### Dump the room-to-URL mapping
Use the `-du` or `--dump-urls` CLI option to dump a table with the `room_name` and the `room_url` .
