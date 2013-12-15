# GEONAMESZIP
A quick and dirty script/api for syncing postal codes / zip codes with a local sqlite3 database.

### Why?
Personally I dislike hitting up a remote server for mostly static information.
Since GeoNames provides this data under a Creative Commons license, this script
pulls all countries and drops it in a sqlite3 for (relatively) fast lookup.

## Important!
This data is provided by GeoNames under the Creative Commons license (http://creativecommons.org/licenses/by/3.0/).
If you use this data, you must provide credit to them whenever it is used.

The python-geonameszip library itself is under the MIT license.

### Example:

Main uses are for postal code validation:

```python
import geonameszip
# NOTE: country is required due to duplicate zip codes based on country.
us_result = geonameszip.lookup_postal_code('77098', 'US')
print(us_result)
# {'city': u'Houston', 'country': u'US', 'lon': -95.4118, 'county': u'Harris', 'state': u'Texas', 'postal_code': u'77098', 'lat': 29.735, 'state_abbreviation': u'TX'}
mx_result = geonameszip.lookup_postal_code('77098', 'MX')
print(mx_result)
# {'city': u'Barrio Bravo', 'country': u'MX', 'lon': -88.6458, 'county': u'Othon P Blanco', 'state': u'Quintana Roo', 'postal_code': u'77098', 'lat': 19.4083, 'state_abbreviation': u'ROO'}
```


## API

`geonameszip`

```python
import_from_file(source_path)
```
- Drops the postal_codes table in the sqlite3 database
- Re-creates the tabl.e
- Inserts all the data provided by a file formatted like `allCountries.txt`.

```python
lookup_postal_code(postal_code, country, conn=None, cursor=None)
```
- Selects the first available option for the `postal_code`, `country` combination.
- NOTE: Currently, if multiple entries match, only the top-most is provided.

```python
update_postal_code(postal_code, country, city, state, state_abbreviation, county, lat, lon, conn=None,commit=True, cursor=None)
```
- _Inserts_ the values provided in the arguments into the database.
- NOTE: This always _inserts_ the data, never updates. The data isn't consistently unique and the database has no primary key so it isn't easy to provide a way to update a single row.
- This can create duplicate entries.
