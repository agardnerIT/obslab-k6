# Observability Lab: Grafana k6 Observability

![Grafana k6 Dynatrace Dashboard](docs/images/k6-dashboard.png)

This demo will run a [Grafana k6](https://k6.io) script and use the [Dynatrace output plugin](https://www.dynatrace.com/hub/detail/grafana-k6) to stream metrics to Dynatrace.

The end of the load test will be signalled to Dynatrace by sending an SDLC event using the teardown function.

## >> [Start the Hands on Tutorial](https://dynatrace.github.io/obslab-k6)