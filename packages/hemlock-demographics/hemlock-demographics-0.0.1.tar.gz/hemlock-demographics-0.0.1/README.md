# Hemlock-Demographics

Demographics items for Hemlock projects.

## Example

```python
from hemlock_demographics import demographics
from hemlock_demographics.items import date_of_birth, gender, race

from hemlock import *

@route('/survey')
def Start(origin=None):
    b = Branch()
    
    p = Page(b)
    demographics(p, date_of_birth, gender, race, require=True)
    
    p = Page(b, terminal=True)
    Label(p, label='<p>End.</p>')
    return b
```

## Documentation

You can find the latest documentation at [https://dsbowen.github.io/hemlock-demographics](https://dsbowen.github.io/hemlock-demographics).

## License

Publications which use this software should include the following citations:

Bowen, D.S. (2020). Hemlock \[Computer software\]. [https://dsbowen.github.io/hemlock](https://dsbowen.github.io/hemlock).

Bowen, D.S. (2020). Hemlock-Demographics \[Computer software\]. [https://dsbowen.github.io/hemlock-demographics](https://dsbowen.github.io/hemlock-demographics).

This project is licensed under the MIT License [LICENSE](https://github.com/dsbowen/hemlock-demographics/blob/master/LICENSE).

Hemlock-CRT requires the Hemlock package, which is available under the [Hemlock Research License](https://github.com/dsbowen/Hemlock/blob/master/LICENSE).