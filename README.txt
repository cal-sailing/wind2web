==================================================================================================================
This document contains a description as well as the install instructions for the CSC wind data web posting system.
This system gets wind data from a csc machine running weewx and pushes the data to Appspot
Once the data is pushed, Jorrit Poelen has something in place to display it on the ppspot page. 

last updated: 08-29-2020
info: cyril: cyrilbiz@gmail.com
=================================================================================================================


The system is built ontop of weewx. Weewx must already be installed and working, acquiring data from the Vantage box located inside the clubhouse.

The following system gets the data from weewx and sends it to be posted on csc website via Appspot.

---------------------
SYSTEM DESCRIPTION
---------------------
The system works as follows:

1. Weewx produces one data frame  (containing wind speed, direction and many other informations at the current time)
A weewx extension (plugin) called csv then writes that data frame to a csv file located at:

  /home/admin/wind2web/data/cscVantageLoop.csv	  

2. Then every second, the python script /home/admin/wind2web/wind2appspot.py is launched by a cron job.
That script takes the cscVantageLoop.csv as input, extracts the relevant infos from it and produces the /home/admin/wind2web/data/cscWind.txt

3. Then a cron job calls the script /home/admin/wind2web/pushWind2Appspot.sh which uploads the file cscWind.txt to appspot.
Jorrit Poelen the the ctual displaying of the data on the appspot page.

-------------------
HOW TO INSTALL
-------------------
You must be logged in as the use "admin"
Your home directory must be /home/admin

1. Download the folder wind2web (this repository) to /home/admin

note: If you do not have a /home/admin directory or if you need to install the system in a different directory then you will have to manually change the path names accordingly in the following files ( because these paths are hardcoded for now):

- wind2web/csv/install.py (change this BEFORE installing the csv extension to weewx)
- wind2web/wind2appspot.py
- wind2web/pushwind2appspot.sh
and 
you need to modify these paths in the crontab (step 3) as well

2. Install the csv weewx extension:
cd /home/admin
sudo wee_extension --install=csv

then stop and restart weewx:

sudo /etc/init.d/weewx stop
sudo /etc/init.d/weewx restart

in the terminal wee_extension --list should now return:
Extension Name    Version   Description
csv               0.10      Emit loop or archive data in CSV format.

note: I modified the file csv/install.py from the original. Therefore do NOT use the original csv code (https://github.com/weewx/weewx/wiki/csv). This is because despite what their documentation says I could not configure weewx.conf to tell the original csv code where to output the data (/home/admin/wind2web/data/cscVantageLoop.csv). Therefore I modified install.py and hardcoded the path there. 

before continuing: now check that the file /home/admin/wind2web/data/cscVantageLoop.csv contains wind data updated every seconds or so.

3. add the following two cron jobs (as admin):

* * * * * /home/admin/wind2web/wind2appspot.py
* * * * * ( sleep 5; /home/admin/wind2web/pushWind2appspot.sh )
