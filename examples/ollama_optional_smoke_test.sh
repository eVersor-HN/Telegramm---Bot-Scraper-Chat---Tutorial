# Optional. Do this only after the base bot is reliable.
curl -fsSL https://ollama.com/install.sh | sh
ollama --version
ollama run qwen2.5:0.5b
ollama run qwen2.5:1.5b
ollama run qwen2.5:3b

# Huihui examples - check current tags on ollama.com/huihui_ai first.
ollama run huihui_ai/phi4-mini-abliterated
ollama run huihui_ai/qwen3-abliterated
