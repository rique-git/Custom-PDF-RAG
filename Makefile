.PHONY: run docker rebuild clean

# ----------------------------
# Local
# ----------------------------

run:
	@echo "Running Streamlit locally..."
	streamlit run app.py

rebuild:
	@echo "Rebuilding pipeline locally..."
	python -c "from src.pipeline import build_pipeline; build_pipeline(force_rebuild=True)"

clean:
	@echo "Cleaning local artifacts..."
	rm -rf data/processed/*
	rm -rf data/vectorstore/*

pull-model:
	@echo "Pulling Ollama model..."
	@ollama list | grep qwen3:4b-instruct-2507-q4_K_M || \
	ollama pull qwen3:4b-instruct-2507-q4_K_M


# ----------------------------
# Docker
# ----------------------------

docker-run:
	@echo "Starting application with Docker..."
	docker compose up

docker-build:
	@echo "Building and starting application with Docker..."
	docker compose up --build

pull-model-docker:
	@echo "Pulling Ollama model for Docker..."
	docker exec ollama ollama list | grep qwen3 || \
	docker exec -it ollama ollama pull qwen3:4b-instruct-2507-q4_K_M
