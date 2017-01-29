# potential-broccoli
Cyber Security Base - Course Project I :: mooc.fi

## Requires
- Python
- PostgreSQL
- Preferably virtualenv
- Preferably unix

## Running
- `./init`
- `./run (--debug)`

```
My project has 5 different security flaws, Injection, Session management, XSS, Insecure object data references and CSRF. The project itself is written with a microframework on python called Flask and it's using psycopg2 to connect to a PostgreSQL database.  The project can be found in github, under https://github.com/sorja/potential-broccoli .

Identifying vulnerabilities
Note: The project was made purposely with flask, as it has little to no security implemented. If you want some kind of security features. The project has little to no validation in fields, which is itself quite risky business.

Identifying and fixing vulnerabilities
Injection
This is quite straight forward. We don’t validate user input anywhere, and the SQLs are straight forward. Ex. user input is foo we can “select * from messages where bar = foo”. If user inputs something else, ex. = everything breaks down. Easy way to fix this is escape adn validate ALL user input.

Session management
Session management is quite broken also, you can get the session with document.cookie and with some XSS you can pop it from the session and send it to another server with an ajax call (attackers server.) Using this authentication / session cookie you can impersonate another user. Fixing this is little bit harder without third party libraries. Luckily, there is a library called “Flask-session” which helps us.

XSS
You can send document.cookie with a script injected for example in a message. HTML is not escaped and neither is javascript. Creating a message with script tags around a post request sending the document.cookie works. Preventing this is easy - escape ALL user input and validate it.

Insecure object data references
This one is quite straight forward, modifying any numeric (id) parameters in URL gives you access to information which should be restricted. Fixing this problem is quite easy; adding validation. Is the current user allowed to access this information? Getting current user from session, popping the current users ID and comparing it to the requested parameter. If it’s not matching, either redirect or give a HTTP error code (403).

CSRF
Cross Site Request Forgery
Because the are no validations or restrictions, there is neither restrictions about the requesters URL. Although, this is not a banking system or so, user is able to make a cross site request forgery - meaning that he is loading a broken image - for example in email - and using the broken image’s fallback to create another request. <img src="http://example.com/reply/1/message&user_id=1" />. In this example the fallback procedure is not used. Tgus creates a new reply by user with id 1 to a message with id 1.


```