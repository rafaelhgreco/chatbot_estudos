"""
Validadores de entrada usando Pydantic para garantir dados estruturados e válidos.
"""

from pydantic import BaseModel, Field, validator
from typing import Optional, Literal
import re


class ParametrosEstudo(BaseModel):
    """Modelo para validação dos parâmetros de estudo do usuário."""
    
    tema: str = Field(..., min_length=3, max_length=200, description="Tema de estudo")
    metodologia: str = Field(..., min_length=3, max_length=100, description="Metodologia escolhida")
    tempo_disponivel: str = Field(..., description="Tempo disponível (ex: 2h/dia, 10h/semana)")
    prazo: str = Field(..., description="Prazo desejado (ex: 2 meses, 8 semanas)")
    nivel: Literal["iniciante", "intermediário", "intermediario", "avançado", "avancado"] = Field(
        ..., 
        description="Nível de conhecimento atual"
    )
    
    @validator('tema')
    def validar_tema(cls, v):
        """Valida se o tema não é muito curto ou vazio."""
        if not v or v.strip() == "":
            raise ValueError("Tema não pode ser vazio")
        if len(v.strip()) < 3:
            raise ValueError("Tema muito curto. Seja mais específico.")
        return v.strip()
    
    @validator('metodologia')
    def validar_metodologia(cls, v):
        """Valida se a metodologia foi informada."""
        if not v or v.strip() == "":
            raise ValueError("Metodologia não pode ser vazia")
        return v.strip()
    
    @validator('tempo_disponivel')
    def validar_tempo(cls, v):
        """Valida formato do tempo disponível."""
        if not v or v.strip() == "":
            raise ValueError("Tempo disponível não pode ser vazio")
        
        # Aceita formatos como: 2h/dia, 1.5h/dia, 10h/semana, 20min/dia
        padrao = r'^\d+(\.\d+)?\s*(h|hora|horas|min|minuto|minutos)\s*/\s*(dia|semana|mes|mês)$'
        if not re.match(padrao, v.strip().lower()):
            raise ValueError(
                "Formato inválido. Use: '2h/dia', '1.5h/dia', '10h/semana', '30min/dia'"
            )
        return v.strip()
    
    @validator('prazo')
    def validar_prazo(cls, v):
        """Valida formato do prazo."""
        if not v or v.strip() == "":
            raise ValueError("Prazo não pode ser vazio")
        
        # Aceita formatos como: 2 meses, 8 semanas, 60 dias
        padrao = r'^\d+\s*(dia|dias|semana|semanas|mes|mês|meses)$'
        if not re.match(padrao, v.strip().lower()):
            raise ValueError(
                "Formato inválido. Use: '2 meses', '8 semanas', '60 dias'"
            )
        return v.strip()
    
    @validator('nivel')
    def normalizar_nivel(cls, v):
        """Normaliza o nível removendo acentos."""
        mapa_niveis = {
            'iniciante': 'iniciante',
            'intermediário': 'intermediário',
            'intermediario': 'intermediário',
            'avançado': 'avançado',
            'avancado': 'avançado'
        }
        return mapa_niveis.get(v.lower(), v)


class DadosConversa(BaseModel):
    """Modelo para armazenar dados da conversa em andamento."""
    
    tema: Optional[str] = None
    metodologia: Optional[str] = None
    tempo_disponivel: Optional[str] = None
    prazo: Optional[str] = None
    nivel: Optional[str] = None
    cronograma_atual: Optional[str] = None
    cronogramas_anteriores: list[str] = Field(default_factory=list)
    
    def esta_completo(self) -> bool:
        """Verifica se todos os dados necessários foram coletados."""
        return all([
            self.tema,
            self.metodologia,
            self.tempo_disponivel,
            self.prazo,
            self.nivel
        ])
    
    def to_parametros(self) -> Optional[ParametrosEstudo]:
        """Converte para ParametrosEstudo se todos os dados estiverem presentes."""
        if not self.esta_completo():
            return None
        
        try:
            return ParametrosEstudo(
                tema=self.tema,
                metodologia=self.metodologia,
                tempo_disponivel=self.tempo_disponivel,
                prazo=self.prazo,
                nivel=self.nivel
            )
        except Exception:
            return None


class FeedbackUsuario(BaseModel):
    """Modelo para feedback do usuário sobre o cronograma."""
    
    sentimento: Literal["positivo", "negativo", "neutro"]
    aprovado: bool
    pontos_positivos: list[str] = Field(default_factory=list)
    pontos_negativos: list[str] = Field(default_factory=list)
    ajustes_solicitados: list[dict] = Field(default_factory=list)
    necessita_esclarecimento: bool = False
    perguntas_usuario: list[str] = Field(default_factory=list)


def extrair_tempo_e_prazo(texto: str) -> tuple[Optional[str], Optional[str]]:
    """
    Tenta extrair tempo disponível e prazo de um texto livre.
    
    Retorna: (tempo_disponivel, prazo) ou (None, None) se não encontrar
    """
    tempo = None
    prazo = None
    
    # Padrões para tempo
    padroes_tempo = [
        r'(\d+(\.\d+)?\s*(h|hora|horas|min|minuto|minutos)\s*/\s*(dia|semana|mes|mês))',
        r'(\d+(\.\d+)?)\s*(h|hora|horas)\s*(por|ao|no|na|de)?\s*(dia|semana)',
    ]
    
    # Padrões para prazo
    padroes_prazo = [
        r'(\d+\s*(dia|dias|semana|semanas|mes|mês|meses))',
        r'em\s+(\d+\s*(dia|dias|semana|semanas|mes|mês|meses))',
    ]
    
    texto_lower = texto.lower()
    
    # Busca tempo
    for padrao in padroes_tempo:
        match = re.search(padrao, texto_lower)
        if match:
            tempo = match.group(1).strip()
            break
    
    # Busca prazo
    for padrao in padroes_prazo:
        match = re.search(padrao, texto_lower)
        if match:
            prazo = match.group(1).strip()
            break
    
    return tempo, prazo


def extrair_nivel(texto: str) -> Optional[str]:
    """
    Tenta extrair o nível de conhecimento do texto.
    
    Retorna: 'iniciante', 'intermediário' ou 'avançado', ou None
    """
    texto_lower = texto.lower()
    
    if any(palavra in texto_lower for palavra in ['iniciante', 'beginner', 'começando', 'zero', 'nunca']):
        return 'iniciante'
    elif any(palavra in texto_lower for palavra in ['intermediário', 'intermediario', 'intermediate', 'médio', 'medio']):
        return 'intermediário'
    elif any(palavra in texto_lower for palavra in ['avançado', 'avancado', 'advanced', 'experiente']):
        return 'avançado'
    
    return None


def validar_tema(tema: str) -> tuple[bool, str]:
    """
    Valida se o tema é adequado.
    
    Retorna: (is_valid, mensagem_erro)
    """
    if not tema or tema.strip() == "":
        return False, "Tema não pode ser vazio"
    
    if len(tema.strip()) < 3:
        return False, "Tema muito curto. Seja mais específico."
    
    if len(tema) > 200:
        return False, "Tema muito longo. Tente ser mais conciso."
    
    return True, ""


def validar_metodologia(metodologia: str) -> tuple[bool, str]:
    """
    Valida se a metodologia é conhecida ou customizada válida.
    
    Retorna: (is_valid, mensagem)
    """
    if not metodologia or metodologia.strip() == "":
        return False, "Metodologia não pode ser vazia"
    
    metodologias_conhecidas = [
        'long-life', 'longlife', 'aprendizado contínuo', 'aprendizado continuo',
        'shoshin', 'mente de principiante',
        'kumon', 'progressão gradual', 'progressao gradual',
        'pomodoro',
        'spaced repetition', 'repetição espaçada', 'repeticao espacada',
        'feynman'
    ]
    
    metodologia_lower = metodologia.lower()
    
    # Verifica se é uma metodologia conhecida
    if any(met in metodologia_lower for met in metodologias_conhecidas):
        return True, "Metodologia conhecida"
    
    # Aceita metodologias customizadas se tiverem mais de 3 caracteres
    if len(metodologia.strip()) >= 3:
        return True, "Metodologia customizada aceita"
    
    return False, "Metodologia não reconhecida. Escolha uma das sugeridas ou descreva melhor."
