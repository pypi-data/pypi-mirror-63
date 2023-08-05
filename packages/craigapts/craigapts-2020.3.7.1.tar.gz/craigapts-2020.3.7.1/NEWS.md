# NEWS

2020.3.7.1

* Scraper now removes duplicate ads and avoids unnecessary requests. `post_id`
is now the primary key in `CLSearch.data`.

2020.3.6.1

* Scraper now gets ads' post IDs from ad URLs. Before, a deep scrape was
required to get post IDs.

* Data columns are rearranged so `post_id` and `datetime_scr` appear first.

* `datatime_scr` now contains seconds, so it will differ across pages if
`deep=False` or across ads if `deep=True`.

2020.2.23.1

* First release.
