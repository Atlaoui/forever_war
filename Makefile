.PHONY: run stop install lock clean

# Run the game
run:
	@.venv/bin/python main.py

# Stop the game (kill any running instance)
stop:
	@pkill -f "python.*main.py" 2>/dev/null || echo "No game process found"

# Install dependencies from lock file
install:
	uv venv
	uv pip install -r requirements.lock

# Generate/update lock file from requirements.txt
lock:
	uv pip compile requirements.txt -o requirements.lock

# Clean up
clean:
	@rm -rf __pycache__ src/__pycache__
	@echo "Cleaned pycache files"
