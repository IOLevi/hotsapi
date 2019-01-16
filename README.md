# IOLevi's Hots API
(Running on an AWS EC2 Instance at http://18.216.106.216/). 

Self-hosted web app, exposing an external API and front end for Heroes of the Storm gaming statistics. 

- Web scraped statistics using BeautifulSoup4 and stored data on a MySQL database, running on a Linux VM, using SQLAlchemy as an ORM. 
- Dynamic front end using Flask for routing, Jinja for templating, and Bootstrap, HTML, CSS, and JS for content.
- User authentication handled with Flask-Login and Flask-WTF, with credentials stored on self-hosted database. 
- Hosted website on a Linux VM (Xenial), with an Nginx webserver, Gunicorn app server, and MySQL database. 
