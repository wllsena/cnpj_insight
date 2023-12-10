# CNPJ Insight

## Documentation

Access the documentation in: [https://wllsena.github.io/cnpj_insight/](https://wllsena.github.io/cnpj_insight/). Read the report in: [report.pdf](./report.pdf). Check out the diagrams in the [diagrams](./diagrams) folder.

If you want to run locally, you can download the SQLite database in [this drive](https://drive.google.com/file/d/1Rpl5RAMi0dN9nUSKiFoBFUoAU5mxIRbJ/view?usp=sharing), otherwise, you can check out the cloud-deployed version in [http://20.195.169.122:8000/](http://20.195.169.122:8000/).

Just let the database file in the root folder of the project. If you want to start a new database, you can migrate.

## Production
```bash
docker-compose -f docker-compose.prod.yml up --build
```

Access: http://localhost:1337

## Development
```bash
docker-compose -f docker-compose.yml up --build
```

Access: http://localhost:8000

In order to run the tests you need to run the following command:

```bash
docker-compose -f docker-compose.yml run --rm web python manage.py test
```

If you have any problems with the docker-compose, try to using the branch `dockerless`.


## Stop

```bash
docker-compose down -v
```

## User stories

| ID | Como um (Tipo de Usuário) | Eu preciso (Fazer alguma tarefa)                                   | Para que eu possa (Objetivo)                                                                                   | Prioridade | Status | Tempo estimado (horas) | Critério de Aceitação                                                              |
| -- | ------------------------- | ------------------------------------------------------------------ | -------------------------------------------------------------------------------------------------------------- | ---------- | ------ | ---------------------- | ---------------------------------------------------------------------------------- |
| 1  | Usuário do sistema        | Avaliar a confiabilidade de uma empresa                            | Saber por que empresa procurar para um melhor serviço                                                          | Alta       | Feito  | 8                      | Avaliações claras e consistentes, fácil interpretação dos resultados.              |
| 2  | Usuário do sistema        | Buscar informações de empresas por CNPJ                            | Obter detalhes relevantes como localidade, proprietário e data de criação                                      | Média      | Feito  | 10                     | Resultados precisos, busca rápida, filtro por CNPJ.                                |
| 3  | Administrador do sistema  | Gerenciar contas de usuário                                        | Manter a segurança do sistema                                                                                  | Alta       | Feito  | 15                     | Capacidade de adicionar, remover e editar contas, sistema de permissões robusto.   |
| 4  | Desenvolvedor do sistema  | Dockerizar o aplicativo                                            | Simplificar a implantação e gerenciamento                                                                      | Alta       | Feito  | 5                      | Aplicativo rodando de forma estável em um container Docker, documentação clara.    |
| 5  | Desenvolvedor do sistema  | Criar um sistema de indexação eficiente para os dados empresariais | Indexação escalável, atualização do índice automatizada, busca rápida e eficiente das informações empresariais | Alta       | Feito  | 20                     | Indexação rápida, atualizações automáticas, pesquisa eficaz.                       |
| 6  | Usuário do sistema        | Comparar duas empresas                                             | Melhorar a qualidade da minha análise                                                                          | Média      | Feito  | 6                      | Interface intuitiva para seleção e comparação, exibição clara de diferenças chave. |
| 7  | Usuário do sistema        | Criar uma conta e fazer login                                      | Acessar recursos adicionais                                                                                    | Alta       | Feito  | 4                      | Processo de registro e login seguro e fácil, recuperação de senha eficiente.       |
| 8  | Administrador do sistema  | Fazer backup do banco de dados                                     | Aumentar a redundância dos dados armazenados                                                                   | Alta       | Feito  | 2                      | Backups regulares, seguros e verificados.                                          |
| 9  | Usuário do sistema        | Exportar os resultados da pesquisa                                 | Realizar uma análise adicional                                                                                 | Média      | Feito  | 3                      | Capacidade de exportar em PDF, integridade dos dados exportados.                   |
| 10 | Usuário do sistema        | Acessar meu histórico de pesquisas                                 | Revisitar empresas e análises que consultei anteriormente                                                      | Média      | Feito  | 6                      | Visualização fácil do histórico, revisitar empresas listadas.                      |

Access the sheet with the user stories and use cases in: [https://docs.google.com/spreadsheets/d/15gOOOYpY2VHKhWmfb38dpLy1Z02NmH_nlopBd-CqTgw/edit?usp=sharing](https://docs.google.com/spreadsheets/d/15gOOOYpY2VHKhWmfb38dpLy1Z02NmH_nlopBd-CqTgw/edit?usp=sharing)

## Coverage

See in detail the coverage in [coverage_report.pdf](./coverage_report.pdf).

```
Name                        Stmts   Miss  Cover   Missing
---------------------------------------------------------
cnpj/__init__.py                0      0   100%
cnpj/admin.py                  60      0   100%
cnpj/apps.py                    4      0   100%
cnpj/cron.py                    6      6     0%   1-9
cnpj/documents.py              15      0   100%
cnpj/forms.py                   8      0   100%
cnpj/models.py                124     12    90%   36, 45, 54, 63, 74, 83, 104, 149, 164, 203, 230-231
cnpj/structure.py              41     41     0%   1-142
cnpj/tests/__init__.py          0      0   100%
cnpj/tests/test_forms.py        0      0   100%
cnpj/tests/test_models.py       0      0   100%
cnpj/tests/test_urls.py        25      0   100%
cnpj/tests/test_views.py       69      0   100%
cnpj/urls.py                    3      0   100%
cnpj/utils.py                  83     71    14%   61-90, 117-197, 212-286
cnpj/views.py                  72     23    68%   124-147, 173-180, 216-222, 282-291, 337-349
cnpj_insight/__init__.py        0      0   100%
cnpj_insight/asgi.py            9      9     0%   10-34
cnpj_insight/settings.py       29      0   100%
cnpj_insight/urls.py            4      0   100%
cnpj_insight/wsgi.py            4      4     0%   10-14
manage.py                      12      2    83%   12-13
media/__init__.py               0      0   100%
static/__init__.py              0      0   100%
staticfiles/__init__.py         0      0   100%
templates/__init__.py           0      0   100%
---------------------------------------------------------
TOTAL                         568    168    70%

```