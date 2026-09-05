# Solução do desafio `operation-001`

## Estado

`documented`.

A unidade versionada mantém o container previamente criado e faz systemd ser o
único responsável por reiniciá-lo. O container usa `RestartPolicy=no`, enquanto
`docker start -a scalepass` permite que systemd observe a saída do processo e
aplique `Restart=on-failure`.

No notebook, o serviço ficou ativo e acessível pelo PC principal na rede local.
Após `docker kill scalepass`, systemd iniciou novamente o container e o contador
`NRestarts` passou para `1`. A configuração sensível permaneceu em `/etc`, fora
do repositório e das evidências.
