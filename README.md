# SugarTreats - Customer Management App on the Enterprise level

SugarTreats is a Customer Management App designed to streamline customer relationship management for a business. Tailored to meet the unique needs of companies and their employees, this app provides an efficient and user-friendly solution for managing customer information, memberships, orders, rewards, and promotions.
<img width="950" alt="ss1" src="https://github.com/maishaSupritee/SugarTreats-app/assets/74114117/a4b3bdcb-4160-4b07-b309-38598cdf3f6a">

<img width="960" alt="ss2" src="https://github.com/maishaSupritee/SugarTreats-app/assets/74114117/955ff0ae-9e7f-4ec0-b826-a0335a9c2ec8">

<img width="960" alt="ss3" src="https://github.com/maishaSupritee/SugarTreats-app/assets/74114117/421b3e2e-0003-42b6-9c4e-900b6781d5d3">

<img width="947" alt="ss4" src="https://github.com/maishaSupritee/SugarTreats-app/assets/74114117/dd55de10-628c-4515-bb2d-842cd5895237">

<img width="947" alt="ss5" src="https://github.com/maishaSupritee/SugarTreats-app/assets/74114117/91b50bf0-f385-4d0c-ae05-395fafeec577">

<img width="949" alt="ss6" src="https://github.com/maishaSupritee/SugarTreats-app/assets/74114117/a30c57f4-9962-4b0c-a322-17642f27c549">

### Purpose:

For this project, I have used an example of a candy company when creating the app to portray how it will look like in its working stages. This is my first ever project in Django, made with the hopes of learning the framework. There are many ecommerce websites or application projects made with Django, but far fewer applications for handling ecommerce from the business perspective instead of the customers. This is why I chose to make this app from the business perspective.

## Key Features

- Centralized Customer Information

  - Provides a central repository for all customer information including phone numbers, email addresses, purchase history, and more.

- Rewards Tracking

  - Keeps track of rewards associated with each product, total rewards earned by customers per order and total rewards earned by a customer across all their purchase history.

- Order Management
  - Efficiently manages customer orders, their status, and history.

# Installation for Windows

## Python Installation:

- Go to https://www.python.org/downloads/release/python-3113/ and download the correct exe file for your system. (64 bit or 32 bit)
- Open the downloaded exe file and select **Add python.exe to PATH on the setup window**.
- In Advanced Options make sure to select **Add python to environment variables**. You can also select **Install python 3.11 for all users** if you want so.
- After successfully installing python go to command prompt and type `python --version` to see if the correct version has been installed.

## VSCode Installation:

- Go to https://code.visualstudio.com/docs/setup/windows for information on how to install and set up VSCode.

## Django Installation:

- In command prompt type `pip install Django==4.2.5`
- To check if Django is installed correctly and can be seen by Python, in the command prompt type:
  `python`
  `>>> import django`
  `>>> print(django.get_version())`
- Also do `pip install django-filter` to get the Django Filter library

# Get Started

- First clone/download the repo
- In your terminal/command prompt cd into the root directory of the project and write:
  `python manage.py runserver`
- Click on the server link displayed in the terminal/command prompt to view the application in your browser
- Quit the server by typing `Ctrl+C` / `Cmd+C` in the terminal.

## Technologies

App is created with:

- Django version: 4.2
- Flask version: 2.2.5
- Python version: 3.11.3
- VSCode version: 1.82.0

This project is created with the help of **Django 3.0 Crash Tutorials** by Dennis Ivy
[Youtube](https://www.youtube.com/watch?v=xv_bwpA_aEA&t=28s&ab_channel=DennisIvy)
