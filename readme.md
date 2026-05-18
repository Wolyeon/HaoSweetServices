# Services for the HaoSweet website

This repo is for services that the website may or may not use
for website operation. I will need to figure out how deployment works first.

# Development

This repo will require some packages to be installed before it can be run properly
packages include:
- Pandas
- FastAPI
- Pydantic
- Google Auth API

The fastest way to get these packages would be through NPM.

Create a virtual environment and then install all the packages onto it before running any of the python services.

# convertExcel.py

Used to convert our excel data into useable json data for the back and front end of the web.

You can use this as a simple python script and will only convert from the data folder for a file name "Menu.xlsx"

# haosweetservices.py

A simple backend web service used for the haosweet website built using FastAPI.

See here for more information: https://fastapi.tiangolo.com/tutorial/

Simply use `fastapi dev` to run the service.

# TODO

- Allow convertExcel.py to take file names through the command line for better flexibility
- Find a way to upload the service onto oracle cloud as it's free hosting on single core servers.
    https://www.oracle.com/ca-en/cloud/free/?intcmp=ohp052322ocift_ca-en
- Rebrand will be inevitable as haosweet is no longer the name we want to use.
- 