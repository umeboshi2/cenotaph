# Application Development Environment

## CoffeeScript

[CoffeeScript](http://coffeescript.org/) is used as the language 
of choice for developing applications with 
[Backbone.Marionette](http://marionettejs.com/).  When I began 
noticing the necessity of learning javascript to achieve a 
better application platform, I decided to use coffeescript for 
a large number of reasons.  I had already been hesitant to use 
javascript, so being a python developer, I started by looking 
at javascript alternatives that would allow me to perform 
client side development without a heavy investment into learning 
another language.  I came across some projects that took a 
python file and compiled it into javascript, but this turned 
out to be a greater hassle than expected.

I happened to chance upon coffee script one day and decided to 
try it out.  While I was initially using it to provide a 
whitespace environment for creating javascript, I found that
the coffeescript language provides a lot of valuable assistance to a 
person learning to program in a javascript environment.  Not 
only does the syntactic sugar provide for cleaner and more 
readable code, it also provides readable reliability when performing 
some common actions that are a bit tricky to do correctly in 
javascript, such as testing for *undefined*.  Even more valuable 
is the default behaviour to wrap the code in an anonymous function,
and also forcing every variable to be declared locally on first chance 
in that anonymous function, making it very difficult to pollute 
the global namespace accidentally.


## Backbone.Marionette

Marionette is the main application framework.  Marionette makes 
it easier to organize application code into smaller more 
manageable module.  It uses a communication mechanism to 
decouple the components of the application, making it easier to 
develop each part separately.

### Application Skeleton

- **main (main-local)**
  This is where the requirejs config is located.  This file is 
  responsible for importing the application module and starting
  the application.
- **application**
  - This module is responsible for the initial setup of the application.
  - This module sets the AppRegions for the main page.
  - It starts the AppRouters of all the sub applications.
  - If logins are used, this module sets the handler for the user info
	and starts the app after fetching the user info.
- **models** and **collections**
  These provide access to models and collections that are 
  global to the application, such as "current user info" for
  the logged in user.
- **msgbus**
  This is the global message bus that allows communication 
  between the main application and the sub apps.

### Child Application Skeleton

- main.coffee
- models and collections

### Frontdoor Application

The frontdoor application is the default child application.  One
child application must exist to perform the function of an "index.html"
page.


