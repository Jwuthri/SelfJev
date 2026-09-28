Use a Linux NVIDIA GPU host with Docker and the [NVIDIA Container Toolkit](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html). This image serves the model, not the marketing website.

## Build the image

Clone the repository and fetch the real adapter files. Git LFS pointers cannot be used as weights.

```bash
git clone https://github.com/Jwuthri/SelfJev.git
cd SelfJev
git lfs install
git lfs pull --include "weights/selfjev_4b/*"
docker build -f deploy/Dockerfile -t selfjev .
```

By default, the pinned base model is baked into the image. For a smaller image, pass `--build-arg BAKE_MODEL=0`; first startup then needs network access to download the model. Allow substantial build time and disk space.

## Run it

```bash
export SELFJEV_API_KEYS="replace-with-a-long-random-key"
docker run -d --name selfjev --restart unless-stopped \
  --gpus all \
  -p 127.0.0.1:8000:8000 \
  -e SELFJEV_API_KEYS \
  -v selfjev-models:/models \
  selfjev
```

The port is bound to the host’s loopback interface. Access it through an SSH tunnel or an HTTPS reverse proxy on that host. The process inside the container listens on all container interfaces.

```bash
docker logs -f selfjev
curl --fail http://localhost:8000/health
```

Readiness comes after model loading. The image includes a `/health` health check.

## Persist fine-tuning jobs

Add a volume at `/root/.selfjev` and enable `--fine-tuning` in the service command. Training shares the GPU; plan for a 48 GB GPU or train separately. See [fine-tuning](/docs/finetuning/).

The checked-in [Dockerfile](https://github.com/Jwuthri/SelfJev/blob/master/deploy/Dockerfile) and [Compose configuration](https://github.com/Jwuthri/SelfJev/blob/master/deploy/docker-compose.yml) are the source of truth. The deployment container has not been exercised end to end in the recorded research runs.
