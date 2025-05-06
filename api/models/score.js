const { DataTypes } = require("sequelize");
const sequelize = require("../db");

const Score = sequelize.define("Score", {
    relevance_score: {
        type: DataTypes.FLOAT,
    },
    last_updated: {
        type: DataTypes.DATE,
        defaultValue: DataTypes.NOW,
    },
    user_id: {
        type: DataTypes.INTEGER,
    },
    item_id: {
        type: DataTypes.INTEGER,
    },
}, {
    indexes: [
        {
            unique: true,
            fields: ["user_id", "item_id"] // Corrigido: minúsculo
        }
    ]
});

module.exports = Score;
