
# SahAI

Offline, voice-first AI ledger for Tamil-speaking shopkeepers, built for Snapdragon-powered HP PCs.

Example: "இன்று 5 கிலோ அரிசி 300 ரூபாய்க்கு விற்றேன்" (Today I sold 5 kg rice for ₹300)
becomes a saved ledger entry: sale, rice, 5 kg, ₹300.

## Pipeline
Speech → Whisper-tiny (ASR) → Llama 3.2 1B (intent) → validator → SQLite ledger → optional sync.
Models are optimized with Qualcomm AI Hub for the Snapdragon NPU.

## Current status
- Built and tested: `ledger_parser.py` parses Tamil and English sentences into structured entries, validates them and writes to SQLite.
- Next: run Whisper-tiny and Llama 3.2 1B on a Snapdragon HP PC via Qualcomm AI Hub and measure speed and accuracy.

## Run the parser
python ledger_parser.py

Requires Python 3. No extra packages needed.

Built with Llama (Meta). Speech model: Whisper (OpenAI).
