
# Como enviar este projeto para o GitHub

## Opção A — Upload pela interface (mais simples)
1. Acesse seu repositório no GitHub (ou crie um novo vazio).
2. Clique em **Add file** → **Upload files**.
3. Extraia o `.zip` deste projeto e **arraste o conteúdo da pasta** `DataFlow-Cloudification-Project/` (não a pasta em si) para a página.
4. Clique em **Commit changes** (mensagem sugerida: `chore: bootstrap dataflow lakehouse portfolio`).

## Opção B — Linha de comando (git)
```bash
unzip DataFlow-Cloudification-Project_full.zip
cd DataFlow-Cloudification-Project

git init
git add .
git commit -m "chore: bootstrap dataflow lakehouse portfolio"
git branch -M main
git remote add origin https://github.com/<usuario>/<repositorio>.git
git push -u origin main
```

> Dica: se você já possui um repositório criado com conteúdo, apenas **copie os arquivos** para a pasta do seu repo local, faça `git add . && git commit && git push`.
