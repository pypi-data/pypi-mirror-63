from AoE2ScenarioParser.helper.datatype import DataType
from AoE2ScenarioParser.helper.retriever import Retriever
import AoE2ScenarioParser.pieces.structs.aoe2_struct as structs


class TerrainStruct(structs.Struct):
    def __init__(self, parser_obj=None, data=None):
        retrievers = [
            Retriever("Terrain ID", DataType("u8")),
            Retriever("Elevation", DataType("u8")),
            Retriever("Unused", DataType("u8")),
            Retriever("Separator?", DataType("4"))
        ]

        super().__init__("Terrain", retrievers, parser_obj, data)
