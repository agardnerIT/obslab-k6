## Getting Started

--8<-- "snippets/live-code-snippets-save-connection-details.md"

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