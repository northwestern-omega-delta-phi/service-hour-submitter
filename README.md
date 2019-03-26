# service-hour-submitter
This is a script to automatically submit service hours from the midwest template for service hours as a google sheet spreadsheet to myodphi. Alpha Alpha finds it easier to keep track of service in a spreadsheet, so this script was written so we don't have to manually transfer the hours over to the site at the end of each quarter. This script may not work with newer iterations of the site. The last time this script was tested was in March of 2019.

### Requirements
Install Python 3
[Download for Mac](https://docs.python-guide.org/starting/install3/osx/#install3-osx)
[Download for Windows](https://docs.python-guide.org/starting/install3/win/#install3-windows)
[Download for Linux](https://docs.python-guide.org/starting/install3/linux/#install3-linux)

Once installed, clone or download this project, then navigate to where you cloned/downloaded the project and run the following commands:

```
pip3 install requests bs4 json
pip3 install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
```

Everything that is showing up in the command line is telling you that it is downloading and installing python modules. It is not breaking your computer : )


### Usage
In `config.json`, enter all of the following information:
- **username** used for myodphi (i.e. "odphi_username": "rojaswestall@gmail.com")
- **password** used for myodphi (i.e. "odphi_password": "password1234")
- **region** your chapter is in (i.e. "region": "Midwest")
- **school** (i.e. "school": "Northwestern University")
- **semester** of service (i.e. "semester": "Winter")
- **year** of service (i.e. "year": "2019")
- **name** as it appears on the chapter service sheet (i.e. "name_on_service_sheet": "Gabriel Rojas-Westall")
- **ID of the google sheet**. This can be found in the URL of the service spreadsheet. In the example below, it's the portion with all of the x's:

https://docs.google.com/spreadsheets/d/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/edit#gid=0123456789

(i.e. "sheets_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")

**Note: The region, school, semester, and year must be exactly as you would normally submit it through the service hours page on myopdhi. You can look at the options section below to see how they are listed exactly on the site**

**It's important that you don't modify anything above odphi_username in the config file!**

From terminal, run the following command and you're done!
```
python3 submitter.py
```

Check to make sure that all the hours were submitted by getting a report of your hours on myodphi!


### Assumptions
- The hours for each individual bro are stored in a tab called "Hours"
- The dates of the service hours take the format "mm/dd/yyyy"
- The format of the sheet follows this [template](https://docs.google.com/spreadsheets/d/1dkmCiNWbt00yAwdC3qgnSNqTY2I8pQ9Vt1f3GGHy5Vo/edit#gid=1403236818)


### Options
The following options are available for a user to select from on the myodphi site. You should choose from the following and copy your choice *exactly* into the `config.json` file.

Region:
- Central Plains
- Central Texas
- East Texas
- Midwest
- Northwest
- North Texas
- Pacific
- Southeast
- Southwest

School:
- Auburn University
- Arizona State University
- Baylor University
- California State University - Bakersfield
- California State University - Monterey Bay
- California State University - Dominguez Hills
- California State University - Fresno
- California State University - Stanislaus
- Colorado State University - Ft. Collins
- Colorado State University - Pueblo
- Eastern Washington University
- Fresno State University
- Heritage University
- Kansas State University
- Michigan State University
- Northeastern Illinois University
- Northern Arizona University
- Northwestern University
- Oklahoma State University
- Oregon State University
- Our Lady of the Lake University
- Portland State University
- Prairie View A&M University
- Sam Houston State University
- Southern Illinois University
- Southern Methodist University
- St. Mary's University
- Stephen F. Austin State University
- Texas A&M - Corpus Christi
- Texas A&M - International
- Texas A&M - Kingsville
- Texas A&M - Commerce
- Texas A&M University
- Texas A&M University - San Antonio
- Texas Christian University
- Texas Southern University
- Texas State University
- Texas Tech University
- University of Arizona
- University of California - Merced
- University of Central Oklahoma
- University of Florida
- University of Houston
- University of Idaho
- University of Illinois - Chicago
- University of Illinois - Urbana-Champaign
- University of Incarnate Word
- University of Nevada - Las Vegas
- University of Nevada - Reno
- University of New Mexico
- University of North Texas
- University of Oklahoma
- University of Texas - Arlington
- University of Texas - Austin
- University of Texas - Dallas
- University of Texas - El Paso
- University of Texas - Pan American
- University of Texas - San Antonio
- University of the Pacific
- University of Utah
- University of Washington
- University of West Florida
- University of Wisconsin - Milkwaukee
- University of Wisconsin - Oshkosh
- University of Wisconsin - Parkside
- Washington State University
- West Texas A&M University
- Western Michigan University
- Western Oregon University

Semester:
- Fall
- Winter
- Spring

Year:
- 2018
- 2019
- 2020
- 2021
- 2022