# -*- coding: utf-8 -*-
"""
Agente Filtro - Responsável por verificar se a pergunta está dentro do escopo do Sub
"""

from typing import Dict, Any, Tuple
import re

class FilterAgent:
    """
    Agente responsável por filtrar perguntas e determinar se estão dentro do escopo
    do Sub (Subsíndico IA) - especialista em gestão condominial e Síndico Pro
    """
    
    def __init__(self):
        # Palavras-chave relacionadas ao universo condominial
        self.condo_keywords = {
            'condomínio', 'condominial', 'síndico', 'subsíndico', 'administração condominial',
            'morador', 'apartamento', 'prédio', 'residencial', 'comercial', 'edifício',
            'assembleia', 'reunião condominial', 'rateio', 'despesas condominiais',
            'manutenção', 'limpeza', 'segurança', 'portaria', 'zelador', 'empregada',
            'elevador', 'piscina', 'academia', 'salao de festas', 'garagem', 'vaga',
            'inadimplência', 'multa', 'juros', 'cobrança', 'processo', 'advogado',
            'convenção', 'regimento interno', 'livro de ocorrências', 'livro de atas',
            'prestação de contas', 'balanço', 'orçamento', 'reserva técnica',
            'reforma', 'obra', 'licitação', 'fornecedor', 'prestador de serviço',
            'seguro', 'incêndio', 'roubo', 'furto', 'vandalismo', 'barulho',
            'animais', 'pet', 'cachorro', 'gato', 'pombo', 'infiltração', 'vazamento',
            'energia elétrica', 'água', 'gás', 'internet', 'tv a cabo', 'telefone',
            'correspondência', 'encomenda', 'delivery', 'visita', 'prestador',
            'funcionário', 'empregado', 'terceirizado', 'contrato', 'recibo',
            'nota fiscal', 'imposto', 'iptu', 'iptu condominial', 'taxa condominial',
            'cota', 'fracão ideal', 'área comum', 'área privativa', 'lazer',
            'playground', 'quadra', 'churrasqueira', 'lavanderia', 'depósito',
            'bicicletário', 'motoboy', 'uber', '99', 'ifood', 'rappi',
            
            # Arquitetura e Engenharia Condominial
            'engenheiro', 'arquiteto', 'projeto', 'construção', 'construcao', 'reforma condominial',
            'obra condominial', 'estrutura', 'fundação', 'fundacao', 'alvenaria', 'hidráulica',
            'hidraulica', 'elétrica', 'eletrica', 'ar condicionado', 'climatização', 'climatizacao',
            'impermeabilização', 'impermeabilizacao', 'pintura', 'acabamento', 'revestimento',
            'azulejo', 'porcelanato', 'granito', 'mármore', 'marmore', 'madeira', 'ferro',
            'alumínio', 'aluminio', 'vidro', 'tijolo', 'cimento', 'areia', 'brita',
            'concreto', 'aço', 'aco', 'ferro', 'tubulação', 'tubulacao', 'encanamento',
            'esgoto', 'dreno', 'calha', 'telhado', 'laje', 'pilar', 'viga', 'coluna',
            'parede', 'teto', 'piso', 'escada', 'rampa', 'corrimão', 'corrimao',
            'porta', 'janela', 'sacada', 'varanda', 'terraço', 'terraco', 'cobertura',
            'subsolo', 'térreo', 'terreo', 'andar', 'pavimento', 'bloco', 'torre',
            'fachada', 'frontispício', 'frontispicio', 'marquise', 'brise', 'cobogó',
            'cobogo', 'graute', 'rejuntamento', 'silicone', 'massa', 'gesso', 'drywall',
            'gesso acartonado', 'forro', 'sanca', 'rodapé', 'rodape', 'guarnição',
            'guarnicao', 'batente', 'folha', 'folha da porta', 'folha da janela',
            'caixilho', 'vidro temperado', 'vidro laminado', 'vidro duplo', 'insulfilm',
            'persiana', 'cortina', 'tela', 'mosquiteiro', 'grade', 'portão', 'portao',
            'cerca', 'muro', 'mureta', 'jardim', 'paisagismo', 'arborização', 'arborizacao',
            'iluminação', 'iluminacao', 'luminária', 'luminaria', 'spot', 'led',
            'sensor', 'automação', 'automacao', 'interfone', 'porteiro eletrônico',
            'porteiro eletronico', 'câmera', 'camera', 'cftv', 'alarme', 'sirene',
            'extintor', 'hidrante', 'sprinkler', 'detector de fumaça', 'detector de fumaca',
            'saída de emergência', 'saida de emergencia', 'escada de incêndio',
            'escada de incendio', 'corredor', 'hall', 'lobby', 'recepção', 'recepcao',
            'área de lazer', 'area de lazer', 'quadra esportiva', 'playground infantil',
            'churrasqueira', 'sala de festas', 'salao de festas', 'lavanderia',
            'depósito', 'deposito', 'garagem', 'vaga', 'box', 'vaga coberta',
            'vaga descoberta', 'estacionamento', 'bicicletário', 'bicicletario',
            'motoboy', 'delivery', 'uber', '99', 'ifood', 'rappi', 'correspondência',
            'correspondencia', 'encomenda', 'visita', 'prestador', 'funcionário',
            'funcionario', 'empregado', 'terceirizado', 'contrato', 'recibo',
            'nota fiscal', 'imposto', 'iptu', 'iptu condominial', 'taxa condominial',
            'cota', 'fracão ideal', 'fracao ideal', 'área comum', 'area comum',
            'área privativa', 'area privativa', 'lazer', 'playground', 'quadra',
            'churrasqueira', 'lavanderia', 'depósito', 'deposito', 'bicicletário',
            'bicicletario', 'motoboy', 'uber', '99', 'ifood', 'rappi',
            
            # Advocacia Condominial
            'advogado condominial', 'advocacia condominial', 'processo condominial',
            'ação condominial', 'acao condominial', 'execução condominial', 'execucao condominial',
            'cobrança judicial', 'cobranca judicial', 'inadimplência', 'inadimplencia',
            'multa condominial', 'juros condominial', 'correção monetária', 'correcao monetaria',
            'penhora', 'embargo', 'protesto', 'notificação extrajudicial', 'notificacao extrajudicial',
            'acordo judicial', 'transação', 'transacao', 'mediação', 'mediacao', 'conciliação',
            'conciliacao', 'arbitragem', 'laudo arbitral', 'sentença', 'sentenca', 'decisão judicial',
            'decisao judicial', 'recurso', 'apelação', 'apelacao', 'agravo', 'mandado de segurança',
            'mandado de seguranca', 'habeas corpus', 'ação popular', 'acao popular',
            'ação civil pública', 'acao civil publica', 'danos morais', 'danos materiais',
            'responsabilidade civil', 'culpa', 'negligência', 'negligencia', 'omissão', 'omissao',
            'falta de vigilância', 'falta de vigilancia', 'segurança', 'seguranca', 'acidente',
            'queda', 'escada', 'elevador', 'piscina', 'área de lazer', 'area de lazer',
            'responsabilidade do síndico', 'responsabilidade do sindico', 'responsabilidade do condomínio',
            'responsabilidade do condominio', 'culpa in vigilando', 'culpa in eligendo',
            'culpa in custodiendo', 'culpa in faciendo', 'culpa in omittendo',
            
            # Contabilidade Condominial
            'contador condominial', 'contabilidade condominial', 'escritório contábil',
            'escritorio contabil', 'prestação de contas', 'prestacao de contas',
            'balanço patrimonial', 'balanco patrimonial', 'demonstração de resultados',
            'demonstracao de resultados', 'dre', 'fluxo de caixa', 'orçamento anual',
            'orcamento anual', 'orçamento mensal', 'orcamento mensal', 'rateio de despesas',
            'rateio condominial', 'cota condominial', 'fracão ideal', 'fracao ideal',
            'área útil', 'area util', 'área construída', 'area construida', 'área total',
            'area total', 'coeficiente de rateio', 'rateio por unidade', 'rateio por área',
            'rateio por area', 'rateio por fração ideal', 'rateio por fracao ideal',
            'despesas ordinárias', 'despesas ordinarias', 'despesas extraordinárias',
            'despesas extraordinarias', 'reserva técnica', 'reserva tecnica', 'fundo de reserva',
            'fundo de obras', 'fundo de emergência', 'fundo de emergencia', 'caixa condominial',
            'conta bancária', 'conta bancaria', 'banco condominial', 'extrato bancário',
            'extrato bancario', 'conciliação bancária', 'conciliacao bancaria',
            'lançamento contábil', 'lancamento contabil', 'debitar', 'creditar',
            'débito', 'debito', 'crédito', 'credito', 'saldo', 'saldo devedor',
            'saldo credor', 'conta a pagar', 'conta a receber', 'fornecedor',
            'prestador de serviço', 'prestador de servico', 'nota fiscal',
            'recibo', 'comprovante', 'documento fiscal', 'imposto condominial',
            'iptu condominial', 'iptu', 'taxa condominial', 'taxa de condomínio',
            'taxa de condominio', 'mensalidade', 'mensalidade condominial',
            'cobrança', 'cobranca', 'inadimplência', 'inadimplencia', 'multa',
            'juros', 'correção monetária', 'correcao monetaria', 'atualização monetária',
            'atualizacao monetaria', 'índice de correção', 'indice de correcao',
            'igpm', 'ipca', 'incc', 'selic', 'cdi', 'taxa de juros', 'mora',
            'juros de mora', 'multa por atraso', 'desconto', 'abatimento',
            'quitação', 'quitacao', 'quitação de débito', 'quitacao de debito',
            'parcelamento', 'acordo de pagamento', 'plano de pagamento',
            'auditoria', 'auditoria contábil', 'auditoria contabil', 'perícia contábil',
            'pericia contabil', 'laudo contábil', 'laudo contabil', 'relatório contábil',
            'relatorio contabil', 'demonstração contábil', 'demonstracao contabil',
            'escrituração', 'escrituracao', 'livro razão', 'livro razao',
            'livro diário', 'livro diario', 'partidas dobradas', 'razão',
            'razao', 'diário', 'diario', 'lançamento', 'lancamento', 'histórico',
            'historico', 'movimentação', 'movimentacao', 'transação', 'transacao',
            'transferência', 'transferencia', 'depósito', 'deposito', 'saque',
            'pagamento', 'recebimento', 'compensação', 'compensacao', 'estorno',
            'cancelamento', 'anulação', 'anulacao', 'correção', 'correcao',
            'ajuste', 'reajuste', 'revisão', 'revisao', 'reclassificação',
            'reclassificacao', 'reversão', 'reversao', 'provisão', 'provisao',
            'contingência', 'contingencia', 'passivo', 'ativo', 'patrimônio',
            'patrimonio', 'patrimônio líquido', 'patrimonio liquido', 'capital',
            'capital social', 'reserva', 'reserva legal', 'reserva estatutária',
            'reserva estatutaria', 'reserva para contingências', 'reserva para contingencias',
            'lucro', 'prejuízo', 'prejuizo', 'resultado', 'resultado do exercício',
            'resultado do exercicio', 'exercício', 'exercicio', 'exercício social',
            'exercicio social', 'ano fiscal', 'ano contábil', 'ano contabil',
            'período', 'periodo', 'mês', 'mes', 'trimestre', 'semestre',
            'ano', 'exercício anterior', 'exercicio anterior', 'exercício atual',
            'exercicio atual', 'exercício seguinte', 'exercicio seguinte'
        }
        
        # Palavras-chave relacionadas ao Síndico Pro
        self.sindico_pro_keywords = {
            'sindico pro', 'sindicopro', 'sistema', 'software', 'aplicativo',
            'dashboard', 'painel', 'relatório', 'relatorio', 'ocorrência', 'ocorrencia',
            'tarefa', 'realização', 'realizacao', 'contrato', 'fornecedor',
            'nps', 'avaliação', 'avaliacao', 'pesquisa', 'enquete', 'votação',
            'votacao', 'enquete', 'poll', 'kanban', 'card', 'coluna', 'status',
            'pendente', 'em andamento', 'concluído', 'concluido', 'atrasado',
            'bloco', 'unidade', 'apartamento', 'morador', 'pessoa', 'usuário',
            'usuario', 'perfil', 'configuração', 'configuracao', 'ajuda',
            'suporte', 'tutorial', 'manual', 'documentação', 'documentacao',
            'funcionalidade', 'feature', 'módulo', 'modulo', 'menu', 'navegação',
            'navegacao', 'login', 'logout', 'senha', 'password', 'email',
            'notificação', 'notificacao', 'alerta', 'lembrete', 'calendário',
            'calendario', 'data', 'prazo', 'vencimento', 'pagamento', 'fatura',
            'boleto', 'pix', 'transferência', 'transferencia', 'banco',
            'conta', 'saldo', 'extrato', 'movimentação', 'movimentacao'
        }
        
        # Perguntas que claramente NÃO são do escopo (mais específicas)
        self.out_of_scope_patterns = [
            # Saúde pessoal (não relacionada ao condomínio)
            r'\b(medic|saúde pessoal|saude pessoal|hospital|clínica médica|clinica medica|consulta médica|exame médico|tratamento médico|doença pessoal|doenca pessoal)\b',
            
            # Direito pessoal (não condominial)
            r'\b(advogado pessoal|processo pessoal|justiça pessoal|justica pessoal|tribunal pessoal|juiz pessoal|promotor pessoal|defensor pessoal|divórcio|divorcio|herança|heranca|testamento|casamento|casamento pessoal)\b',
            
            # Contabilidade pessoal (não condominial)
            r'\b(contador pessoal|contabilidade pessoal|imposto pessoal|receita pessoal|declaração pessoal|declaracao pessoal|imposto de renda pessoal|ir pessoal)\b',
            
            # Psicologia pessoal
            r'\b(psicólogo pessoal|psicologo pessoal|terapeuta pessoal|psiquiatra pessoal|consulta psicológica pessoal|depressão|depressao|ansiedade|estresse|estresse pessoal)\b',
            
            # Odontologia pessoal
            r'\b(dentista pessoal|odontolog pessoal|clínica odontológica pessoal|clinica odontologica pessoal|consulta odontológica|consulta odontologica)\b',
            
            # Especialidades médicas pessoais
            r'\b(urolog pessoal|ginecolog pessoal|cardiolog pessoal|neurolog pessoal|ortoped pessoal|dermatolog pessoal|consulta urológica|consulta ginecológica|consulta cardiológica)\b',
            
            # Educação pessoal
            r'\b(escola pessoal|faculdade pessoal|universidade pessoal|curso pessoal|estudo pessoal|aluno pessoal|professor pessoal|matrícula pessoal|matricula pessoal)\b',
            
            # Entretenimento e lazer pessoal
            r'\b(restaurante pessoal|bar pessoal|lanchonete pessoal|pizzaria pessoal|hambúrguer pessoal|hamburger pessoal|comida pessoal|almoço pessoal|almoco pessoal)\b',
            
            # Viagem pessoal
            r'\b(viagem pessoal|hotel pessoal|passagem pessoal|aéreo pessoal|aereo pessoal|trem pessoal|ônibus pessoal|onibus pessoal|turismo pessoal|férias pessoal|ferias pessoal)\b',
            
            # Transporte pessoal
            r'\b(carro pessoal|moto pessoal|bicicleta pessoal|transporte pessoal|uber pessoal|99 pessoal|taxi pessoal|táxi pessoal|compra de carro|compra de moto)\b',
            
            # Moda e vestuário pessoal
            r'\b(roupa pessoal|sapato pessoal|bolsa pessoal|acessório pessoal|acessorio pessoal|moda pessoal|fashion pessoal|comprar roupa|comprar sapato)\b',
            
            # Tecnologia pessoal
            r'\b(tecnologia pessoal|computador pessoal|celular pessoal|smartphone pessoal|tablet pessoal|laptop pessoal|compra de computador|compra de celular)\b',
            
            # Entretenimento pessoal
            r'\b(filme pessoal|série pessoal|serie pessoal|netflix pessoal|youtube pessoal|instagram pessoal|facebook pessoal|entretenimento pessoal|diversão pessoal|diversao pessoal)\b',
            
            # Música pessoal
            r'\b(música pessoal|musica pessoal|spotify pessoal|deezer pessoal|show pessoal|concerto pessoal|festival pessoal|música pessoal|musica pessoal)\b',
            
            # Esporte pessoal
            r'\b(esporte pessoal|futebol pessoal|basquete pessoal|vôlei pessoal|volei pessoal|tênis pessoal|tenis pessoal|natação pessoal|natacao pessoal|academia pessoal|ginástica pessoal|ginastica pessoal)\b',
            
            # Política pessoal
            r'\b(política pessoal|politica pessoal|eleição pessoal|eleicao pessoal|candidato pessoal|partido pessoal|governo pessoal|votação pessoal|votacao pessoal)\b',
            
            # Religião pessoal
            r'\b(religião pessoal|religiao pessoal|igreja pessoal|templo pessoal|missa pessoal|culto pessoal|oração pessoal|oracao pessoal|religião pessoal|religiao pessoal)\b'
        ]
    
    def analyze_message(self, message: str, context: Dict[str, Any] = None) -> Tuple[bool, str, Dict[str, Any]]:
        """
        Analisa se a mensagem está dentro do escopo do Sub
        
        Args:
            message: Mensagem do usuário
            context: Contexto adicional
            
        Returns:
            Tuple com (está_no_escopo, resposta, metadados)
        """
        message_lower = message.lower()
        
        # Verificar padrões que claramente NÃO são do escopo (mais específicos)
        for pattern in self.out_of_scope_patterns:
            if re.search(pattern, message_lower):
                # Verificar se não há contexto condominial na mensagem
                condo_context_in_message = any(word in message_lower for word in [
                    'condomínio', 'condominial', 'síndico', 'conselho', 'assembleia', 'morador'
                ])
                
                if not condo_context_in_message:
                    return False, self._get_out_of_scope_response(message), {
                        'reason': 'out_of_scope_pattern',
                        'pattern_matched': pattern,
                        'confidence': 'high'
                    }
        
        # Contar palavras-chave relacionadas ao condomínio
        condo_score = sum(1 for keyword in self.condo_keywords if keyword in message_lower)
        
        # Contar palavras-chave relacionadas ao Síndico Pro
        sindico_pro_score = sum(1 for keyword in self.sindico_pro_keywords if keyword in message_lower)
        
        # Verificar se há perguntas sobre funcionalidades do sistema
        system_questions = any(word in message_lower for word in [
            'como', 'onde', 'quando', 'por que', 'porque', 'qual', 'quais',
            'funciona', 'fazer', 'criar', 'editar', 'excluir', 'buscar',
            'filtrar', 'ordenar', 'exportar', 'importar', 'configurar'
        ])
        
        # Verificar contexto condominial na mensagem
        condo_context_words = [
            'condomínio', 'síndico', 'conselho', 'assembleia', 'morador', 'apartamento',
            'prédio', 'edifício', 'bloco', 'unidade', 'área comum', 'área privativa'
        ]
        has_condo_context = any(word in message_lower for word in condo_context_words)
        
        # Verificar se é uma pergunta sobre arquitetura/engenharia condominial
        architecture_engineering_words = [
            'engenheiro', 'arquiteto', 'projeto', 'construção', 'reforma', 'obra',
            'estrutura', 'fachada', 'fundação', 'hidráulica', 'elétrica', 'impermeabilização'
        ]
        has_architecture_context = any(word in message_lower for word in architecture_engineering_words)
        
        # Verificar se é uma pergunta sobre advocacia condominial
        legal_words = [
            'advogado', 'advocacia', 'processo', 'ação', 'acao', 'execução', 'execucao',
            'cobrança judicial', 'cobranca judicial', 'penhora', 'embargo', 'protesto',
            'notificação extrajudicial', 'notificacao extrajudicial', 'acordo judicial',
            'transação', 'transacao', 'mediação', 'mediacao', 'conciliação', 'conciliacao',
            'arbitragem', 'laudo arbitral', 'sentença', 'sentenca', 'decisão judicial',
            'decisao judicial', 'recurso', 'apelação', 'apelacao', 'agravo',
            'responsabilidade civil', 'culpa', 'negligência', 'negligencia', 'omissão', 'omissao'
        ]
        has_legal_context = any(word in message_lower for word in legal_words)
        
        # Verificar se é uma pergunta sobre contabilidade condominial
        accounting_words = [
            'contador', 'contabilidade', 'escritório contábil', 'escritorio contabil',
            'prestação de contas', 'prestacao de contas', 'balanço patrimonial', 'balanco patrimonial',
            'demonstração de resultados', 'demonstracao de resultados', 'dre', 'fluxo de caixa',
            'orçamento anual', 'orcamento anual', 'orçamento mensal', 'orcamento mensal',
            'rateio de despesas', 'rateio condominial', 'coeficiente de rateio',
            'despesas ordinárias', 'despesas ordinarias', 'despesas extraordinárias', 'despesas extraordinarias',
            'reserva técnica', 'reserva tecnica', 'fundo de reserva', 'fundo de obras',
            'conta bancária', 'conta bancaria', 'extrato bancário', 'extrato bancario',
            'lançamento contábil', 'lancamento contabil', 'debitar', 'creditar',
            'saldo', 'conta a pagar', 'conta a receber', 'auditoria', 'auditoria contábil',
            'auditoria contabil', 'perícia contábil', 'pericia contabil', 'laudo contábil',
            'laudo contabil', 'relatório contábil', 'relatorio contabil'
        ]
        has_accounting_context = any(word in message_lower for word in accounting_words)
        
        # Calcular score total
        total_score = condo_score + sindico_pro_score
        
        # Critérios para considerar dentro do escopo (mais rigorosos)
        is_in_scope = (
            total_score >= 1 or  # Pelo menos uma palavra-chave relevante
            (system_questions and sindico_pro_score >= 1) or  # Pergunta sobre sistema + palavra-chave
            (has_architecture_context and has_condo_context) or  # Arquitetura/engenharia + contexto condominial
            (has_architecture_context and self._is_condo_context(context)) or  # Arquitetura + contexto de síndico
            (has_legal_context and has_condo_context) or  # Advocacia + contexto condominial
            (has_legal_context and self._is_condo_context(context)) or  # Advocacia + contexto de síndico
            (has_accounting_context and has_condo_context) or  # Contabilidade + contexto condominial
            (has_accounting_context and self._is_condo_context(context))  # Contabilidade + contexto de síndico
        )
        
        metadata = {
            'condo_score': condo_score,
            'sindico_pro_score': sindico_pro_score,
            'total_score': total_score,
            'system_question': system_questions,
            'has_condo_context': has_condo_context,
            'has_architecture_context': has_architecture_context,
            'has_legal_context': has_legal_context,
            'has_accounting_context': has_accounting_context,
            'confidence': 'high' if total_score >= 2 else 'medium' if total_score >= 1 else 'low'
        }
        
        if is_in_scope:
            return True, "", metadata
        else:
            return False, self._get_out_of_scope_response(message), metadata
    
    def _is_condo_context(self, context: Dict[str, Any] = None) -> bool:
        """Verifica se o contexto indica ser um síndico"""
        if not context:
            return False
        
        user_role = context.get('user_role', '').lower()
        condo_type = context.get('condo_type', '').lower()
        
        return (
            'sindico' in user_role or
            'condominial' in user_role or
            'administrador' in user_role or
            'condo' in condo_type or
            'residencial' in condo_type or
            'comercial' in condo_type
        )
    
    def _get_out_of_scope_response(self, original_message: str) -> str:
        """Gera resposta educada para perguntas fora do escopo"""
        return f"Olá! Sou o Sub, especialista em gestão condominial e no sistema Síndico Pro. 😊\n\nSua pergunta está fora da minha área de atuação. Posso te ajudar com gestão condominial, sistema Síndico Pro, legislação condominial e administração financeira. Como posso te ajudar com seu condomínio?"
