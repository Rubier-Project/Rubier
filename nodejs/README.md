# NodeJS Rubier Version

```js
const { Rubier } = require("./index");
const app = new Rubier("AUTH");

app.getMe({
    callback: (data) => {
        console.log(data);
    }
})
```
