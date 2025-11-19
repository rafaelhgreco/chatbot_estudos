"""
Gerenciador de fluxo de conversa (Workflow Manager).
Implementa máquina de estados para controlar o fluxo do chatbot.
"""

from enum import Enum
from typing import Optional, Dict, Any
from utils.validators import DadosConversa, extrair_tempo_e_prazo, extrair_nivel


class EstadoConversa(Enum):
    """Estados possíveis da conversa."""
    INICIAL = "inicial"
    COLETANDO_TEMA = "coletando_tema"
    APRESENTANDO_METODOLOGIAS = "apresentando_metodologias"
    COLETANDO_PARAMETROS = "coletando_parametros"
    GERANDO_CRONOGRAMA = "gerando_cronograma"
    APRESENTANDO_CRONOGRAMA = "apresentando_cronograma"
    COLETANDO_FEEDBACK = "coletando_feedback"
    REFINANDO_CRONOGRAMA = "refinando_cronograma"
    APROVADO = "aprovado"
    ERRO = "erro"


class WorkflowManager:
    """
    Gerencia o fluxo de conversa e transições entre estados.
    Mantém contexto da conversa e determina próximos passos.
    """
    
    def __init__(self):
        self.estado_atual = EstadoConversa.INICIAL
        self.dados_conversa = DadosConversa()
        self.historico_estados = [EstadoConversa.INICIAL]
        self.contador_tentativas = 0
        self.max_tentativas = 3
    
    def get_estado(self) -> EstadoConversa:
        """Retorna o estado atual da conversa."""
        return self.estado_atual
    
    def get_dados(self) -> DadosConversa:
        """Retorna os dados coletados da conversa."""
        return self.dados_conversa
    
    def get_contexto_resumido(self) -> Dict[str, Any]:
        """Retorna um resumo do contexto atual para uso em prompts."""
        return {
            "estado": self.estado_atual.value,
            "tema": self.dados_conversa.tema,
            "metodologia": self.dados_conversa.metodologia,
            "tempo": self.dados_conversa.tempo_disponivel,
            "prazo": self.dados_conversa.prazo,
            "nivel": self.dados_conversa.nivel,
            "tem_cronograma": self.dados_conversa.cronograma_atual is not None
        }
    
    def transicionar_para(self, novo_estado: EstadoConversa):
        """Transiciona para um novo estado."""
        self.historico_estados.append(novo_estado)
        self.estado_atual = novo_estado
    
    def processar_mensagem_inicial(self) -> tuple[EstadoConversa, str]:
        """
        Processa mensagem quando está no estado inicial.
        
        Retorna: (próximo_estado, tipo_prompt)
        """
        self.transicionar_para(EstadoConversa.COLETANDO_TEMA)
        return EstadoConversa.COLETANDO_TEMA, "boas_vindas"
    
    def processar_tema(self, mensagem: str) -> tuple[EstadoConversa, str]:
        """
        Processa mensagem quando está coletando tema.
        
        Retorna: (próximo_estado, tipo_prompt)
        """
        # Armazena o tema
        self.dados_conversa.tema = mensagem.strip()
        
        # Transiciona para apresentar metodologias
        self.transicionar_para(EstadoConversa.APRESENTANDO_METODOLOGIAS)
        return EstadoConversa.APRESENTANDO_METODOLOGIAS, "confirmar_tema"
    
    def processar_metodologia(self, mensagem: str) -> tuple[EstadoConversa, str]:
        """
        Processa mensagem quando usuário escolhe metodologia.
        
        Retorna: (próximo_estado, tipo_prompt)
        """
        # Armazena a metodologia
        self.dados_conversa.metodologia = mensagem.strip()
        
        # Transiciona para coletar parâmetros
        self.transicionar_para(EstadoConversa.COLETANDO_PARAMETROS)
        return EstadoConversa.COLETANDO_PARAMETROS, "coletar_parametros"
    
    def processar_parametros(self, mensagem: str) -> tuple[EstadoConversa, str, bool]:
        """
        Processa mensagem quando está coletando parâmetros.
        Tenta extrair tempo, prazo e nível da mensagem.
        
        Retorna: (próximo_estado, tipo_prompt, parametros_completos)
        """
        # Tenta extrair informações da mensagem
        tempo, prazo = extrair_tempo_e_prazo(mensagem)
        nivel = extrair_nivel(mensagem)
        
        # Atualiza dados se encontrou
        if tempo:
            self.dados_conversa.tempo_disponivel = tempo
        if prazo:
            self.dados_conversa.prazo = prazo
        if nivel:
            self.dados_conversa.nivel = nivel
        
        # Verifica se todos os parâmetros foram coletados
        if self.dados_conversa.esta_completo():
            self.transicionar_para(EstadoConversa.GERANDO_CRONOGRAMA)
            return EstadoConversa.GERANDO_CRONOGRAMA, "gerar_cronograma", True
        else:
            # Ainda faltam parâmetros, mantém no mesmo estado
            self.contador_tentativas += 1
            
            if self.contador_tentativas >= self.max_tentativas:
                # Após várias tentativas, preenche com padrões
                if not self.dados_conversa.tempo_disponivel:
                    self.dados_conversa.tempo_disponivel = "1h/dia"
                if not self.dados_conversa.prazo:
                    self.dados_conversa.prazo = "2 meses"
                if not self.dados_conversa.nivel:
                    self.dados_conversa.nivel = "intermediário"
                
                self.transicionar_para(EstadoConversa.GERANDO_CRONOGRAMA)
                return EstadoConversa.GERANDO_CRONOGRAMA, "gerar_cronograma_com_padroes", True
            
            return EstadoConversa.COLETANDO_PARAMETROS, "coletar_parametros", False
    
    def cronograma_gerado(self, cronograma: str):
        """Marca que o cronograma foi gerado com sucesso."""
        self.dados_conversa.cronograma_atual = cronograma
        self.transicionar_para(EstadoConversa.APRESENTANDO_CRONOGRAMA)
    
    def cronograma_erro(self):
        """Marca que houve erro na geração do cronograma."""
        self.transicionar_para(EstadoConversa.ERRO)
    
    def processar_feedback(self, mensagem: str) -> tuple[EstadoConversa, str]:
        """
        Processa feedback do usuário sobre o cronograma.
        
        Retorna: (próximo_estado, tipo_acao)
        """
        mensagem_lower = mensagem.lower()
        
        # Detecta feedback positivo
        palavras_positivas = ['aprovado', 'perfeito', 'ótimo', 'otimo', 'excelente', 'bom', 'gostei', '👍', '✅']
        if any(palavra in mensagem_lower for palavra in palavras_positivas):
            self.transicionar_para(EstadoConversa.APROVADO)
            return EstadoConversa.APROVADO, "feedback_positivo"
        
        # Detecta feedback negativo genérico
        palavras_negativas = ['não gostei', 'nao gostei', 'ruim', 'mal', '👎', '❌']
        if any(palavra in mensagem_lower for palavra in palavras_negativas):
            return EstadoConversa.COLETANDO_FEEDBACK, "feedback_negativo_generico"
        
        # Detecta solicitação de ajuste
        palavras_ajuste = ['mudar', 'alterar', 'ajustar', 'modificar', 'reduzir', 'aumentar', 'adicionar', 'remover']
        if any(palavra in mensagem_lower for palavra in palavras_ajuste):
            # Salva cronograma anterior
            if self.dados_conversa.cronograma_atual:
                self.dados_conversa.cronogramas_anteriores.append(self.dados_conversa.cronograma_atual)
            
            self.transicionar_para(EstadoConversa.REFINANDO_CRONOGRAMA)
            return EstadoConversa.REFINANDO_CRONOGRAMA, "refinar_cronograma"
        
        # Se não identificou clara intenção, pede esclarecimento
        return EstadoConversa.COLETANDO_FEEDBACK, "pedir_esclarecimento"
    
    def cronograma_refinado(self, novo_cronograma: str):
        """Atualiza com cronograma refinado."""
        self.dados_conversa.cronograma_atual = novo_cronograma
        self.transicionar_para(EstadoConversa.APRESENTANDO_CRONOGRAMA)
    
    def resetar(self):
        """Reseta o workflow para início."""
        self.estado_atual = EstadoConversa.INICIAL
        self.dados_conversa = DadosConversa()
        self.historico_estados = [EstadoConversa.INICIAL]
        self.contador_tentativas = 0
    
    def pode_gerar_cronograma(self) -> bool:
        """Verifica se tem dados suficientes para gerar cronograma."""
        return self.dados_conversa.esta_completo()
    
    def get_faltando_parametros(self) -> list[str]:
        """Retorna lista de parâmetros que ainda faltam."""
        faltando = []
        
        if not self.dados_conversa.tempo_disponivel:
            faltando.append("tempo disponível")
        if not self.dados_conversa.prazo:
            faltando.append("prazo")
        if not self.dados_conversa.nivel:
            faltando.append("nível de conhecimento")
        
        return faltando
    
    def get_progresso(self) -> Dict[str, Any]:
        """Retorna informações de progresso para exibir na UI."""
        total_etapas = 5  # tema, metodologia, parâmetros, cronograma, feedback
        etapa_atual = 0
        
        if self.dados_conversa.tema:
            etapa_atual += 1
        if self.dados_conversa.metodologia:
            etapa_atual += 1
        if self.dados_conversa.esta_completo():
            etapa_atual += 1
        if self.dados_conversa.cronograma_atual:
            etapa_atual += 1
        if self.estado_atual == EstadoConversa.APROVADO:
            etapa_atual += 1
        
        return {
            "etapa_atual": etapa_atual,
            "total_etapas": total_etapas,
            "percentual": int((etapa_atual / total_etapas) * 100),
            "descricao": self._get_descricao_etapa()
        }
    
    def _get_descricao_etapa(self) -> str:
        """Retorna descrição amigável da etapa atual."""
        descricoes = {
            EstadoConversa.INICIAL: "Iniciando conversa",
            EstadoConversa.COLETANDO_TEMA: "Coletando tema de estudo",
            EstadoConversa.APRESENTANDO_METODOLOGIAS: "Escolhendo metodologia",
            EstadoConversa.COLETANDO_PARAMETROS: "Coletando informações de tempo e prazo",
            EstadoConversa.GERANDO_CRONOGRAMA: "Gerando cronograma personalizado",
            EstadoConversa.APRESENTANDO_CRONOGRAMA: "Apresentando cronograma",
            EstadoConversa.COLETANDO_FEEDBACK: "Aguardando seu feedback",
            EstadoConversa.REFINANDO_CRONOGRAMA: "Refinando cronograma",
            EstadoConversa.APROVADO: "Cronograma aprovado! ✅",
            EstadoConversa.ERRO: "Erro no processamento"
        }
        return descricoes.get(self.estado_atual, "Processando...")
