The repository includes an AWS lifecycle command: provision a GPU instance, install SelfJev, run it as a systemd service, and remove it when finished. **Provisioning creates billable resources.** Check the current price and your account’s GPU quota before running `up`.

## Choose a machine

Start with `g6.xlarge` (L4, 24 GB VRAM) for light serving, or `g5.xlarge` (A10G, 24 GB). The native engine’s correctness was checked on an A10G. L4 serving latency has not been measured. An L40S with 48 GB gives more memory for training and larger workloads.

Use the [AWS instance specifications](https://aws.amazon.com/ec2/instance-types/) and your region’s live pricing. The CLI’s preset prices are estimates, not a billing quote.

## Deploy a bounded trial

Configure AWS credentials with EC2 permissions, then install the deploy extra:

```bash
pip install "selfjev[deploy] @ git+https://github.com/Jwuthri/SelfJev"
selfjev deploy aws machines
selfjev deploy aws up --name selfjev-trial \
  --instance g6.xlarge \
  --region us-east-2 \
  --allow-cidr YOUR_PUBLIC_IP/32 \
  --max-hours 2 \
  --ssh
```

Replace `YOUR_PUBLIC_IP/32` with your actual public IPv4 CIDR. The time cap terminates the instance; save anything you need before it expires. The command prints an endpoint and API key and waits for readiness, unless `--no-wait` is used.

First boot fetches dependencies and the base model. It can take up to 30 minutes. The deployment helper exists, but its full provisioning flow has not been validated in the recorded experiments.

## Call and observe

Use an SSH tunnel or put an HTTPS proxy in front of the endpoint before sending credentials over a public network. The helper serves HTTP on port 8000; it does not provision a TLS domain.

```bash
selfjev deploy aws status --name selfjev-trial
selfjev deploy aws list
```

Deployment records, including the key, live under `~/.selfjev/deployments/`. On the instance, setup logs are in `/var/log/selfjev-setup.log`.

## Tear down

```bash
selfjev deploy aws down --name selfjev-trial
```

This terminates the deployment, rather than pausing it. Always inspect your AWS console afterward for any remaining billable resources, including disks created outside the helper.

Source: [deployment guide and CLI behavior](https://github.com/Jwuthri/SelfJev/blob/master/docs/deploy.md).
