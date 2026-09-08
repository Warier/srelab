# Solução do desafio `load-001`

## Estado

`documented`.

O cenário usa uma conta e evento dedicados, configurados apenas por ambiente.
Cada usuário virtual mantém sua própria sessão, autentica em `on_start` e executa
o catálogo, o detalhe e a compra na proporção 6:3:1. As respostas esperadas são
validadas sem seguir redirecionamentos de POST.

As duas rodadas oficiais de 20 usuários não tiveram falhas. Um teste exploratório
posterior com 100 usuários revelou ao menos uma falha `sqlite is locked` durante
uma compra. Não houve correção nesta etapa: é evidência para reproduzir a disputa
de escrita e discutir SQLite/PostgreSQL nos desafios de concorrência.
