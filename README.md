# Knowledge Graph Generator

An app that generates a knowledge graph from the provided article, newspaper, or research paper link. This app allows users to visualize relationships and nodes in a given piece of text. The app uses OpenAI's GPT-3.5-turbo to parse the text and NetworkX to visualize the generated graph.

[video.webm](https://github.com/vidit8patel/KnowledgeGraphGenerator/assets/105821053/c2a22291-6d22-454b-bd6b-e5ee9909e429)

![Output1](https://github.com/vidit8patel/KnowledgeGraphGenerator/assets/105821053/68b79242-18c3-46fc-9b11-232b0f2edc89)

![Output2](https://github.com/vidit8patel/KnowledgeGraphGenerator/assets/105821053/07615117-0eda-4bda-935d-13f682310122)


## Prerequisites

- Python
- OpenAI API Key
- Streamlit
- NetworkX
- Matplotlib
- BeautifulSoup
- Requests

## Installation

Clone the repository and navigate to the directory:

```sh
git clone https://github.com/vidit8patel/KnowledgeGraphGenerator.git
cd knowledgegraphgenerator
```


## Install the Dependencies
Run the following command to install the required dependencies:

```sh
pip install -r requirements.txt
```

## Usage
Run the Streamlit app using the following command:

```sh
streamlit run app.py
```

Open your web browser and go to http://localhost:8501 to access the app.

Paste the link to an article, newspaper, or research paper in the provided input field.
Specify the maximum number of edges per node and the maximum number of nodes for the graph.
Click on the 'Generate Knowledge Graph' button to visualize the knowledge graph.
Features
URL Input: Allows the user to input the URL of the desired article.
Max Edges and Nodes Input: Provides options to set maximum limits for edges per node and nodes in the graph.
Knowledge Graph Visualization: Visualizes the extracted information from the article as a knowledge graph using nodes and edges to represent entities and their relationships.
