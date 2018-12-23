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
