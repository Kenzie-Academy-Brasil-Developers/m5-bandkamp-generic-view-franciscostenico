#   **M5 Band-Kamp API**

Essa aplicação é responsável por fornecer ao usuário uma RestAPI desenvolvida em Django, capaz de criar uma interação com um CRUD de usuários completo, bem como com a possibilidade de criação e listagens de Albuns e Músicas.

<br>

___
##  DER - Diagrama da aplicação

<br>


![BandKamp - ERD](./DER-BandKamp.svg)

<br>

**É feito uma interação entre 3 tabelas, sendo elas:**

1. `Users`: Tabela de cadastro de usuários. Faz uma relação **1:N** com a tabela *Albums*, onde um usuário pode criar vários albuns, enquanto que um álbum pode pertencer a apenas um usuário;
2.  `Albums`: Tabela para cadastro de álbums. Faz uma relação de **1:N** com a tabela *Songs*, onde um álbum pode conter várias músicas, mas uma música só pode pertencer a um álbum. Tambem faz uma relação de **N:1** com a table *Users*, já citada no item 1;
3.  `Songs`: Tabela para cadastro de músicas. Faz uma relação de **N:1** com a tabela *Albums*, já citada no item 2;
___

##  **Endpoints disponíveis**

Todas as rotas da API compartilham de uma mesma *URL Base*: **http://localhost:8000/api/**

<br>

### **`POST users/`** Criação de um novo usuário

Como esta é apenas uma aplicação experimental, todos os usuários cadastrados serão superuser.

<br>

**Corpo de requisição:**
```json
{
	"username": "franciscoSt",
	"email": "francisco@teste.com",
	"password": "1234Teste",
	"first_name": "Francisco",
	"last_name": "Stenico"
}
```

**Corpo de resposta**

<p><span style="color: #00af4d; font-weight: 700">201 </span><span style="color: #66ffaa">CREATED</span>: Usuário cadastrado com sucesso.</p>

```json
{
	"id": 1,
	"username": "franciscoSt",
	"email": "francisco@teste.com",
	"first_name": "Francisco",
	"last_name": "Stenico",
	"is_superuser": true
}
```

<p><span style="color: #df3d3d; font-weight: 700">400 </span><span style="color: #ff8888">BAD REQUEST</span>: O username e o email escolhido já estão em uso.</p>

```json
{
	"username": [
		"A user with that username already exists."
	],
	"email": [
		"This field must be unique."
	]
}
```

<p><span style="color: #df3d3d; font-weight: 700">400 </span><span style="color: #ff8888">BAD REQUEST</span>: Campos obrigatórios ausentes.</p>


```json
{
	"email": [
		"This field is required."
	],
	"password": [
		"This field is required."
	]
}
```
**Obs:** Em todas as requisições, caso algum campo obrigatório esteja ausente, será retornado um ***400 - BAD REQUEST*** no mesmo modelo abaixo:

<br>

___

### **`POST users/login`** Login de usuário

<br>

Esta rota retornará por padrão dois tokens de autenticação, um `refresh` token e um `access` token.

<br>

**Corpo da requisição**

```json
{
	"username": "franciscoSt",
	"password": "1234Teste"
}
```

Será feita a comparação entre a senha passada e a hash da mesma vinda do banco de dados. Caso ocorra esse match, o usuário receberá os dois tokens, caso contrário, retornará um *HTTP error*.

<br>

### **Corpos de respostas**

<br>

<p><span id="token" style="color: #00af4d; font-weight: 700">200 </span><span style="color: #66ffaa">OK</span>: Usuário cadastrado com sucesso.</p>

```json
{
	"refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTY3MTcxNTM2NiwiaWF0IjoxNjcxMTEwNTY2LCJqdGkiOiIzZDUyZDVkYjI5YWY0YTY2YjAxMGNlMWM3YmU0MzJjYiIsInVzZXJfaWQiOjJ9.d_KGiIj81mVx87RPUn7TVODboVLIJele-REdAuTuikg",
	"access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjcxMTY0NTY2LCJpYXQiOjE2NzExMTA1NjYsImp0aSI6Ijc3NGUxYjJiZWNkOTQxMjQ4MzM4NTc0MzcxNmZiNWQ0IiwidXNlcl9pZCI6Mn0.DOxNsr2FasBQqZuSCn7A2DpFt5Un_F5ywk4svAudLc8"
}
```

<p><span style="color: #df3d3d; font-weight: 700">401 </span><span style="color: #ff8888">UNAUTHORIZED</span>: Usuário e/ou senha inválidos.</p>

```json
{
	"detail": "No active account found with the given credentials"
}
```
<br>

___
### **`GET users/<int:user_id>/`**: Listagem de um perfil de usuário 🔒
##### ***ATENÇÃO**: Esta rota exige autenticação.*

<br>

A listagem deve ser feita apenas do próprio perfil do usuário. Caso seja feita a tentativa de listagem do perfil de outro usuário, um ***403 FORBIDDEN*** será lançado.

**Corpo de resposta**

<p><span style="color: #00af4d; font-weight: 700">200 </span><span style="color: #66ffaa">OK</span>: Listagem de usuário feita com sucesso.</p>

```json
{
	"id": 1,
	"username": "franciscoSt",
	"email": "francisco@teste.com",
	"first_name": "Francisco",
	"last_name": "Stenico",
	"is_superuser": true
}
```

<p><span style="color: #df3d3d; font-weight: 700">403 </span><span style="color: #ff8888">FORBIDDEN</span>: Tentativa de listagem de outro usuário.</p>

```json
{
	"detail": "You do not have permission to perform this action."
}
```

Caso o token de acesso não seja fornecido, um erro ***401 UNAUTHORIZED*** será lançado.

<p><span style="color: #df3d3d; font-weight: 700">401 </span><span style="color: #ff8888">UNAUTHORIZED</span>: Token de acesso não fornecido.</p>

```json
{
	"detail": "Authentication credentials were not provided."
}
```

No caso do token ser fornecido, mas não ser um token válido, será levantado um erro ***403 FORBIDDEN***.

<p><span style="color: #df3d3d; font-weight: 700">401 </span><span style="color: #ff8888">UNAUTHORIZED</span>: Token de acesso inválido.</p>

```json
{
	"detail": "Given token not valid for any token type",
	"code": "token_not_valid",
	"messages": [
		{
			"token_class": "AccessToken",
			"token_type": "access",
			"message": "Token is invalid or expired"
		}
	]
}
```

<br>
<p style="text-align: center; font-size: 1.2rem; color: #d6c15a"><span style="font-weight: 700">NOTA:</span> Os dois ultimos erros serão levantados em todas as rotas caso o <a href="#token">token</a> de acesso não seja fornecido ou inválido.</p>
<br>

___
### **`PATCH users/<int:user_id>/`**: Atualização de um perfil de usuário 🔒
##### ***ATENÇÃO**: Esta rota exige autenticação.*

<br>

A atualização feita pode ser tanto completa quanto parcial.

<br>

**Corpo de requisição**
```json
// Exemplo 1
{
	"username": "francisco.stenico"
}

// Exemplo 2
{
	"username": "francisco.stenico",
	"email": "francisco.stenico@teste.com",
	"first_name": "Fran",
	"last_name": "C. Stenico"
}
```

**Corpo de resposta**

<p><span style="color: #00af4d; font-weight: 700">200 </span><span style="color: #66ffaa">OK</span>: Atualização de usuário feita com sucesso.</p>

```json
{
	"id": 1,
	"username": "francisco.stenico",
	"email": "francisco.stenico@teste.com",
	"first_name": "Fran",
	"last_name": "C. Stenico",
	"is_superuser": true
}
```

Caso a *pk* passada como parâmetro não referencie nenhum usuário um ***404 NOT FOUND*** será levantado.

<p><span style="color: #df3d3d; font-weight: 700">404 </span><span style="color: #ff8888">NOT FOUND</span>: Usuário não encontrado.</p>

```json
{
	"detail": "Not found."
}
```

<br>
<p style="text-align: center; font-size: 1.2rem; color: #d6c15a"><span style="font-weight: 700">NOTE:</span> Em toda rota que for passado uma 'pk' como parâmetro de uma URL, se a mesma não retornar nenhum match, será lançado o mesmo erro 404 acima.</p>
<br>

___

### **`DELETE users/<int:user_id>/`**: Deleção de um perfil de usuário 🔒
##### ***ATENÇÃO**: Esta rota exige autenticação.*

<br>

Rota de deleção de usuário. Nesta rota é feito um hard delete, ou seja, os dados não persistirão no database caso retorne um sucesso desta rota.

<br>

**Corpo de resposta**

<p><span style="color: #00af4d; font-weight: 700">204 </span><span style="color: #66ffaa">NO CONTENT</span>: Deleção de usuário feita com sucesso.</p>

#### *Nenhum corpo de resposta é retornado desta solicitação.*

<br>

___

### **`POST albums/`**: Criação de um novo álbum 🔒
##### ***ATENÇÃO**: Esta rota exige autenticação.*

<br>

Rota responsável pela criação de um novo álbum de músicas. A partir deste, será possível ligar novas musicas adicionada através de seu *album_id*.

É passado a seguinte informação implicitamente à requisição:
- `user_id` : Recuperado do <a href="#token">token de autenticação</a> passado no login do usuário.

<br>

**Corpo de requisição**

```json
{
	"name": "Black Album",
	"year": 1991
}
```

**Corpo de resposta**

<p><span style="color: #00af4d; font-weight: 700">201 </span><span style="color: #66ffaa">CREATED</span>: Novo album criado!</p>

```json
{
	"id": 5,
	"name": "Black Album",
	"year": 1991,
	"user_id": 1
}
```

**NOTE:** O id do usuário logado que fez a requisição será vinculado ao album criado.

<br>

___
### **`GET albums/`**: Listagem de todos os álbums catalogados

<br>

Esta rota listará todos os álbuns catalogados, fazendo uma paginação de 2 em 2 itens.

**Corpo de resposta**

<p><span style="color: #00af4d; font-weight: 700">200 </span><span style="color: #66ffaa">OK</span>: Listagem de todos os álbuns catalogados.</p>

```json
{
    "count": 13,
    "next": "http://127.0.0.1:8000/api/albums/?page=5",
    "previous": "http://127.0.0.1:8000/api/albums/?page=3",
    "results": [
        {
			"id": 5,
			"name": "Black Album",
			"year": 1991,
			"user_id": 1
		},
		{
			"id": 6,
			"name": "Endgame",
			"year": 2011,
			"user_id": 2
		}
    ]
}
```

<br>

___
### **`POST albums/<int: album_id>/songs`**: Criação de uma nova música 🔒
##### ***ATENÇÃO**: Esta rota exige autenticação.*

<br>

Está rota é responsável pela criação de novas músicas. Nela, serão passados implicitamente o seguinte valor:
- **`album_id`** : Passado através do parâmetro da *URL*;

**Corpo de requisição**

```json
{
	"title": "The Unforgiven",
	"duration": 386
}
```

**Corpo de resposta**

<p><span style="color: #00af4d; font-weight: 700">201 </span><span style="color: #66ffaa">CREATED</span>: Nova música criada!</p>

```json
{
	"id": 4,
	"title": "The Unforgiven",
	"duration": "386",
	"album_id": 5
}
```

<br>

___
### **`POST albums/<int: album_id>/songs`**: Listagem do catálogo de músicas relacionadas a um álbum especifico 🔒

<br>

Rota responsável pela listagem de todas as músicas relacionadas ao `album_id` passado como parâmetro na *URL* da requisição.

<br>

**Corpo de resposta**

<p><span style="color: #00af4d; font-weight: 700">200 </span><span style="color: #66ffaa">OK</span>: Listagem do catálogo de músicas feita com sucesso!</p>

```json
{
	"count": 5,
	"next": "http://127.0.0.1:8000/api/albums/1/songs/?page=3",
	"previous": "http://127.0.0.1:8000/api/albums/1/songs/",
	"results": [
		{
			"id": 3,
			"title": "Holier Than Thou",
			"duration": "228",
			"album_id": 5
		},
		{
			"id": 4,
			"title": "The Unforgiven",
			"duration": "386",
			"album_id": 5
		}
	]
}
```
<br>

___

<br>

#### **Todos os testes manuais referentes ao que foi pedido na tarefa foram feitos, tendo todos passado com êxito retornando o resultado esperado!**

</br>

#### **Problemas ou dúvidas referentes ao desenvolvimento da aplicação?**
<div style="text-align: center"><br>
	<h3 style="font-weight: 700">Contatos</h3>
    <a href="https://kenzieacademybrasil.slack.com/archives/D036X87KUCV">
        <img alt="Francisco-Slack" height="30" width="40" src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/slack/slack-original.svg" />
    </a>
    <a href="mailto:francisco.stenico@gmail.com">
        <img alt="Francisco-Gmail" height="25" width="35" src="https://upload.wikimedia.org/wikipedia/commons/thumb/7/7e/Gmail_icon_%282020%29.svg/512px-Gmail_icon_%282020%29.svg.png?20221017173631" />
    </a>
    <a href="https://www.linkedin.com/in/franciscostenico/">
        <img alt="Francisco-LinkedIn" height="30" width="40" src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/linkedin/linkedin-original.svg" />
    </a>
	<p style="font-size: .75rem; color: #0a9afa; font-weight: 700">Francisco Correr Stenico - Desenvolvedor Web Full-Stack</p>
</div>

