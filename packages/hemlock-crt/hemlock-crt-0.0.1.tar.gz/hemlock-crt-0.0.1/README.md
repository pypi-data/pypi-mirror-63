# Hemlock-CRT

A Cognitive Reflection Test (CRT) for Hemlock projects.

## Example

```python
from hemlock_crt import CRT
from hemlock_crt.items import ball_bat, machines, lily_pads

from hemlock import *

@route('/survey')
def Start(origin=None):
    b = Branch()
    CRT(b, ball_bat, machines, lily_pads)
    p = Page(b, terminal=True)
    Label(p, label='<p>End.</p>')
    return b
```

## Documentation

You can find the latest documentation at [https://dsbowen.github.io/hemlock-crt](https://dsbowen.github.io/hemlock-crt).

## License

Publications which use this software should include the following citations:

Bowen, D.S. (2020). Hemlock \[Computer software\]. [https://dsbowen.github.io/hemlock](https://dsbowen.github.io/hemlock).

Bowen, D.S. (2020). Hemlock-CRT \[Computer software\]. [https://dsbowen.github.io/hemlock-crt](https://dsbowen.github.io/hemlock-crt).

This project is licensed under the MIT License [LICENSE](https://github.com/dsbowen/hemlock-crt/blob/master/LICENSE).

Hemlock-CRT requires the Hemlock package, which is available under the [Hemlock Research License](https://github.com/dsbowen/Hemlock/blob/master/LICENSE).