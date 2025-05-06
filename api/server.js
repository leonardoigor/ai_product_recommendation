const express = require("express");
const app = express();
const { sequelize } = require("./models");
const apiRoutes = require("./routes/api");

app.use(express.json());
app.use("/api", apiRoutes);

sequelize.sync({ alter: true })
    .then(() => {
        console.log("✅ DB sincronizado");
        app.listen(3000, () => console.log("🚀 API rodando em http://localhost:3000/api"));
    })
    .catch(a => {
        console.log(`error: ${a}`)
    });
