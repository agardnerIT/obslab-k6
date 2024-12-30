<script>
    function sleep(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }
    async function saveConnectionDetails() {
        localStorage.setItem("serverAddress", document.getElementById("serverAddress").value);
        localStorage.setItem("secretKey", document.getElementById("secretKey").value);

        document.getElementById("save-connection-details").innerHTML = "&#9989;"; // Set button to a checkmark
        // Sleep for 2s then reset button so users know they can reset details
        // if they got them wrong
        await sleep(1000);
        document.getElementById("save-connection-details").innerHTML = "Save Connection Details";

    }
</script>

<style>

.md-typeset__table {
   min-width: 100%;
}

.md-typeset table:not([class]) {
    display: table;
}
.connection-input {
    min-width: 100%;
}
</style>

!!! info "Live Code Snippets"
    The code snippets in this tutorial can be executed live from within the browser. To enable this, just follow the instructions below.

    Then click the green buttons below each code snippet. After the command has executed, the response will appear in a popup box at the bottom of the screen.

    If you do not want to use this functionality, you can still copy and paste the commands into the codespace terminal.

## Set Details for Live Code Snippets

Retrieve authentication token by running this command in your codespace terminal:

```
cat /tmp/secret
```

Retrieve the URL by going to the `Ports` tab in the codespace, click the row corresponding to port `8000` and press `Ctrl + c`.
Alternatively you can right click and choose `Copy Local address`

Paste the details into these boxes and click the Save button.


| Connection Item      | Description                          |
| ----------- | ------------------------------------ |
| Server URL       | <input type="text" id="serverAddress" class="connection-input" />  |
| Secret Key       | <input type="password" id="secretKey" class="connection-input" />  |

<!--
<table>
<tr>
    <td><label for="secretKey">Set secret key:</label></td>
    <td><input type="password" id="secretKey" class="connection-input" /></td>
</tr>
<tr>
    <td><label for="serverAddress">Set server address:</label></td>
    <td><input type="text" id="serverAddress" class="connection-input" /></td>
</tr>
</table>
-->

<button id="save-connection-details" class="md-button" onclick="saveConnectionDetails()">Save Connection Details</button>

## Gather Details: Tenant ID

You will need access to a Dynatrace tenant. If you do not have access, [sign up for a free 15 day trial](https://dt-url.net/trial){target=_blank}.

Make a note of your Dynatrace tenant ID. It is the first bit of your URL (eg. `abc12345` in the following examples):

```
https://abc12345.live.dynatrace.com
https://abc12345.apps.dynatrace.com
```

Reformat the URL like this: `https://TENANT_ID.live.dynatrace.com` eg. `https://abc12345.live.dynatrace.com`

## Gather Details: Create API Token

k6 requires an API token to stream metrics to Dynatrace.

Create an API token with the following permissions:

- `metrics.ingest`
- `openpipeline.events_sdlc`

## Start Demo

Click this button to launch the demo in a new tab.

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/dynatrace/obslab-k6){target=_blank}

<div class="grid cards" markdown>
- [Click Here to Run the Demo :octicons-arrow-right-24:](run-demo.md)
</div>