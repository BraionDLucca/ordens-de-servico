from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime
from models.ordem_servico_model import OrdemServico
from models.usuario_model import Usuario
from models.produto_model import Peca
from models.PecaOrdemServico import PecaOrdemServico as OSPeca

class ReportRepository:
    # O construtor (__init__) recebe a conexão com o banco de dados (db).
    # Isso aplica a Injeção de Dependência, garantindo que o repositório 
    # apenas execute as queries, sem se preocupar em abrir ou fechar a conexão.
    def __init__(self, db: Session):
        self.db = db

    def get_count_by_status(self):
        # OBJETIVO: Agrupar as ordens pelo status e contar quantas existem em cada grupo.
        return self.db.query(
            OrdemServico.status,
            # func.count conta os IDs. O .label('total') cria um "apelido" 
            # para essa coluna no resultado, facilitando a leitura depois.
            func.count(OrdemServico.id).label('total')
        ).group_by(OrdemServico.status).all() # O .all() retorna uma lista com todos os resultados.
    
    def get_overdue_orders(self):
        # Retornar a lista de ordens que passaram do prazo limite.
        return self.db.query(OrdemServico).filter(
            # A ordem não pode estar concluída ou cancelada.
            OrdemServico.status.notin_(['Concluida', 'Cancelada']), 
            
            # A data de conclusão deve ser menor (anterior) ao momento exato atual (datetime.now()).
            OrdemServico.data_conclusao < datetime.now()
         ).all()
    
    def get_top_tecnicos(self, limit: int = 5):
        #Gerar um ranking dos técnicos que mais possuem ordens de serviço.
        return self.db.query(
            Usuario.nome,
            func.count(OrdemServico.id).label('total_atendimento')
        # Faz o cruzamento (JOIN) entre as tabelas usando as chaves estrangeiras.
        # O .desc() garante que a ordenação seja do maior para o menor.
        ).join(OrdemServico, Usuario.id == OrdemServico.tecnico_id)\
        .group_by(Usuario.id)\
        .order_by(func.count(OrdemServico.id).desc())\
        .limit(limit).all() # Limita para trazer apenas os top N técnicos.
    
    def get_top_pecas_usadas(self, limit: int = 5): 
        # OBJETIVO: Descobrir quais peças do estoque são mais consumidas.
        return self.db.query(
            Peca.nome, 
            # ATENÇÃO: Aqui usamos func.sum() (soma) e não count(). 
            # Queremos somar as quantidades usadas, não contar quantas vezes apareceram.
            func.sum(OSPeca.quantidade).label('total_usado')
        ).join(OSPeca, Peca.id == OSPeca.peca_id)\
         .group_by(Peca.id)\
         .order_by(func.sum(OSPeca.quantidade).desc())\
         .limit(limit).all()
    
    def get_average_service_time(self):
        #Calcular a média geral do tempo que a empresa leva para concluir uma OS.
        avg_time = self.db.query(
            # Subtrai a data de abertura da data de conclusão e tira a média (avg).
            func.avg(OrdemServico.data_conclusao - OrdemServico.data_abertura)
        ).filter(OrdemServico.status == 'Concluída').scalar() 
        # O .scalar() é usado aqui porque não queremos uma lista, queremos apenas 
        # extrair aquele número único (a média em si) direto do banco.
        
        return avg_time
