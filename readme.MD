# ⚖️ CRM Modular para Advogados (e muito mais)

Bem-vindo ao **CRM— um projeto pensado para ser **desacoplado**, escalável e adaptável a diferentes nichos de mercado.** 🛠️

> 🔍 **Objetivo:** Criar um sistema de gestão de relacionamento com clientes (**CRM**) que possa ser personalizado para diversos tipos de negócios — começando pelo nicho jurídico, com foco em advogados.

---

## 🚀 Visão Geral

Este projeto nasceu da necessidade de um CRM que **não esteja amarrado a um único modelo de negócio**, mas que possa ser estendido facilmente com regras específicas para diferentes perfis de usuários e segmentos.

Atualmente, ele está sendo desenvolvido com foco no **setor jurídico**, oferecendo recursos prontos para o dia a dia de um escritório de advocacia — mas sua arquitetura permite expansão futura para médicos, consultores, imobiliárias, farmaceuticos e etc.

---

## 🧠 Estrutura Inteligente

- 🧩 **Classe Base de Usuário (`User`)**  
  Uma estrutura genérica que serve de base para qualquer outro tipo de usuário. Toda autenticação, sessão e controle de acesso herda dessa camada.

- ⚖️ **Classe `Lawyer` (Advogado)**  
  Estende a classe `User`, com campos e rotas específicas para o segmento jurídico.  
  Isso permite ter tabelas separadas, mas integradas, mantendo a organização e clareza no banco de dados.

---

## 🔐 Autenticação e Segurança

- 🔑 Sistema de login com geração de token de sessão.
- ⏳ Sessões com validade configurável (padrão: 30 dias).
- 🌐 Verificação de IP para garantir que o token seja usado do mesmo local de origem.
- 🚫 Logout com remoção segura do token de sessão.

---

## 📚 Funcionalidades da API para `Lawyers`

O sistema já conta com uma API robusta para gerenciamento de advogados:

| Método   | Rota                                   | Descrição                                           |
| -------- | -------------------------------------- | --------------------------------------------------- |
| `POST`   | `/lawyers/`                            | 👤 Criação de um novo advogado                      |
| `PUT`    | `/lawyers/{id}`                        | ✏️ Atualização dos dados de um advogado             |
| `GET`    | `/lawyers/`                            | 📄 Listagem de todos os advogados                   |
| `GET`    | `/lawyers/{id}`                        | 🔍 Detalhes de um advogado específico               |
| `DELETE` | `/lawyers/{id}`                        | 🗑️ Exclusão individual                              |
| `DELETE` | `/lawyers/list`                        | 🗑️🗑️ Exclusão em massa a partir de uma lista de IDs |
| `PUT`    | `/lawyers/list`                        | ✅❌ Ativação ou desativação em massa de advogados  |
| `POST`   | `/lawyers/{id}/upload_profile_picture` | 📸 Upload da foto de perfil do advogado             |

---

## 🧩 Foco em Modularidade

O CRM foi projetado com desacoplamento em mente:

- Cada módulo (`User`, `Lawyer`, etc.) é **isolado e reutilizável**
- O projeto facilita a criação de **novos tipos de usuários** (como `Client`, `Staff`, `Partner`, etc.)
- Utiliza boas práticas de separação entre responsabilidades: autenticação, controle de sessão, modelos de dados e rotas bem divididas.

---

## 🔮 Próximos Passos

- 📁 CRUD para gestão de clientes dos advogados
- 📆 Agenda com lembretes e compromissos
- 📑 Upload de documentos por cliente
- 📊 Dashboards com estatísticas personalizadas
<!-- - 🌍 Internacionalização (multi-idioma) -->

---

## 🤝 Contribua com o Projeto

Você curtiu a ideia? Quer ajudar a melhorar ou expandir para outros nichos?  
Sinta-se à vontade para:

- ⭐ Dar uma estrela no repositório
- 🛠️ Enviar PRs com melhorias ou novas funcionalidades
- 🧠 Sugerir ideias via [issues](https://github.com/GBobello/crm/issues)

---

<!-- ## 🧾 Licença

Este projeto está sob a licença **MIT** — use, adapte e contribua como quiser!  
📄 Veja mais no arquivo [LICENSE](./LICENSE) -->
