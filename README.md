# Sistema de Gerenciamento de Tarefas (To-Do List)

Sistema web desenvolvido em Python com Flask para gerenciamento de tarefas, com foco em usabilidade e performance. O projeto permite a criação, edição, exclusão e reordenação de tarefas de forma intuitiva.

## 🔗 Link de Acesso (Demo Online)
> **[Clique aqui para acessar o sistema online](https://masanari.pythonanywhere.com)**

## 🚀 Funcionalidades Principais
- **CRUD Completo:** Crie, leia, atualize e exclua tarefas facilmente.
- **Drag & Drop (Arrastar e Soltar):** Reordene a prioridade das tarefas apenas arrastando os itens na lista (com salvamento automático via AJAX).
- **Validação de Duplicidade:** O sistema impede o cadastro de duas tarefas com o mesmo nome.
- **Indicadores Visuais:** Tarefas com custo igual ou superior a R$ 1.000,00 são destacadas automaticamente em amarelo.
- **Ordenação Manual:** Botões para subir e descer a ordem das tarefas individualmente.

## 🛠️ Tecnologias Utilizadas
- **Backend:** Python 3, Flask
- **Banco de Dados:** SQLite (com tabela otimizada para ordenação).
- **Frontend:** HTML5, CSS3, Bootstrap 5
- **JavaScript:** SortableJS (para o Drag & Drop)
- **Hospedagem**: Pythonanywhere 

## 📦 Como Rodar Localmente
Se você quiser rodar este projeto na sua máquina:

1. **Clone o repositório:**
   ```bash
   git clone https://github.com/MasanariGit/Sistema-de-tarefas.git ```
   
   
   ## 🔮 Próximos Passos (Roadmap)

Como este projeto é um **MVP (Produto Mínimo Viável)** focado na demonstração pública, o banco de dados é atualmente compartilhado. As próximas atualizações focadas na V 2.0 incluem:

- [ ] **Sistema de Autenticação:** Implementar Login e Cadastro para que cada usuário tenha sua lista privada.
- [ ] **Categorias:** Permitir filtrar tarefas por etiquetas (ex: Trabalho, Pessoal).
- [ ] **Exportação:** Criar botão para baixar a lista em PDF ou Excel.

## 📝 Sobre o Desenvolvimento

Este projeto foi desenvolvido como um **MVP (Produto Mínimo Viável)** focado na resolução de problemas reais de organização.

O desafio principal foi implementar a lógica de **reordenação no banco de dados**, garantindo que a troca de posições fosse persistente e não apenas visual.