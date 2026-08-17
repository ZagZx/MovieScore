# Requisitos MovieScore


### Requisitos funcionais
| RF | Requisito | Descrição |
| --- | --- | --- |
| RF01 | Cadastro de usuários | No sistema devem existir funcionalidades para o cadastro do usuário. |
| RF02 | Autenticação | Deve haver possibilidade de realizar login e logout.|
| RF03 | Avaliações | Deve ser possível avaliar um filme, série ou anime em uma pontuação de estrelas, de meia estrela até um máximo de 5 e opcionalmente, escrever um comentário.|
| RF04 | Favoritos |Deve ser possível para o usuário adicionar um conteúdo a uma lista de favoritos.|
| RF05 | Assistidos | Deve ser possível para o usuário adicionar um conteúdo a uma lista de assistidos.
| RF06 | Perfil de usuário | O usuário pode customizar seu perfil, podendo adicionar um texto de “Sobre mim”, foto de perfil e uma lista de gêneros favoritos. Isso ficará visível a outros usuários, também deve ser possível visualizar as listas de favoritos e assistidos do usuário, além de suas avaliações.
| RF07 | Buscar por nome | Deve ser possível realizar a pesquisa dos conteúdos por nome, selecionando se quer buscar por filme/série ou anime.
| RF08 | Conteúdo em destaque| Listagem dos filmes, séries e animes (separadamente) melhores avaliados, em ordem decrescente. Será exibida na página inicial porém de forma limitada, para visualizar mais conteúdo, deverá acessar a página específica para conteúdos de destaque.|



### Requisitos não funcionais
| RNF | Requisito | Descrição |
| --- | --- | --- |
| RNF01 | Os dados de filmes, séries e animes devem ser buscados em uma API externa | Dados como título, descrição, imagens e categorias devem ser buscadas apenas via API externa e não serão armazenados no banco.|
| RNF02 | Usabilidade | Todas as funcionalidades da aplicação devem ter um meio de acesso via interface web.|
| RNF03 | Autenticação | A autenticação deve ser realizada com tokens JWT.|
| RNF04 | Acesso | As funcionalidades de avaliar, comentar e favoritar devem ser restritas a usuários autenticados.|
