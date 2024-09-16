# Personal Diary Web App

## Overview

Welcome to the Personal Diary Web App, a platform designed to help you capture and organize your thoughts seamlessly. Whether you're creating a new account or logging in, this website empowers you to write and track your diary entries effortlessly. Dive into your memories, manage tasks, and enjoy a user-friendly experience.


Getting Started

Writing Your Diary
You can initiate your diary entry journey by clicking the "Write" option in the top bar or the "Write a New Diary" button on the welcome page. After pouring your thoughts onto the screen, ensure to click the "Done" button to securely save your reflections.

Viewing Your Diary
To revisit specific moments, click on "Your Diary" in the top bar. Choose the desired date, and the web app will display your written entries. In case you haven't documented anything for that day, an apology page provides a friendly reminder.

Managing Tasks
Efficiently manage your tasks by navigating to the "Tasks" section in the top bar. Add new tasks by clicking the "Add" button, check them off with the "Check" button, or delete tasks using the "Delete" button.



## Project Structure

### Static
The "Static" folder contains the "styles.css" file, housing the CSS code for styling.

### Templates
- .apology.html: An HTML file for the apology page that appears when unexpected actions occur.
- .diary.html: HTML for viewing previous diary entries, featuring an input for selecting the date.
- .index.html: HTML for the welcome page.
- .layout.html: Shared layout for the web pages.
- .login.html: HTML for the login page, including username and password fields.
- .register.html: HTML for the register page, with fields for username, password, and configuration.
- .task.html: HTML for the tasks page.
- .view.html: HTML for viewing a specific diary entry.
- .write.html: HTML for writing a new diary entry.

### app.py
The Python file, App.py, houses multiple functions responsible for the website's functionalit.

Index:
This function returns the index page. If the method is GET, it retrieves the page; if the method is POST, it writes the page.

Login:
This function returns the login page. If the method is GET, it displays the login page; if the method is POST, it checks whether the user entered a username or password. If not, it provides an apology page. If entered, it looks up the username, and if it matches the password, it logs the user in.

Logout:
This function redirects to the login page.

Register:
This function returns the register page. If the method is GET, it displays the register page; if the method is POST, it provides an apology if the user doesn't meet the requirements or if the username is already taken. Otherwise, it logs the user in.

Write:
This function returns the write page. If the method is GET, it displays the write page; if the method is POST, it updates the Database if the user entered their diary and pressed "done."

Diary:
This function returns the diary page. If the method is GET, it displays the diary page; if the method is POST, it prompts the user to enter the desired date. If there is a diary for that date, it transfers them to the view page with that specific diary; otherwise, it shows an apology page.

Tasks:
This function returns the tasks page. If the method is GET, it displays the tasks page; if the method is POST, it inserts a new task into the database if the user entered a new task.

Delete:
This function is for task deletion on the task page, deleting the task from the database if the user removes it.

Check:
This function updates the task status in the database if the user checks or unchecks the task.


### Diary.db
This database contains user-specific information, including diaries and tasks.

### Helper.py
Helper.py includes various functions crucial for the project's smooth operation, such as apology and login requirements.

### Requirements.txt
This file lists the necessary packages for the web application to function correctly.

