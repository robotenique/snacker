# project-team-16
CSC301, Fall 2018, team project.

# Setup (Backend)

We are using Python with the Flask framework, and the PyCharm IDE.

Links:

Flask: http://flask.pocoo.org/

Pycharm IDE: https://www.jetbrains.com/pycharm/ (Download community version)

Install Flask:

pip install Flask

pip install flask-bcrypt

pip install dnspython

pip install mongoengine

pip install Flask-WTF

pip install Pillow

pip install Flask-Table

pip install flask_login

### Run the application

You can run the application inside PyCharm, by clicking on the 'Run' button, or using `shift + F10`.

You can also run the application with debug mode on terminal, by using (on linux):

```bash
$ cd snacker/flaskr
$ export FLASK_APP='app.py' FLASK_ENV=debug
$ flask run
```

Windows cmd (Powershell different)

```
$ cd snacker/flaskr
$ set FLASK_APP=app.py
$ flask run
```

To test the code, go to your local url displayed on the console and refresh the page, you should see printed stuff from db operations on your console. If having troubles, ask for help in groupchat.
## Code Style

### Indentation

Indent your code blocks with *4 spaces*.Never use tabs or mix tabs and spaces. In cases of implied line continuation, you should align wrapped elements vertically:
```python
       foo = long_function_name(var_one, var_two,
                                var_three, var_four)

       # Aligned with opening delimiter in a dictionary
       foo = {
           long_dictionary_key: value1 +
                                value2,
           ...
       }
```

### Naming

`module_name`,
`package_name`,
`ClassName`,
`method_name`,
`ExceptionName`,
`function_name`,
`GLOBAL_CONSTANT_NAME`,
`global_var_name`,
`instance_var_name`,
`function_parameter_name`,
`local_var_name`.

Function names, variable names, and filenames should be descriptive; eschew
abbreviation. In particular, do not use abbreviations that are ambiguous
to the readers not involved in your part of the project.
Do not abbreviate by deleting
letters within a word.

Always use a `.py` filename extension. Never use dashes.

#### Names to Avoid

-   single character names except for counters or iterators. You may use "e" as
    an exception identifier in try/except statements.
-   dashes (`-`) in any package/module name
-   `__double_leading_and_trailing_underscore__` names (reserved by Python)

Create a mongo account and tell Jayde your mongo email address.
