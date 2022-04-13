## Script for Checking WiFi Connectivity

This script is built to check whether devices are connected to a WiFi or not. Depending on the connectivity state, appropriate Device Tags will be added.

### Prerequisites

**config.properties** needs to be updated to provide the following information:

```
[seetest_authorization]
access_key=<insert access key>

[seetest_urls]
cloud_url=https://uscloud.experitest.com # replace with your Cloud URL
```

### Flow

This is the flow of the script and what it does when triggered:

- Get list of all devices from a SeeTest Cloud
- Get state of devices
  - If device is offline - Write it into a .txt file in root project folder
  - If device is in use - Write it into a .txt file in root project folder
  - If device is in error - Write it into a .txt file in root project folder
  - If device is online - Run HTTP Request to ping against a website and write it into a .txt file in root project folder
    - If Ping is successful, all good
    - if Ping is not successful, parse the error message
      - If the error message contains "No Internet", add relevant tag to device
  - If device is in any other state - Write it into a .txt file in root project folder

### How to set up environment

Open a Terminal window in the project root folder, and type in the following commands:

```commandline
python3 -m pip install --user virtualenv
python3 -m venv env
source env/bin/activate
pip3 install -r requirements.txt
```

Above steps creates a local virtual environment where Python3, Pip3 and all relevant dependencies reside. 

To run the script, running the following command:

```commandline
./env/bin/python3 main.py
```

As long as the **./env** folder exist, for each execution we can simply run above command, no need to re-run all the commands each time.

### Running the script periodically

Let's look at how we can use Mac's in built Cron Job mechanism using **crontab**.

1. Create a **script.sh** file with the following content:

```commandline
./env/bin/python3 main.py
```

And store the file in the root location of the project.

2. Open a Terminal window in the root project directory
3. Type in the following command which will open up an Editor for configuring Cron Jobs:

```commandline
env EDITOR=nano crontab -e
```

4. Provide the following content in the Editor:

```commandline
*/30 * * * * cd ~/PycharmProjects/CT-Check-Devices-WiFi-State-Periodically && ./script.sh
```

How often you want to run the Cron Job can be modified. Above script runs it every 30 minutes. To find out more, see here:
https://crontab.guru/

5. Save and Exit out of the Editor with Control + X, followed by Y (yes), and then Enter.

You can also view active cron jobs by typing in the following command in the Terminal:

```commandline
crontab -l
```
