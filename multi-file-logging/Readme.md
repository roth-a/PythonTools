## Logging Example with prettyprint output

This logging example show how to use decorators and logging in python.

This is an example  and not meant for production use. As you can see it is extremely slow, but gives a very nice output, showing exactly which function were called and how deep they are embedded in other functions.

### Output

```python
=====================================
Test deep function call logging:

Myclass.func args: (1, 2, {'useless_dict': [...]}) kwargs: {'op': 'dd'}
|   Myclass.helperfunc args: (1, 2, {'useless_dict': [...]}) kwargs: {}
|   |   Myclass.helperfunc2 args: ({'useless_dict': [...]},) kwargs: {}
|   |   |   Myclass.helperfunc3 args: (5, 7, ['bla', 'bla', 'bla']) kwargs: {}
|   |   |   Myclass.helperfunc3 after 2.124ms  returns 5
|   |   Myclass.helperfunc2 after 4.261ms  returns 5
|   Myclass.helperfunc after 5.598ms  returns 8
Myclass.func after 7.106000000000001ms  returns 11

=====================================
Now test cross-file logging:

call_other_file args: ({'useless_dict': [...]},) kwargs: {}
|   function_in_sub args: ({'useless_dict': [...]},) kwargs: {}
|   function_in_sub after 0.719ms  returns {'useless_dict': [{...}]}
call_other_file after 2.175ms  returns {'useless_dict': [{...}]}

=====================================
Test exception 1 level down:

Myclass.call_crash_function args: ({'useless_dict': [...]},) kwargs: {}

|   Myclass.crash args: ({'useless_dict': [...]},) kwargs: {}

Exception in Myclass.crash in {'useless_dict': [{'use_less_sub_structure': 0}]} with args (<main.Myclass object at 0x7fd4a0188748>,
 {'useless_dict': [{'use_less_sub_structure': 0}]}), kwargs {}
Traceback (most recent call last):
  File "/my_path/PythonTools/multi-file-logging/logger_decorator.py", line 46, in decorated
    result = fn(*args, **kwargs)
  File "/my_path/PythonTools/multi-file-logging/main.py", line 46, in crash
    raise ValueError(str(i))

ValueError: {'useless_dict': [{'use_less_sub_structure': 0}]}

Exception in Myclass.call_crash_function in {'useless_dict': [{'use_less_sub_structure': 0}]} with args (<main.Myclass object at 0x7fd4a0188748>,
 {'useless_dict': [{'use_less_sub_structure': 0}]}), kwargs {}
Traceback (most recent call last):
  File "/my_path/PythonTools/multi-file-logging/logger_decorator.py", line 46, in decorated
    result = fn(args, **kwargs)
  File "/my_path/PythonTools/multi-file-logging/main.py", line 38, in call_crash_function
    return self.crash(i)
  File "/my_path/PythonTools/multi-file-logging/logger_decorator.py", line 60, in decorated
    raise ex
  File "/my_path/PythonTools/multi-file-logging/logger_decorator.py", line 46, in decorated
    result = fn(args, **kwargs)
  File "/my_path/PythonTools/multi-file-logging/main.py", line 46, in crash
    raise ValueError(str(i))
ValueError: {'useless_dict': [{'use_less_sub_structure': 0}]} 

```

