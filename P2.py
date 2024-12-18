from collections import deque

class Campista:
    def __init__(self, objetos, peso_maximo):
        self.objetos = objetos
        self.peso_maximo = peso_maximo

    def ordenar_objetos_por_utilidad_peso(self):
        self.objetos.sort(key=lambda obj: obj['utilidad'] / obj['peso'], reverse=True)

    def resolver_mochila(self):
        n = len(self.objetos)
        peso_max = self.peso_maximo

        # Tabla DP: dp[i][w]
        dp = [[0] * (peso_max + 1) for _ in range(n + 1)]

        # Llena la tabla DP
        for i in range(1, n + 1):
            peso, utilidad = self.objetos[i - 1]['peso'], self.objetos[i - 1]['utilidad']
            for w in range(1, peso_max + 1):
                if peso <= w:
                    dp[i][w] = max(dp[i - 1][w], dp[i - 1][w - peso] + utilidad)
                else:
                    dp[i][w] = dp[i - 1][w]

        # Reconstruir la solución óptima
        w = peso_max
        objetos_seleccionados = []
        for i in range(n, 0, -1):
            if dp[i][w] != dp[i - 1][w]:  # Si el objeto fue incluido
                objetos_seleccionados.append(self.objetos[i - 1])
                w -= self.objetos[i - 1]['peso']

        return dp[n][peso_max], objetos_seleccionados

    def explorar_combinaciones_bfs(self):
        cola = deque()
        cola.append((0, 0, []))  # (utilidad_actual, peso_actual, objetos_seleccionados)
        max_utilidad = 0
        mejor_seleccion = []

        while cola:
            utilidad_actual, peso_actual, seleccion_actual = cola.popleft()

            if utilidad_actual > max_utilidad:
                max_utilidad = utilidad_actual
                mejor_seleccion = seleccion_actual

            for obj in self.objetos:
                if obj not in seleccion_actual and peso_actual + obj['peso'] <= self.peso_maximo:
                    cola.append((utilidad_actual + obj['utilidad'],
                                 peso_actual + obj['peso'],
                                 seleccion_actual + [obj]))

        return max_utilidad, mejor_seleccion

# Ejemplo de cosas que quieres llevar
if __name__ == "__main__":
    # Lista de objetos (puedes modificar estos datos)
    objetos = [
        {"nombre": "Linterna", "peso": 2, "utilidad": 10},
        {"nombre": "Cuerda", "peso": 1, "utilidad": 5},
        {"nombre": "Botiquín", "peso": 3, "utilidad": 15},
        {"nombre": "Manta", "peso": 4, "utilidad": 7},
        {"nombre": "Cantimplora", "peso": 1, "utilidad": 8}
    ]
    peso_maximo = 5 # Capacidad de la mochila

    # Crear el campista
    campista = Campista(objetos, peso_maximo)

    # Resolver usando programación dinámica
    campista.ordenar_objetos_por_utilidad_peso()  # Ordenar objetos por utilidad/peso
    utilidad_dp, seleccion_dp = campista.resolver_mochila()

    # Resolver usando BFS
    utilidad_bfs, seleccion_bfs = campista.explorar_combinaciones_bfs()

    # Mostrar resultados
    print("Resultados Programación Dinámica:")
    print(f"Máxima utilidad: {utilidad_dp}")
    print("Objetos seleccionados:")
    for obj in seleccion_dp:
        print(f" - {obj['nombre']} (Peso: {obj['peso']}, Utilidad: {obj['utilidad']})")

    print("\nResultados BFS:")
    print(f"Máxima utilidad: {utilidad_bfs}")
    print("Objetos seleccionados:")
    for obj in seleccion_bfs:
        print(f" - {obj['nombre']} (Peso: {obj['peso']}, Utilidad: {obj['utilidad']})")
