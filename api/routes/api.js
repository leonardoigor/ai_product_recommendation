const express = require("express");
const { faker } = require('@faker-js/faker');
const { sequelize } = require("../models");
const cors = require("cors")
const router = express.Router();
const { User, Item, Interaction, Score } = require("../models");



router.use(cors())

router.use(async (req, res, next) => {
    console.log('--- Nova Requisição ---');
    console.log('Método:', req.method);
    console.log('Rota:', req.originalUrl);
    // console.log('Headers:', req.headers);
    // console.log('Body:', req.body);

    // Se quiser medir o tempo da requisição:
    const start = Date.now();
    res.on('finish', () => {
        const duration = Date.now() - start;
        console.log(`Requisição finalizada em ${duration}ms`);
        console.log('Status:', res.statusCode);
    });

    next();
});


// === CRUD compatível com json-server ===

// Usuários
router.get("/users", async (req, res) => res.json(await User.findAll()));
router.post("/users", async (req, res) => res.json(await User.create(req.body)));

// Itens
router.get("/items", async (req, res) => res.json(await Item.findAll()));
router.post("/items", async (req, res) => res.json(await Item.create(req.body)));

router.get("/items/generate", async (req, res) => {
    try {
        const items = [];

        for (let i = 0; i < 1_000; i++) {
            items.push({
                item_id: i + 1,
                category: faker.commerce.department(), // Gera uma categoria aleatória
            });
        }

        const bk = await Item.bulkCreate(items, { ignoreDuplicates: true });

        res.json({ message: "50 items gerados com sucesso!", items });
    } catch (error) {
        console.error(error);
        res.status(500).json({ error: "Erro ao gerar itens." });
    }
});

// Interações
router.get("/interactions", async (req, res) => res.json(await Interaction.findAll({ include: [User, Item] })));
router.post("/interactions", async (req, res) => res.json(await Interaction.create(req.body)));

// Scores
router.get("/scores", async (req, res) => res.json(await Score.findAll({ include: [User, Item] })));
router.post("/scores", async (req, res) => res.json(await Score.create(req.body)));
router.delete("/scores/:score_id", async (req, res) => {
    try {
        const { score_id } = req.params;
        const deleted = await Score.destroy({ where: { id: score_id } });

        if (deleted) {
            res.status(204).send(); // Sem conteúdo, deletado com sucesso
        } else {
            res.status(404).json({ error: "Score não encontrado" });
        }
    } catch (error) {
        console.error("Erro ao deletar score:", error);
        res.status(500).json({ error: "Erro interno no servidor" });
    }
});



// Recomendação com ordenação de score
router.get("/recommendations/:user_id", async (req, res) => {
    const userId = parseInt(req.params.user_id);
    const page = parseInt(req.query.page) || 1;
    const limit = parseInt(req.query.limit) || 10;
    const offset = (page - 1) * limit;

    const query = `
        SELECT 
            i.item_id,
            i.category,
            COALESCE(s.relevance_score, -1) AS score
        FROM 
            "Items" i
        LEFT JOIN 
            "Scores" s
            ON i.item_id = s.item_id AND s.user_id = :userId
        ORDER BY 
            score DESC
        LIMIT :limit OFFSET :offset;
    `;

    try {
        const results = await sequelize.query(query, {
            replacements: { userId, limit, offset },
            type: sequelize.QueryTypes.SELECT
        });

        res.json({
            page,
            limit,
            results
        });
    } catch (err) {
        console.error("Erro ao buscar recomendações:", err);
        res.status(500).json({ error: "Erro ao buscar recomendações" });
    }
});
module.exports = router;
