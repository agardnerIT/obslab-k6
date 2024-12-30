<style>
        .executor {
            padding: 10px 20px;
            font-size: 16px;
            cursor: pointer;
            background-color: #4CAF50;
            color: white;
            border: none;
            border-radius: 4px;
        }
        .executor:hover {
            background-color: #45a049;
        }
        #response {
            visibility: hidden;
            background-color: rgba(34,139,34,0.9);
            position: fixed;
            bottom: 5px;
            color: #fff;
            padding: 20px;
            z-index: 900; // Force on top of everything else
        }
        #response.show {
            visibility: visible;
            -webkit-animation: fadein 0.2s, fadeout 0.5s 10s;
            animation: fadein 0.2s, fadeout 0.5s 10s;
        }

        @-webkit-keyframes fadein {
            from {bottom: 0; opacity: 0;} 
            to {bottom: 30px; opacity: 1;}
        }

        @keyframes fadein {
            from {bottom: 0; opacity: 0;}
            to {bottom: 30px; opacity: 1;}
        }

        @-webkit-keyframes fadeout {
            from {bottom: 30px; opacity: 1;} 
            to {bottom: 0; opacity: 0;}
        }

        @keyframes fadeout {
            from {bottom: 30px; opacity: 1;}
            to {bottom: 0; opacity: 0;}
        }
</style>

<script>
        // filePath is optional
        // if not provided, defaults to an empty string
        async function sendRequest(btn, snippetID, filePath = "") {

            var rect = btn.getBoundingClientRect();
            console.log(rect.top, rect.right, rect.bottom, rect.left);

            try {
                // disable button
                // change icon & colour to make
                // users aware of a pending response
                btn.disabled = true;
                btn.innerHTML = "&#8987;" // Set icon to loading spinner
                btn.style.cursor = "progress"; // Set mouseover cursor to loading spinner
                btn.style.backgroundColor = "grey"; // Set colour to grey to indicate a change

                const response = await fetch(localStorage.getItem("serverAddress") + "query", {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        filename: filePath,
                        snippet_id: snippetID,
                        secret_key: localStorage.getItem("secretKey")
                    })
                });
                const data = await response.json();

                if (data["output"]) {
                    // Re-enable the button
                    btn.disabled = false;
                    btn.innerHTML = "&#9658;" // Set icon back to play
                    btn.style.cursor = "pointer"; // Set mouseover cursor back to pointer
                    btn.style.backgroundColor = "#4CAF50"; // Set colour to back to green to indicate re-enabled

                    document.getElementById('response').innerHTML = data["output"]
                    var x = document.getElementById("response");
                    x.className = "show";
                    setTimeout(function(){ x.className = x.className.replace("show", ""); }, 10000);
                }

            } catch (error) {
                document.getElementById('response').innerText = 'Error: ' + error.message;
            }
        }
</script>

<pre id="response">Response will appear here...</pre>