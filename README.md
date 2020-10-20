# Suggestify API

Request suggestions for a track using its ```title``` and ```artist```.

## Usage:

```
const axios = require("axios"),
      base_url = "https://suggestify-api.herokuapp.com/",
      predict_endpoint = base_url + "predict";


function requestSuggestions (artist, title) {
  axios
    .post(predict_endpoint, { artist, title })
    .then(({ data: { error, recommendations} }) => {
        if (error) console.log(error);   
        else {
            recommendations.forEach(({ artists, title }, i) => {
                console.log(`Track #${i + 1}`);
                console.log(`artists: ${artists}`);
                console.log(`title: ${title}`);
            });
        }
    })
    .catch(console.error);
}

requestSuggestions("shakira", "waka waka");
```
