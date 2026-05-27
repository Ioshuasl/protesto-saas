## Compilação do backend

Abrir o repositório api
```bash
cd api
```

**Ambiente virtual python** no linux:
```bash
source venv/bin/activate 
```

**Ambiente virutal python** no windows

```bash
venv\Scripts\activate
```

Iniciar api em modo de desenvolvimento
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```