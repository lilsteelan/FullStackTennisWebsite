[![header][header-url]][header-link]
# Full Stack Dummy Website 
> A full-stack application built with SQL-Alchemy and Stripe API

[![Project Version][version-image]][version-url]
[![Frontend][Frontend-image]][Frontend-url]
[![Backend][Backend-image]][Backend-url]

## Table of Contents

- [Overview](#overview)
- [Built With](#built-with)
- [Demonstration](#demonstration)
- [Installation](#installation)
- [Features](#features)
- [Contact](#contact)

## Overview

This application allows customers to view, contact and sign up for tennis lessons, without the need for any third-party interactions. 
The website includes integrated payments with stripe as well as automated statistics and notifications that are sent to the admin
when someone new has signed up for a lesson. All of which can be accessed and modified through the dashboard.

### Built With
* Python
* HTML
* CSS
* Fast API
* Stripe API
* SQL Alchemy
* Bcrypt
* Flask
  * login
  * session
  * admin
  * bcrypt
  * sqlalchemy

## Demonstration

* Home Page
<img src="https://github.com/lilsteelan/OcconorDummyWebsite/assets/62084214/7e8a0455-8659-493e-a7a8-8f2fa882cc31" alt="drawing" width="400"/>

* Admin Panel
<img src="https://github.com/lilsteelan/OcconorDummyWebsite/assets/62084214/b339266e-19d2-44df-95d1-1bfc46cfac6c" alt="drawing" width="400"/>

* Stripe Payment
<img src="https://github.com/lilsteelan/OcconorDummyWebsite/assets/62084214/7f1f13af-8875-40ff-a7f5-30ea8b0426ca" alt="drawing" width="400"/>

* Lesson Selection Page
<img src="https://github.com/lilsteelan/OcconorDummyWebsite/assets/62084214/46542751-5723-4e72-8c30-e3f9b4b4e150" alt="drawing" width="400"/>

Video Demonstration


### Installation

To install, navigate to root directory of folder and install the requirements

Windows: 
```sh
pip install -r requirements.txt
```
Then run the following command

Run the file ( debug mode by default )
```sh
python -m app.py
```

**Note:** The Stripe payment will not work, as the stripe keys, and payment ID's are private and not publicly available on the repo.
If you wish to run the program with stripe integration you must implement it yourself through the creation of a .env file and setting the values as follows:

```sh
STRIPE_PRIVATE_KEY='sk_test_su'
Court_Kangaroos='price_etc'
Little_Smash='price_etc'
Young_Beginners='price_etc'
Beginner_Intermediate='price_etc'
Advanced='price_etc'
Competitive_Squad='price_etc'
ENDPOINT_SECRET='whsec_etc'
SECRET_KEY='something_super_secret'
PEOPLEKEY = 'something_super_secret'
```

### Features

This project was designed to demonstrate:

* Integrated Stripe Payment within flask
  * Stripe WebBooks
* SQL Alchemy DataBase Management
* Dynamically Loaded Admin Dashboard
* Session Data
* Dynamically Loaded Tennis Lesson Pages
* Dynamic Admin page
  * Custom search filters
  * Options for individual automated entries

  
### Contact
Feel free if you have any questions regarding the program

**email** : [stellan.lindrud@gmail.com](stellan.lindrud@gmail.com)


<!-- Markdown link & img dfn's -->

[header-url]: banner.png
[header-link]: https://github.com/alexandrerosseto

[repository-url]: https://github.com/alexandrerosseto/wbshopping

[cloud-provider-url]: https://wbshopping.herokuapp.com

[linkedin-url]: https://www.linkedin.com/in/alexandrerosseto

[wiki]: https://github.com/yourname/yourproject/wiki

[version-image]: https://img.shields.io/badge/Version-1.0.0-brightgreen?style=for-the-badge&logo=appveyor
[version-url]: https://img.shields.io/badge/version-1.0.0-green
[Frontend-image]: https://img.shields.io/badge/Frontend-HTML_CSS-blue?style=for-the-badge
[Frontend-url]: https://img.shields.io/badge/Frontend-HTML_CSS-blue?style=for-the-badge
[Backend-image]: https://img.shields.io/badge/Backend-Python-important?style=for-the-badge
[Backend-url]: https://img.shields.io/badge/Backend-Python-important?style=for-the-badge


