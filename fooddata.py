import json
from models import Ingrediente


# Clase que nos permite trabajar con los datos de prueba
class FoodData:

    # Propiedad que almacenará todos los alimentos
    alimentos = []
    platos = []
    fileAlimentos = None

    def __init__(self):
        # Carga del fichero de datos de prueba
        filePlatos = open("data/platos.json")
        self.fileAlimentos = open("data/alimentos.json")
        self.alimentos = json.load(self.fileAlimentos)
        self.platos = json.load(filePlatos)
        self.fileAlimentos.close()

    # INGREDIENTES
    # Devolucion asincrona de datos de alimentos
    async def get_ingredientes(self, skip, total):
        return {"alimentos": self.alimentos["alimentos"][skip : (total + skip)]}

    # Devolución asincrona de todos los datos de alimentos (sin filtros)
    async def get_allIngredientes(self):
        return self.alimentos

    # Devolucion asincrona de un alimento
    async def get_ingrediente(self, ingrediente_id: int):
        # Código antiguo
        # alimento={"Error, el ID: " + str(ingrediente_id) + " no se ha encontrado"}
        # alimento se inicializa a nulo
        # si no se encuentra el alimento se devolverá el nulo en vez de un objeto JSON
        alimento = None
        # Recorremos todos los datos JSON
        for item in self.alimentos["alimentos"]:
            # Comparamos el id que es int
            if item["id"] == ingrediente_id:
                alimento = item
                break
        return alimento

    # Recibimos y guardamos un nuevo ingrediente
    async def write_ingrediente(self, ingrediente: Ingrediente):
        self.fileAlimentos = open("data/alimentos.json", "w")
        # Obtenemos el ultimo ID de la lista
        ultimo_alimento = self.alimentos["alimentos"][-1]["id"]
        # Añadimos un nuevo id al ingrediente nuevo
        ingredienteDict = ingrediente.model_dump()
        ingredienteDict["id"] = ultimo_alimento + 1
        self.alimentos["alimentos"].append(ingredienteDict)
        json.dump(self.alimentos, self.fileAlimentos, indent=2)
        self.fileAlimentos.close()
        return ingredienteDict

    # Recibimos y actualizamos un ingrediente del JSON
    async def update_ingrediente(self, ingrediente_id: int, ingrediente: Ingrediente):

        self.fileAlimentos = open("data/alimentos.json", "w")

        # Buscamos el ingrediente

        ingredienteEncontrado = None

        ingredientePos = 0

        # Recorremos todos los datos JSON

        for item in self.alimentos["alimentos"]:

            # Comparamos el id que es int

            if item["id"] == ingrediente_id:

                ingredienteEncontrado = item

                break

            ingredientePos = ingredientePos + 1

        # Si se ha encontrado

        if ingredienteEncontrado:

            # Realizamos la actualization

            ingredienteDict = ingrediente.model_dump()

            for elem in ingredienteDict:

                if ingredienteDict[elem]:

                    # cambiamos el valor

                    self.alimentos["alimentos"][ingredientePos][elem] = ingredienteDict[
                        elem
                    ]

            json.dump(self.alimentos, self.fileAlimentos, indent=2)

            self.fileAlimentos.close()

            return self.alimentos["alimentos"][ingredientePos]

        else:

            return None

    # PLATOS
    # Devolución asincrona de datos de alimentos
    async def get_platos(self, skip, total):
        return {"platos": self.platos["platos"][skip : (total + skip)]}

    # Devolución asincrona de todos los datos de alimentos (sin filtros)
    async def get_allPlatos(self):
        return self.platos

    # Devolución asincrona de un alimento
    async def get_plato(self, plato_id: int):
        plato = None
        # Recorremos todos los datos JSON
        for item in self.platos["platos"]:
            # Comprobamos el id que es int
            if item["id"] == plato_id:
                plato = item
                break

        return plato

    async def get_ingredientePlato(self, plato_id: int, ingrediente_id: int):
        plato = await self.get_plato(plato_id)
        ingrediente = None

        if plato:
            for item in plato["ingredientes"]:
                if item["id"] == ingrediente_id:
                    ingrediente = await self.get_ingrediente(ingrediente_id)
                    break
        return ingrediente
