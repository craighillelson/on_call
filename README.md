# on_call
script for building an on call schedule

# Requirements
* [dateuitl](https://pypi.org/project/python-dateutil/)
* [pyinputplus](https://pypi.org/project/PyInputPlus/)

# Instructions
1. Download on_call.py.
1. Upload a csv of employee email addresses and their associated team number to the same directory you saved "on_call.py" to. Associating a team number with an employee is done to create depth or failover for each on call shift. An example csv follows.

employee|team
michael@dundermifflin.com|1
dwight@dundermifflin.com|1
jim@dundermifflin.com|1
pam@dundermifflin.com|1
stanley@dundermifflin.com|2
oscar@dundermifflin.com|2
angela@dundermifflin.com|2
toby@dundermifflin.com|2

1. Navigate to the proper directory and in Terminal, type "python3 on_call.py"


