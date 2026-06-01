# O APIRouter permite criar rotas modulares (separadas do main.py).
# O Depends é a ferramenta do FastAPI para Injeção de Dependência.
from fastapi import APIRouter, Depends

# Importa o tipo Session para o Python saber que a variável 'db' é uma conexão de banco.
from sqlalchemy.orm import Session

# Importa a função que abre e fecha a conexão com o banco de dados.
from core.database import get_db

# Importa a camada de Serviço, onde estão as regras de negócio e formatação.
from services.report_service import ReportService # Corrigi para "services" (plural) como nas boas práticas

# Importa o Schema do Pydantic que garante que a resposta saia no formato exato.
from schemas.report_schema import DashboardResponse

# Cria o "mini-aplicativo" de rotas. 
# prefix: Garante que TODAS as rotas deste arquivo comecem com /relatorios
# tags: Agrupa essas rotas visualmente lá na documentação do Swagger.
router = APIRouter(prefix="/relatorios", tags=["Relatórios e Consultas"])

# Define o método HTTP (GET) e o caminho final da rota. O caminho completo será: /relatorios/dashboard
# CORREÇÃO: Havia um erro de digitação ("dashbosrd"). Corrigido para "dashboard".
# response_model: Trava a saída da API. Se o ReportService devolver algo diferente
# do que está no DashboardResponse, o FastAPI bloqueia e avisa o erro.
@router.get("/dashboard", response_model=DashboardResponse)

# A função obter_dashboard é chamada toda vez que alguém acessa a rota.
# O parâmetro db: Session = Depends(get_db) é a Injeção de Dependência em ação:
# Antes de rodar a função, o FastAPI executa o get_db, pega a conexão aberta e injeta aqui.
def obter_dashboard(db: Session = Depends(get_db)):
    
    # Instancia o Service passando a conexão do banco para ele.
    # O Controller não faz consultas e nem regras matemáticas, ele delega o trabalho.
    service = ReportService(db) 
    
    # Executa o método principal do Service e devolve o JSON perfeitamente formatado para o usuário.
    return service.get_dashboard_stats()