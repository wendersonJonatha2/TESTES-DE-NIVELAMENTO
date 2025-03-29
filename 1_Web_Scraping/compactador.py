import zipfile
import os
from pathlib import Path

# Configuração definitiva de caminhos
BASE_DIR = Path(__file__).parent.absolute()  # Pasta 1_Web_Scraping
ANEXOS_DIR = BASE_DIR / 'anexos'
RESULTADOS_DIR = BASE_DIR / 'resultados'

def verificar_arquivos():
    """Verifica se os arquivos existem no local correto"""
    arquivos_necessarios = ['Anexo_I.pdf', 'Anexo_II.pdf']
    faltando = []
    
    for arquivo in arquivos_necessarios:
        if not (ANEXOS_DIR / arquivo).exists():
            faltando.append(arquivo)
    
    if faltando:
        print("\n❌ ERRO: Arquivos não encontrados em:", ANEXOS_DIR)
        for arq in faltando:
            print(f"- {arq}")
        print("\nPor favor:")
        print(f"1. Crie a pasta 'anexos' em: {BASE_DIR}")
        print(f"2. Coloque os arquivos PDF nela")
        return False
    return True

def compactar_anexos(nome_arquivo):
    """Realiza a compactação"""
    try:
        RESULTADOS_DIR.mkdir(exist_ok=True)
        caminho_zip = RESULTADOS_DIR / nome_arquivo
        
        with zipfile.ZipFile(caminho_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for pdf in ['Anexo_I.pdf', 'Anexo_II.pdf']:
                zipf.write(ANEXOS_DIR / pdf, pdf)
                print(f"✓ {pdf} adicionado")
        
        print(f"\n✅ Arquivo criado: {caminho_zip}")
        return True
    except Exception as e:
        print(f"\n❌ Erro na compactação: {e}")
        return False

if __name__ == "__main__":
    print("\n=== COMPACTADOR DE ANEXOS ===")
    print(f"Local correto dos anexos: {ANEXOS_DIR}\n")
    
    if not verificar_arquivos():
        exit(1)
    
    nome = input("Digite seu nome para o arquivo ZIP: ").strip()
    nome_zip = f"Teste_{nome}.zip" if nome else "Teste_Padrao.zip"
    
    compactar_anexos(nome_zip)

    # Adicione no final do script para abrir a pasta de resultados
import os
os.startfile(RESULTADOS_DIR)