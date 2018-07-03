# FOLLOW API

Used by entities (subscribers) to follow (express interest) about data produced by another entity
* `apikey`: of the entity requesting data access
* `entityID`: Refers to the name of the entity whose data is required
* `permission`: Can be read, write, read-write. Permission will be mentioned to interested entity.
* `validity`: Can be in terms of Years(Y), Months(M), Days(D), Hours(H), Minutes(m) and Seconds(s)
**URL** : `https://localhost:10443/api/1.0.0/follow`

**Method** : `POST`

**Auth required** : YES

**Curl example**
Entity with `apikey` 9810db90bb6f4c3eae98359d080ac1fe is requesting entity `camera` for `read` permission for a `validity` period of 10 days (`10D`). This follow request gets approved when the device owner uses the `/share` API to accept the follow request with read permission.

```bash
curl -ik -X POST https://localhost:10443/api/1.0.0/follow \
-H 'apikey: 9810db90bb6f4c3eae98359d080ac1fe' \
-d '{"entityID": "camera", "permission":"read", "validity": "10D"}'
```
## Success Response

**Code** : `200 OK`

**Content example**

```json
A follow request has been made to entity camera with read access at 2018-04-08 10:08:01 GMT.
```
## Error Response

**Condition** : If `apikey` is wrong.

**Code** : `403 FORBIDDEN`

**Content** :

```json
{
"message": "Invalid authentication credentials"
}
```
