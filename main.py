import io
import streamlit as st
import networkx as nx
import openai
import json
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup
import requests

# Set up OpenAI API key
openai.api_key = 'API_KEY'


def main():
    """
    Main function to execute the Streamlit app.
    The function initializes the app title, inputs and executes necessary functions on button press.
    """

    st.title("Knowledge Graph Generator")

    # Streamlit widgets to take user inputs
    url = st.text_input("Article/Newspaper/Research Paper link here:")
    num_edges = st.number_input("Max Number of Edges per Node", value=2, min_value=1, step=1)
    num_nodes = st.number_input("Max Number of Nodes", value=10, min_value=1, step=1)

    # Button to start the knowledge graph generation process
    if st.button('Generate Knowledge Graph'):
        if url:
            article = get_article_text(url)  # Scrape and get article text from the URL
            if article:
                parsed_data = parse_article(article, num_edges,
                                            num_nodes)  # Parse the article text to extract relevant data
                graph_json = generate_graph(parsed_data, num_edges, num_nodes)  # Generate a graph based on parsed data
                draw_graph(graph_json)  # Draw and display the generated graph
            else:
                st.warning('Could not retrieve readable article text from the provided URL.')
        else:
            st.warning('Please input an article URL to proceed.')


def get_article_text(url: str) -> str:
    """
    Fetches and returns the article text from a given URL using web scraping.

    Parameters:
    url (str): The URL of the article.

    Returns:
    str: The extracted article text.
    """
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        paragraphs = soup.find_all('p')
        return " ".join([para.text for para in paragraphs])
    except Exception as e:
        st.error(f"Error in retrieving article: {e}")
        return ""


def parse_article(article: str, num_edges: int, num_nodes: int) -> dict:
    """
    Parses the given article and extracts relevant information to form a knowledge graph.
    It communicates with OpenAI API to generate knowledge graph nodes and edges from the article text.

    Parameters:
    article (str): The article text.
    num_edges (int): The maximum number of edges per node.
    num_nodes (int): The maximum number of nodes in the graph.

    Returns:
    dict: The parsed nodes and edges information in dictionary format.
    """
    try:
        max_article_length = 2600  # Maximum allowed length of the article
        if len(article) > max_article_length:
            article = article[:max_article_length]
            st.warning("The article is too long and has been truncated.")

        computed_max_tokens = 4096 - len(article) - 80  # Compute max_tokens for OpenAI API request

        # OpenAI API call to generate knowledge graph data from the article text
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": f'Create a Knowledge Graph from the given article text with meaningful relationships, simplified context, and adhering to the constraints. Node = {{id: (1/2/3...) label: (text label))}},Edge = {{src: (source node id) dst: (destination node id) label: (relationship label)}} Return a compact JSON: {{ "edges": [edges list], "nodes": [nodes list] }} Constraints: Max Number of edges per node: {num_edges} Max number of Nodes: {num_nodes}. Assign the src and dst in edges according to the relationship label cautiously.',
                },
                {"role": "user", "content": f"Article: {article}"},
            ],
            temperature=0.4,
            max_tokens=computed_max_tokens,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
        )
        content = response['choices'][0]['message']['content']
        return json.loads(content.strip())

    except Exception as e:
        st.error(f"Error in parsing article: {e}")
        return {"nodes": [], "edges": []}


def generate_graph(parsed_data, num_edges, num_nodes):
    """
    Generates a graph from the parsed data using NetworkX.
    The graph is generated based on the constraints for nodes and edges provided by the user.

    Parameters:
    parsed_data (dict): The parsed nodes and edges information in dictionary format.
    num_edges (int): The maximum number of edges per node.
    num_nodes (int): The maximum number of nodes in the graph.

    Returns:
    dict: The generated nodes and edges information in dictionary format.
    """
    G = nx.DiGraph()
    nodes = parsed_data.get("nodes", [])[:num_nodes]
    edges = parsed_data.get("edges", [])

    # Adding nodes and edges to the graph based on constraints
    for node in nodes:
        G.add_node(node['id'], label=node['label'])

    for edge in edges:
        src = edge['src']
        dst = edge['dst']
        if src in G and dst in G and G.degree(src) < num_edges:
            G.add_edge(src, dst, label=edge['label'])

    return {
        "nodes": nodes,
        "edges": [{'src': edge[0], 'dst': edge[1], 'label': edge[2]['label']} for edge in G.edges(data=True)]
    }


def draw_graph(graph_json):
    """
    Draws and displays the generated graph using NetworkX and Matplotlib.

    Parameters:
    graph_json (dict): The generated nodes and edges information in dictionary format.
    """
    G = nx.DiGraph()
    for node in graph_json['nodes']:
        G.add_node(node['id'], label=node['label'])

    for edge in graph_json['edges']:
        G.add_edge(edge['src'], edge['dst'], label=edge['label'])

    # Remove isolated nodes
    isolated_nodes = [node for node, degree in dict(G.degree()).items() if degree == 0]
    G.remove_nodes_from(isolated_nodes)

    pos = nx.spring_layout(G, k=0.8)  # Layout for our graph

    # Drawing nodes and edges
    plt.figure(figsize=(15, 10))
    nx.draw_networkx_nodes(G, pos, node_size=6000, node_color='#ff0000')
    nx.draw_networkx_edges(G, pos, edge_color='black', connectionstyle='arc3,rad=0', node_size=6000)
    labels = {node: G.nodes[node]['label'] for node in G.nodes()}
    nx.draw_networkx_labels(G, pos, labels=labels, font_size=10, font_color='#000000', font_weight='bold')

    edge_labels = nx.get_edge_attributes(G, 'label')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=10, font_color='black',
                                 font_family='sans-serif')

    plt.axis('off')
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    plt.close()
    buf.seek(0)
    st.image(buf, caption='Knowledge Graph', use_column_width=True)


if __name__ == "__main__":
    main()  # Execute main function
