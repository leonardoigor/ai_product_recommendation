const express = require('express');
const path = require('path');

const app = express();
const port = 3001;

// Serve arquivos estáticos da pasta "public"
app.use("/static", express.static(path.join(__dirname, 'public')));

app.get('/', (req, res) => {
    res.send('Hello World!');
});

app.listen(port, () => {
    console.log(`Server is running on http://localhost:${port}`);
});
