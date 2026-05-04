# Markov Chain Text Generator (Hashtable Edition)

An authentic, from-scratch implementation of a Markov Chain text generator. This program analyzes a source text file and generates new, randomized content based on word-frequency patterns, using a custom-built Hashtable for data storage.

## Overview
Unlike standard Python implementations that rely on built-in dictionaries, this project features a **manual Hashtable implementation**. It demonstrates the mechanics of hashing algorithms, linear probing for collision resolution, and the probabilistic logic of Markov Chains.

## Features
* **Custom Hashtable Class**: Built using a 2D list structure.
* **Polynomial Hashing**: Implements a `31 * p + ord(c)` hashing algorithm.
* **Collision Handling**: Utilizes linear probing (with wrap-around) to manage hash collisions.
* **Adjustable Markov Order**: Supports custom prefix lengths to control how closely the output mimics the source text.
* **Formatted Output**: Automatically wraps generated text into clean, 10-word lines.

## Technical Specs
* **Language**: Python 3.x
* **Data Structure**: Hashtable (Open Addressing / Linear Probing)
* **Randomization**: Seeded for reproducibility (`SEED = 8`).

## Usage

Run the script via your terminal. The program will prompt for four inputs in the following order:

1.  **File Name**: The path to your `.txt` source file.
2.  **Hashtable Size**: Integer (e.g., `2000`). Large sizes reduce collisions.
3.  **Prefix Length**: Integer (e.g., `2`). The number of words the bot "looks back" at.
4.  **Word Count**: Integer (e.g., `100`). Total words to generate.

## Example Execution:
```bash
python writer_bot_ht.py

## Example Input:
moby_dick.txt
5000
2
50
