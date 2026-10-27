# Documentação - Gerenciador de Senhas

Gerenciador de senhas em Python com CustomTkinter. Armazena senhas em arquivo texto (`senhas.txt`) e separa interface da lógica de negócio.

---

## Estrutura do Projeto

| Arquivo | Responsabilidade |
|---|---|
| `main.py` | Janela principal e widgets |
| `config.py` | Constantes, temas, cores e caminhos |
| `commands.py` | Lógica de negócio e manipulação de arquivo |
| `password_details_window.py` | Janela de edição/visualização (instância única) |
| `notification.py` | Toasts de aviso |
| `senhas.txt` | Dados persistidos (nome/senha) |

---

## Execução

```bash
python main.py
```

Depende de:

```bash
pip install customtkinter pyperclip
```

---

## Formato do Arquivo `senhas.txt`

Texto puro, UTF-8. Cada senha ocupa **duas linhas**:

```
Gmail
senhaDoGmail
GitHub
outraSenha123
Banco
senhaDoBanco
```

Regras:
- Linha ímpar = nome da senha
- Linha par = senha
- Sempre pares completos (nome + senha)

---

## Manipulação do Arquivo

### Carregar Senhas (`carregar_senhas_salvas`)

Lê o arquivo linha a linha, remove espaços e monta um dicionário:

```python
self.senhas_salvas = {'Gmail': 'senhaDoGmail', ...}
```

### Salvar Senha (`salvar_senha`)

- Valida nome e senha não vazios
- Verifica duplicidade com `senha_existe(nome)`
- Abre o arquivo em modo `append` (`'a'`) e acrescenta nome + senha
- Recarrega a combobox

### Editar Senha (`editar_senha`)

- Atualiza o dicionário em memória
- **Reescreve todo o arquivo** com modo `write` (`'w'`)
- Recarrega a combobox
- Retorna `0` em sucesso ou `-1` em erro

### Excluir Senha (`excluir_senha`)

- Remove do dicionário
- **Reescreve todo o arquivo** sem o item excluído
- Mostra notificação de sucesso

> **Atenção:** exclusão e edição reescrevem o arquivo inteiro. Se houver falha na gravação, o arquivo original é preservado.

---

## Funcionalidades

| Ação | Método | Descrição |
|---|---|---|
| Gerar senha | `gerar_senha()` | Sorteia caracteres de `CHARACTER_SET` conforme tamanho do slider |
| Copiar senha | `copiar_senha(senha)` | Usa `pyperclip.copy()` e exibe toast |
| Salvar senha | `salvar_senha()` | Valida e acrescenta ao arquivo |
| Ver detalhes | `ver_senha()` | Abre janela de edição (instância única) |
| Editar senha | `editar_senha()` | Atualiza nome/senha e reescreve arquivo |
| Excluir senha | `excluir_senha()` | Remove item e reescreve arquivo |
| Carregar senhas | `carregar_senhas_salvas()` | Lê o arquivo e preenche o dicionário |

---

## Janela de Detalhes

`PasswordDetailsWindow` implementa **singleton**:
- Apenas uma janela aberta por vez
- Se já existir, traz para frente e foca
- Destruição limpa a referência para permitir recriação

---

## Variáveis Principais

| Variável | Tipo | Uso |
|---|---|---|
| `self.app.length_var` | `ctk.IntVar` | Tamanho escolhido (12-30) |
| `self.app.generated_password_var` | `ctk.StringVar` | Senha gerada |
| `self.app.password_name_var` | `ctk.StringVar` | Nome para salvar |
| `self.app.selected_password_var` | `ctk.StringVar` | Nome selecionado na combobox |
| `self.commands.senhas_salvas` | `dict` | `{nome: senha}` em memória |

---

## Fluxo de Trabalho

1. **Início:** `main.py` inicia, carrega `senhas.txt` e preenche a combobox
2. **Gerar:** usuário ajusta slider e clica em "Gerar senha"
3. **Salvar:** usuário digita nome e clica em "Salvar" → grava no arquivo
4. **Selecionar:** usuário escolhe um item da combobox → senha aparece na caixa de texto
5. **Editar:** usuário clica em "Ver detalhes", altera campos e clica em "Salvar alterações"
6. **Copiar:** usuário clica em "Copiar" → senha vai para a área de transferência
7. **Excluir:** usuário clica em "Excluir" → remove do arquivo e do dicionário

---

## Limitações e Pontos de Atenção

- **Sem criptografia:** senhas ficam em texto puro no arquivo
- **Exclusão sem confirmação:** não pede confirmação antes de apagar
- **Combobox não atualiza após excluir:** os dados somem da lista apenas ao recarregar/reabrir o app
- **Arquivo corrompido:** número ímpar de linhas pode causar `IndexError`
- **Campos não são limpos após salvar**
- **Janela de detalhes não atualiza os campos** se já estiver aberta
- **Caminho relativo:** execute `main.py` dentro da pasta do projeto

