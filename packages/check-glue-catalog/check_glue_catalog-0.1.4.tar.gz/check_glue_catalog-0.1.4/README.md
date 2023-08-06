[![Python 3.7](https://img.shields.io/badge/python-3.7-blue.svg)](https://www.python.org/downloads/release/python-370/)
[![PyPI version](https://badge.fury.io/py/check-glue-catalog.svg)](https://badge.fury.io/py/check-glue-catalog)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/msantino/check-glue-catalog.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/msantino/check-glue-catalog/context:python)
[![Twitter Follow](https://img.shields.io/twitter/follow/msantino.svg?style=social&label=Follow)](https://twitter.com/msantino)

# Check Glue Catalog

Get Glue catalog details to check if tables are outdated.

```bash
pip install check-glue-catalog
```

```python
from check_glue_catalog import get_tables

result = get_tables(catalog_name="glue_database_name")

print(result)
```

```JSON
{
  "outdated": 3,
  "updated": 23,
  "outdated_list": [
    {
      "table_name": "table_name_1",
      "due_days": 2,
      "rows": "7",
      "last_updated": "2020-03-10 05:43:37"
    },
    {
      "table_name": "other_table",
      "due_days": 76,
      "rows": "5",
      "last_updated": "2019-12-27 11:08:13"
    },
    {
      "table_name": "some_table",
      "due_days": 97,
      "rows": "5",
      "last_updated": "2019-12-06 16:22:52"
    }
  ]
}
```