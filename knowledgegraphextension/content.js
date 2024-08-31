// Listener to handle messages from the extension popup or background script
chrome.runtime.onMessage.addListener(async (request, sender, sendResponse) => {
    if (request.action === 'generate_graph') {
        const numNodes = request.numNodes;
        const numEdges = request.numEdges;

        console.log('Sending request to API...');

        const apiUrl = 'http://127.0.0.1:5000/generate_graph';
        const payload = {
            url: window.location.href,  // Use the current page's URL
            num_nodes: numNodes,
            num_edges: numEdges
        };

        try {
            const response = await fetch(apiUrl, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(payload)
            });

            console.log('Received response:', response);

            if (!response.ok) {
                throw new Error('Failed to generate the knowledge graph.');
            }

            console.log('Converting response to blob...');
            const blob = await response.blob();
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

        } catch (error) {
            console.error('Error:', error);
            sendResponse({ status: 'error', message: error.message });
        }

        return true;  // Will respond asynchronously
    }
});
