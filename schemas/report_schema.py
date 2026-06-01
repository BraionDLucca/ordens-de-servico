# Importa a classe mãe do Pydantic. Qualquer classe que herdar do BaseModel 
# ganha "superpoderes" de validação automática e conversão de dados.
from pydantic import BaseModel

# Importa módulos de tipagem do Python. 
# List = para criar listas de objetos (arrays).
# Dict = para criar dicionários (chave-valor, como objetos JSON).
from typing import List, Dict


# O objetivo de criar essas classes menores é manter o princípio da Responsabilidade Única.

# Schema para definir como os dados de um Técnico devem sair da API.
class TopTecnico(BaseModel):    
    # O Pydantic vai barrar a resposta se 'nome' não for texto (string)
    # ou se 'total_atendimentos' não for um número inteiro.
    nome: str
    total_atendimentos: int

# Schema para padronizar a saída do relatório das peças do estoque.
class PecaMaisUtilizada(BaseModel):
    peca: str 
    quantidade: int

# Schema para formatar os dados básicos das ordens que passaram do prazo.
class OrdemAtrasada(BaseModel):
    id: int 
    cliente_id: int 


# --- MODELO PRINCIPAL (O AGREGADOR) ---

# Este é o Schema que vai diretamente na rota do FastAPI (no response_model).
# Ele funciona como um "agregador", juntando todos os modelinhos menores acima em um grande objeto.
class DashboardResponse(BaseModel):
    
    # Dict[str, int]: Significa que esperamos um dicionário onde a chave é texto e o valor é número.
    # Exemplo gerado: {"Concluída": 15, "Em Andamento": 3}
    ordens_por_status: Dict[str, int]
    
    # O total de atrasos é um número inteiro simples.
    total_atrasadas: int 
    
    # Aqui aplicamos Composição: Dizemos que não é uma lista qualquer, mas sim 
    # uma Lista de objetos "OrdemAtrasada". O Pydantic vai verificar item por item da lista!
    ordens_atrasadas: List[OrdemAtrasada]
    
    # Lista validada de objetos "TopTecnico"
    top_tecnicos: List[TopTecnico]
    
    # Lista validada de objetos "PecaMaisUtilizada"
    pecas_mais_utilizadas: List[PecaMaisUtilizada]
    
    # O tempo médio geralmente é convertido para string (texto) no Service 
    # (ex: "2 dias", "14:30:00") para ficar amigável para o frontend ler.
    tempo_medio_atendimento: str