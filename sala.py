import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

class Material:
    def __init__(self, nome, condutividade, descricao=""):
        self.nome = nome
        self.k = condutividade  # W/(m·K)
        self.descricao = descricao

class Abertura:
    def __init__(self, tipo, largura, altura, material):
        self.tipo = tipo
        self.largura = largura
        self.altura = altura
        self.material = material
        self.area = largura * altura

class FonteTermica:
    def __init__(self, tipo: str, potencia: float = None, btu: float = None, quantidade: int = 1):
        self.tipo = tipo
        self.potencia = potencia
        self.btu = btu
        self.quantidade = quantidade

    @property
    def ganho_perda_total(self) -> float:
        if self.tipo == 'ar condicionado' and self.btu is not None:
            potencia_watts = self.btu * 0.29307107
            return -potencia_watts * self.quantidade
        elif self.potencia is not None:
            return self.potencia * self.quantidade
        return 0

BIBLIOTECA_MATERIAIS = {
    'concreto': Material('Concreto', 1.75, 'Concreto normal'),
    'tijolo': Material('Tijolo', 0.72, 'Tijolo cerâmico'),
    'madeira': Material('Madeira', 0.15, 'Madeira maciça'),
    'isopor': Material('Isopor', 0.04, 'EPS - Poliestireno expandido'),
    'vidro_simples': Material('Vidro Simples', 1.0, 'Vidro comum 6mm'),
    'vidro_duplo': Material('Vidro Duplo', 0.32, 'Vidro duplo com câmara de ar'),
    'pvc': Material('PVC', 0.20, 'PVC rígido'),
    'alvenaria': Material('Alvenaria', 0.90, 'Alvenaria de tijolos'),
    'drywall': Material('Drywall', 0.35, 'Gesso acartonado'),
    'ceramica': Material('Cerâmica', 1.3, 'Piso cerâmico')
}

TABELA_GANHOS_PERDAS = {
    'pessoa': 115,
    'computador': 250,
    'lampada': 70,
    'ar condicionado': None,
    'impressora': 320,
    'geladeira': 180,
    'microondas': 1500
}

def listar_materiais():
    print("\nMateriais Disponíveis:")
    print("-" * 60)
    print(f"{'Código':<15} {'Material':<20} {'Condutividade':<15} {'Descrição'}")
    print("-" * 60)
    for codigo, material in BIBLIOTECA_MATERIAIS.items():
        print(f"{codigo:<15} {material.nome:<20} {material.k:<15.3f} {material.descricao}")
    print("-" * 60)

def listar_ganhos_perdas():
    print("\nTabela de Ganhos e Perdas Térmicas:")
    print("-" * 60)
    print(f"{'Fonte':<20} {'Potência (W) / BTU'}")
    print("-" * 60)
    for fonte, valor in TABELA_GANHOS_PERDAS.items():
        if valor:
            print(f"{fonte:<20} {valor} W")
        else:
            print(f"{fonte:<20} {'A ser fornecido pelo usuário'}")
    print("-" * 60)

def listar_opcoes(dic):
    print("\nSelecione uma das opções:")
    for i, (key, value) in enumerate(dic.items(), 1):
        print(f"{i}. {key} {'(A ser fornecido pelo usuário)' if value is None else ''}")
    print("0. Sem mais")
    return dic

def escolher_opcao(dic):
    listar_opcoes(dic)
    escolha = int(input("Digite o número da opção desejada: "))
    if escolha == 0:
        return 'sem mais'
    keys = list(dic.keys())
    return keys[escolha - 1]

def calcular_temperatura_interna(camadas, aberturas, fontes_termicas, temp_externa, dimensoes):
    largura, altura, profundidade = dimensoes
    area_total = 2 * (largura * altura + largura * profundidade + altura * profundidade)
    volume = largura * altura * profundidade

    area_aberturas = sum(a.area for a in aberturas)

    if area_aberturas >= area_total:
        raise ValueError("Área das aberturas não pode ser maior que a área total")

    area_paredes = area_total - area_aberturas

    R_paredes = 0
    for material, espessura in camadas:
        R_paredes += espessura / (material.k * area_paredes)

    R_aberturas = 0
    for abertura in aberturas:
        R_aberturas += 0.02 / (abertura.material.k * abertura.area)

    R_total = R_paredes + R_aberturas
    h_total = 15.0
    R_total += 1 / (h_total * area_total)
    carga_termica = sum(fonte.ganho_perda_total for fonte in fontes_termicas)
    cp_ar = 1200
    tempo = 3600
    delta_T = (carga_termica * tempo) / (cp_ar * volume)
    temp_interna = temp_externa + delta_T
    max_delta = 30

    if abs(temp_interna - temp_externa) > max_delta:
        temp_interna = temp_externa + max_delta if temp_interna > temp_externa else temp_externa - max_delta

    return temp_interna

def visualizar_sala(camadas, aberturas, temp_externa, temp_interna, dimensoes):
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')

    largura, altura, profundidade = dimensoes

    vertices = np.array([
        [0, 0, 0], [largura, 0, 0], [largura, profundidade, 0], [0, profundidade, 0],
        [0, 0, altura], [largura, 0, altura], [largura, profundidade, altura], [0, profundidade, altura]
    ])

    faces = [
        [vertices[0], vertices[1], vertices[5], vertices[4]],  # frente
        [vertices[1], vertices[2], vertices[6], vertices[5]],  # direita
        [vertices[2], vertices[3], vertices[7], vertices[6]],  # fundo
        [vertices[3], vertices[0], vertices[4], vertices[7]],  # esquerda
        [vertices[0], vertices[1], vertices[2], vertices[3]],  # base
        [vertices[4], vertices[5], vertices[6], vertices[7]]  # topo
    ]

    ax.add_collection3d(Poly3DCollection(faces, facecolors='white', alpha=0.25, linewidth=1, edgecolor='black'))

    for abertura in aberturas:
        if abertura.tipo == 'janela':
            vertices_janela = np.array([
                [0.1, 0, altura / 2],
                [0.1, 0, altura / 2 + abertura.altura],
                [0.1 + abertura.largura, 0, altura / 2 + abertura.altura],
                [0.1 + abertura.largura, 0, altura / 2]
            ])
            face_janela = [vertices_janela]
            ax.add_collection3d(Poly3DCollection(face_janela, facecolors='lightblue', alpha=0.5))
        elif abertura.tipo == 'porta':
            vertices_porta = np.array([
                [largura / 2, 0, 0],
                [largura / 2, 0, abertura.altura],
                [largura / 2 + abertura.largura, 0, abertura.altura],
                [largura / 2 + abertura.largura, 0, 0]
            ])
            face_porta = [vertices_porta]
            ax.add_collection3d(Poly3DCollection(face_porta, facecolors='brown', alpha=0.5))

    max_dim = max(largura, altura, profundidade)
    ax.set_box_aspect([largura / max_dim, profundidade / max_dim, altura / max_dim])

    ax.set_xlabel('Largura (m)')
    ax.set_ylabel('Profundidade (m)')
    ax.set_zlabel('Altura (m)')

    plt.title(f'Simulação da Sala\nTemp. Externa: {temp_externa:.1f}°C\nTemp. Interna: {temp_interna:.1f}°C')

    ax.set_xlim([0, largura])
    ax.set_ylim([0, profundidade])
    ax.set_zlim([0, altura])

    plt.show()


def main():
    try:

        print("Alunos:")
        print("Caio Cezar Jotta Nogueira (202212094)")
        print("Daniel Monteiro de Carvalho (202212193)")
        print("Davi Costa Antunes Narcizo (202211007)")
        print("Gabriel Victor Martins Carvalho (202212175)")
        print("Yago da Costa Jardim Alves Braga (202211004)")
        print("\nSimulação de Transferência de Calor em uma Sala")

        largura = float(input("Largura da sala (m): "))
        altura = float(input("Altura da sala (m): "))
        profundidade = float(input("Profundidade da sala (m): "))
        temp_externa = float(input("Temperatura externa (°C): "))

        dimensoes = (largura, altura, profundidade)

        print("\nConfigurações da sala:")
        listar_materiais()
        listar_ganhos_perdas()

        camadas = []
        while True:
            material = escolher_opcao(BIBLIOTECA_MATERIAIS)
            if material == 'sem mais':
                break
            espessura = float(input(f"Espessura da camada de {BIBLIOTECA_MATERIAIS[material].nome} (mm): ")) / 1000
            camadas.append((BIBLIOTECA_MATERIAIS[material], espessura))

        aberturas = []
        while True:
            print("\nAdicione uma abertura:")
            print("1. Porta")
            print("2. Janela")
            print("0. Sem mais")
            escolha = int(input("Digite o número da opção desejada: "))
            if escolha == 0:
                break
            tipo = 'porta' if escolha == 1 else 'janela'
            largura_abertura = float(input(f"Largura da {tipo} (m): "))
            altura_abertura = float(input(f"Altura da {tipo} (m): "))
            material = escolher_opcao(BIBLIOTECA_MATERIAIS)
            if material == 'sem mais':
                continue
            aberturas.append(Abertura(tipo, largura_abertura, altura_abertura, BIBLIOTECA_MATERIAIS[material]))

        fontes_termicas = []
        while True:
            tipo_fonte = escolher_opcao(TABELA_GANHOS_PERDAS)
            if tipo_fonte == 'sem mais':
                break

            quantidade = int(input(f"Quantidade de {tipo_fonte}: "))

            if tipo_fonte == 'ar condicionado':
                btu = float(input(f"Capacidade do {tipo_fonte} (BTU): "))
                ligado = input(f"O {tipo_fonte} está ligado? (s/n): ").lower() == 's'
                if ligado:
                    fontes_termicas.append(FonteTermica(tipo_fonte, btu=btu, quantidade=quantidade))
            elif tipo_fonte == 'pessoa':
                potencia = TABELA_GANHOS_PERDAS[tipo_fonte]
                fontes_termicas.append(FonteTermica(tipo_fonte, potencia=potencia, quantidade=quantidade))
            else:
                ligado = input(f"O {tipo_fonte} está ligado? (s/n): ").lower() == 's'
                if ligado:
                    potencia = TABELA_GANHOS_PERDAS[tipo_fonte]
                    fontes_termicas.append(FonteTermica(tipo_fonte, potencia=potencia, quantidade=quantidade))

        temp_interna = calcular_temperatura_interna(camadas, aberturas, fontes_termicas, temp_externa, dimensoes)
        print(f"\nTemperatura interna estimada: {temp_interna:.1f}°C")

        visualizar_sala(camadas, aberturas, temp_externa, temp_interna, dimensoes)

    except ValueError as e:
        print(f"\nErro: {e}")
    except Exception as e:
        print(f"\nOcorreu um erro inesperado: {e}")
        raise

if __name__ == "__main__":
    main()