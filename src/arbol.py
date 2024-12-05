import sys

# Clase que representa un vértice
class Vertice:
    def __init__(self, id):
        self.id = id

# Clase que representa una arista con su peso
class Arista:
    def __init__(self, u, v, peso):
        self.u = u
        self.v = v
        self.peso = peso

# Clase que representa la gráfica
class Grafica:
    def __init__(self):
        self.vertices = {}
        self.aristas = []

    # Agregar un vértice a la gráfica
    def agregar_vertice(self, id):
        if id not in self.vertices:
            self.vertices[id] = Vertice(id)

    # Agregar una arista a la gráfica
    def agregar_arista(self, u, v, peso):
        self.aristas.append(Arista(u, v, peso))

    # Método para calcular el bosque generador máximo
    def bosque_generador_maximo(self):
        # Ordenar aristas por peso de mayor a menor
        self.aristas.sort(key=lambda arista: arista.peso, reverse=True)

        # Inicializar estructuras para union-find
        parent = {}
        rank = {}

        for v in self.vertices:
            parent[v] = v
            rank[v] = 0

        def find(v):
            if parent[v] != v:
                parent[v] = find(parent[v])
            return parent[v]

        def union(u, v):
            root_u = find(u)
            root_v = find(v)
            if root_u != root_v:
                if rank[root_u] > rank[root_v]:
                    parent[root_v] = root_u
                elif rank[root_u] < rank[root_v]:
                    parent[root_u] = root_v
                else:
                    parent[root_v] = root_u
                    rank[root_u] += 1

        # Generar bosque sin ciclos redundantes
        bosque = {}
        for arista in self.aristas:
            if find(arista.u) != find(arista.v):  # Evita ciclos
                union(arista.u, arista.v)
                root = find(arista.u)
                if root not in bosque:
                    bosque[root] = []
                bosque[root].append(arista)

        # Consolidar los árboles finales
        componentes = {}
        for vertice in self.vertices:
            root = find(vertice)
            if root not in componentes:
                componentes[root] = []
            componentes[root].extend(bosque.get(root, []))

        # Eliminar duplicados y retornar árboles únicos
        resultado = []
        for aristas in componentes.values():
            aristas_unicas = {f"{arista.u},{arista.v}:{arista.peso}": arista for arista in aristas}
            resultado.append(list(aristas_unicas.values()))

        return resultado

def main():
    # Verificar si se proporcionó el archivo de entrada (para no ponerlo en la terminal como en las pracs pasadas jajfjafj)
    if len(sys.argv) < 2:
        print("Por favor, proporciona el nombre del archivo de entrada.")
        return

    archivo_entrada = sys.argv[1]
    grafica = Grafica()

    try:
        with open(archivo_entrada, 'r') as archivo:
            lineas = archivo.readlines()

            # Leer vértices de la primera línea
            vertices = lineas[0].strip().split(',')
            for vertice in vertices:
                grafica.agregar_vertice(vertice)

            # Leer aristas de las líneas siguientes
            for linea in lineas[1:]:
                partes = linea.strip().split(':')
                u, v = partes[0].split(',')
                peso = int(partes[1])
                grafica.agregar_arista(u, v, peso)

        # Generar el bosque
        bosque = grafica.bosque_generador_maximo()

        # Imprimir el resultado
        print(f"Número de árboles: {len(bosque)}")
        for i, aristas in enumerate(bosque, 1):
            print(f"\nÁrbol {i}:")
            for arista in aristas:
                print(f"{arista.u},{arista.v}:{arista.peso}")

    except FileNotFoundError:
        print("No se pudo encontrar el archivo de entrada.")

if __name__ == "__main__":
    main()

