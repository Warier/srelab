# Domínio e regras funcionais

## Atores

### Visitante

- consulta eventos;
- cria uma conta;
- entra em uma conta existente.

### Usuário autenticado

- possui todas as capacidades do visitante;
- publica eventos;
- compra ingressos;
- consulta os próprios pedidos;
- encerra a sessão.

A versão atual não possui papéis separados de comprador, organizador e
administrador. Todo usuário autenticado pode publicar eventos.

## Evento

Um evento possui título, descrição, local, data, preço único e quantidade de
ingressos disponíveis. O preço é armazenado em centavos para evitar cálculos com
ponto flutuante.

Um evento é publicado imediatamente. Não há rascunho, revisão, cancelamento ou
edição.

## Pedido

Um pedido pertence a um comprador e a um evento. Ele registra a quantidade, o
valor total e o estado.

Regras atuais:

- cada compra contém ingressos de somente um evento;
- a quantidade deve estar entre 1 e 10;
- a quantidade não pode exceder o estoque visto pela aplicação;
- o valor total é o preço atual multiplicado pela quantidade;
- toda compra aceita recebe imediatamente o estado `paid`;
- o estoque é reduzido no mesmo commit que cria o pedido.

## Fluxos principais

### Publicar um evento

1. Usuário entra na conta.
2. Informa título, descrição, local, data, preço e estoque.
3. A aplicação valida os valores básicos.
4. O evento é persistido e passa a aparecer no catálogo.

### Comprar ingressos

1. Usuário abre um evento.
2. Escolhe uma quantidade entre 1 e 10.
3. A aplicação verifica a disponibilidade atual.
4. A aplicação reduz o estoque e cria um pedido pago.
5. Usuário é redirecionado ao histórico de ingressos.

## Fora do escopo atual

- assentos numerados;
- lotes com preços diferentes;
- carrinho;
- reserva com expiração;
- pagamentos reais e reembolsos;
- transferência ou validação de ingresso;
- notificações;
- múltiplas moedas;
- papéis administrativos.
