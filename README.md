# Verificador de Integridade de Arquivos

## Descrição

Este projeto verifica a integridade de arquivos de log, detectando alterações ou adulterações.

A verificação é feita com SHA-256 e assinatura digital. O hash e a assinatura são armazenados no PostgreSQL, e a assinatura é cifrada no banco com `pgcrypto`.

## Objetivo

Garantir que arquivos de log não foram modificados sem autorização, ajudando a melhorar a segurança do sistema.

## Configuração

Antes de usar o projeto, crie um arquivo `.env` com suas credenciais:

```bash
cp .env.example .env
```

Depois edite `.env` e defina valores seguros para:
- `POSTGRES_USER`
- `POSTGRES_PASSWORD`
- `PGCRYPTO_PASSPHRASE`

**Importante:** O arquivo `.env` é ignorado pelo Git e não será commitado.

## Funcionalidades

* Calcular hash de arquivos
* Assinar o hash com RSA
* Armazenar hash e assinatura no PostgreSQL
* Cifrar a assinatura no banco com `pgcrypto`
* Verificar alterações nos arquivos
* Atualizar o registro manualmente

## Como testar

```bash
# 1. Criar e ativar o ambiente virtual
.\.venv\Scripts\Activate.ps1

# 2. Instalar dependências
pip install -r requirements.txt

# 3. Subir o PostgreSQL e o serviço da aplicação
docker compose up -d

# Se o banco já foi criado antes, recrie o volume para aplicar o novo schema
# docker compose down -v
# docker compose up -d

# 4. Registrar um arquivo
python main.py init teste.log

# 5. Verificar integridade
python main.py check teste.log

# 6. Atualizar o registro apos mudar um arquivo nao-log
python main.py update arquivo_config.txt
```

### Resultado esperado

* `init` registra o hash e a assinatura do arquivo no banco
* `check` mostra `Arquivo íntegro` se o conteúdo não mudou
* `check` mostra `Arquivo alterado` se o conteúdo mudou
* `check` mostra `Arquivo não monitorado` se o caminho não estiver cadastrado
* `update` é bloqueado para arquivos `.log`

## Casos de teste manuais

Use os comandos abaixo, com o ambiente virtual ativo.

### Caso 1: arquivo íntegro

```bash
python main.py init teste.log
python main.py check teste.log
```

Saída esperada no segundo comando: `Arquivo íntegro`.

### Caso 2: arquivo alterado

```bash
python main.py init teste.log
Add-Content ola.log "alteracao"
python main.py check teste.log
```

Saída esperada no último comando: `Arquivo alterado`.

### Caso 3: arquivo não monitorado

```bash
python main.py check nao_monitorado.log
```

Saída esperada: `Arquivo não monitorado`.

### Observações

* A aplicação usa o banco PostgreSQL configurado no `docker-compose.yml`
* A assinatura é cifrada no PostgreSQL com `pgcrypto`
* O app usa a variável `PGCRYPTO_PASSPHRASE` para gravar e ler a assinatura cifrada
* Se você mudar a passphrase do `pgcrypto`, os registros antigos deixam de ser legíveis até usar a mesma passphrase
* Se o banco já existia antes desta mudança, recrie o volume para aplicar o tipo `bytea` e habilitar `pgcrypto`
* Use apenas `check` para logs. O comando `update` é permitido somente para arquivos nao-log.
## Estrutura de banco

A tabela `hashes` guarda:

* `path`: caminho do arquivo monitorado
* `hash`: hash SHA-256 em texto
* `signature`: assinatura cifrada em `bytea`
* `data_criacao`: data do último cadastro ou atualização

O banco precisa da extensão `pgcrypto` habilitada para usar `pgp_sym_encrypt` e `pgp_sym_decrypt`.

## Fluxo de Desenvolvimento e CI/CD

Este projeto utiliza um fluxo baseado em branches para garantir qualidade e seguranca antes de subir codigo para MAIN.

### Estrutura de branches

* main: branch de producao (codigo estavel)
* dev: branch de desenvolvimento (integracao de features)
* feature/*: branches para desenvolvimento de novas funcionalidades

### Politica de CI para branches

* Push direto para `main` falha no pipeline
* Pull Request para `dev` e `main` deve vir de branch `feature/*`
* Fluxo recomendado: `feature/*` -> `dev` e depois `dev` -> `main`
* Apos push na `dev`, o workflow abre PR automatica de `dev` para `main` quando nao existir uma PR aberta

### Fluxo de trabalho

Criar uma nova feature a partir da dev:

```bash
git checkout dev
git pull origin dev
git checkout -b feature/nome-da-feature
```

Desenvolver a funcionalidade e commitar:

```bash
git add .
git commit -m "feat: descricao da feature"
git push -u origin feature/nome-da-feature
```

Abrir um Pull Request:

* De: feature/nome-da-feature
* Para: dev

Apos aprovacao e testes, fazer merge na dev.

Quando a dev estiver estavel, abrir outro Pull Request:

* De: dev
* Para: main