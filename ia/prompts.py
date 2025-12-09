from groq import Groq
import os

from dotenv import load_dotenv
load_dotenv()

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

def gerar_pdi_simples(titulo_pdi, descricao_usuario):
    prompt = f"""
Você é uma IA especialista em Desenvolvimento Individual.

Gere automaticamente:

1) 3 METAS recomendadas
   - Cada meta deve conter:
       • título
       • descrição
       • 2–3 tarefas recomendadas
           - cada tarefa deve ter: título e descrição

2) 3 PROJETOS recomendados
   - Cada projeto deve conter:
       • título
       • descrição
       • 2–3 tarefas recomendadas
           - cada tarefa deve ter: título e descrição

Retorne EXATAMENTE neste formato JSON:

{{
  "metas": [
    {{
      "titulo": "...",
      "descricao": "...",
      "tarefas": [
        {{
          "titulo": "...",
          "descricao": "..."
        }}
      ]
    }}
  ],
  "projetos": [
    {{
      "titulo": "...",
      "descricao": "...",
      "tarefas": [
        {{
          "titulo": "...",
          "descricao": "..."
        }}
      ]
    }}
  ]
}}
"""

    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
    )

    return response.choices[0].message.content

