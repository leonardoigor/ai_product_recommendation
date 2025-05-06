from sqlalchemy import text
from models import SessionLocal
from models import (
    Base,
    User,
    Item,
    UserInteraction,
    UserItemScore,
    get_db,
    engine,
)
from sqlalchemy.orm import Session
from sklearn.preprocessing import LabelEncoder
import torch
import torch.nn as nn
import numpy as np
import os
import pandas as pd


def check_system_environment():
    import locale

    print(f"Encoding do sistema: {locale.getpreferredencoding()}")
    print(
        f"Arquivos .env estão salvos como UTF-8? {'SIM' if os.path.isfile('.env') else 'NÃO'}"
    )

    # Verifica encoding do arquivo .env
    try:
        with open(".env", "r", encoding="utf-8") as f:
            f.read()
        print(".env é válido em UTF-8")
    except UnicodeDecodeError:
        print("ERRO: .env contém caracteres não-UTF-8!")


def check_database_encoding():
    with engine.connect() as conn:
        result = conn.execute(text("SHOW server_encoding;"))
        encoding = result.scalar()
        print(f"Encoding do banco: {encoding} (deve ser UTF8)")
        assert encoding == "UTF8", "O banco deve usar encoding UTF8!"


# ==================== 1. Criação das Tabelas ====================
def create_tables():
    check_system_environment()
    check_database_encoding()

    try:
        Base.metadata.create_all(bind=engine)
        print("✅ Tabelas criadas com sucesso!")
    except Exception as e:
        print(f"❌ Erro ao criar tabelas: {e}")
        raise


# ==================== 2. Treinamento do Modelo ====================
class Recommender(nn.Module):
    def __init__(self, n_users, n_items, n_categories, embedding_dim=50):
        super().__init__()
        self.user_embed = nn.Embedding(n_users, embedding_dim)
        self.item_embed = nn.Embedding(n_items, embedding_dim)
        self.category_embed = nn.Embedding(n_categories, embedding_dim)
        self.fc = nn.Linear(3 * embedding_dim, 1)

    def forward(self, user, item, category):
        u = self.user_embed(user)
        i = self.item_embed(item)
        c = self.category_embed(category)
        combined = torch.cat([u, i, c], dim=1)
        return torch.sigmoid(self.fc(combined)).squeeze()


def train_model(db: Session):
    # Busca dados
    interactions = db.query(UserInteraction).all()

    # Pré-processamento
    df = pd.DataFrame(
        [(i.user_id, i.item_id, i.item.category) for i in interactions],
        columns=["user_id", "item_id", "category"],
    )

    user_enc = LabelEncoder()
    item_enc = LabelEncoder()
    category_enc = LabelEncoder()

    df["user_idx"] = user_enc.fit_transform(df["user_id"])
    df["item_idx"] = item_enc.fit_transform(df["item_id"])
    df["category_idx"] = category_enc.fit_transform(df["category"])

    # Modelo
    model = Recommender(
        n_users=len(user_enc.classes_),
        n_items=len(item_enc.classes_),
        n_categories=len(category_enc.classes_),
    )

    # ... (restante do treinamento igual ao anterior)

    return model, user_enc, item_enc, category_enc


# ==================== 3. Geração de Recomendações ====================
def generate_recommendations(db: Session, user_id: int, top_k: int = 10):
    user = db.query(User).filter(User.user_id == user_id).first()
    if not user:
        return []

    # Busca scores pré-computados
    recommendations = (
        db.query(Item, UserItemScore.relevance_score)
        .join(UserItemScore, Item.item_id == UserItemScore.item_id)
        .filter(UserItemScore.user_id == user_id)
        .order_by(UserItemScore.relevance_score.desc())
        .limit(top_k)
        .all()
    )

    return [(item.item_id, item.category, score) for item, score in recommendations]


# ==================== 4. Exemplo de Uso ====================
if __name__ == "__main__":
    create_tables()

    # Exemplo de inserção de dados
    with SessionLocal() as db:
        # Cria usuário
        new_user = User(user_id=1, username="joao")
        db.add(new_user)

        # Cria item
        new_item = Item(item_id=101, category="roupas")
        db.add(new_item)

        # Cria interação
        new_interaction = UserInteraction(user_id=1, item_id=101, interaction_type=1)
        db.add(new_interaction)

        db.commit()

    # Treina e recomenda
    model, user_enc, item_enc, category_enc = train_model(SessionLocal())
    print(generate_recommendations(SessionLocal(), user_id=1))
