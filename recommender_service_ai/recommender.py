import requests
import pandas as pd
import torch
import torch.nn as nn
from sklearn.preprocessing import LabelEncoder

JSON_SERVER_URL = "http://localhost:3000/api"


class Recommender(nn.Module):
    def __init__(self, n_users, n_categories, embedding_dim=50):
        super().__init__()
        self.user_embed = nn.Embedding(n_users, embedding_dim)
        self.category_embed = nn.Embedding(n_categories, embedding_dim)
        self.fc = nn.Linear(2 * embedding_dim, 1)

    def forward(self, user, category):
        u = self.user_embed(user)
        c = self.category_embed(category)
        combined = torch.cat([u, c], dim=1)
        return torch.sigmoid(self.fc(combined)).squeeze()


def fetch_data():
    users = requests.get(f"{JSON_SERVER_URL}/users").json()
    interactions = requests.get(f"{JSON_SERVER_URL}/interactions").json()
    items = requests.get(f"{JSON_SERVER_URL}/items").json()
    return users, items, interactions


def train_models_per_user(users, items, interactions):
    df = pd.DataFrame(
        [
            (i["UserUserId"], i["Item"]["category"])
            for i in interactions
            if i.get("Item")
        ],
        columns=["UserUserId", "category"],
    )

    category_enc = LabelEncoder()
    df["category_idx"] = category_enc.fit_transform(df["category"])

    models_by_user = {}

    for user in users:
        user_id = user["user_id"]
        user_df = df[df["UserUserId"] == user_id]
        if user_df.empty:
            continue

        model = Recommender(
            n_users=1,  # apenas um usuário
            n_categories=len(category_enc.classes_),
        )

        criterion = nn.BCELoss()
        optimizer = torch.optim.Adam(model.parameters(), lr=0.01)
        labels = torch.ones(len(user_df), dtype=torch.float32)

        user_tensor = torch.tensor([0] * len(user_df), dtype=torch.long)  # sempre 0
        category_tensor = torch.tensor(user_df["category_idx"].values, dtype=torch.long)

        model.train()
        for epoch in range(10):
            optimizer.zero_grad()
            outputs = model(user_tensor, category_tensor)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()
            print(f"User {user_id} | Epoch {epoch+1} | Loss: {loss.item():.4f}")

        models_by_user[user_id] = model

    return models_by_user, category_enc


def update_scores(models_by_user, category_enc, users, items):
    # Limpa scores existentes
    response = requests.get(f"{JSON_SERVER_URL}/scores")
    if response.status_code == 200:
        scores = response.json()
        for score in scores:
            score_id = score["id"]
            requests.delete(f"{JSON_SERVER_URL}/scores/{score_id}")

    # Gera novos scores
    for user in users:
        user_id = user["user_id"]
        if user_id not in models_by_user:
            continue

        model = models_by_user[user_id]
        model.eval()

        with torch.no_grad():
            for item in items:
                if not item.get("category"):
                    continue
                try:
                    cat_idx = category_enc.transform([item["category"]])[0]
                    u = torch.tensor([0])  # um único usuário
                    c = torch.tensor([cat_idx])
                    score = model(u, c).item()

                    data = {
                        "user_id": user_id,
                        "item_id": item["item_id"],
                        "relevance_score": score,
                    }
                    requests.post(f"{JSON_SERVER_URL}/scores", json=data)
                except Exception as e:
                    continue


def get_recommendations(UserUserId, top_k=5):
    scores = requests.get(
        f"{JSON_SERVER_URL}/scores?user_id={UserUserId}&_sort=relevance_score&_order=desc&_limit={top_k}"
    ).json()
    result = []
    for s in scores:
        query = f"{JSON_SERVER_URL}/items?item_id={s['item_id']}"
        item = requests.get(query).json()[0]
        result.append((item["item_id"], item["category"], s["relevance_score"]))
    return result


if __name__ == "__main__":
    users, items, interactions = fetch_data()
    models_by_user, category_enc = train_models_per_user(users, items, interactions)
    update_scores(models_by_user, category_enc, users, items)

    # Exemplo de uso
    UserUserId = 1
    recs = get_recommendations(UserUserId)
    print(f"Recomendações para o usuário {UserUserId}:")
    for rec in recs:
        print(f"Item {rec[0]} ({rec[1]}) - Score: {rec[2]:.4f}")
