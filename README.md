cenotaph
========

Empty project using pyramid and cornice


cenotaph README
==================

Getting Started
---------------

- cd <directory containing this file>

- $VENV/bin/python setup.py develop

- $VENV/bin/initialize_cenotaph_db development.ini

- $VENV/bin/pserve development.ini


todo
---------

- session management

- client admin section for user management

- user manager

- populate admin account

- user menu in navbar

- local fonts and remote fonts in config

- form info in rest interface
  - add form by collection url
  - update form by the model url
  - forms accessible with GET request, parameter to be decided later...
  - presence of query field returns json description of form, instead
  - the model or collection requested.  However every request may also
    place the form in the response.  Collection url requests will get
	create forms, while model url requests will get update forms.
  - validators are described by simple strings supported on client or
	a reserved name shared between server and client for special validation.
  - validators from server describe server validation
  - coffee code to create view.ui propery for formview
  - input template for form_group_input_div
	- input_id: 'input_password'
	- input_type: 'textarea'
    - label: 'Password'
    - input_attributes:
		- name: 'password'
        - type: 'password'
        - placeholder: 'Enter password'
  - There is still no form with a selection widget
  
