arrow-adapters
======
Making the arrow time library play nice with others, so that every timestamp can have a timezone.  Support for: postgres, sqlite, sqlalchemy, graphene.

Automatically converts time values to UTC before persisting in the DB and loads back with local timezone.


### Install
```pip install arrow-adapters```


### Usage
```python
import arrow_adapters.auto
```

----
[![installs](https://img.shields.io/pypi/dm/time_adapters.svg?label=installs)](https://pypi.org/project/time_adapters)
