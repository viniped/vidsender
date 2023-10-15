from pathlib import Path

def generate_summary(folder_path: str) -> str:
    video_root = Path(folder_path)
    zip_root = Path("zip_files")  # Pasta "zip_files" no mesmo diretório do script
    
    # Cabeçalho personalizado
    summary = (
        f"⚠️ Atenção ⚠️\n"
        f"Clique aqui para ver o Menu \n"
        f"Utilize as # para saltar entre os vídeos.\n\n"
    )

    # Obtém uma lista ordenada de subpastas em ordem alfabética
    subfolders = sorted([f for f in video_root.iterdir() if f.is_dir()])

    for i, subfolder in enumerate(subfolders):
        # Processa cada subpasta
        video_summary = ""
        video_files = sorted(subfolder.glob('*.mp4'))
        
        for j, video_file in enumerate(video_files):
            video_summary += f"#F{j+1:02} "

        # Adiciona ao resumo apenas se houver arquivos .mp4 na subpasta
        if video_summary:
            if i > 0:
                summary += "\n"  # Adicionar quebra de linha entre as pastas
            summary += f"== {subfolder.name}\n"
            summary += video_summary.rstrip() + "\n"

    # Processa a pasta "zip_files"
    zip_summary = ""
    zip_entries = [entry for entry in zip_root.iterdir() if entry.is_file() and entry.suffix == '.zip']
    
    for i, entry in enumerate(zip_entries):
        zip_summary += f"#M{i+1:02} "

    # Adiciona ao resumo apenas se houver arquivos .zip na pasta "zip_files"
    if zip_summary:
        summary += "\n== Materiais do Curso\n"
        summary += zip_summary.rstrip() + "\n"

    return summary