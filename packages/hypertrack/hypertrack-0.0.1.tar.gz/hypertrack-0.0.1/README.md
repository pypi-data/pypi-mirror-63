# hypertrack-python

### Installation

Install from PyPi using [pip](https://pip.pypa.io/en/latest/), a package manager for Python.

```bash
pip install hypertrack
```

Or, you can download the source code and then run:
```bash
python setup.py install
```


### Getting Started
Just import hypertrack `Client` and start using it
```python
from hypertrack.rest import Client

account_id = "your_account_id"
secret_key = "your_secret_key"

hypertrack = Client(account_id, secret_key)
```
Now you have access to `devices` and `trips` API's
```python
# Get device name
device = hypertrack.devices.get('A50F7BB2-D67D-48A5-9B68-D5747B97381F')
device_name = device['device_info']['name']

# Create trip without destination
trip_data = {
    'device_id': 'A50F7BB2-D67D-48A5-9B68-D5747B97381F'
}

trip = hypertrack.trips.create(trip_data)
```


### Devices API methods
| Name  | Description | Arguments | 
| ------------- | ------------- | ------------- |
| `.start_tracking(device_id)`  | Start tracking | `device_id` - a string representing the ID of device, case sensitive |
| `.stop_tracking(device_id)`  | Stop tracking  | `device_id` - a string representing the ID of device, case sensitive |
| `.change_name(device_id, name)`  | Update a single device's name | `device_id` - a string representing the ID of device, case sensitive<br/> `name` - new device name |
| `.patch_metadata(device_id, metadata)`  | Update a single device's metadata  | `device_id` - a string representing the ID of device, case sensitive<br/> `metadata` - new device metadata dict |
| `.get_all(pagination=False, pagination_token)`  | Get all tracked devices. | `pagination` - if set to `True` it will split result by pages and response will containe `pagination_token` <br/> `pagination_token` - that should be provided to fetch next page |
| `.get(device_id)`  | Get a single device | `device_id` - a string representing the ID of a tracked device, case sensitive|
| `.get_history(device_id, history_date)`  | Get a single device history. | `device_id` - a string representing the ID of a tracked device, case sensitive<br/>`history_date` - a string representing specific date in format YYYY-MM-DD |
| `.get_account_history(history_date)`  | Get data for all tracked devices for a specified day. Data is available for the the last 60 days. | `history_date` - a string representing specific date in format YYYY-MM-DD<br/>`response` - response object can be one of: `blob` or `file`<br/>`response_type` - response type can be one of: `json` or `csv`<br/>`unit` - metric or imperial system: `km` or `mi` |
| `.delete(device_id)`  | Remove a single device. Once it is removed, the device will not be able send location data| `device_id` - a string representing the ID of device, case sensitive |

### Trips API methods
| Name  | Description | Arguments |
| ------------- | ------------- | ------------- |
| `.create(trip_data)`  | Start a new trip for a device. | `trip_data` - object with trip [data](https://hypertrack.com/docs/#references-apis-trips-start-trip) |
| `.get_all(trip_status='completed', pagination_token)`  | Get all trips. This endpoint return active trips by default | `trip_status` - (optional) a string representing the trip status to filter by. Default is `active` . Can be one of `active \| completed \| processing_completion`<br/>`paginationToken` allows you to request next page of trips list |
| `.get(trip_id)`  | Get a single trip | `trip_id` - a string representing the ID of a trip, case sensitive |
| `.patch_geofence_metadata(trip_id, geofence_id, metadata)`  | Update a trip geofence metadata. | `trip_id` - a string representing the trip ID<br/>`geofence_id` - a string representing the geofence ID for which metadata is being updated<br/>`metadata` - is dict with data to update |
| `.get_geofence(trip_id, geofence_id)`  | Get trip geofence | `trip_id` - a string representing the trip ID<br/>`geofence_id` - a string representing the geofence ID for which metadata is being updated |
| `.create_geofences(trip_id, geofences)`  | Add more geofences to an ongoing trip, in addition to geofences you might have created when creating trip. | `trip_id` - a string representing the trip ID<br/>`geofences` - list of geofences |
| `.complete(trip_id)`  | Complete an active trip. This will initiate a procedure on the HyperTrack platform | `trip_id` - a string representing the trip ID |


### Error handling
HyperTrack wrapper will throw `HyperTrackException` in case of any errors from HypertTrack API.

Exception will represent HyperTrack error [object](https://hypertrack.com/docs/#references-http-errors).

```python
from hypertrack.exceptions import HyperTrackException

try:
    hypertrack.devices.get('AAAAAAAA-AAAA-AAAA-AAAA-AAAAAAAAAAAA')
except HyperTrackException as e:
    print(e.status)
    # --> 404
    print(e.code)
    # --> device_not_found
```
### Examples
Create trip without destination but with geofences:
```python
trip = hypertrack.trips.create({
    'device_id': device_id,
    'geofences': [{
      "geometry": {
        "type": "Point",
        "coordinates": [
          35.105761016637075,
          47.856801319070776
        ]
      },
      "radius": 65,
      "metadata": {"id": "dec43d3c-766c-4f6a-bd78-dfe873556782"}
    }, {
      "geometry": {
        "type": "Point",
        "coordinates": [
          35.10460766676067,
          47.85663214471151
        ]
      },
      "radius": 55,
      "metadata": {"id": "f2e56252-53e3-4194-8d53-d946716618e7"}
    }]
})
```

Change trip geofence metadata: 
```python
geofence_id = trip['geofences'][0]['geofence_id']
hypertrack.trips.patch_geofence_metadata(trip['trip_id'], geofence_id, {'id': '123'})
```

Get changed trip geofence metadata:
```python
geofence = hypertrack.trips.get_geofence(trip['trip_id'], geofence_id)
print(geofence['metadata'])
# --> {'id': '123'}
```