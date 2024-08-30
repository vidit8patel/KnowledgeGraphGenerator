// Listener to handle messages from the extension popup or background script
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    if (request.action === 'generate_graph') {
        const numNodes = request.numNodes;
        const numEdges = request.numEdges;

        console.log('Sending request to Flask API...');

        const apiUrl = 'http://localhost:5000/generate_graph';
        const payload = {
            url: window.location.href,  // Use the current page's URL
            num_nodes: numNodes,
            num_edges: numEdges
        };

        fetch(apiUrl, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(payload)
        })
            .then(response => {
                console.log('Received response:', response);
                if (response.ok) {
                    return response.blob();
                } else {
                    throw new Error('Failed to generate the knowledge graph.');
                }
            })
            .then(blob => {
                console.log('Converting response to blob...');
                const url = URL.createObjectURL(blob);
                console.log('Blob URL:', url);
                sendResponse({ status: 'success', imageUrl: url });

                // Automatically download the generated knowledge graph
                const link = document.createElement('a');
                link.href = url;
                link.download = 'knowledgegraph.png';
                document.body.appendChild(link);
                link.click();
                document.body.removeChild(link);
            })
            .catch(error => {
                console.error('Error:', error);
                sendResponse({ status: 'error', message: error.message });
            });

        return true;  // Will respond asynchronously
    }
});
