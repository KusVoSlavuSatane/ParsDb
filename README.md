# Как установить?

Сначала нужно установить uv - менедежер пакет и виртуальных сред

Через скрипт
```pwsh
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Через pip
```pwsh
pip install uv
```

После установки нужно в корне проекта запустить комманду
```pwsh
uv sync
uv run main.py
```

# Починить потом
