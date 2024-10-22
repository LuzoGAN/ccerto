import pandas as pd
import flet as ft

# Carregar o arquivo Excel
df = pd.read_excel(r"C:\Users\luzo.neto\Downloads\Rede_Coopcerto_base_completa.xlsx")

# Função para obter os valores únicos de uma coluna
def obter_valores_unicos(coluna, filtro=None, filtro_coluna=None):
    if filtro is not None and filtro_coluna is not None:
        return ['Todos'] + sorted(df[df[filtro_coluna] == filtro][coluna].dropna().unique().tolist())
    else:
        return ['Todos'] + sorted(df[coluna].dropna().unique().tolist())


# Função para aplicar filtros e atualizar a tabela
def aplicar_filtros(controls, razao_social, nome_fantasia, uf_selecionado, cidade_selecionada, produto_selecionado):
    df_filtrado = df.copy()

    # Aplicar filtros de Razão Social e Nome Fantasia
    if razao_social:
        df_filtrado = df_filtrado[df_filtrado['Razão Social'].str.lower().str.contains(razao_social.lower())]

    if nome_fantasia:
        df_filtrado = df_filtrado[df_filtrado['Nome Fantasia'].str.lower().str.contains(nome_fantasia.lower())]

    # Aplicar filtros de UF, Cidade e Produto Habilitado
    if uf_selecionado != "Todos":
        df_filtrado = df_filtrado[df_filtrado['UF'] == uf_selecionado]

    if cidade_selecionada != "Todos":
        df_filtrado = df_filtrado[df_filtrado['Cidade'] == cidade_selecionada]

    if produto_selecionado != "Todos":
        df_filtrado = df_filtrado[df_filtrado['Produto Habilitado'] == produto_selecionado]

    # Limpar controles da tabela
    controls.clear()

    # Atualizar tabela com resultados filtrados
    for _, row in df_filtrado.iterrows():
        controls.append(
            ft.DataRow(cells=[
                ft.DataCell(ft.Text(row["CNPJ"])),
                ft.DataCell(ft.Text(row["Razão Social"])),
                ft.DataCell(ft.Text(row["Nome Fantasia"])),
                ft.DataCell(ft.Text(row["Endereço"])),
                ft.DataCell(ft.Text(row["Bairro"])),
                ft.DataCell(ft.Text(row["Cidade"])),
                ft.DataCell(ft.Text(row["UF"])),
                ft.DataCell(ft.Text(row["Produto Habilitado"])),
                ft.DataCell(ft.Text(row["Última Venda Coopcerto"])),
            ])
        )


# Função para atualizar as cidades com base na UF selecionada
def atualizar_cidades(e, cidade_dropdown, uf_value):
    # Obter as cidades únicas para a UF selecionada
    cidades = obter_valores_unicos("Cidade", filtro=uf_value, filtro_coluna="UF")

    # Limpar e atualizar as opções de cidades
    cidade_dropdown.options = [ft.dropdown.Option(x) for x in cidades]
    cidade_dropdown.value = "Todos"
    cidade_dropdown.update()


def main(page: ft.Page):
    # Carregar valores únicos para os comboboxes
    valores_uf = obter_valores_unicos("UF")
    valores_produto = obter_valores_unicos("Produto Habilitado")

    # Criação dos filtros (entradas e comboboxes)
    razao_social = ft.TextField(label="Razão Social", width=200)
    nome_fantasia = ft.TextField(label="Nome Fantasia", width=200)

    # Dropdowns para UF e Cidade (cidade será atualizada dinamicamente)
    uf_selecionado = ft.Dropdown(
        label="UF",
        options=[ft.dropdown.Option(x) for x in valores_uf],
        width=150,
        on_change=lambda e: atualizar_cidades(e, cidade_selecionada, uf_selecionado.value)
    )

    cidade_selecionada = ft.Dropdown(label="Cidade", options=[ft.dropdown.Option("Todos")], width=150)

    produto_selecionado = ft.Dropdown(label="Produto Habilitado",
                                      options=[ft.dropdown.Option(x) for x in valores_produto], width=200)

    # Lista de controle para a tabela
    tabela_dados = []

    # Tabela
    tabela = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("CNPJ")),
            ft.DataColumn(ft.Text("Razão Social")),
            ft.DataColumn(ft.Text("Nome Fantasia")),
            ft.DataColumn(ft.Text("Endereço")),
            ft.DataColumn(ft.Text("Bairro")),
            ft.DataColumn(ft.Text("Cidade")),
            ft.DataColumn(ft.Text("UF")),
            ft.DataColumn(ft.Text("Produto Habilitado")),
            ft.DataColumn(ft.Text("Última Venda Coopcerto")),
        ],
        rows=[]
    )

    # Envolver a tabela em uma coluna com rolagem
    tabela_container = ft.Column(
        controls=[tabela],
        expand=True,
        height=400,  # Definindo a altura do container para limitar o espaço e ativar a rolagem
        scroll=ft.ScrollMode.AUTO  # Habilitando a rolagem automática
    )

    # Botão de busca
    def on_search_click(e):
        aplicar_filtros(tabela.rows, razao_social.value, nome_fantasia.value, uf_selecionado.value,
                        cidade_selecionada.value, produto_selecionado.value)
        page.update()

    buscar_button = ft.ElevatedButton(text="Buscar", on_click=on_search_click)

    # Layout da página
    page.add(
        ft.Row([razao_social, nome_fantasia]),
        ft.Row([uf_selecionado, cidade_selecionada, produto_selecionado]),
        buscar_button,
        tabela_container  # Adiciona o container com rolagem
    )


# Iniciar a aplicação
ft.app(target=main)
