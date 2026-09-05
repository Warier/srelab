# Desafio `operation-001`: serviço recuperável no notebook

## Estado

`active`.

## Resultado esperado

Operar a imagem existente do ScalePass no notebook Arch Linux como um único
serviço gerenciado por systemd. O processo deve sobreviver a uma falha do
container, obedecer a limites explícitos e atender o PC principal pela rede local.

Não há imagem nova nem mudança na aplicação neste desafio. O resultado é uma
operação reproduzível do artefato `scalepass:0.1.0` já construído no desafio 006.

## Arquivo a criar

Crie `deploy/systemd/scalepass.service`. Ele será a cópia versionada da unidade
instalada no notebook; segredos e caminhos particulares do host não entram no
repositório.

O serviço deve ter esta responsabilidade única:

```text
systemd ── inicia e reinicia ──> Docker ── executa ──> container ScalePass
                                                   └─> volume /data
```

Use systemd como único responsável pelo reinício. Portanto, crie o container com
`--restart=no` e use `Restart=on-failure` na unidade. Duas políticas de reinício
concorrentes deixam a origem de uma recuperação ambígua.

## Preparação no notebook

No Arch Linux, instale e habilite o daemon Docker. Depois de adicionar o usuário
ao grupo `docker`, encerre e abra a sessão antes de testar sem `sudo`:

```bash
sudo pacman -S docker
sudo systemctl enable --now docker
sudo usermod -aG docker "$USER"
```

No notebook, obtenha o repositório na `main` atual e construa localmente a mesma
imagem. O registry é assunto futuro:

```bash
git clone <URL_DO_REPOSITORIO> scalepass
cd scalepass
git switch main
git pull --ff-only origin main
docker build -t scalepass:0.1.0 .
```

Crie um arquivo somente do host para a configuração sensível; nunca o versione,
nem copie seu valor para as evidências:

```bash
sudo install -d -m 0750 /etc/scalepass
sudo sh -c 'umask 077; openssl rand -hex 32 > /etc/scalepass/secret'
sudo sh -c 'printf "SCALEPASS_SECRET_KEY=%s\\n" "$(cat /etc/scalepass/secret)" > /etc/scalepass/scalepass.env'
```

O comando acima só é um exemplo de geração. Confira permissões com
`sudo stat -c '%a %U:%G' /etc/scalepass/scalepass.env`; o arquivo deve ser legível
apenas por root. Se não houver `openssl`, use outra fonte criptograficamente
segura para gerar o segredo.

## Container e unidade

Crie o volume e o container uma vez. Não use `docker run` dentro da unidade, pois
reinícios tentariam criar nomes e volumes novamente:

```bash
docker volume create scalepass-data
docker create --name scalepass \
  --restart=no \
  --memory=384m --memory-swap=384m --cpus=0.50 \
  --publish 0.0.0.0:8000:8000 \
  --mount source=scalepass-data,target=/data \
  --env-file /etc/scalepass/scalepass.env \
  scalepass:0.1.0
```

No `deploy/systemd/scalepass.service`, use os caminhos retornados por
`command -v docker` (em Arch normalmente `/usr/bin/docker`) e inclua, no mínimo:

- dependência de `docker.service` e de rede disponível;
- `ExecStartPre` que confirma a existência do container;
- `ExecStart` com `docker start -a scalepass`;
- `ExecStop` com `docker stop --time 15 scalepass`;
- `Restart=on-failure` e `RestartSec=5`;
- `WantedBy=multi-user.target`.

Uma referência de formato é:

```ini
[Unit]
Description=ScalePass container
Requires=docker.service
After=docker.service network-online.target
Wants=network-online.target

[Service]
Type=simple
Restart=on-failure
RestartSec=5
TimeoutStopSec=20
ExecStartPre=/usr/bin/docker container inspect scalepass
ExecStart=/usr/bin/docker start -a scalepass
ExecStop=/usr/bin/docker stop --time 15 scalepass

[Install]
WantedBy=multi-user.target
```

Instale a unidade a partir da cópia versionada e a habilite:

```bash
sudo install -D -m 0644 deploy/systemd/scalepass.service /etc/systemd/system/scalepass.service
sudo systemctl daemon-reload
sudo systemctl enable --now scalepass
```

## Prova exigida

1. `systemctl is-enabled scalepass` retorna `enabled` e
   `systemctl is-active scalepass` retorna `active`.
2. `docker inspect` mostra `Memory=402653184`, `NanoCpus=500000000` e política
   de restart `no` para o container.
3. No PC principal, `curl --fail http://<IP_LAN_DO_NOTEBOOK>:8000/api/events`
   retorna 200. Se falhar, investigue IP, rota, firewall e publicação de porta;
   não use `--network host` como atalho.
4. Execute `docker kill scalepass` e aguarde mais de cinco segundos. Sem chamar
   `systemctl restart`, prove que o serviço voltou a `active`, que
   `systemctl show -p NRestarts scalepass` aumentou e que o HTTP voltou a 200.
5. Mostre em `journalctl -u scalepass -b --no-pager` somente as linhas do ciclo
   de falha e recuperação. Não inclua o segredo.

`--memory-swap` igual a `--memory` impede swap adicional para o container. O
limite de CPU é uma quota média, não afinidade com um núcleo; a explicação de
`NanoCpus` está no chat deste desafio.

## Critérios de aceite

- a unidade está versionada em `deploy/systemd/` e passa em
  `systemd-analyze verify deploy/systemd/scalepass.service`;
- systemd, e não Docker, recupera o container após `docker kill`;
- os limites de 384 MiB e 0,5 CPU são verificáveis pelo inspect;
- o PC principal obtém HTTP 200 pela LAN;
- nenhum segredo ou arquivo de `/etc` entra no Git;
- gates existentes no repositório permanecem verdes;
- a evidência é curta: estado, limites, HTTP LAN, reinício e logs resumidos.

## Estudo direcionado

- ciclo de vida de um serviço systemd: unit, `enable`, `start`, `status`, journal
  e política de reinício;
- container criado versus iniciado, `docker start -a` e sinais de parada;
- volume nomeado, publicação de porta e diagnóstico de conectividade LAN;
- quota de CPU e limite de memória/swap no Docker.

Referências:

- [Docker: limites de recursos](https://docs.docker.com/engine/containers/resource_constraints/)
- [Docker: executar containers](https://docs.docker.com/reference/cli/docker/container/run/)
- [systemd.service](https://www.freedesktop.org/software/systemd/man/latest/systemd.service.html)
- [systemd.unit](https://www.freedesktop.org/software/systemd/man/latest/systemd.unit.html)

## Fora do escopo

Registry, Compose, HTTPS, proxy reverso, deploy automatizado, firewall como
política definitiva, Kubernetes e uma segunda instância. O próximo desafio mede
o comportamento deste único serviço sob carga.

## Git

- Branch: `challenge/007-notebook-service-operation`.
- Entrada: `challenge/007/start`.
- Conclusão: `challenge/007/solved`.
