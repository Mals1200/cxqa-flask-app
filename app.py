<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Prompt Flow</title>
</head>
<body>
    <h1>Ask a Question</h1>
    <form id="question-form">
        <textarea name="input" rows="4" cols="50" placeholder="Type your question here..." required></textarea><br><br>
        <input type="submit" value="Submit">
    </form>
    <h2>Response:</h2>
    <pre id="response"></pre>
    
    <script>
        document.getElementById('question-form').onsubmit = async function(event) {
            event.preventDefault(); // Prevent default form submission
            const input = event.target.input.value; // Get the input from the form
            const responseElement = document.getElementById('response');
            responseElement.textContent = "Loading..."; // Indicate loading state

            try {
                const res = await fetch('/predict', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/x-www-form-urlencoded'  // Use URL-encoded format for a form
                    },
                    body: new URLSearchParams({input: input})  // Properly encode the form data
                });

                if (!res.ok) { // Check if response status is ok
                    throw new Error(`HTTP error! status: ${res.status}`);
                }

                const data = await res.json(); // Wait for the response JSON
                responseElement.textContent = JSON.stringify(data, null, 2); // Display the response
            } catch (error) {
                console.error('Error occurred while fetching:', error); // Log error to console
                responseElement.textContent = `Error: ${error.message}`;  // Display error message
            }
        };
    </script>
</body>
</html>
