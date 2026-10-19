- Containers are isolated environments. so container networking provides an interface for containers to communicate with eachother
- docker's network drivers-   
1. bridge- single host multiple containers+ tunnelling (masking network configurations)
2. host networking- 
3. overlay- multiple host, multiple containers
- Anatomy of a bridge network:
* my host machine- 3 containers- flask application, database, redis
* how do the containers find eachother in a network?- we assign names instead static ip addresses for which docker maintains a DNS server.
* containers resolve eachother by name, no hardcoded IPs, no config drift.
* local host port and container port- will be used to talk to eachother
* we use one public facing container like the flask application and then use APIs to communicate with the remaining containers. 
- In the assignment we're using Werkzeug. It is used as the underlying foundation of popular python frameworks. it handles the low-level details of communication between web servers and python applications. Provides powerful request and response objects to easily parse HTTP headers, query arguments, form data, cookies, and file uploads without dealing with raw WSGI dictionaries
- apparmour provides security. create profiles mentioning what you're supposed to do ie least privilege anything not mentioned not allowed- implicit ignoration. you create a profile file, load it into docker, then any container that runs will have loaded app armour. 