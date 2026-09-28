Run SelfJev on a **GPU-backed Compute Engine VM**. This is a manual deployment path; the project has no GCP provisioning command and has not validated this guide end to end.

## 1. Provision the host

Request GPU quota in a region with capacity. A G2 VM with one NVIDIA L4 (24 GB VRAM) is a reasonable serving starting point. Check the selected machine’s system RAM, disk, and current hourly cost before creating it. L4 latency is not benchmarked for the current model.

Use a GPU-ready Linux image, or install a compatible NVIDIA driver using Google’s guide. Verify `nvidia-smi` on the host before installing SelfJev. Budget at least 50 GB free disk for dependencies and model files.

## 2. Install SelfJev

SSH to the VM and install Git, Git LFS, and uv, then follow the [quickstart](/docs/). Keep the service on loopback during initial testing:

```bash
export SELFJEV_API_KEYS="replace-with-a-long-random-key"
uv run --no-sync selfjev serve --host 127.0.0.1 --port 8000
```

This command runs from the prepared SelfJev checkout. The base model downloads on first start. For a persistent endpoint, supervise the process with systemd or use the [Docker deployment](/docs/docker/) with a restart policy.

## 3. Test through a tunnel

From your local machine, use your actual instance and zone:

```bash
gcloud compute ssh INSTANCE_NAME --zone ZONE \
  -- -N -L 8000:127.0.0.1:8000
```

Keep the tunnel open and point the SDK at `http://localhost:8000`. A production public endpoint needs HTTPS termination, authentication, and appropriate firewall rules. Do not expose the unauthenticated service to the internet.

## 4. Delete trial resources

Delete the VM when done, and review persistent disks, reserved addresses, and other resources separately. Stopped VMs may retain chargeable storage.

Provider references: [accelerator-optimized machines, including G2](https://cloud.google.com/compute/docs/accelerator-optimized-machines), [GPU driver installation](https://cloud.google.com/compute/docs/gpus/install-drivers-gpu), and [gcloud compute ssh](https://cloud.google.com/sdk/gcloud/reference/compute/ssh). This guide describes a deployment plan, not a measured GCP configuration.
