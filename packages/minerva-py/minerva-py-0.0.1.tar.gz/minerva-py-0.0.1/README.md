# minerva-py

minerva-py is the python client to fetch data from minerva datahub

## Installation

```
$ pip install minerva-py
```

## Example

```python
from minerva import Client

client = Client(user={user}, password='{password}')
data = client.fetch('marketdata?sector=information_technology&begin=2020-01-10&end=2020-02-20&start=0&size=20')
```


## datahub docs

<https://datahub.moyiquant.com/api-docs/>