# Configuração do Projeto Python

Este guia descreve o passo a passo para configurar o ambiente de desenvolvimento e produção de um projeto Python, incluindo ambiente virtual, dependências, banco de dados, e ajuste de desempenho com múltiplos núcleos.

---

## 1. Clonar o Projeto

Clone o repositório do projeto a partir do Git:

```bash
git clone https://git.oriustecnologia.com/OriusTecnologia/saas_api.git
```

---

## 2. Criar o Ambiente Virtual

Crie um **ambiente virtual** isolado para o projeto:

```bash
python -m venv venv
```

---

## 3. Ativar o Ambiente Virtual

Ative o ambiente virtual antes de instalar as dependências:

```bash
venv\Scripts\activate
```

> **Em sistemas Linux/Mac:**
>
> ```bash
> source venv/bin/activate
> ```

---

## 4. Instalar Dependências do Sistema

O projeto depende de compiladores nativos para algumas bibliotecas Python.

### Windows

Baixe e instale o **Microsoft C++ Build Tools**:
[https://visualstudio.microsoft.com/pt-br/visual-cpp-build-tools/](https://visualstudio.microsoft.com/pt-br/visual-cpp-build-tools/)

Durante a instalação, selecione o pacote:

```
Desktop Development With C++
```

### Linux

Execute no terminal:

```bash
sudo apt update
sudo apt install -y build-essential libpq-dev
```

---

## 5. Instalar as Bibliotecas do Projeto

Com o ambiente virtual **ativado**, instale as dependências listadas no arquivo `requirements.txt`:

```bash
pip install -r requirements.txt
```

---

## 6. Configuração do Banco de Dados (Firebird)

Crie o arquivo **`.env`** na raiz do projeto e configure as variáveis de ambiente necessárias para a conexão com o banco de dados Firebird:

```env
ORIUS_API_FDB_HOST=localhost
ORIUS_API_FDB_NAME=S:/Bases/SANTARITA.FDB
ORIUS_API_FDB_PORT=3050
ORIUS_API_FDB_USER=SYSDBA
ORIUS_API_FDB_PASSWORD=302b3c
ORIUS_API_FDB_CHARSET=UTF8
ORIUS_API_FDB_POOL_PRE_PING=true
ORIUS_API_FDB_POOL_SIZE=5
ORIUS_API_FDB_POOL_MAX_OVERFLOW=10
ORIUS_CLIENT_STATE=go

# Postman (opcional — sync da coleção Orius)
POSTMAN_API_KEY=
POSTMAN_COLLECTION_UID=
```

Essas configurações definem o acesso ao banco, o charset e o gerenciamento de conexões da aplicação.

Para sincronizar a coleção Postman, veja também `postman.sync.env.example` e a [seção 14](#14-sincronização-da-coleção-postman).

---

## 7. Modo Desenvolvimento

Execute a aplicação em ambiente local:

```bash
uvicorn main:app --reload
```

O modo `--reload` recarrega a aplicação automaticamente ao detectar alterações no código.

Acesse a documentação da API em:

```
http://localhost:8000/docs
```

Opcionalmente, para expor a aplicação na rede:

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

---

## 8. Modo Produção

A execução em produção varia conforme o sistema operacional.

---

### **Windows (modo produção simulado)**

O **Gunicorn** não é compatível com Windows, pois depende do módulo `fcntl` exclusivo de sistemas Unix.
Portanto, em ambiente Windows, recomenda-se usar o **Uvicorn** diretamente com múltiplos _workers_:

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

> O parâmetro `--workers` define quantos processos simultâneos serão utilizados.
> Idealmente, use `(número_de_CPUs * 2) + 1`.

#### Alternativa compatível (Windows)

Instale e use o **Hypercorn**, uma alternativa semelhante ao Gunicorn:

```bash
pip install hypercorn
hypercorn main:app --workers 4 --bind 0.0.0.0:8000
```

---

### **Linux (modo produção real)**

Em ambientes Linux (ou Docker), utilize o **Gunicorn** com o **Uvicorn Worker** para obter o máximo desempenho.

#### Instalar Gunicorn (caso ainda não instalado)

```bash
pip install gunicorn uvicorn
```

#### Executar com múltiplos núcleos

```bash
gunicorn main:app \
  -k uvicorn.workers.UvicornWorker \
  --workers 4 \
  --bind 0.0.0.0:8000 \
  --timeout 120 \
  --log-level info
```

#### Parâmetros principais

| Parâmetro                          | Função                                   |
| ---------------------------------- | ---------------------------------------- |
| `-k uvicorn.workers.UvicornWorker` | Usa o Uvicorn como worker ASGI           |
| `--workers 4`                      | Define o número de núcleos usados        |
| `--bind 0.0.0.0:8000`              | Expõe a aplicação em todas as interfaces |
| `--timeout 120`                    | Tempo limite de resposta (em segundos)   |
| `--log-level info`                 | Define o nível de logs                   |

#### Dica de cálculo de workers

```
(número_de_CPUs * 2) + 1
```

Exemplo: servidor com 2 CPUs → `--workers 5`

---

### **Execução em segundo plano (Linux)**

Para rodar a aplicação continuamente:

```bash
nohup gunicorn main:app -k uvicorn.workers.UvicornWorker --workers 4 --bind 0.0.0.0:8000 &
```

Verifique se está rodando:

```bash
ps aux | grep gunicorn
```

---

## 9. Logs e Monitoramento

É possível direcionar os logs de acesso e erro para arquivos dedicados:

```bash
gunicorn main:app \
  -k uvicorn.workers.UvicornWorker \
  --workers 4 \
  --bind 0.0.0.0:8000 \
  --access-logfile logs/access.log \
  --error-logfile logs/error.log
```

---

## 10. Estrutura Recomendada de Deploy

```
/app
├── main.py
├── api/
├── packages/
├── requirements.txt
├── logs/
│   ├── access.log
│   └── error.log
└── systemd/
    └── saas_api.service
```

---

## 11. Resumo dos Comandos

| Etapa                       | Comando                                                                              |
| --------------------------- | ------------------------------------------------------------------------------------ |
| Clonar projeto              | `git clone https://git.oriustecnologia.com/OriusTecnologia/saas_api.git`             |
| Criar venv                  | `python -m venv venv`                                                                |
| Ativar venv                 | `venv\Scripts\activate` _(Windows)_<br>`source venv/bin/activate` _(Linux/Mac)_      |
| Instalar dependências       | `pip install -r requirements.txt`                                                    |
| Rodar em desenvolvimento    | `uvicorn main:app --reload`                                                          |
| Rodar em produção (Windows) | `uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4`                            |
| Rodar em produção (Linux)   | `gunicorn main:app -k uvicorn.workers.UvicornWorker --workers 4 --bind 0.0.0.0:8000` |
| Alternativa (Windows)       | `hypercorn main:app --workers 4 --bind 0.0.0.0:8000`                                 |
| Sync coleção Postman        | `python3 scripts/sync_postman_collection.py` (ver [seção 14](#14-sincronização-da-coleção-postman)) |

---

## 12. Recomendações Finais

- Em **Windows**, use Uvicorn ou Hypercorn apenas para testes e ambientes locais.
- Para **produção real**, use **Linux** com Gunicorn + Uvicorn Worker, idealmente em container **Docker**.
- Monitore o consumo de CPU/RAM e ajuste o número de _workers_ conforme o ambiente.
- Automatize o serviço em produção via **systemd** (ex: `/etc/systemd/system/saas_api.service`) para iniciar junto com o servidor.

---

uvicorn main:app --host 0.0.0.0 --port 8000

## 13. Configuração de acesso ao Firebird

1. Configurar o Firebird para aceitar conexões remotas:
   Como o Firebird está "fora" do Docker, ele pode estar configurado para ouvir apenas em localhost. Para o Docker conseguir conectar, o Firebird precisa ouvir na interface de rede do Docker ou em todas as interfaces.

No arquivo firebird.conf (geralmente em /opt/firebird), verifique a linha: RemoteBindAddress =

Mude para: RemoteBindAddress = 0.0.0.0 (ou apenas para o IP 172.17.0.1).

Reinicie o serviço do Firebird.

1. Configurar as Variáveis no Easypanel:
   Na aba Environment do seu serviço no Easypanel, configure sua conexão assim:

ORIUS_API_FDB_HOST=172.17.0.1

---

## 14. Sincronização da coleção Postman

A coleção de testes da API fica em `Orius.postman_collection.json` na raiz de `api/`. O script `scripts/sync_postman_collection.py` envia esse arquivo para a coleção **Orius** na nuvem do Postman via [Postman API](https://www.postman.com/postman/postman-public-workspace/documentation/12959542-c8142d51-e97c-46b8-7705-0e9d27a4b4e2), sem dependências extras (apenas biblioteca padrão do Python).

### Pré-requisitos

1. **API key** — Postman → Settings → API keys → Generate API Key.
2. **Coleção na conta** — a coleção **Orius** já deve existir no Postman (importe `Orius.postman_collection.json` manualmente na primeira vez, se necessário).
3. Variáveis no `api/.env` (modelo em `postman.sync.env.example`):

```env
POSTMAN_API_KEY=sua_api_key
# Opcional: obrigatório se houver mais de uma coleção com o mesmo nome
POSTMAN_COLLECTION_UID=
# Opcional: outro caminho para o JSON
# POSTMAN_COLLECTION_FILE=Orius.postman_collection.json
```

O **UID** da coleção aparece em Postman → coleção Orius → `…` → **Info** → **UID** (formato `12345678-uuid-...`). Se existir apenas uma coleção chamada **Orius**, o script descobre o UID automaticamente.

### Comandos

Execute sempre a partir da pasta `api/`:

```bash
# Validar JSON local (sem chamar a API)
python3 scripts/sync_postman_collection.py --dry-run

# Listar coleções da conta (para copiar o UID)
python3 scripts/sync_postman_collection.py --list

# Enviar uma vez
python3 scripts/sync_postman_collection.py

# Tempo real: reenvia ~1,5 s após cada salvamento do arquivo
python3 scripts/sync_postman_collection.py --watch
```

| Flag | Descrição |
|------|-----------|
| `--dry-run` | Valida o JSON; não usa `POSTMAN_API_KEY` |
| `--list` | Lista UID e nome das coleções da API key |
| `--watch` | Observa o arquivo e sincroniza após cada save (debounce 1,5 s) |
| `--file CAMINHO` | JSON alternativo (padrão: `Orius.postman_collection.json`) |

### Boas práticas

- Corpos **raw JSON** nas requisições devem incluir `options.raw.language: "json"` (e, quando fizer sentido, header `Content-Type: application/json`), para o Postman não abrir o body como texto.
- Após alterar endpoints no CRUD, atualize a pasta correspondente na coleção e rode o sync (ou deixe `--watch` ativo durante a implementação).
- O arquivo exportado (~1,7 MB) não traz `id`/`uid` por item; o `PUT` substitui o conteúdo da coleção na nuvem — adequado quando o repositório Git é a fonte da verdade.
