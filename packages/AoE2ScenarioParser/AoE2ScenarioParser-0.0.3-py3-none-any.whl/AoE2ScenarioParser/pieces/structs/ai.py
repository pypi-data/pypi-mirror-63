from AoE2ScenarioParser.helper.datatype import DataType
from AoE2ScenarioParser.helper.retriever import Retriever
import AoE2ScenarioParser.pieces.structs.aoe2_struct as structs


class AIStruct(structs.Struct):
    def __init__(self, parser_obj=None, data=None):
        retrievers = [
            Retriever("Unknown, always 0", DataType("u32")),
            Retriever("Unknown, always 0 (2)", DataType("u32")),
            Retriever("AI .per file text", DataType("str32")),
        ]

        super().__init__("AI", retrievers, parser_obj, data)
