# Suggestify API

Request suggestions for a track using its ```title``` and ```artist```.

## Usage:

```
const axios = require("axios"),
      base_url = "http://localhost:8000",
      predict_endpoint = base_url + "/predict";


function requestSuggestions (artist, title) {
  axios
    .post(predict_endpoint, { artist, title })
    .then(res => console.log(res.data))
    .catch(error => {
      console.error(error)
    })
}

requestSuggestions("Shakira", "Waka Waka");
```
