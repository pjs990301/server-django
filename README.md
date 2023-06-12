# MoWA Django
 This repository is Django, which implements the backend of MoWA.
 
 ## Table of Contents
 1. Introduction
 2. Installation
 3. License
 4. Contact

## Introdcution
MoWA Django is the main backend of MoWA. If Django is currently running on AWS EC2, the port is running on 8000. [MoWA Swagger Link](http://3.37.161.170:8000/swagger/)     
Data from AWS RDS mysql can be accessed through MoWA Django, and the Django REST API requests and responds to Android data.    
However, due to the expiration of AWS Prettyer in the future, we will be closing the server, so if you need more information, please contact us at the contact below.     

 <div align="center">
    <h4>The following shows the API of our MoWA.</h4><br>
    <img alt="img.png" src="https://github.com/pjs990301/server-django/blob/master/fig/api.png?raw=true"/>
</div>

![image](https://github.com/pjs990301/server-django/assets/70201882/cc66ee42-1c74-4dec-8237-dde35af16833)

<br>

## Installation
Clone a project using Git:
<pre><code>git clone https://github.com/pjs990301/server-django.git</code></pre>

Create and activate virtual environments:
<pre><code>conda activate your_environments</code></pre>

Install the required dependencies:
<pre><code>pip install -r requirements.txt</code></pre>

Perform database migration:
<pre><code>python manage.py migrate</code></pre>

Run the development server:
<pre><code>python manage.py runserver</code></pre>

<code>Open http://localhost:8000/ in a web browser.</code>

<br>

## License
Our repository worked on the MIT license.
Please refer to the following [Link](https://github.com/pjs990301/server-django/blob/master/LICENSE) for more information

<br>

## Contact
- Pull Request
- p990301@gachon.ac.kr
