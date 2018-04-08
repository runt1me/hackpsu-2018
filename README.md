# Deconstructing the Facebook data disaster

We made a tool to help you understand the breadth of data Facebook collects and stores on its users. Check it out!

## How it Works

In the wake of recent news of data leakage on Facebook, a tool was created to allow you to download a dataset containing
personal profile information stored by Facebook. Our tool parses some of this dataset and performs certain analytics to help
the user make sense of the vast swaths of data.

**To download the data:**

From your news feed, click on settings under the top-right corner drop-down:
![Picture of the drop-down](https://github.com/runt1me/hackpsu-2018/raw/master/pics/fb_data_one.png "Step One")

Click the hyperlink that reads "Download a copy of my Facebook data".
![The hyperlink](https://github.com/runt1me/hackpsu-2018/raw/master/pics/fb_data_two.png "Step Two")

Unzip the downloaded file. 

**To use our tool**:
Be sure that the unzipped directory containing your Facebook data is in the same directory as the python source file `fb.py`.
Run the following command in a command window or terminal:

```bash
$ python fb.py --dir <facebook_data_dir_name>
```

When the script finishes running, several CSV files will be placed in your current directory.
These files can easily be ingested into Splunk using the provided XML, creating a dashboard with nicely organized metrics:

## Our analytics

Facebook keeps a record of every IP address that has been associated with your account. We geolocated these and placed them on a map,
giving a fairly accurate picture of where the user has lived and travelled:

![A map of where you have been](https://github.com/runt1me/hackpsu-2018/raw/master/pics/Facebook_Data_Map.png "Your IP addresses on a map")

Using information from the user-agent string of the connecting web browser, we are able to determine with high confidence the
type of device used to connect to Facebook. If compromised, this information could be leveraged to launch tailored attacks or
ad campaigns based on the types of devices that a user has:

![Primary device and friend info](https://github.com/runt1me/hackpsu-2018/raw/master/pics/Facebook_Data_Data.png "OS, friend info")

Facebook keeps a log of every friend you have, every friend you have removed, every friend request you have blocked,
and outstanding friend requests that have not been accepted or rejected. Aggregating this data has the capacity to reveal major life
events, such as an uptick in new friends when the user moves, starts college, or joins a new social community:

![Friend Graph](https://github.com/runt1me/hackpsu-2018/raw/master/pics/Facebook_Data_Metrics.png "friend info")

*The spikes in the graph tend to correspond to major life events.*

[See this guide for help installing Splunk.](http://docs.splunk.com/Documentation/Splunk/7.0.3/Installation/InstallonLinux)

## Challenges & Limitations

+ Facebook delivers the data as a `.htm` file. As a result, parsing the data into an ingestable format is an involved task. Sometimes, parsing logic is reusable; sometimes it isn't. A small change to the `.htm` file could result in a substantial amount of code changes required to parse the data.
+ Splunk has an ingest limit of 500 Mb/day for free accounts, so we were limited in the amount of data that we could analyze in our 24-hour timeframe.
+ Since we only used our own Facebook data, and we are similar in many demographics (age, gender, vocation..), we ended up analyzing a fairly homogenous dataset.
+ Our Splunk instance is managed on one of our own laptops, so processing power for advanced data analytics is limited.
+ Due to the serious privacy concerns associated with this data, we limited the ability to drilldown with certain features (location, friends' names)

## Future Directions

+ We made the parsing code modular, so new users can quickly use our tool by simply downloading their data directory and receive the appropriate output CSV files.
+ More complex mathematical operations could provide further insights on time-series data (clustering, classification, etc.)
+ Analyzing more sections of Facebook data would involve writing parsing logic for the appropriate `.htm` files and creating new Splunk rules to manage the ingest of the appropriate parsed `.csv` files.
