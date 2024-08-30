from flask import Flask, request, jsonify, send_file
from flask_cors import CORS

from knowledgegraph import get_article_text, generate_graph,draw_graph, parse_article
import io
import networkx as nx
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup
import requests

app = Flask(__name__)
CORS(app)


@app.route('/')
def hello():
    return "Hello, Flask is running!"

@app.route('/generate-knowledge-graph', methods=['POST'])
def generate_knowledge_graph():
    data = request.json
    url = data.get('url')
    num_edges = data.get('num_edges', 2)
    num_nodes = data.get('num_nodes', 10)

    article = get_article_text(url)
    if not article:
        return jsonify({"error": "Unable to retrieve article text"}), 400

    parsed_data = parse_article(article, num_edges, num_nodes)
    graph_json = generate_graph(parsed_data, num_edges, num_nodes)

    # Generate the graph image and send it back as a response
    image_stream = draw_graph(graph_json)  # Ensure this is a BytesIO stream
    return send_file(image_stream, mimetype='image/png', as_attachment=True, download_name='knowledge_graph.png')



# Route to return graph as an image
@app.route('/graph-image', methods=['POST'])
def graph_image():
    data = request.json
    graph_json = data.get('graph_json')

    if not graph_json:
        return jsonify({"error": "Graph data is required"}), 400

    image = draw_graph(graph_json)
    return send_file(image, mimetype='image/png')


# Other functions for article scraping, parsing, and graph generation would go here

if __name__ == '__main__':
    app.run(debug=True)
