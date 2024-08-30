document.getElementById('generate-graph').addEventListener('click', async () => {
    const numNodes = document.getElementById('num-nodes').value;
    const numEdges = document.getElementById('num-edges').value;

    document.getElementById('status').textContent = "Generating knowledge graph...";

    chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
        chrome.tabs.sendMessage(tabs[0].id, { action: 'generate_graph', numNodes, numEdges }, (response) => {
            if (response.status === 'success') {
                document.getElementById('status').textContent = "Knowledge graph generated!";
                const link = document.createElement('a');
                link.href = response.imageUrl;
                link.download = 'knowledgegraph.png';
                link.click();
            } else {
                document.getElementById('status').textContent = "Failed to generate graph.";
            }
        });
    });
});
