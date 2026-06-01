from sqlalchemy.orm import Session
from repositories.report_repository import ReportRepository

class ReportService:
    def __init__(self, db: Session):
        self.repo = ReportRepository(db)

    def get_dashboard_stats(self):
        # 1. Ordens por status
        status_counts = self.repo.get_count_by_status()
        status_dict = {row.status: row.total for row in status_counts}

        # 2. Ordens em atraso
        overdue = self.repo.get_overdue_orders()
        
        # 3. Top Técnicos
        top_techs = self.repo.get_top_tecnicos()
        techs_list = [{"nome": row.nome, "atendimentos": row.total_atendimentos} for row in top_techs]

        # 4. Peças mais utilizadas
        top_parts = self.repo.get_top_pecas_usadas()
        parts_list = [{"peca": row.nome, "quantidade": row.total_usado} for row in top_parts]

        # 5. Tempo médio
        avg_time = self.repo.get_average_service_time()
        # Formatar timedelta para string ou horas dependendo da necessidade
        avg_time_str = str(avg_time) if avg_time else "0:00:00"

        return {
            "ordens_por_status": status_dict,
            "total_atrasadas": len(overdue),
            "ordens_atrasadas": [{"id": os.id, "cliente": os.cliente_id} for os in overdue],
            "top_tecnicos": techs_list,
            "pecas_mais_utilizadas": parts_list,
            "tempo_medio_atendimento": avg_time_str
        }