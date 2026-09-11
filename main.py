from service import VendaService
from exceptions import ProdutoNaoEncontradoException

service = VendaService()

service.iniciar_venda()
service.processar_codigo("00123")
service.processar_codigo("01011", 2)

try:
    service.processar_codigo("99999")
except ProdutoNaoEncontradoException as erro:
    print(erro)

total = service.finaliza_venda()
print(f"Total da venda: R${total:.2f}")
