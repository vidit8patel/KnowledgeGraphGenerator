# Knowledge Graph Generator

An app that generates a knowledge graph from the provided article, newspaper, or research paper link. This app allows users to visualize relationships and nodes in a given piece of text. It uses Google's GenerativeAI Gemini to parse the text and NetworkX to visualize the generated graph. It consists of a web application built with Streamlit and a browser extension that allows users to generate and download knowledge graphs directly from their browser.

[video.webm](https://github.com/vidit8patel/KnowledgeGraphGenerator/assets/105821053/c2a22291-6d22-454b-bd6b-e5ee9909e429)

![Output1](https://github.com/vidit8patel/KnowledgeGraphGenerator/assets/105821053/68b79242-18c3-46fc-9b11-232b0f2edc89)

![Output2](https://github.com/vidit8patel/KnowledgeGraphGenerator/assets/105821053/07615117-0eda-4bda-935d-13f682310122)


https://github.com/user-attachments/assets/719ed10b-9828-454c-a739-7c64502658fa



## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Technologies Used](#technologies-used)
- [Installation](#installation)
  - [Web Application](#web-application)
  - [Browser Extension](#browser-extension)
- [Usage](#usage)
  - [Web Application](#web-application-usage)
  - [Browser Extension](#browser-extension-usage)
- [RESTful API](#restful-api)
- [Debugging and Troubleshooting](#debugging-and-troubleshooting)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgements](#acknowledgements)

## Overview

The Knowledge Graph Generator project aims to simplify the process of extracting and visualizing relationships within textual data. The web application scrapes text from provided URLs, processes it using a generative AI model, and outputs a knowledge graph. The browser extension allows users to generate these graphs directly from their current browser page and download them as images.

## Features

- **Web Scraping**: Extracts text content from any given URL.
- **AI-Powered Parsing**: Uses Google's Generative AI to identify entities and relationships within the text.
- **Graph Visualization**: Visualizes relationships in a knowledge graph using NetworkX and Matplotlib.
- **Browser Extension**: Generate and download knowledge graphs directly from any webpage.
- **RESTful API**: A Flask-based API to support the backend logic, enabling the generation of knowledge graphs as images.

## Technologies Used

- **Python**: Core programming language.
- **Streamlit**: For building the web application interface.
- **NetworkX & Matplotlib**: For creating and visualizing knowledge graphs.
- **BeautifulSoup & Requests**: For web scraping.
- **Flask**: To create the RESTful API.
- **Google Generative AI**: For natural language processing.
- **JavaScript**: For browser extension logic.
- **HTML/CSS**: For browser extension UI.

## Installation

### Web Application

1. **Clone the repository:**
   \`\`\`bash
   git clone https://github.com/yourusername/knowledge-graph-generator.git
   cd knowledge-graph-generator
   \`\`\`

2. **Install dependencies:**
   \`\`\`bash
   pip install -r requirements.txt
   \`\`\`

3. **Set up environment variables:**
   - Create a `.env` file in the project directory and add your Google Generative AI API key:
     \`\`\`
     API_KEY=your_api_key_here
     \`\`\`

4. **Run the Flask server:**
   \`\`\`bash
   python app.py
   \`\`\`

5. **Run the Streamlit app:**
   \`\`\`bash
   streamlit run app.py
   \`\`\`

### Browser Extension

1. **Navigate to the extension directory:**
   \`\`\`bash
   cd browser-extension
   \`\`\`

2. **Load the extension in Chrome:**
   - Open Chrome and go to `chrome://extensions/`.
   - Enable "Developer mode" in the top right corner.
   - Click "Load unpacked" and select the `browser-extension` folder.

## Usage

### Web Application Usage

1. **Access the Streamlit app:**
   - Open the app in your browser using the URL provided by Streamlit (usually `http://localhost:8501`).
  
2. **Input URL and Settings:**
   - Enter the URL of the article or webpage you want to analyze.
   - Set the maximum number of nodes and edges.
   - Click "Generate Knowledge Graph" to see the visualization.

### Browser Extension Usage

1. **Navigate to a webpage:**
   - Visit any article or webpage you want to analyze.

2. **Use the extension:**
   - Click on the Knowledge Graph Generator icon in the browser toolbar.
   - Choose the desired settings for nodes and edges.
   - Click "Generate Graph" to download the graph as an image.

## RESTful API

The Flask API allows you to generate and download knowledge graphs as images. 

### Endpoint: `/generate_graph`

- **Method:** `POST`
- **Content-Type:** `application/json`
- **Payload:**
  \`\`\`json
  {
      "url": "https://example.com/article",
      "num_nodes": 10,
      "num_edges": 2
  }
  \`\`\`

- **Response:** A PNG image of the generated knowledge graph.

### Example cURL Command

\`\`\`bash
curl -X POST -H "Content-Type: application/json" -d '{"url": "https://example.com/article", "num_nodes": 10, "num_edges": 2}' http://localhost:5000/generate_graph --output knowledgegraph.png
\`\`\`

## Debugging and Troubleshooting

- **Stuck on "Generating Knowledge Graph..."**: Ensure the Flask server is running and accessible. Use Developer Tools to inspect the network requests and console logs.
- **CORS Issues**: Make sure the Flask app allows cross-origin requests by enabling CORS.

## Contributing

Contributions are welcome! Please fork this repository and submit a pull request for any improvements or new features.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgements

- [Streamlit](https://streamlit.io/)
- [Google Generative AI](https://cloud.google.com/generative-ai)
- [NetworkX](https://networkx.github.io/)
- [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/)
- [Flask](https://flask.palletsprojects.com/)

---
