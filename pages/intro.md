# So Here We Are


## Two Parts (Server/Client)

A web service should be accept a request for a CRUD operation of 
some sort.  The service should only return responses in certain 
structure, but without any layout or interaction information (the 
service may perform this task indirectly by serving the resources 
that allow the client to display and interact with the servie).

A person always uses a client program to access web services.  A very 
common platform to access web services is the web browser.  The client 
program decides how to allow interaction with and display the information 
from the web service.

## Development

There is a serious attempt to make things easy to develop an application.

### Server

There is an attempt to make it easy to provide an interface to objects 
in a database over a web service.  This can be pretty difficult, as there 
is only so much that can be done to make database access and usage conform 
to simple pattern.  If the patterns are too simple, the result is a very 
inefficient database, especially when it grows in size, as well as too 
much memory usage from extensive use of the ORM on many objects.

There are other things to consider on the server side beyond accessing 
records in a remote database, such as authentication, authorization, 
and user management.  There has been an attempt to provide an environment 
that performs these functions flexibly.

When serving an html resource, the web service should always provide 
a page with the necessary "link" tags in the "head" and an **empty** 
"body" element that will be filled by the client, likely by the 
resources being advertised in the "link" tags of the page.

### Client

yada yada




# [GitHub Pages](#)


## Projects

Here is a list of projects:

- [paella](https://github.com/umeboshi2/paella)([website](paella))

- [hubby](https://github.com/umeboshi2/hubby)([website](hubby))

- [bumblr](https://github.com/umeboshi2/bumblr)([website](bumblr))

- [conspectus](https://github.com/umeboshi2/conspectus)([website](conspectus))

- [trumpet](https://github.com/umeboshi2/trumpet)


## News

Here is a page of [news](#pages/news)

## GitHub Pages

How I create this [website](#pages/github-pages)


[timeline](#pages/timeline)
