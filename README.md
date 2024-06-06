[![Pylint](https://github.com/marquies/scene-graph-conversion/actions/workflows/pylint.yml/badge.svg?branch=main)](https://github.com/marquies/scene-graph-conversion/actions/workflows/pylint.yml)
# Scene Graph Conversion

The scripts in the repository are used to convert Rendering Scene Graphs, recorded with a Metaverse Recording Tool in Unity, into Visual Scene Graphs.

Rendering scene graphs recorded from virtual wolrds can be found here https://patricksteinert.de/256-metaverse-records-dataset/mvr-dataset/

## Prerequisits

The script uses some libs to produce graphml and images with OpenAI

The following command installs packages in bulk according to the configuration file, requirements.txt. In some environments, use pip3 instead of pip.

```
pip install -r requirements.txt
```

To use OpenAI in the script, set your OpenAI API Key with

```
export OPENAI_API_KEY=<openai_api_key>
```


## Quick Start

Use the script with the example data. Just execute 

```
python demo.py
```
