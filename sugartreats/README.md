# SugarTreats - Customer Management App on the Enterprise level
SugarTreats is a Customer Management App designed to streamline customer relationship management for a business. Tailored to meet the unique needs of companies and their employees, this app provides an efficient and user-friendly solution for managing customer information, memberships, orders, rewards, and promotions.

### Purpose:
For this project, I have used an example of a candy company when creating the app to portray how it will look like in its working stages. This is my first ever project in Django, made with the hopes of learning the framework. There are many ecommerce websites or application projects made with Django, but far fewer applications for handling ecommerce from the business perspective instead of the customers. This is why I chose to make this app from the business perspective.

## Key Features
1. Centralized Customer Information
Provides a central repository for all customer information including phone numbers, email addresses, purchase history, and more.

2. Rewards Tracking
Keeps track of rewards associated with each product, total rewards earned by customers per order and total rewards earned by a customer across all their purchase history.

3. Order Management
Efficiently manages customer orders, their status, and history.

# Installation for Windows
## Python Installation:
* Go to https://www.python.org/downloads/release/python-3113/ and download the correct exe file for your system. (64 bit or 32 bit)
* Open the downloaded exe file and select **Add python.exe to PATH"" on the setup window**.
* In Advanced Options make sure to select **Add python to environment variables**. You can also select **Install python 3.11 for all users** if you want so.
* After successfully installing python go to command prompt and type ``` python --version ``` to see if the correct version has been installed.

## VSCode Installation:
* Go to https://code.visualstudio.com/docs/setup/windows for information on how to install and set up VSCode.

## Django Installation:
* In command prompt type ``` pip install Django==4.2.5 ```
* To check if Django is installed correctly and can be seen by Python, in the command prompt type: 
```python```
```>>> import django```
```>>> print(django.get_version())```
* Also do ```pip install django-filter``` to get the Django Filter library

## Technologies
App is created with:
* Django version: 4.2
* Flask version: 2.2.5
* Python version: 3.11.3
* VSCode version: 1.82.0

This project is created with the help of **Django 3.0 Crash Tutorials** by Dennis Ivy
[Youtube](https://www.youtube.com/watch?v=xv_bwpA_aEA&t=28s&ab_channel=DennisIvy)