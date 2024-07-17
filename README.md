
# Domain Checker

This project checks the availability of a specified domain and sends notifications to Mattermost.

## Building and Pushing the Container

1. Ensure you have Docker installed and you're logged in to Docker Hub.

2. Build the Docker image:
   ```
   docker build -t lbr88/domain-checker:latest .
   ```

3. Push the image to Docker Hub:
   ```
   docker push lbr88/domain-checker:latest
   ```

## Deploying with Helm

1. Ensure you have Helm installed and your Kubernetes cluster is configured.

2. Clone this repository:
   ```
   git clone https://github.com/yourusername/domain-checker.git
   cd domain-checker
   ```

3. Copy the example values file and edit it with your specific configuration:
   ```
   cp values.example.yaml values.yaml
   ```
   Edit `values.yaml` with your preferred text editor.

4. Install the Helm chart:
   ```
   helm install domain-checker ./domain-checker
   ```

   Or, if you want to override any values directly from the command line:
   ```
   helm install domain-checker ./domain-checker --set domain=yourdomain.com --set webhookUrl=https://your-mattermost-webhook-url
   ```

5. To upgrade the deployment after making changes:
   ```
   helm upgrade domain-checker ./domain-checker
   ```

## Configuration

The following table lists the configurable parameters of the domain-checker chart and their default values.

| Parameter                | Description             | Default        |
|--------------------------|-------------------------|----------------|
| `image.repository`       | Image repository        | `lbr88/domain-checker` |
| `image.tag`              | Image tag               | `latest`       |
| `image.pullPolicy`       | Image pull policy       | `IfNotPresent` |
| `domain`                 | Domain to check         | `example.com`       |
| `webhookUrl`             | Mattermost webhook URL  | `"https://example.com/webhook/"`           |
| `schedule`               | Cron schedule           | `"*/5 * * * *"` |
| `resources.limits.cpu`   | CPU limit               | `100m`         |
| `resources.limits.memory`| Memory limit            | `128Mi`        |
| `resources.requests.cpu` | CPU request             | `50m`          |
| `resources.requests.memory`| Memory request        | `64Mi`         |

Specify each parameter using the `--set key=value[,key=value]` argument to `helm install`.

## Uninstalling the Chart

To uninstall/delete the `domain-checker` deployment:

```
helm delete domain-checker
```

This will remove all the Kubernetes components associated with the chart and delete the release.
```