import io
import streamlit as st
import networkx as nx
import json
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup
import requests
import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv()
API_KEY = os.getenv("API_KEY")

genai.configure(api_key=API_KEY)



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
    try:
        model = genai.GenerativeModel(
            model_name="gemini-1.5-flash",
            system_instruction = f"""You are an expert in text analysis and knowledge representation. Your task is to construct a detailed Knowledge Graph from the provided article text. Your task is to extract key entities and their relationships, ensuring clarity and relevance.

                1. **Nodes**: Represent key entities (e.g., people, organizations, concepts) as nodes. Each node should have:
                   - A unique `id` (1, 2, 3, ...).
                   - A `label` summarizing the entity (text label).

                2. **Edges**: Identify and represent meaningful relationships between these entities as directed edges. Each edge should:
                   - Connect two nodes, using `src` (source node id) and `dst` (destination node id).
                   - Include a `label` describing the relationship (e.g., 'is part of', 'influences', 'was founded by').

                3. **Constraints**:
                   - Maximum number of nodes: {num_nodes}.
                   - Maximum number of edges per node: {num_edges}.
                   - Ensure that the `src` and `dst` in edges accurately reflect the logical relationship.

                4. **Output**:
                   - Return the graph in a compact JSON format: `{{ "nodes": [nodes list], "edges": [edges list] }}`.
                   - Each node should be a dictionary with `"id"` and `"label"`.
                   - Each edge should be a dictionary with `"src"`, `"dst"`, and `"label"`.

                Focus on clarity, relevance, and adhering to the constraints when constructing the graph.
                """
        )
        response = model.generate_content(article)
        
        # Extract text content
        content_parts = response.candidates[0].content.parts
        if content_parts:
            content = content_parts[0].text
        else:
            st.error("No content parts found in the response.")
            return {"nodes": [], "edges": []}

        # Print raw content for debugging
        st.write("Raw response content:")
        st.write(content)

        # Clean up content: remove extra formatting
        cleaned_content = content.strip()
        
        # Remove any extraneous characters or formatting
        if cleaned_content.startswith('```json'):
            cleaned_content = cleaned_content[len('```json'):].strip()
        if cleaned_content.endswith('```'):
            cleaned_content = cleaned_content[:-len('```')].strip()

        if cleaned_content:
            try:
                # Parse JSON
                content_json = json.loads(cleaned_content)
                return content_json
            except json.JSONDecodeError as e:
                st.error(f"Received invalid JSON from the model: {e}")
                st.write(f"Content that failed to parse: {cleaned_content}")
                return {"nodes": [], "edges": []}
        else:
            st.error("Empty response from the model.")
            return {"nodes": [], "edges": []}

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
    nx.draw_networkx_labels(G, pos, labels=labels, font_size=10, font_color='white', font_weight='bold')

    edge_labels = nx.get_edge_attributes(G, 'label')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=10, font_color='black',
                                 font_family='sans-serif')

    plt.axis('off')
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    plt.close()
    buf.seek(0)
    #return buf 
    st.image(buf, caption='Knowledge Graph', use_column_width=True)


if __name__ == "__main__":
    main()  # Execute main function


#https://justpaste.it/7o396