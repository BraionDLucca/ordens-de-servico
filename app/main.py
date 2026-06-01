from fastapi import FastAPI
from core.database import engine, Base


# importa todos os models para o Base reconhecer as tabelas
import models.usuario_model
import models.cliente_model
import models.ordem_servico_model
import models.historico_status_model
import models.produto_model
import models.HistoricoPeca
import models.PecaOrdemServico

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="API de Assistência Técnica",
    description="Gestão de OS, clientes, técnicos e peças.",
    version="1.0.0"
)

from routers.auth_router import router as auth_router
from routers.cliente_router import router as cliente_router
from routers.ordem_servico_router import router as ordem_servico_router

app.include_router(auth_router)
app.include_router(cliente_router)
app.include_router(ordem_servico_router)

@app.get("/")
def read_root():
    return {"status": "online"}
