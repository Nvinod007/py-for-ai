# 04 Deploying and cloud basics

## Where can my app run?

| Option | Good for | Notes |
|---|---|---|
| **Vercel** | Front ends, light APIs, Python functions | Very easy Git-based deploys, preview links per branch |
| **Render / Railway / Fly.io** | Containers and small backends | Push to Git or give a Dockerfile, simple pricing |
| **Google Cloud Run / AWS App Runner / Azure Container Apps** | Containers that scale to zero | Pay per use, a good first "real cloud" choice |
| **AWS ECS / Kubernetes** | Large teams and complex systems | Powerful, more to learn |
| **AWS Lambda / Cloud Functions** | Event-driven small tasks | Cold starts, time limits |
| **A VM (EC2, droplet)** | Full control | You manage patches and uptime |

Start with a container platform (Cloud Run, Render, Fly). Move up only when you must.

## The usual deploy flow

1. Code in Git, push to a branch.
2. CI runs checks, then builds the Docker image.
3. Image goes to a registry.
4. The platform runs the new image, health checks it, then switches traffic.
5. If it fails, **roll back** to the previous image.

## Cloud words you will hear

| Word | Meaning |
|---|---|
| Region | Data centre location, pick the closest to your users |
| IAM / roles | Permissions, give the least needed |
| Object storage (S3, GCS) | Files at any size, cheap |
| Managed database (RDS, Cloud SQL, Neon, Supabase) | Postgres without running it yourself |
| Secrets manager | Safe place for API keys |
| Load balancer | Spreads traffic over many copies |
| Autoscaling | More or fewer copies based on load |
| CDN | Caches content near users |
| Logs / metrics / traces | How you see what the app is doing |

## Keys and security basics

1. Secrets live in the platform's secret manager, never in Git or the image.
2. Use separate keys for dev and production.
3. Give each service the smallest permissions it needs.
4. Turn on HTTPS (platforms do it for you).
5. Add authentication and rate limits before the app is public, especially if it calls a paid LLM API.
6. Set budget alerts in your cloud account on day one.

## Example: deploy the container to Cloud Run (sketch)

```bash
gcloud run deploy example-api \
  --source ./05_example_app \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars APP_ENV=production
```

Set secrets with `--set-secrets` rather than `--set-env-vars`.

## After deploy: check the app

- `curl https://<your-url>/health`
- Read logs in the platform dashboard.
- Watch latency, error rate, and cost for a few days.

## Practice

1. Deploy `05_example_app` to one platform of your choice.
2. Break it on purpose (bad env var), read the logs, fix it.
3. Roll back to the previous version.
