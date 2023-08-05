# TaskSquirrel

TaskSquirrel executes tasks from a `Tasqfile.yml`. It is similar to `make`
or `invoke`. It also supports Kubernetes workflows like `Argo` and `Airflow`.

Differences from other tools are:

- configuration is in YAML
- it supports multiple scripts / languages
- it supports Jinja2 templating
- it has built-in support for executing code in Docker and on Kubernetes clusters
- it is completely serverless: all it requires for interacting with a K8s cluster is Kubectl

TaskSquirrel is a good replacement for `invoke` and `make` even if you don't use
the container-related features, but it is particularly well suited to data analysis
and deep learning workflows.


# Commands

- `tasq --help` -- display help
- `tasq list` -- list all commands
- `tasq run command` -- run a command

# Example

## Simple replacement for invoke

```
tasks:
    venv:
      - doc: build the virtual environment
      - script: |
          test -d venv || virtualenv venv
          venv/bin/pip3 install -U -r requirements.txt

    newversion:
      - doc: increase the patch version number
      - python: |
          version = map(int, open("VERSION").read().strip().split("."))
          version[-1] += 1
          with open("VERSION", "w") as stream:
            stream.write(".".join(map(str, version)))

    publish:
      - doc: publish to PyPI
      - script: twine upload
```

## Kubernetes Example

```
params:

  cluster: "mycluster"
  image: "mycompute"

tasks:

    image:
      docker_container: {{ image }}
        dockerfile: ./Docker
        push: tmbdev/{{ image }}
        context:
          - simple.key
          - scripts/start.sh

    kutest:
      - doc: start a job on K8s and wait for its completion
      - task: image
      - with_braceexpand: "{000..999}"
        param: shard
        tasks:
          - kubectl_apply: hello
            template_name: myjob
            params:
              id: hello-{{ shard }}
              script: |
                echo hello-{{ shard }};
                sleep 30
      - kubectl_wait:
        kind: jobs
        prefix: hello-
      - script: kubectl delete jobs --all

k8s_templates:

  myjob: |
    apiVersion: batch/v1
    kind: Job
    metadata:
      name: "{{ id }}"
    spec:
      template:
        spec:
          containers:
          - name: main
            image: "{{ image }}"
            command: ["/bin/bash", "-c", "{{ script }}"]
          restartPolicy: Never
      backoffLimit: 4
```

# Status

It's pre-alpha.
