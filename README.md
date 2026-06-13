# movie-script-preprocessor-project

## Overview

**movie-script-preprocessor-project** is a Python-based preprocessing pipeline for linguistic analysis of Russian-language dialogue scripts.

The program processes annotated dialogue files (UTF-8, .txt) in the format:

```text
[character_name] dialogue text
```
It recursively finds all .txt files inside raw_scripts/ and aggregates dialogue across files.

Automatically:

* extracts character names and normalises them (lowercase, ё → е)
* groups all utterances by character into per‑character corpora
* performs sentence segmentation and tokenisation using UDPipe
* generates morphosyntactic annotations in CoNLL‑U format
* converts the annotated data into AntConc‑ready plain‑text corpora (word forms only, order preserved)

The resulting corpora can be used for:
* lexical analysis
* stylistic comparison between characters
* frequency analysis
* morphosyntactic analysis
* linguistic profiling
* corpus-based research using AntConc


---

## Table of contents

* [Overview](#overview)
* [Project goal](#project-goal)
* [Pipeline description](#pipeline-description)
* [Project structure](#project-structure)
* [System requirements](#system-requirements)
* [Installation and setup](#installation-and-setup)
* [Input format](#input-format)
  * [Supported format](#supported-format)
  * [Dialogue format](#dialogue-format)
* [Processing pipeline](#processing-pipeline)
  * [1. Input stage](#1-input-stage)
  * [2. Preprocessing stage](#2-preprocessing-stage)
  * [3. UDPipe analysis stage](#3-udpipe-analysis-stage)
  * [4. Conversion stage](#4-conversion-stage)
* [Running the program](#running-the-program)
* [Output](#output)
* [Implementation notes](#implementation-notes)
* [License](#license)

---

## Project goal

The goal of the project is to convert raw annotated dialogue scripts into linguistically enriched corpora using UDPipe, enabling syntactic analysis and downstream corpus processing in tools such as AntConc.

---

## Pipeline description

The pipeline consists of four sequential stages with clearly defined input/output contracts. Each stage produces an intermediate representation required for the next stage.

### 1. Input stage

Raw script files are placed manually into:

raw_scripts/

Example input:

```text
[character_name] dialogue text
```

If multiple input files are present, all dialogue lines are processed sequentially and aggregated into a single corpus per character across all files.

---

### 2. Preprocessing stage

The preprocessing stage performs only structural cleanup – no lemmatisation, stopword removal, or other linguistic transformations.

Steps:

Extract character names from [...] and normalise (lowercase, ё→е).

For each dialogue line, extract the text after the closing bracket.

Keep the original line order; do not merge or split lines.

Write the cleaned text (one line per original dialogue line) into cleaned_scripts/<character>_cleaned.txt.

Example:
Input: [крош] Привет! Как дела?
Output in крош_cleaned.txt: Привет! Как дела?

Note: If a character has no dialogue tokens (e.g. [крош] with empty text), the file will be empty.

| Input line format | Behavior                              |
| ----------------- | ------------------------------------- |
| `[крош] Привет!`  | processed                             |
| `[крош]`          | character registered, no tokens added |
| `крош Привет!`    | ignored                               |
| `крош: Привет!`   | ignored                               |
| `[крош Привет!`   | ignored                               |

---

### 3. UDPipe analysis stage

The cleaned character files are processed by UDPipe using the Russian model:
assets/model/russian-syntagrus-ud-2.0-170801.udpipe

UDPipe performs sentence segmentation and tokenization directly on raw text. Preprocessing does not perform any token-level operations to avoid interfering with model-level linguistic decisions.

Input: cleaned_scripts/*_cleaned.txt (UTF-8).
Output: input_conllu/<character>.conllu in CoNLL‑U format (version 2.0).

UDPipe performs:

* sentence segmentation (respects ., !, ? etc.)
* morphological analysis (lemma, UPOS, XPOS, features)
* dependency parsing (heads, relations)

If a cleaned file is empty, no .conllu file is generated.
The model is included in the repository – no additional download is required.

---

### 4. Conversion stage

converter.py reads each .conllu file and extracts token-level representations from the FORM column (optionally enriched with annotation depending on configuration)
It then writes these word forms sequentially into a plain text file, separated by spaces.

Important:

Linguistic annotations (lemmas, POS tags, dependency relations) are not preserved in the final .txt files – they are only available in the intermediate .conllu files.

Word order is preserved as produced by UDPipe within each sentence and token stream.

Sentence boundaries are not marked in the output (AntConc treats the whole file as a single stream of tokens).

Example:
CoNLL-U token line: 1 Привет привет INTJ _ _ _ _ _
Extracted word form: Привет

Output file output_antconc/крош_ready.txt might contain:
Привет как дела иди сюда

---

## Project structure

```text
movie-script-preprocessor-project/
│
├── assets/model/                                # UDPipe model used for morphological
│   └── russian-syntagrus-ud-2.0-170801.udpipe   # and syntactic annotation
│
├── raw_scripts/                                 # Place input dialogue scripts here
│   └── *.txt
│
├── cleaned_scripts/                             # Automatically generated intermediate corpora
│   └── *_cleaned.txt
│
├── input_conllu/                                # Automatically generated UDPipe output
│   └── *.conllu
│
├── output_antconc/                              # Automatically generated final corpora
│   └── *_ready.txt
│
├── main.py                                      # Program entry point
├── processor.py                                 # Script preprocessing logic
├── converter.py                                 # CoNLL-U to AntConc conversion
├── requirements.txt                             # Project dependencies
├── .gitignore
├── LICENSE
└── README.md
```

---

## System requirements

Python 3.8+
pip

Dependencies:
ufal.udpipe

---

## Installation and setup

### 1. Create virtual environment

* Windows
python -m venv venv
venv\Scripts\activate

* Linux/macOS
python3 -m venv venv
source venv/bin/activate

### 2. Install dependencies
pip install -r requirements.txt

Then verify UDPipe model exists
ls assets/model/russian-syntagrus-ud-2.0-170801.udpipe

---

## Input format

### Supported format

All input scripts must be .txt files encoded in UTF-8.
Place them inside raw_scripts/. The program searches recursively (**/*.txt), so files in subdirectories are also processed.

If multiple files exist, all dialogue lines are read sequentially and merged into a single corpus per character.

### Dialogue format

```text
[character_name] dialogue text
```

Example:

```text
[крош] Привет!
[ежик] Здравствуй!
```

---

## Processing pipeline

### 1. Input stage

System scans `raw_scripts/` for `.txt` files.

---

### 2. Preprocessing stage

* extract character names
* clean dialogue minimally
* serves as an intermediate representation preserving original dialogue structure before UDPipe processing
* prepare text for UDPipe

---

### 3. UDPipe analysis stage

Model:

assets/model/russian-syntagrus-ud-2.0-170801.udpipe

* sentence splitting
* tokenization
* CoNLL-U generation

---

### 4. Conversion stage

converter.py:

* reads `input_conllu/`
* converts tokens
* outputs AntConc-compatible text

---

## Running the program

```bash
python main.py
```

Pipeline automatically:

* reads scripts
* runs UDPipe
* generates `.conllu`
* converts output

---

## Output

### Intermediate

input_conllu/ежик_cleaned.conllu – contains full morphological and syntactic annotation for debugging or advanced analysis.

### Final
output_antconc/ежик_ready.txt – plain text, one space between words, no metadata.

Example of output_antconc/крош_ready.txt:

привет друг пошли гулять снег идёт весело

Each file is named after the normalised character name, followed by _ready.txt.

---

## Implementation notes

* All .txt files inside raw_scripts/ are processed recursively; corpora are merged across files per character.
* UDPipe model is fixed (Russian‑SynTagRus). To use another model, replace the file in assets/model/ and ensure the naming matches.
* The converter extracts the FORM column from CoNLL‑U; linguistic annotations are not present in the final AntConc files.
* All text is assumed to be UTF‑8 encoded. Files with other encodings may cause errors.
* Entry point: main.py orchestrates the four stages.

---

## License

This project is distributed under the **MIT License**.

See the `LICENSE` file for complete license information.
```
