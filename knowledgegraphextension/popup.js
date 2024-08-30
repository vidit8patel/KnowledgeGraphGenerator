document.getElementById('generate').addEventListener('click', async () => {
    const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
    chrome.scripting.executeScript({
        target: { tabId: tab.id },
        function: generateKnowledgeGraph,
    });
});

async function generateKnowledgeGraph() {
    const url = window.location.href;
    const response = await fetch('http://127.0.0.1:5000/generate-knowledge-graph', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ url, num_edges: 2, num_nodes: 10 }),
    });

    if (response.ok) {
        const imageBlob = await response.blob();
        const imageUrl = URL.createObjectURL(imageBlob);

        // Create an anchor element and simulate a click to download the image
        const a = document.createElement('a');
        a.href = imageUrl;
        a.download = 'knowledge_graph.png'; // Set the filename
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);

        // Optionally, revoke the Object URL after the download
        URL.revokeObjectURL(imageUrl);
    } else {
        alert('Failed to generate knowledge graph. Check the console for details.');
        console.error('Error:', await response.text());
    }
}
