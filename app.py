from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from knowledgegraph import get_article_text, generate_graph, parse_article
import io
import networkx as nx
import matplotlib.pyplot as plt

app = Flask(__name__)
CORS(app)  # Enable Cross-Origin Resource Sharing


@app.route("/")
def hello():
    """
    Basic route to check if Flask is running.
    """
    return "Hello, Flask is running!"


@app.route("/generate_graph", methods=["POST"])
def generate_graph_endpoint():
    """
    Endpoint to generate a knowledge graph based on the provided URL and user constraints.
    """
    try:
        # Extract the request data
        data = request.json
        url = data.get("url")
        num_nodes = int(data.get("num_nodes", 10))
        num_edges = int(data.get("num_edges", 2))

        # Get and parse the article text
        article = get_article_text(url)
        if not article:
            return jsonify({"error": "Unable to retrieve article text."}), 400

        parsed_data = parse_article(article, num_edges, num_nodes)
        if not parsed_data:
            return jsonify({"error": "Failed to parse article."}), 500

        graph_json = generate_graph(parsed_data, num_edges, num_nodes)

        # Draw the graph and return as image
        image_buffer = draw_graph(graph_json)

        # Return the image as a response
        return send_file(
            image_buffer,
            mimetype="image/png",
            as_attachment=True,
            download_name="knowledgegraph.png",
        )

    except Exception as e:
        return jsonify({"error": str(e)}), 500


def draw_graph(graph_json: dict) -> io.BytesIO:
    """
    Draws the knowledge graph and returns it as an image buffer.

    Parameters:
        graph_json (dict): The generated nodes and edges information in dictionary format.

    Returns:
        io.BytesIO: A buffer containing the image data.
    """
    G = nx.DiGraph()
    for node in graph_json["nodes"]:
        G.add_node(node["id"], label=node["label"])

    for edge in graph_json["edges"]:
        G.add_edge(edge["src"], edge["dst"], label=edge["label"])

    # Remove isolated nodes
    isolated_nodes = [node for node, degree in dict(G.degree()).items() if degree == 0]
    G.remove_nodes_from(isolated_nodes)

    pos = nx.spring_layout(G, k=0.8)  # Layout for our graph

    # Drawing nodes and edges
    plt.figure(figsize=(15, 10))
    nx.draw_networkx_nodes(G, pos, node_size=6000, node_color="#add8e6")
    nx.draw_networkx_edges(
        G, pos, edge_color="black", connectionstyle="arc3,rad=0", node_size=6000
    )
    labels = {node: G.nodes[node]["label"] for node in G.nodes()}
    nx.draw_networkx_labels(
        G, pos, labels=labels, font_size=10, font_color="black", font_weight="bold"
    )

    edge_labels = nx.get_edge_attributes(G, "label")
    nx.draw_networkx_edge_labels(
        G,
        pos,
        edge_labels=edge_labels,
        font_size=10,
        font_color="black",
        font_family="sans-serif",
    )

    plt.axis("off")
    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    plt.close()
    buf.seek(0)
    return buf


if __name__ == "__main__":
    app.run()
