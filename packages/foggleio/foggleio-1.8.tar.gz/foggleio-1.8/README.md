# foggle-io

Continuous deployment has never been easy but with the help of Foggle.io you can be one step closer

## Installing

Using npm:

```bash
$ pip install foggleio
```

## Usage

```python
import foggleio

result = foggleio.enabled('<--TENANT-ID-->', '<--ENVIRONMENT-->', '<--FEATURE-TOGGLE-KEY-->', 'my-consumer')

if result:
    print('Feature toggle enabled for \'my-consumer\'')
else:
    print('Feature toggle disabled for \'my-consumer\'')

```

## License

[MIT](LICENSE)
