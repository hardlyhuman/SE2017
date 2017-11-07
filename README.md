# SE2017
Smart Attendance Management System - SE2017

Due to version of celery being used you may get the following errors while trying to run server

Error #1

``` ImportError: cannot import name python_2_unicode_compatible ```

This refrence this issue https://github.com/celery/django-celery-results/issues/9

Fix:

Replace
 ``` from celery.five import python_2_unicode_compatible ```

with 
 ``` from django.utils.encoding import python_2_unicode_compatible  ```
 
 Error #2:
 
 ``` 
from kombu.utils import json 
ImportError: cannot import name json
```

References https://github.com/celery/celery/issues/2250

Fix:

Replace
  ``` from kombu.utls import json ```

with
  ``` import json```
  
 
 
 
