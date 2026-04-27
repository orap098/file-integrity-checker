# Verificador de Integridade de Arquivos

## Descrição

Este projeto tem como objetivo desenvolver uma ferramenta que verifica a integridade de arquivos de log, detectando possíveis alterações ou adulterações.

A verificação é feita através do cálculo de hashes utilizando o algoritmo SHA-256, comparando os valores atuais com os previamente armazenados.

## Objetivo

Garantir que arquivos de log não foram modificados sem autorização, ajudando a melhorar a segurança do sistema.

## Funcionalidades (planejadas)

* Calcular hash de arquivos
* Armazenar hashes de referência
* Verificar alterações nos arquivos
* Identificar possíveis adulterações
* Atualizar hashes manualmente

## Como usar (planejado)

```bash
# Inicializar hashes
./integrity-check init <caminho>

# Verificar integridade
./integrity-check check <caminho>

# Atualizar hash
./integrity-check update <caminho>
```
## Fluxo de Desenvolvimento e CI/CD

Este projeto utiliza um fluxo baseado em branches para garantir qualidade e seguranca antes de subir codigo para producao.

### Estrutura de branches

* main: branch de producao (codigo estavel)
* dev: branch de desenvolvimento (integracao de features)
* feature/*: branches para desenvolvimento de novas funcionalidades

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

## Status do projeto

🚧 Em desenvolvimento
