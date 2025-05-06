const sequelize = require("../db");
const User = require("./user");
const Item = require("./item");
const Interaction = require("./interaction");
const Score = require("./score");

// Relacionamentos
User.hasMany(Interaction);
User.hasMany(Score);

Item.hasMany(Interaction);
Item.hasMany(Score);

Interaction.belongsTo(User);
Interaction.belongsTo(Item);

Score.belongsTo(User);
Score.belongsTo(Item);

module.exports = {
    sequelize,
    User,
    Item,
    Interaction,
    Score,
};
