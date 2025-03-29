import pandas as pd
import tabula
import zipfile
import os
from pathlib import Path
import warnings


warnings.filterwarnings('ignore')


BASE_DIR = Path(__file__).parent
INPUT_DIR = BASE_DIR / "input"
OUTPUT_DIR = BASE_DIR / "output"


INPUT_DIR.mkdir(exist_ok=True)
OUTPUT_DIR.mkdir(exist_ok=True)

def extrair_tabela_pdf():
    """Extrai tabelas do PDF com tratamento de erros"""
    caminho_pdf = INPUT_DIR / "Anexo_I.pdf"
    
    if not caminho_pdf.exists():
        print(f"❌ Arquivo não encontrado: {caminho_pdf}")
        return None

    print("⏳ Extraindo tabelas...")
    
    try:
        
        dfs = tabula.read_pdf(
            str(caminho_pdf),
            pages='all',
            multiple_tables=True,
            encoding='latin-1',
            guess=False,
            stream=True
        )
        
        if not dfs:
            print("⚠️ Nenhuma tabela encontrada no PDF")
            return None
            
        df = pd.concat(dfs, ignore_index=True)
        print(f"✅ {len(df)} registros extraídos")
        return df
        
    except Exception as e:
        print(f"❌ Erro na extração: {str(e)}")
        return None

def processar_dados(df):
    """Processa e limpa os dados"""
    if df is None:
        return None
    
    
    df.replace({
        "OD": "Odontológico",
        "AMB": "Ambulatorial"
    }, inplace=True)
    
    
    df.dropna(how='all', inplace=True)
    
    return df

def salvar_resultados(df, nome):
    """Salva CSV e cria ZIP"""
    if df is None or df.empty:
        return False

    nome_csv = f"Rol_Procedimentos_{nome}.csv"
    nome_zip = f"Teste_{nome}.zip"
    
    
    try:
        df.to_csv(OUTPUT_DIR / nome_csv, index=False, encoding='utf-8-sig')
        print(f"💾 CSV salvo: {OUTPUT_DIR / nome_csv}")
    except Exception as e:
        print(f"❌ Erro ao salvar CSV: {e}")
        return False

    
    try:
        with zipfile.ZipFile(OUTPUT_DIR / nome_zip, 'w') as zipf:
            zipf.write(OUTPUT_DIR / nome_csv, arcname=nome_csv)
        print(f"📦 ZIP criado: {OUTPUT_DIR / nome_zip}")
        return True
    except Exception as e:
        print(f"❌ Erro ao criar ZIP: {e}")
        return False

if __name__ == "__main__":
    print("\n" + "="*50)
    print("  TRANSFORMADOR DE DADOS - ANS")
    print("="*50 + "\n")
    
    nome = input("Digite seu nome para o arquivo: ").strip() or "Padrao"
    
    df = extrair_tabela_pdf()
    df = processar_dados(df)
    
    if df is not None:
        salvar_resultados(df, nome)
    
    print("\n✅ Processo finalizado!")