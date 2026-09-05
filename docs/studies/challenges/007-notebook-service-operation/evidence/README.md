# Evidências do desafio `operation-001`

## Estado

`pending`.

Ao concluir, registre de forma curta: estado do serviço, limites no inspect,
HTTP pela LAN, recuperação após `docker kill` e trecho mínimo do journal.

```bash
sudo docker inspect --format 'Memory={{.HostConfig.Memory}} NanoCpus={{.HostConfig.NanoCpus}} RestartPolicy={{.HostConfig.RestartPolicy.Name}}' scalepass
Memory=402653184 NanoCpus=500000000 RestartPolicy=no
[warier@warierArch srelab]$ systemctl show -p NRestarts scalepass
NRestarts=0
[warier@warierArch srelab]$ journalctl -u scalepass -b --no-pager -n 25
Sep 05 04:01:36 warierArch docker[13064]: INFO:     172.17.0.1:38342 - "GET /static/style.css HTTP/1.1" 200 OK
Sep 05 04:01:37 warierArch docker[13064]: INFO:     172.17.0.1:38342 - "GET /favicon.ico HTTP/1.1" 404 Not Found
Sep 05 04:01:45 warierArch docker[13064]: INFO:     172.17.0.1:37554 - "POST /login HTTP/1.1" 400 Bad Request
Sep 05 04:01:45 warierArch docker[13064]: INFO:     127.0.0.1:55508 - "GET /api/events HTTP/1.1" 200 OK
Sep 05 04:01:47 warierArch docker[13064]: INFO:     172.17.0.1:37554 - "GET /register HTTP/1.1" 200 OK
Sep 05 04:01:57 warierArch docker[13064]: INFO:     127.0.0.1:52982 - "GET /api/events HTTP/1.1" 200 OK
Sep 05 04:01:57 warierArch docker[13064]: New user registered: 1
Sep 05 04:01:57 warierArch docker[13064]: INFO:     172.17.0.1:52164 - "POST /register HTTP/1.1" 303 See Other
Sep 05 04:01:57 warierArch docker[13064]: INFO:     172.17.0.1:52164 - "GET / HTTP/1.1" 200 OK
Sep 05 04:02:01 warierArch docker[13064]: INFO:     172.17.0.1:52164 - "GET /events/new HTTP/1.1" 200 OK
Sep 05 04:02:08 warierArch docker[13064]: INFO:     127.0.0.1:56864 - "GET /api/events HTTP/1.1" 200 OK
Sep 05 04:02:20 warierArch docker[13064]: INFO:     127.0.0.1:37620 - "GET /api/events HTTP/1.1" 200 OK
Sep 05 04:02:20 warierArch docker[13064]: New event created: 1
Sep 05 04:02:20 warierArch docker[13064]: INFO:     172.17.0.1:46798 - "POST /events HTTP/1.1" 303 See Other
Sep 05 04:02:20 warierArch docker[13064]: INFO:     172.17.0.1:46798 - "GET /events/1 HTTP/1.1" 200 OK
Sep 05 04:02:31 warierArch docker[13064]: INFO:     127.0.0.1:52672 - "GET /api/events HTTP/1.1" 200 OK
Sep 05 04:02:34 warierArch docker[13064]: Order paid: 1
Sep 05 04:02:34 warierArch docker[13064]: INFO:     172.17.0.1:43780 - "POST /events/1/buy HTTP/1.1" 303 See Other
Sep 05 04:02:34 warierArch docker[13064]: INFO:     172.17.0.1:43780 - "GET /orders HTTP/1.1" 200 OK
Sep 05 04:02:38 warierArch docker[13064]: INFO:     172.17.0.1:43780 - "GET / HTTP/1.1" 200 OK
Sep 05 04:02:43 warierArch docker[13064]: INFO:     127.0.0.1:59274 - "GET /api/events HTTP/1.1" 200 OK
Sep 05 04:02:54 warierArch docker[13064]: INFO:     127.0.0.1:57630 - "GET /api/events HTTP/1.1" 200 OK
Sep 05 04:03:06 warierArch docker[13064]: INFO:     127.0.0.1:55584 - "GET /api/events HTTP/1.1" 200 OK
Sep 05 04:03:17 warierArch docker[13064]: INFO:     127.0.0.1:52916 - "GET /api/events HTTP/1.1" 200 OK
Sep 05 04:03:29 warierArch docker[13064]: INFO:     127.0.0.1:38854 - "GET /api/events HTTP/1.1" 200 OK
[warier@warierArch srelab]$ docker kill scalepass
permission denied while trying to connect to the docker API at unix:///var/run/docker.sock
[warier@warierArch srelab]$ sudo docker kill scalepass
[sudo] password for warier: 
scalepass
[warier@warierArch srelab]$ journalctl -u scalepass -b --no-pager -n 25systemctl is-active scalepassFailed to add match '25systemctl': Invalid argument
[warier@warierArch srelab]$ systemctl is-active scalepass
active
[warier@warierArch srelab]$ systemctl show -p NRestarts scalepass
NRestarts=1
[warier@warierArch srelab]$ journalctl -u scalepass -b --no-pager -n 25
Sep 05 04:31:35 warierArch docker[20727]:                     "DNSNames": null
Sep 05 04:31:35 warierArch docker[20727]:                 }
Sep 05 04:31:35 warierArch docker[20727]:             }
Sep 05 04:31:35 warierArch docker[20727]:         },
Sep 05 04:31:35 warierArch docker[20727]:         "ImageManifestDescriptor": {
Sep 05 04:31:35 warierArch docker[20727]:             "mediaType": "application/vnd.oci.image.manifest.v1+json",
Sep 05 04:31:35 warierArch docker[20727]:             "digest": "sha256:7bdbfa500506ddfacbcea2a2ed3cf81ff02596b1e8b8d0ec901827f272716af6",
Sep 05 04:31:35 warierArch docker[20727]:             "size": 1813,
Sep 05 04:31:35 warierArch docker[20727]:             "platform": {
Sep 05 04:31:35 warierArch docker[20727]:                 "architecture": "amd64",
Sep 05 04:31:35 warierArch docker[20727]:                 "os": "linux"
Sep 05 04:31:35 warierArch docker[20727]:             }
Sep 05 04:31:35 warierArch docker[20727]:         }
Sep 05 04:31:35 warierArch docker[20727]:     }
Sep 05 04:31:35 warierArch docker[20727]: ]
Sep 05 04:31:35 warierArch systemd[1]: Started ScalePass container.
Sep 05 04:31:43 warierArch docker[20737]: INFO:     Started server process [1]
Sep 05 04:31:43 warierArch docker[20737]: INFO:     Waiting for application startup.
Sep 05 04:31:43 warierArch docker[20737]: ScalePass started
Sep 05 04:31:43 warierArch docker[20737]: INFO:     Application startup complete.
Sep 05 04:31:43 warierArch docker[20737]: INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
Sep 05 04:31:43 warierArch docker[20737]: INFO:     127.0.0.1:56074 - "GET /api/events HTTP/1.1" 200 OK
Sep 05 04:31:55 warierArch docker[20737]: INFO:     127.0.0.1:39242 - "GET /api/events HTTP/1.1" 200 OK
Sep 05 04:32:06 warierArch docker[20737]: INFO:     127.0.0.1:46114 - "GET /api/events HTTP/1.1" 200 OK
Sep 05 04:32:18 warierArch docker[20737]: INFO:     127.0.0.1:34232 - "GET /api/events HTTP/1.1" 200 OK
```