# movie-script-preprocessor-project

## Overview

**movie-script-preprocessor-project** is a Python-based text preprocessing tool designed for linguistic analysis of character speech in the animated series **“Smeshariki” (Kikoriki)**.

The program processes annotated dialogue scripts and automatically:

* extracts character utterances;
* tokenizes dialogue text;
* normalizes words through lemmatization;
* removes Russian stop words;
* generates separate text corpora for each character.

The resulting corpora are intended for further linguistic analysis, including the identification of distinctive speech patterns, lexical preferences, and stylistic differences between characters.

---

## Table of contents

* [Overview](#overview)
* [Project goal](#project-goal)
* [Features](#features)
* [Project structure](#project-structure)
* [System requirements](#system-requirements)
* [Installation and setup](#installation-and-setup)
* [Input data format](#input-data-format)

  * [Supported file format](#supported-file-format)
  * [Dialogue format](#dialogue-format)
  * [Parsing rules](#parsing-rules)
  * [Malformed input behavior](#malformed-input-behavior)
* [Processing pipeline](#processing-pipeline)

  * [1. Script discovery](#1-script-discovery)
  * [2. Tokenization and dialogue compilation](#2-tokenization-and-dialogue-compilation)
  * [3. Lemmatization and stop word removal](#3-lemmatization-and-stop-word-removal)
  * [4. Corpus generation](#4-corpus-generation)
* [Output](#output)
* [Error handling](#error-handling)
* [Implementation notes and limitations](#implementation-notes-and-limitations)
* [License](#license)

---

## Project goal

The preprocessing pipeline was developed to support linguistic research on the speech characteristics of characters from the animated series **“Smeshariki”**.

The generated corpora can be used for:

* lexical analysis;
* stylistic comparison between characters;
* frequency analysis;
* identification of idiolectal features;
* linguistic profiling.

---

## Features

The program performs the following operations:

1. Recursively searches for `.txt` dialogue files.
2. Extracts character names and dialogue text.
3. Converts text to lowercase.
4. Tokenizes dialogue into words.
5. Removes punctuation and non-alphanumeric symbols.
6. Lemmatizes tokens to dictionary forms.
7. Removes Russian stop words.
8. Generates one corpus file per character.
9. Preserves the original word order within each character’s utterances.

---

## Project structure

```text
movie-script-preprocessor-project/
│
├── raw_scripts/                     # Folder containing unprocessed scripts
│   └── *.txt
│
├── cleaned_scripts/                 # Automatically created folder with character corpora
│   ├── ежик_corpus.txt
│   ├── крош_corpus.txt
│   ├── бараш_corpus.txt
│   └── ...
│
├── main.py                          # Program entry point
├── processor.py                    # Text preprocessing logic
├── requirements.txt                # Project dependencies
├── .gitignore                      # Ignored files and directories
├── LICENSE                         # MIT License
└── README.md                       # Project documentation
```

### Directory description

| Path               | Description                                      |
| ------------------ | ------------------------------------------------ |
| `raw_scripts/`     | Stores input `.txt` script files                 |
| `cleaned_scripts/` | Stores generated corpora (created automatically) |
| `main.py`          | Executes the preprocessing pipeline              |
| `processor.py`     | Contains text preprocessing functions            |
| `requirements.txt` | Lists required Python packages                   |

---

## System requirements

### Software requirements

* Python **3.8 or higher**
* `pip`

### Supported operating systems

The project is cross-platform and can run on:

* Windows
* Linux
* macOS

Any operating system capable of running Python **3.8+** should be compatible.

### Dependencies

The following Python packages are required:

```text
pymorphy3==2.0.6
spacy==3.8.14
```

No additional spaCy language model download is required.

The project uses the built-in Russian stop word list provided by:

```python
spacy.lang.ru.Russian().Defaults.stop_words
```

---

## Installation and setup

It is recommended to use a virtual environment.

### 1. Create a virtual environment

#### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

#### Linux / macOS

```bash
python -m venv venv
source venv/bin/activate
```

### 2. Install dependencies

Run:

```bash
pip install -r requirements.txt
```

---

## Input data format

### Supported file format

The program processes:

```text
.txt
```

files encoded in:

```text
UTF-8
```

All input files must be placed inside:

```text
raw_scripts/
```

### Multi-file behavior

The program recursively searches for **all `.txt` files** inside `raw_scripts/`, including nested directories.

Implementation:

```python
Path("./raw_scripts").rglob("*.txt")
```

If multiple files are present:

* all files are processed;
* all dialogue lines are read sequentially;
* the content is combined into a single processing stream;
* character corpora are compiled across all discovered files.

Example:

```text
raw_scripts/
├── episode_1.txt
├── episode_2.txt
└── archive/
    └── special_episode.txt
```

In this case, dialogues from all files are merged into the same character corpora.

If isolated corpora are required per script, files should be processed separately.

### Dialogue format

Each dialogue line must follow the structure:

```text
[character_name] dialogue text
```

Example:

```text
[крош] Здесь! Быстрей сюда!
[ежик] Бегу, бегу!
[бараш] Сегодня дождь обещали.
```

Each line is expected to contain:

1. a character name enclosed in square brackets `[]`;
2. a space after the closing bracket `]`;
3. dialogue text on the same line.

### Parsing rules

#### Character name normalization

Character names are:

* extracted from square brackets;
* converted to lowercase;
* normalized by replacing `ё` with `е`.

Example:

```text
[Ёжик] → ежик
```

This normalization improves consistency but may introduce ambiguity in rare linguistic cases (for example, distinctions between `все` and `всё` are removed).

---

#### Dialogue preprocessing

Dialogue text is:

1. converted to lowercase;
2. split into tokens using whitespace;
3. stripped of any non-alphanumeric characters using `isalnum()`.

Example input:

```text
[Крош] Здесь! Быстрей сюда!
```

After tokenization:

```text
здесь быстрей сюда
```

Important behavior:

* punctuation marks are removed;
* digits are preserved;
* alphanumeric characters remain;
* service annotations are cleaned as ordinary text;
* token order is preserved.

Example:

```text
[крош] У меня 3 яблока!
```

Becomes:

```text
у меня 3 яблока
```

Digits remain unchanged during lemmatization.

---

#### Service annotations

The program does not process service annotations specially.

Example:

```text
{неразбр}
```

After cleaning:

```text
неразбр
```

Only alphanumeric characters survive preprocessing.

### Malformed input behavior

The parser processes only lines matching the expected format.

The following examples illustrate how malformed input is handled.

#### Valid line

```text
[крош] Привет!
```

Processed successfully.

---

#### Missing dialogue text

```text
[крош]
```

The character name is extracted, but no dialogue tokens are added.

---

#### Missing square brackets

```text
крош Привет!
```

Skipped silently.

---

#### Missing closing bracket

```text
[крош Привет!
```

Skipped silently.

---

#### Incorrect formatting

```text
крош: Привет!
```

Skipped silently.

The current implementation does **not** log warnings for skipped lines.

As a result, malformed input may pass unnoticed unless manually inspected.

---

## Processing pipeline

The preprocessing pipeline consists of four stages.

### 1. Script discovery

Function:

```python
find_scripts()
```

The program recursively searches for `.txt` files inside:

```text
./raw_scripts
```

If no files are found, the program raises:

```python
ScriptNotFoundError
```

---

### 2. Tokenization and dialogue compilation

Function:

```python
tokenize_and_compile()
```

This stage:

* extracts character names;
* separates metadata from dialogue;
* tokenizes dialogue text;
* aggregates tokens by character.

Output structure:

```python
dict[str, list[str]]
```

Example:

```python
{
    "крош": ["здесь", "быстрей", "сюда"],
    "ежик": ["бегу", "бегу"]
}
```

Character names are normalized to lowercase and `ё` is replaced with `е`.

The original word order is preserved.

---

### 3. Lemmatization and stop word removal

Function:

```python
lemmatize_and_clean()
```

Libraries used:

```text
pymorphy3
spaCy
```

#### Lemmatization

Words are normalized using:

```python
pymorphy3.MorphAnalyzer()
```

Examples:

```text
бегу → бежать
помогите → помочь
пилюли → пилюля
```

---

#### Stop word removal

The project uses the built-in Russian stop word list from spaCy:

```python
Russian().Defaults.stop_words
```

Examples of removed stop words:

```text
и, в, на, но, это, что, как
```

Stop words are removed after lemmatization.

Output structure:

```python
dict[str, list[str]]
```

---

### 4. Corpus generation

Function:

```python
write_cleaned_file()
```

The program automatically creates:

```text
cleaned_scripts/
```

if it does not already exist.

For each character, a separate corpus file is generated:

```text
<character_name>_corpus.txt
```

Examples:

```text
ежик_corpus.txt
крош_corpus.txt
бараш_corpus.txt
```

Each file contains:

* lemmatized tokens;
* stop words removed;
* whitespace-separated tokens;
* preserved token order.

Example output:

```text
солнце уходить прогреться думать хватить
```

---

## Running the program

Open a terminal in the project root directory and run:

```bash
python main.py
```

Example console output:

```text
Hi!! <3    Looking for your scripts now...
Scripts found! Let's compile them now <3
Your scripts have been compiled successfully! ^_^
Yay! The scripts are ready! Let's upload them to a folder now

Saved one! - cleaned_scripts/ежик_corpus.txt!
Saved one! - cleaned_scripts/крош_corpus.txt!
Saved one! - cleaned_scripts/бараш_corpus.txt!

Your files are good to go now :3
```

---

## Output

After successful execution, processed corpora are saved to:

```text
cleaned_scripts/
```

Each file represents the processed speech corpus of a single character.

Example:

```text
ежик_corpus.txt
```

Possible content:

```text
бежать прогреться солнце думать помочь
```

---

## Error handling

The project defines custom exception classes for execution failures.

| Exception                    | Description                                  |
| ---------------------------- | -------------------------------------------- |
| `ScriptNotFoundError`        | No `.txt` files found in `raw_scripts/`      |
| `ScriptCompilationError`     | Script compilation returned an empty result  |
| `ScriptPreprocessingError`   | Preprocessing stage returned an empty result |
| `CleanScriptNotWrittenError` | Processed files could not be written         |

Important implementation detail:

Malformed dialogue lines are skipped silently and do **not** trigger exceptions.

---

## Implementation notes and limitations

* The preprocessing pipeline preserves word order.
* Character names are normalized (`ё → е`).
* Digits are preserved during preprocessing.
* The program does not log skipped lines.
* Multiple input files are merged into shared character corpora.
* No sentence segmentation is performed.
* No POS tagging or syntactic parsing is applied.

---

## License

This project is distributed under the **MIT License**.

See the `LICENSE` file for complete license information.
