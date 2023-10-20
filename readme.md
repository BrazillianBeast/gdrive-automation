## What is this project:
The idea of this project came after seeing a base
project that would allow you to upload a specific file to your google drive account, after this the idea of this project was born which consists in
having a script that given a schedule will always
upload a specific file to your google drive. for
example a backup of a important file, after backing it up, it will also delete older versions of
the same file and will also empty your trash automatically so you can always have a fresh version
updated of your specific file.

## Getting started

-1 Before being able to run this project you will need
a OAUTH KEY from google which you will find how to get in the youtube video linked down below

-2 After getting your OAUTH KEY JSON FILE, you will rename it to **service_account.json** and copy it to
the same directory where your app.py is located at.

-3 At your project root folder run `"pip install -r requirements.txt"`

## Usage

`"python app.py <your_specific_file_path>"`

### After running this command the script will:

-1 remove any file with the same name of the file you have selected to upload in the gdrive folder you choose as your upload directory by passing its ID.

-2 Upload your brand new file you selected, in the gdrive folder

-3 write logs about the process in a .log file inside the project folder



## Base project inspired from:
https://www.youtube.com/watch?v=tamT_iGoZDQ&t=386s
