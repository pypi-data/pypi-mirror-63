from AoE2ScenarioParser.helper.datatype import DataType
from AoE2ScenarioParser.helper.retriever import Retriever
import AoE2ScenarioParser.pieces.structs.aoe2_struct as structs
from AoE2ScenarioParser.pieces.structs.unit import UnitStruct


class PlayerUnitsStruct(structs.Struct):
    def __init__(self, parser_obj=None, data=None):
        retrievers = [
            Retriever("Unit count", DataType("u32"), save_as="unit_count"),
            Retriever("Units", DataType(UnitStruct), set_repeat="{unit_count}")
        ]

        super().__init__("Player Units", retrievers, parser_obj, data)
