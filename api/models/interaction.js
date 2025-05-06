const { DataTypes } = require("sequelize");
const sequelize = require("../db");

const Interaction = sequelize.define("Interaction", {
    interaction_type: DataTypes.INTEGER,
    timestamp: {
        type: DataTypes.DATE,
        defaultValue: DataTypes.NOW,
    },
});

module.exports = Interaction;
