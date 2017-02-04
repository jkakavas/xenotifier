# Introduction 
xenotifier.py is a script that polls xe.gr for new house ads and notifies via email

# Instructions

 * Fill in the required configuration parameters in the script
 * create a virtualenv (i.e. named xenotifier)
 * create a cronjob i.e.

   ```
   00,30 * * * * cd /home/user/xe && env GMAIL_USERNAME='john_doe' GMAIL_PWD='hunter2' XE_RECIPIENTS='john@example.com, doe@example.com ' /home/user/.virtualenvs/xenotifier/bin/python xenotifier.py > /dev/null 2>&1
   ```


