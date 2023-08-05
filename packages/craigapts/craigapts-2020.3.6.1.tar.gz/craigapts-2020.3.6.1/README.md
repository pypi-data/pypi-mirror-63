# craigapts

Python package for scraping apartment data from Craigslist.

## Install

Stable version from PyPI:

```sh
pip install craigapts
```

Dev version from GitLab:

```sh
pip install git+https://gitlab.com/everetr/craigapts.git
```

## Examples

```python3
from craigapts import CLSearch

GEO   = "newjersey"
QUERY = "'no section 8'"

# get basic data available on search result pages
c1 = CLSearch(GEO, QUERY)
print(c1.data)

# get details by navigating to each individual ad
c2 = CLSearch(GEO, QUERY, deep=True)
print(c2.data)
```

## Changelog

2020.3.6.1

* Scraper now gets ads' post IDs from ad URLs. Before, a deep scrape was
required to get post IDs.

* Data columns are rearranged so `post_id` and `datetime_scr` appear first.

* `datatime_scr` now contains seconds, so it will differ across pages if
`deep=False` or across ads if `deep=True`.

2020.2.23.1

* First release.

## TODO

* Replace `requests` dependency with `urllib3`? Because minimalism.
* Let user specify which variables, how many pages, and how many ads to scrape
* CLI
