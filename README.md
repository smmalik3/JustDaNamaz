# JustDaNamaz
# Developed by Salman Malik
# MIT License

Alexa Skill for Islamic Prayer Times

This Voice Enabled Skill allows you to ask Alexa when any prayer is during the day.

For example, you can ask Alexa to first open the skill by saying:
"Alexa, open prayer times."

Alexa will then open the skill and after the welcome message will wait for your next command which can be any of the following:

1. When is Fajr?
2. When is Dhuhr?
3. When is Asr?
4. When is Maghrib?
5. When is Isha?
6. Cancel or Stop

This skill requests permission to know the zipcode of the device you are using in order to calculate the correct prayer time for your area. 

If permission is not given the skill will not work.

Below is information onn the Prayer Times API that was used to develop this skill.
Thanks to www.aladhan.com for developing it!

Prayer Times API Doc

Example: 

curl http://api.aladhan.com/v1/calendar?latitude=51.508515&longitude=-0.1254872&method=2&month=4&year=2017

Prayer Times Calendar by city - http://api.aladhan.com/v1/calendarByCity

//return prayer times for DC for November 2018
curl 'http://api.aladhan.com/v1/calendarByCity?city=DC&country=US&method=2&day=17&month=11&year=2018'

//returns prayers times for DC based on current date and timezone
curl 'http://api.aladhan.com/v1/timingsByCity/1542492774?city=DC&country=US&method=2'


--> TIMEZONES: http://php.net/manual/en/timezones.america.php

See Below for details:

Timings By City - http://api.aladhan.com/v1/timingsByCity/:date_or_timestamp
Description:
Returns all prayer times for a specific date in a particular city.

Method: GET
Parameters:
"date_or_timestamp" (string) -
A date in the DD-MM-YYYY format or UNIX timestamp. Default's to the current date.

"city" (string) -
A city name. Example: London

"country" (string) -
A country name or 2 character alpha ISO 3166 code. Examples: GB or United Kindom

"state" (string) -
State or province. A state name or abbreviation. Examples: Colorado / CO / Punjab / Bengal

"method" (number) -
A prayer times calculation method. Methods identify various schools of thought about how to compute the timings. This parameter accepts values from 0-12 and 99, as specified below:
0 - Shia Ithna-Ansari
1 - University of Islamic Sciences, Karachi
2 - Islamic Society of North America
3 - Muslim World League
4 - Umm Al-Qura University, Makkah 
5 - Egyptian General Authority of Survey
7 - Institute of Geophysics, University of Tehran
8 - Gulf Region
9 - Kuwait
10 - Qatar
11 - Majlis Ugama Islam Singapura, Singapore
12 - Union Organization islamic de France
13 - Diyanet İşleri Başkanlığı, Turkey
99 - Custom. See https://aladhan.com/calculation-methods

"tune" (string) -
Comma Separated String of integers to offset timings returned by the API in minutes. Example: 5,3,5,7,9,7. See https://aladhan.com/calculation-methods

"school" (number) -
0 for Shafi (or the standard way), 1 for Hanafi. If you leave this empty, it defaults to Shafii.

"midnightMode" (number) -
0 for Standard (Mid Sunset to Sunrise), 1 for Jafari (Mid Sunset to Fajr). If you leave this empty, it defaults to Standard.

"timezonestring" (string) -
A valid timezone name as specified on http://php.net/manual/en/timezones.php . Example: Europe/London. If you do not specify this, we'll calcuate it using the co-ordinates you provide.

"latitudeAdjustmentMethod" (number) -
Method for adjusting times higher latitudes - for instance, if you are checking timings in the UK or Sweden.
1 - Middle of the Night
2 - One Seventh
3 - Angle Based

"adjustment" (number) -
Number of days to adjust hijri date(s). Example: 1 or 2 or -1 or -2

Endpoint URL: http://api.aladhan.com/v1/timingsByCity/:date_or_timestamp
Example Request: http://api.aladhan.com/v1/timingsByCity?city=Dubai&country=United Arab Emirates&method=8
