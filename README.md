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

## Status do projeto

🚧 Em desenvolvimento
