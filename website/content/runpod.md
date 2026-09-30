Use a **GPU Pod** for the persistent SelfJev HTTP server. This is a manual setup guide, not an implemented `selfjev deploy runpod` command. It has not been tested end to end by this project.

## 1. Configure the Pod

Choose a CUDA/PyTorch template with a 24 GB NVIDIA GPU, 16–32 GB system RAM, and sufficient persistent storage (budget 50 GB). Check the live hourly price before deploying. Configure SSH and set HTTP port **8000** in the Pod template.

Keep the checkout and model cache on a persistent volume, for example under `/workspace`. Storage and compute can have separate billing and lifecycle rules.

## 2. Install and serve

Connect using the Pod’s SSH instructions. Install Git LFS and uv if your template does not include them. Check the GPU with `nvidia-smi`.

```bash
cd /workspace
git clone https://github.com/Jwuthri/SelfJev.git
cd SelfJev
git lfs install
git lfs pull --include "weights/selfjev_4b_vision/*"
export HF_HOME=/workspace/huggingface
uv sync --frozen --no-dev --extra serve --extra gpu
export SELFJEV_API_KEYS="replace-with-a-long-random-key"
uv run --no-sync selfjev serve --host 0.0.0.0 --port 8000
```

Run the service under a process supervisor for ongoing use; an interactive SSH process may stop when the session closes. Wait until `/health` responds successfully inside the Pod.

## 3. Connect your application

The HTTP proxy exposes the service at the following base URL, with your own Pod id:

```text
https://POD_ID-8000.proxy.runpod.net
```

Set this as the SDK’s `base_url` and pass your Bearer key. The proxy provides HTTPS; the endpoint is public, so authentication must be configured. The proxy has a 100-second request timeout: long operations should use job submission and polling rather than a blocking inference request.

## 4. Finish the trial

Terminate the Pod when done. Review any retained volumes separately; stopping compute does not necessarily delete storage or stop its charges.

Provider references: [SSH access](https://docs.runpod.io/pods/configuration/use-ssh), [HTTP ports, proxy URLs, and timeouts](https://docs.runpod.io/pods/configuration/expose-ports). Provider behavior was checked when writing this guide; use the linked docs for current console details.
