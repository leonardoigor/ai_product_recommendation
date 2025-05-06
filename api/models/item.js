const { DataTypes } = require("sequelize");
const sequelize = require("../db");

const Item = sequelize.define("Item", {
    item_id: {
        type: DataTypes.INTEGER,
        primaryKey: true,
    },
    category: {
        type: DataTypes.STRING,
    },
});

module.exports = Item;
