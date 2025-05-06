# No shell do Django
from myapp.models import Produto

p = Produto.objects.create(
    nome="Camiseta Café com Poesia çãõ", categoria="Roupas", preco=99.90
)

print(Produto.objects.filter(categoria__contains="Roupas").first().nome)
# Deve mostrar: "Camiseta Café com Poesia çãõ"
