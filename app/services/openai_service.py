from openai import OpenAI
from app.config import settings
from typing import Dict

class OpenAIService:
    def __init__(self):
        self.client = OpenAI(api_key=settings.openai_api_key)
    
    def generate_full_summary(self, transcription: str) -> str:
        """Gera resumo completo da transcrição"""
        prompt = f"""Analise a seguinte transcrição de uma sessão de psicoterapia e gere um resumo completo e detalhado.

Transcrição:
{transcription}

Resumo completo:"""
        
        response = self.client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Você é um assistente especializado em análise de sessões de psicoterapia."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3
        )
        
        return response.choices[0].message.content
    
    def generate_anonymous_summary(self, transcription: str) -> str:
        """Gera resumo anonimizado (sem nomes, dados pessoais)"""
        prompt = f"""Analise a seguinte transcrição de uma sessão de psicoterapia e gere um resumo anonimizado que:
1. Remova todos os nomes próprios
2. Remova dados pessoais identificáveis (endereços, telefones, etc.)
3. Seja mais superficial e genérico
4. Pode ser compartilhado com outros profissionais sem expor o paciente
5. Mantenha apenas informações clínicas relevantes de forma genérica

Transcrição:
{transcription}

Resumo anonimizado:"""
        
        response = self.client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Você é um assistente especializado em anonimização de dados clínicos, garantindo privacidade e conformidade ética."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3
        )
        
        return response.choices[0].message.content
    
    def generate_patient_demand(self, transcription: str) -> str:
        """Identifica a demanda trazida pelo paciente"""
        prompt = f"""Analise a seguinte transcrição de uma sessão de psicoterapia e identifique qual foi a demanda principal trazida pelo paciente nesta sessão.

Transcrição:
{transcription}

Demanda do paciente:"""
        
        response = self.client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Você é um assistente especializado em identificar demandas e necessidades em sessões de psicoterapia."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3
        )
        
        return response.choices[0].message.content
    
    def generate_context(self, transcription: str) -> str:
        """Gera contexto da sessão"""
        prompt = f"""Analise a seguinte transcrição de uma sessão de psicoterapia e gere um resumo do contexto da sessão, incluindo:
- Situação atual do paciente
- Temas principais discutidos
- Dinâmica da sessão
- Observações relevantes

Transcrição:
{transcription}

Contexto:"""
        
        response = self.client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Você é um assistente especializado em análise contextual de sessões de psicoterapia."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3
        )
        
        return response.choices[0].message.content
    
    def generate_ia_analysis(self, transcription: str) -> str:
        """Gera análise FAP (Functional Analytic Psychotherapy) baseada no livro 'FAP Descomplicada'"""
        
        # Persona e contexto do sistema
        system_message = """Persona: Você é um(a) supervisor(a) clínico(a) sênior, especialista em Psicoterapia Analítica Funcional (FAP), cujo conhecimento e prática são estritamente baseados na metodologia, princípios e linguagem apresentados no livro "FAP Descomplicada" (cujo conteúdo relevante foi fornecido anteriormente). Seu papel é me orientar na elaboração de evoluções de caso FAP que sejam clinicamente úteis, concisas e funcionalmente precisas, refletindo a aplicação prática da teoria do livro.

Contexto Teórico e Estrutura de Conhecimento (Baseado em "FAP Descomplicada"):

Sua análise e orientação devem derivar exclusivamente das seguintes informações e estruturas conceituais extraídas do livro "FAP Descomplicada":

Objetivo Central: Ajudar o terapeuta a ser consciente, corajoso e habilidoso na interação momento a momento com o cliente, utilizando a relação terapêutica como veículo principal para a mudança comportamental, fundamentado na análise funcional e na Ciência Comportamental Contextual (CBS).

Base Teórica: Behaviorismo Radical, Análise do Comportamento, com forte ênfase na Ciência Comportamental Contextual (CBS), vendo o comportamento como aprendido e funcionalmente determinado pelo contexto (histórico e presente).

Estrutura do Livro: Organizado em Teoria (Parte 1: Ideias - Caps 1-5) e Prática (Parte 2: A Prática - Caps 6-13), com foco na aplicação clínica dos princípios.

Conceitos Teóricos Essenciais (a aplicar):

Análise Funcional: Aplicada primordialmente à relação terapêutica in vivo para entender a função dos comportamentos (antecedentes, respostas, consequências na interação).

Comportamentos Clinicamente Relevantes (CCRs):
- CCR1: Comportamentos-problema do cliente que ocorrem em sessão, funcionalmente ligados aos problemas fora dela.
- CCR2: Comportamentos de melhora/progresso do cliente em sessão.
- Classes Funcionais (FIAT adaptado): Identificar CCRs relacionados à Asserção de Necessidades (A), Comunicação Bidirecional (B), Conflito (C), Autorrevelação/Proximidade (D).

Comportamentos do Terapeuta:
- T1: Comportamentos do terapeuta que interferem no progresso.
- T2: Comportamentos do terapeuta que facilitam o progresso (incluindo aplicação habilidosa das 5 regras).

Modelo Consciência, Coragem e Amor (ACL): Usar como ferramenta de análise funcional da conexão social e guia para a postura terapêutica (avaliar/promover esses aspectos na interação).

As 5 Regras da FAP: Aplicar como guia do processo terapêutico momento a momento: 1. Observar CCRs; 2. Evocar CCRs; 3. Reforçar CCR2; 4. Observar o efeito; 5. Generalizar.

Princípios da CBS: Aplicar conceitos como comportamento aprendido, função do comportamento (apetitivo/aversivo), reforçamento/punição, flexibilidade psicológica (vs. rigidez por regras/história), e o papel da linguagem (RFT brevemente).

Instruções Essenciais de Execução:
- Pergunte Sempre que Necessário: Se informações cruciais para realizar uma análise FAP robusta estiverem faltando ou ambíguas, interrompa a geração da evolução e faça perguntas claras e direcionadas. Não preencha lacunas com suposições.
- Exclusividade FAP (Livro): Sua base de conhecimento e análise é unicamente o conteúdo e a metodologia do livro "FAP Descomplicada" fornecido. Não introduza conceitos ou técnicas de outras abordagens terapêuticas.
- Linguagem FAP (Livro): Utilize consistentemente a terminologia técnica da FAP (CCR1, CCR2, T1, T2, 5 Regras, ACL, Análise Funcional, Evocar, Reforçar, Generalizar, etc.) conforme definida e utilizada no livro.
- Foco Funcional e Relacional: Mantenha o foco na função do comportamento dentro da interação terapêutica. A relação terapêutica é o principal motor da mudança.
- Concisão e Precisão Funcional: Seja sucinto, mas garanta que a análise funcional FAP seja o núcleo da evolução, não apenas uma descrição superficial."""
        
        # Prompt do usuário com formato da evolução FAP
        user_prompt = """Analise a seguinte transcrição de uma sessão de psicoterapia e gere uma evolução FAP completa seguindo rigorosamente o formato abaixo.

FORMATO DA EVOLUÇÃO FAP:

1. Resumo da Sessão:
Gere um breve resumo (2-3 frases) dos principais eventos e processos FAP da sessão.

2. Demanda Trazida e Contexto Inicial:
- Relatos do paciente (eventos privados, comportamentos observáveis fora da sessão, objetivos para a sessão).
- Identifique Antecedentes (A) relevantes para os comportamentos relatados fora da sessão.
- Análise FAP Inicial: Com base na demanda e na conceituação de caso FAP (se disponível), aponte possíveis CCR1s que podem estar funcionalmente relacionados.

3. Intervenção Clínica (FAP in vivo):
- Descreva as ações específicas do terapeuta (perguntas, observações, evocações, reforçamentos, uso de exercícios, etc.).
- Análise Funcional da Intervenção (FAP): Justifique CADA ação principal do terapeuta usando a FAP:
  * Qual(is) das 5 Regras da FAP está(ão) sendo aplicada(s)?
  * Como a intervenção visa observar/evocar/reforçar um CCR específico?
  * Análise ACL: A ação promove Consciência, Coragem ou Amor? É uma resposta de Amor a uma Coragem do cliente?
  * Classifique a intervenção como potencial T1 ou T2 e justifique funcionalmente.

4. Resposta do Paciente (Observação de CCRs - Regra 1):
- Descreva as reações observáveis (comportamento motor, expressões) e os relatos verbais do paciente à intervenção. Diferencie claramente.
- Análise FAP da Resposta: Identifique explicitamente os comportamentos do paciente como potenciais CCR1s ou CCR2s ocorrendo em resposta à intervenção. Explique a função (o que o comportamento busca obter ou evitar naquele momento da interação).
- Análise ACL: A resposta demonstrou Consciência, Coragem, Amor (ou dificuldades nessas áreas)?

5. Análise Funcional ABC Principal da Interação:
Sintetize a principal contingência de três termos (A-B-C) observada durante a interação terapêutica chave da sessão.
- A (Antecedente): Qual ação do terapeuta (T2 ou T1) ou evento imediato precedeu o CCR principal?
- B (Behavior/Comportamento): Qual foi o CCR1 ou CCR2 mais significativo do paciente observado em resposta a A?
- C (Consequência): Qual foi a resposta imediata do terapeuta (potencialmente reforçadora - Regra 3/T2, ou não - T1) e/ou o efeito observado no paciente (Regra 4)?

IMPORTANTE: Se as informações fornecidas não permitirem identificar claramente A, B ou C para esta análise, você DEVE fazer perguntas específicas para obter os detalhes necessários ANTES de tentar completar esta seção ou fazer suposições.

6. Planejamento (Próxima Sessão e Generalização - Regra 5):
- Objetivos FAP específicos para a próxima sessão (Ex: focar em evocar CCR2 de assertividade, observar T1 específico).
- Tarefas de casa (se houver) explicitamente ligadas à prática de CCR2s em contextos externos relevantes (generalização). Descreva a tarefa e sua justificativa funcional FAP, baseando-se nos princípios do Cap. 12 do livro.
- Ações futuras do terapeuta ou ajustes nas estratégias FAP (Ex: variar forma de reforçar, usar exercício específico).

7. Correlação com Sessão Anterior (Opcional):
Breve comparação FAP (progresso em CCR2s específicos, mudanças na frequência de CCR1s, evolução na aplicação das regras, T1s/T2s recorrentes). Adicionar apenas se informações da sessão anterior forem fornecidas.

TRANSCRIÇÃO DA SESSÃO:
{transcription}

Gere a evolução FAP completa seguindo rigorosamente o formato acima, aplicando o conhecimento do livro "FAP Descomplicada" para uma análise funcional precisa e clinicamente útil."""
        
        formatted_prompt = user_prompt.format(transcription=transcription)
        
        response = self.client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": formatted_prompt}
            ],
            temperature=0.3
        )
        
        return response.choices[0].message.content
    
    def anonymize_names_in_transcription(self, transcription: str, patient_name: str, psychologist_name: str) -> str:
        """Substitui nomes de pessoas por letras na transcrição (P para Pedro, R para Rafael, etc.)"""
        prompt = f"""Analise a seguinte transcrição de uma sessão de psicoterapia e substitua todos os nomes próprios de pessoas por letras do alfabeto.

Regras:
- O nome do paciente "{patient_name}" deve ser substituído pela primeira letra do nome (ex: Pedro -> P, Rafael -> R, Maria -> M)
- O nome da psicóloga "{psychologist_name}" deve ser substituído pela primeira letra do nome
- Outros nomes próprios mencionados devem ser substituídos pela primeira letra do nome
- Mantenha o resto do texto exatamente como está
- Preserve a formatação e pontuação

Transcrição:
{transcription}

Transcrição com nomes substituídos por letras:"""
        
        response = self.client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Você é um assistente especializado em anonimização de transcrições, substituindo nomes por letras."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.1
        )
        
        return response.choices[0].message.content
    
    def generate_session_questions(self, transcription: str, patient_name: str, psychologist_name: str) -> list[str]:
        """Gera perguntas sobre a sessão para a psicóloga responder"""
        prompt = f"""Você é um assistente que gera perguntas reflexivas para psicólogos sobre suas sessões de terapia.

REGRAS OBRIGATÓRIAS:
- Use APENAS "Paciente" para se referir ao paciente
- Use "você" para se referir à psicóloga (a pessoa que vai responder as perguntas)
- NUNCA use nomes próprios, letras (como P, R, etc.) ou qualquer identificador pessoal
- Se a transcrição mencionar nomes ou letras, ignore-os completamente e use apenas "Paciente" e "você"

As perguntas devem ser direcionadas à psicóloga, usando "você" quando apropriado. Exemplos:
- "Como você percebeu que o Paciente reagiu quando..."
- "O que você observou sobre a reação do Paciente diante de..."
- "Como você interveio quando o Paciente mencionou..."

Gere entre 3 a 5 perguntas objetivas e específicas baseadas no conteúdo da transcrição.
As perguntas devem ajudar a psicóloga a refletir sobre:
- Reações e comportamentos do Paciente
- Suas próprias intervenções e observações
- Dinâmicas da sessão
- Aspectos importantes que podem ter passado despercebidos

Retorne APENAS as perguntas, uma por linha, sem numeração ou marcadores.
NUNCA mencione nomes próprios, letras ou identificadores pessoais.

Transcrição:
{transcription}

Perguntas:"""
        
        response = self.client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Você é um assistente especializado em análise de sessões de psicoterapia. Você gera perguntas reflexivas direcionadas à psicóloga, usando APENAS 'Paciente' para o paciente e 'você' para a psicóloga. NUNCA use nomes próprios, letras ou identificadores pessoais."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.5
        )
        
        # Separa as perguntas por linha
        questions_text = response.choices[0].message.content.strip()
        questions = [q.strip() for q in questions_text.split('\n') if q.strip()]
        
        return questions
    
    def generate_conclusion(self, transcription: str, context: str, patient_demand: str, analise_da_ia: str, answers: list[str]) -> str:
        """Gera a conclusão final da sessão baseada no contexto, análise e respostas do psicólogo"""
        
        # Formata as respostas para incluir no prompt
        answers_text = "\n".join([f"{i+1}. {answer}" for i, answer in enumerate(answers)]) if answers else "Nenhuma resposta fornecida ainda."
        
        prompt = f"""Você é um assistente especializado em elaborar conclusões de sessões de psicoterapia seguindo a metodologia FAP (Functional Analytic Psychotherapy).

IMPORTANTE: Use APENAS "Paciente" para se referir ao paciente e "você" para se referir à psicóloga. NUNCA use nomes próprios, letras ou identificadores pessoais.

Elabore uma conclusão completa da sessão seguindo RIGOROSAMENTE a estrutura abaixo. Use as informações fornecidas e as respostas da psicóloga às perguntas reflexivas.

ESTRUTURA OBRIGATÓRIA:

0. Resumo da Sessão:
[Breve resumo (2-3 frases) dos principais eventos e processos FAP da sessão]

1. Demanda Trazida e Contexto Inicial:
- Relatos do Paciente: [Descrição dos relatos do paciente]
- Antecedentes (A) Relevantes: [Contexto histórico e imediato]
- Análise FAP Inicial: [CCR1s e CCR2s potenciais identificados]

2. Intervenção Clínica (FAP in vivo):
[Descrição das ações específicas do terapeuta com análise funcional FAP de cada intervenção principal]

3. Resposta do Paciente (Observação de CCRs - Regra 1):
[Descrição das reações e comportamentos do paciente com análise FAP]

4. Análise Funcional ABC Principal da Interação:
[Análise da contingência A-B-C principal observada]

5. Planejamento (Próxima Sessão e Generalização - Regra 5):
- Objetivos FAP Próxima Sessão: [Objetivos específicos]
- Tarefas de Casa: [Se houver, com justificativa FAP]
- Ações Futuras Terapeuta: [Ações e ajustes]

6. Correlação com Sessão Anterior:
[Breve comparação FAP com sessões anteriores, se aplicável]

INFORMAÇÕES DA SESSÃO:

Transcrição:
{transcription}

Contexto:
{context}

Demanda do Paciente:
{patient_demand}

Análise da IA (FAP):
{analise_da_ia}

Respostas da Psicóloga às Perguntas Reflexivas:
{answers_text}

Elabore a conclusão completa seguindo EXATAMENTE a estrutura acima, usando apenas "Paciente" e "você" para se referir às pessoas envolvidas."""
        
        response = self.client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Você é um assistente especializado em análise FAP de sessões de psicoterapia. Você elabora conclusões detalhadas seguindo rigorosamente a metodologia FAP, usando apenas 'Paciente' e 'você' para se referir às pessoas. NUNCA use nomes próprios ou identificadores pessoais."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3
        )
        
        return response.choices[0].message.content
    
    def process_session(self, transcription: str) -> Dict[str, str]:
        """Processa toda a sessão e retorna todos os resultados"""
        return {
            "full_summary": self.generate_full_summary(transcription),
            "anonymous_summary": self.generate_anonymous_summary(transcription),
            "patient_demand": self.generate_patient_demand(transcription),
            "context": self.generate_context(transcription),
            "analise_da_ia": self.generate_ia_analysis(transcription)
        }

