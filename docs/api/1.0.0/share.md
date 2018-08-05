# SHARE API

Used by entities (data producers) to allow followers (who expressed interest) to access their data.

To allow followers (who expressed interest) to access your data, use the API with the following parameters in the body.


* `apikey` of the entity who will grant access
* `entityID` refers to the name of the entity to whom data should be shared
* `permission` can be read, write, read-write. Permission will be given to interested entity.
* `validity`: Can be in terms of Years(Y), Months(M), Days(D), Hours(H), Minutes(m) and Seconds(s)

**URL** : `http://localhost/api/1.0.0/share`

**Method** : `POST`

**Auth required** : YES

**Curl example**
Entity with `apikey` 4aefb1678fa74ce183edb44c79405dc1 is sharing its data with `app1` with only `read` permission, for a period of 10 days.

```bash
curl -ik -X POST http://localhost/api/1.0.0/share \
-H 'apikey:  4aefb1678fa74ce183edb44c79405dc1' \
-d '{"entityID": "app1", "permission":"read", "validity": "10D"}'
```
## Success Response

**Code** : `200 OK`

**Content example**

```json
Read access given to app1 at camera exchange.
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
