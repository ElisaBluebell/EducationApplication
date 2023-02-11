import json
#
# with open("0208.py") as f:
#     json_object = json.load(f)
#
# print(json_object["id"])
# print(json_object["email"])
# print(json_object["address"])

import json

json_object = {
    "id": 1,
    "username": "Bret",
    "email": "Sincere@april.biz",
    "address": {
        "street": "Kulas Light",
        "suite": "Apt. 556",
        "city": "Gwenborough",
        "zipcode": "92998-3874"
    },
    "admin": False,
    "hobbies": None
}
with open("output.json", "w") as f:
    json.dump(json_object, f, indent=2)