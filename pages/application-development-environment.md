# Application Development Environment

## node.js

A [node.js](http://nodejs.org) environment is used to develop and
build the applications.  [Grunt](http://gruntjs.com/) is used to
build and optimize the static resources for the client application.
The Gruntfile is written in coffeescript.  [bower](http://bower.io)
is also used in the node environment to install the upstream
static resources needed by the application.

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

The application skeleton was inspired by this github
[project](https://github.com/t2k/backbone.marionette-RequireJS),
which provides some simple boilerplate code to start
a single page application using marionette, coffeescript, and
requirejs.  It also taught me to use bower to manage the
components and their dependencies.

- **main (main-local)**
  This is where the requirejs config is located.  This file is 
  responsible for importing the application module and starting
  the application.
- **application**
  - This module is responsible for the initial setup of the
	[application](http://marionettejs.com/docs/marionette.application.html).
  - This module sets the
	[Regions](http://marionettejs.com/docs/marionette.region.html)
	for the main page.
  - It starts the
	[AppRouters](http://marionettejs.com/docs/marionette.approuter.html)
	of all the sub applications.
  - If logins are used, this module sets the handler for the user info
	and starts the app after fetching the user info.
- **models** and **collections**
  These provide access to
  [models](http://backbonejs.org/#Model) and
  [collections](http://backbonejs.org/#Collection) that are 
  global to the application, such as "current user info" for
  the logged in user.
- **msgbus**
  This is the global
  [message bus]( https://github.com/marionettejs/backbone.wreqr)
  (MainBus) that allows communication 
  between the main application and the sub apps.

### Child Application Skeleton

The child application exists in a subdirectory of the main
application root (since, I'm making these modules somewhat 
interchangeable and transferrable, this may change) and 
provides a certain set of functionality for the application.

- **main**
  - The main module is responsible creating the router that maps
	the routes to methods on the controller.
- **models** and **collections**
  - These modules provide the models and collections specific to
	the child application.
- **msgbus**
  - This is the child specific message bus (AppBus).  The channel
	it defines *must* have a unique name.
- **controller**
  - The [controller](http://marionettejs.com/docs/marionette.controller.html)
	basically handles the route requests by managing the views
	for those routes.
- **views**
  These are the
  [views](http://marionettejs.com/docs/marionette.region.html)
  that will be used in this child application.
- **templates**
  These are the teacup templates for the views in this child application.

### Frontdoor Application

The frontdoor application is the default child application.  One
child application must exist to perform the function of an "index.html"
page.  This can be considered the root path of the main application.
The frontdoor application can be required last in the application module
and interact with the functionality of those child applications, such as
accessing models, collections, templates, and views of those child
applications with the controller of the frontdoor application.

