#!/bin/bash

# ------------------------------
# Configuration
# ------------------------------
BASE_MODEL="llama3.2:latest"
BASE_MODEL_FILE="my_llama3_model"
CUSTOM_MODEL_FILE="my_custom_llama3"
FINE_TUNE_FILE="fine_tune_data.jsonl"
PORT=11434
TEMPERATURE=0.7    # Adjust randomness
NUM_CTX=4096       # Context window for the model

# ------------------------------
# Step 1: Pull Base Model
# ------------------------------
echo "Pulling base model: $BASE_MODEL ..."
ollama pull $BASE_MODEL

# ------------------------------
# Step 2: Save Base Model as Modelfile
# ------------------------------
echo "Saving base model as modelfile: $BASE_MODEL_FILE ..."
ollama save $BASE_MODEL $BASE_MODEL_FILE

# ------------------------------
# Step 3: Prepare Fine-Tuning Data
# ------------------------------
if [ ! -f $FINE_TUNE_FILE ]; then
    echo "Creating sample fine-tune data in $FINE_TUNE_FILE ..."
    cat <<EOL > $FINE_TUNE_FILE
{"prompt": "Hello", "completion": "Hi there!"}
{"prompt": "How are you?", "completion": "I'm doing well, thanks!"}
{"prompt": "Translate English to French: How are you?", "completion": "Comment ça va?"}
EOL
fi

# ------------------------------
# Step 4: Fine-Tune Base Model
# ------------------------------
echo "Fine-tuning base model to create custom modelfile: $CUSTOM_MODEL_FILE ..."
ollama fine-tune $BASE_MODEL_FILE $FINE_TUNE_FILE --name $CUSTOM_MODEL_FILE

# ------------------------------
# Step 5: Serve Fine-Tuned Model with Parameters
# ------------------------------
echo "Starting Ollama server on port $PORT with model: $CUSTOM_MODEL_FILE, temperature: $TEMPERATURE, num_ctx: $NUM_CTX ..."
ollama serve --model $CUSTOM_MODEL_FILE --port $PORT --temperature $TEMPERATURE --num_ctx $NUM_CTX
