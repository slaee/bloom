const express = require('express');
const app = express();

app.use(express.json());

app.post('/login', (req, res) => {
    var obj = {};
    var data = JSON.parse(req.body);
    Object.assign(obj, data);

    // Check if the object has isAdmin property
    if (obj.isAdmin) {
        res.send("User is admin!");
    } else {
        res.send("User is not admin!");
    }
});

app.listen(3000, () => console.log('Server running on port 3000'));