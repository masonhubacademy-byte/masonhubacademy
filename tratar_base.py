import pandas as pd
import re

def limpar_telefone(phone):
    if pd.isna(phone):
        return None
    # Remove qualquer caractere que não seja número
    nums = re.sub(r'\D', '', str(phone))
    
    # Se começar com 0, remove o zero do DDD
    if nums.startswith('0'):
        nums = nums[1:]
        
    # Adiciona o DDI 55 se tiver apenas 10 ou 11 dígitos (DDD + Número)
    if len(nums) in [10, 11]:
        nums = '55' + nums
        
    return nums

def processar_leads(caminho_arquivo):
    try:
        # Carrega o arquivo Excel
        df = pd.read_excel(caminho_arquivo)
        total_inicial = len(df)
        
        # 1. Filtra registros cujo status não seja 'Resolvido'
        # Ajuste o nome da coluna 'Status' se na sua planilha estiver diferente
        if 'Status' in df.columns:
            df = df[df['Status'].astype(str).str.strip().str.lower() != 'resolvido']
        
        # Padroniza a coluna de nome, se existir
        coluna_nome = [col for col in df.columns if 'nome' in col.lower() or 'lead' in col.lower() or 'cliente' in col.lower()]
        if coluna_nome:
            target_nome = coluna_nome[0]
            df['Nome_Tratado'] = df[target_nome].astype(str).str.strip().str.title()
        
        # 2. Higieniza a coluna de telefone
        # Ajuste o nome da coluna 'Telefone' se na sua planilha estiver como 'WhatsApp' ou 'Contato'
        coluna_telefone = [col for col in df.columns if 'tel' in col.lower() or 'whats' in col.lower()]
        if coluna_telefone:
            target_col = coluna_telefone[0]
            df['Telefone_Limpo'] = df[target_col].apply(limpar_telefone)
            # Remove linhas onde o telefone ficou inválido
            df = df[df['Telefone_Limpo'].notnull()]
            # Compatibilidade com o seu código anterior caso use essa nomenclatura no futuro
            df['WhatsApp_Formatado'] = df['Telefone_Limpo'] 
        
        # 3. Salva a base tratada
        caminho_saida = 'E:\\MAÇONARIA\\MASONHUBACADEMY\\leads_tratados.csv'
        df.to_csv(caminho_saida, index=False, encoding='utf-8-sig')
        
        print(f"=== PROCESSAMENTO CONCLUÍDO ===")
        print(f"Leads iniciais: {total_inicial}")
        print(f"Leads ativos prontos para envio: {len(df)}")
        print(f"Arquivo gerado: {caminho_saida}")
        
    except Exception as e:
        print(f"Erro ao processar planilha: {e}")

if __name__ == '__main__':
    # Tenta com a extensao dupla que consta na sua pasta, depois com a normal
    try:
        processar_leads('E:\\MAÇONARIA\\MASONHUBACADEMY\\leads.xlsx.xlsx')
    except Exception:
         processar_leads('E:\\MAÇONARIA\\MASONHUBACADEMY\\leads.xlsx')