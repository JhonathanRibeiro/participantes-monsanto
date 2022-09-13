import requests as req
import pandas as pd
import numpy as np
import json

# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Recupera os dados dos usuários 
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
url = 'https://api.monsanto.com/public/vc/legacy/participants/list?crop=SOJA&countryId=1&participantType=POD'
response = req.get(url, timeout=None)
discParticipantes = json.loads(response.content)
participantesCulturaSoja = pd.DataFrame(discParticipantes)
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Renomeando colunas
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
participantesCulturaSoja = participantesCulturaSoja.rename(columns={
    'affiliateDocument':'CNPJ/CPF',
    'affiliateName': 'NOME DO PARTICIPANTE', 
    'affiliateCity':'CIDADE',
    'affiliateStateDesc': 'ESTADO',
    'title': 'TITULO_TAREFA',
    'affiliateTelephone': 'TELEFONE',
    'affiliateFullAddress':'ENDEREÇO'
})
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Criando nova coluna com valor padrão 
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
participantesCulturaSoja['TIPO_DO_PARTICIPANTE'] = 'RECEBEDOR DE GRÃOS'
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Removendo colunas
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
participantesCulturaSoja.pop('affiliateDocumentType')
participantesCulturaSoja.pop('affiliateState')
participantesCulturaSoja.pop('endVigor')
participantesCulturaSoja.pop('participantTypeValue')
# # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# # Alterando ordem das colunas do Dataframe
# # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
participantesCulturaSoja = participantesCulturaSoja[['TIPO_DO_PARTICIPANTE','CNPJ/CPF','NOME DO PARTICIPANTE','ENDEREÇO','ESTADO','CIDADE','TELEFONE']]
# # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# # Usando o ExcelWriter, cria um doc .xlsx, usando engine='xlsxwriter'
# # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
writer = pd.ExcelWriter('relatorio_participantes.xlsx', engine='openpyxl')
# # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# # Salvando os dados na planilha
# # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
participantesCulturaSoja.to_excel(writer, sheet_name='participantes', index=False)
# # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# # Fecha o ExcelWriter e gera o arquivo .xlsx
# # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
writer.save()
print('PLANILHA GERADA COM SUCESSO!')
# # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++