"""Importer for drawings stored in a DXF format."""

#
#  (C) Copyright 2017, 2018  Pavel Tisnovsky
#
#  All rights reserved. This program and the accompanying materials
#  are made available under the terms of the Eclipse Public License v1.0
#  which accompanies this distribution, and is available at
#  http://www.eclipse.org/legal/epl-v10.html
#
#  Contributors:
#      Pavel Tisnovsky
#

from collections.abc import Iterator
from io import TextIOWrapper
from typing import Optional

from drawing import Drawing
from entities.arc import Arc
from entities.circle import Circle
from entities.drawing_entity_type import DrawingEntityType
from entities.line import Line
from entities.polyline import Polyline
from entities.text import Text
from importers.dxf_codes import DxfCodes
from importers.dxf_reader_state import DxfReaderState


class DxfImporter:
    """Importer for drawings stored in a DXF format."""

    def __init__(self, filename: str) -> None:
        """Initialize the importer."""
        self.filename = filename
        self.state_switcher = {
            DxfReaderState.BEGINNING: DxfImporter.process_beginning,
            DxfReaderState.BEGINNING_SECTION: DxfImporter.process_beginning_section,
            DxfReaderState.SECTION_HEADER: DxfImporter.process_section_header,
            DxfReaderState.SECTION_TABLES: DxfImporter.process_section_tables,
            DxfReaderState.SECTION_BLOCKS: DxfImporter.process_section_blocks,
            DxfReaderState.SECTION_ENTITIES: DxfImporter.process_section_entities,
            DxfReaderState.SECTION_OBJECTS: DxfImporter.process_section_objects,
            DxfReaderState.SECTION_CLASSES: DxfImporter.process_section_classes,
            DxfReaderState.SECTION_BLOCK: DxfImporter.process_section_block,
            DxfReaderState.ENTITY: DxfImporter.process_entity,
        }

    def dxf_entry(self, fin: TextIOWrapper) -> Iterator[tuple[int, str]]:
        """Generate pair dxf_code + dxf_data for each iteration."""
        linenumber = 0
        while True:
            line1 = None
            line2 = None
            linenumber += 1
            line1 = fin.readline()
            try:
                linenumber += 1
                line2 = fin.readline()
            except Exception as e:
                print(f"Error on line: {linenumber}")
                line2 = ""
            if not line1 or not line2:
                break
            code = int(line1.strip())
            data = line2.strip()
            yield code, data

    def init_import(self) -> None:
        """Initialize the object state before import."""
        self.state = DxfReaderState.BEGINNING
        self.entity_type = DrawingEntityType.UNKNOWN
        self.blockName : Optional[str] = None
        self.statistic = {
            DrawingEntityType.UNKNOWN: 0,
            DrawingEntityType.LINE: 0,
            DrawingEntityType.CIRCLE: 0,
            DrawingEntityType.ARC: 0,
            DrawingEntityType.TEXT: 0,
            DrawingEntityType.POLYLINE: 0,
        }
        self.entities :list = []

    def detect_encoding(self) -> Optional[str]:
        """Detect the encoding of DXF file."""
        encodings = ["utf-8", "windows-1250", "windows-1252"]
        for encoding in encodings:
            try:
                with open(self.filename, encoding=encoding) as fin:
                    fin.readlines()
                    fin.seek(0)
            except UnicodeDecodeError as e:
                # ok, we expect some errors ;)
                pass
            else:
                print(f"Encoding: {encoding}")
                return encoding
        return None

    def import_dxf(self) -> Drawing:
        """Import the DXF file and return structure containing all entities."""
        self.init_import()

        encoding = self.detect_encoding()

        with open(self.filename, encoding=encoding) as fin:
            lines = 0
            for code, data in self.dxf_entry(fin):
                function = self.state_switcher.get(
                    self.state, lambda self, code, data: "nothing"
                )
                function(self, code, data)
                lines += 1
        # print(lines)
        # print(self.statistic)
        return Drawing(self.entities, self.statistic, lines)

    def process_beginning(self, code: int, data: str) -> None:
        """Part of the DXF import state machine."""
        if code == DxfCodes.TEXT_STRING:
            if data == "SECTION":
                self.state = DxfReaderState.BEGINNING_SECTION
                print("section")
            elif data == "EOF":
                self.state = DxfReaderState.EOF
                print("eof")
        elif code == DxfCodes.COMMENT:
            print(data)
        else:
            raise Exception(f"unknown code {code} for state " "BEGINNING")

    def process_beginning_section_name_attribute(self, code: int, data: str) -> None:
        """Change the state of DXF reader."""
        if data == "HEADER":
            self.state = DxfReaderState.SECTION_HEADER
            print("    section header")
        elif data == "TABLES":
            self.state = DxfReaderState.SECTION_TABLES
            print("    section tables")
        elif data == "BLOCKS":
            self.state = DxfReaderState.SECTION_BLOCKS
            print("    section blocks")
        elif data == "ENTITIES":
            self.state = DxfReaderState.SECTION_ENTITIES
            print("    section entities")
        elif data == "OBJECTS":
            self.state = DxfReaderState.SECTION_OBJECTS
            print("    section objects")
        elif data == "CLASSES":
            self.state = DxfReaderState.SECTION_CLASSES
            print("    section classes")
        else:
            raise Exception(
                f"unknown data {data} for state " "BEGINNING_SECTION"
            )

    def process_beginning_section(self, code: int, data: str) -> None:
        """Part of the DXF import state machine."""
        if code == DxfCodes.NAME:
            self.process_beginning_section_name_attribute(code, data)
        else:
            raise Exception(
                f"unknown code {code} for state " "BEGINNING_SECTION"
            )

    def process_section_header(self, code: int, data: str) -> None:
        """Part of the DXF import state machine."""
        if code == DxfCodes.TEXT_STRING:
            if data == "ENDSEC":
                self.state = DxfReaderState.BEGINNING
                print("    end section header")

    def process_section_tables(self, code: int, data: str) -> None:
        """Part of the DXF import state machine."""
        if code == DxfCodes.TEXT_STRING:
            if data == "ENDSEC":
                self.state = DxfReaderState.BEGINNING
                print("    end section tables")

    def process_section_blocks(self, code: int, data: str) -> None:
        """Part of the DXF import state machine."""
        if code == DxfCodes.TEXT_STRING:
            if data == "BLOCK":
                self.state = DxfReaderState.SECTION_BLOCK
                # print("    block")
            elif data == "ENDSEC":
                self.state = DxfReaderState.BEGINNING
                print("    end section blocks")

    def process_section_block(self, code: int, data: str) -> None:
        """Part of the DXF import state machine."""
        if code == DxfCodes.TEXT_STRING:
            if data == "ENDBLK":
                # print("        end block")
                self.state = DxfReaderState.SECTION_BLOCKS
        elif code == DxfCodes.NAME:
            self.state = DxfReaderState.SECTION_BLOCK
            self.blockName = data
            # print("        begin block '{b}'".format(b=self.blockName))

    def process_section_entities_entity_type(self, code: int, data: str) -> None:
        """Change the state according to entity type code read from DXF."""
        self.polyline_points_x : list[float] = []
        self.polyline_points_y : list[float] = []
        if data == "LINE":
            self.state = DxfReaderState.ENTITY
            self.entityType = DrawingEntityType.LINE
        elif data == "CIRCLE":
            self.state = DxfReaderState.ENTITY
            self.entityType = DrawingEntityType.CIRCLE
        elif data == "ARC":
            self.state = DxfReaderState.ENTITY
            self.entityType = DrawingEntityType.ARC
        elif data == "LWPOLYLINE":
            self.state = DxfReaderState.ENTITY
            self.entityType = DrawingEntityType.POLYLINE
        elif data == "MTEXT" or data == "TEXT":
            self.state = DxfReaderState.ENTITY
            self.entityType = DrawingEntityType.TEXT

    def process_section_entities(self, code: int, data: str) -> None:
        """Part of the DXF import state machine."""
        if code == DxfCodes.TEXT_STRING:
            self.process_section_entities_entity_type(code, data)

    def process_section_objects(self, code: int, data: str) -> None:
        """Part of the DXF import state machine."""
        if code == DxfCodes.TEXT_STRING:
            if data == "ENDSEC":
                print("    end section objects")

    def process_section_classes(self, code, data) -> None:
        """Part of the DXF import state machine."""
        if code == DxfCodes.TEXT_STRING:
            if data == "ENDSEC":
                print("    end section classes")
                self.state = DxfReaderState.BEGINNING

    def process_entity_type_attribute(self, code: int, data: str) -> None:
        """Store the previously read entity and try to process next one."""
        self.statistic[self.entityType] += 1
        self.store_entity()
        self.state = DxfReaderState.SECTION_ENTITIES
        self.entityType = DrawingEntityType.UNKNOWN
        self.layer : Optional[str] = None
        self.color : Optional[int] = None
        self.polyline_points_x = []
        self.polyline_points_y = []
        self.mirror = 1
        if data == "LINE":
            self.state = DxfReaderState.ENTITY
            self.entityType = DrawingEntityType.LINE
        elif data == "CIRCLE":
            self.state = DxfReaderState.ENTITY
            self.entityType = DrawingEntityType.CIRCLE
        elif data == "ARC":
            self.state = DxfReaderState.ENTITY
            self.entityType = DrawingEntityType.ARC
        elif data == "LWPOLYLINE":
            self.state = DxfReaderState.ENTITY
            self.entityType = DrawingEntityType.POLYLINE
        elif data == "MTEXT" or data == "TEXT":
            self.state = DxfReaderState.ENTITY
            self.entityType = DrawingEntityType.TEXT
        elif data == "ENDSEC":
            self.state = DxfReaderState.BEGINNING
            self.entityType = DrawingEntityType.UNKNOWN
            print("    end entities")

    def process_entity(self, code: int, data: str) -> None:
        """Part of the DXF import state machine."""
        if code == DxfCodes.LAYER_NAME:
            self.layer = data.replace(" ", "_")
        elif code == DxfCodes.X1:
            self.x1 = float(data)
            if self.entityType == DrawingEntityType.POLYLINE:
                self.polyline_points_x.append(self.x1)
        elif code == DxfCodes.Y1:
            self.y1 = float(data)
            if self.entityType == DrawingEntityType.POLYLINE:
                self.polyline_points_y.append(self.y1)
        elif code == DxfCodes.X2:
            self.x2 = float(data)
        elif code == DxfCodes.Y2:
            self.y2 = float(data)
        elif code == DxfCodes.RADIUS:
            self.radius = float(data)
        elif code == DxfCodes.ANGLE1:
            self.angle1 = float(data)
        elif code == DxfCodes.ANGLE2:
            self.angle2 = float(data)
        elif code == DxfCodes.COLOR:
            self.color = int(data)
        elif code == DxfCodes.PRIMARY_TEXT:
            self.text = data
        elif code == DxfCodes.MIRROR:
            self.mirror = int(float(data))
        elif code == DxfCodes.TEXT_STRING:
            self.process_entity_type_attribute(code, data)

    def store_entity(self) -> None:
        """Store entity read from DXF file."""
        if self.entityType == DrawingEntityType.LINE:
            self.store_line()
        elif self.entityType == DrawingEntityType.CIRCLE:
            self.store_circle()
        elif self.entityType == DrawingEntityType.ARC:
            self.store_arc()
        elif self.entityType == DrawingEntityType.POLYLINE:
            self.store_polyline()
        elif self.entityType == DrawingEntityType.TEXT:
            self.store_text()
        else:
            print("unknown entity?")

    def store_line(self) -> None:
        """Store line read from DXF file."""
        self.entities.append(
            Line(self.x1, -self.y1, self.x2, -self.y2, self.color, self.layer)
        )

    def store_polyline(self) -> None:
        """Store polyline read from DXF file."""
        for i in range(len(self.polyline_points_y)):
            self.polyline_points_y[i] = -self.polyline_points_y[i]
        self.entities.append(
            Polyline(
                self.polyline_points_x, self.polyline_points_y, self.color, self.layer
            )
        )
        self.polyline_points_x = []
        self.polyline_points_y = []

    def store_circle(self) -> None:
        """Store circle read from DXF file."""
        if self.mirror == -1:
            print("MIRROR")
            self.x1 = -self.x1
        self.entities.append(
            Circle(self.x1, -self.y1, self.radius, self.color, self.layer)
        )

    def store_arc(self) -> None:
        """Store arc read from DXF file."""
        self.entities.append(
            Arc(
                self.x1,
                -self.y1,
                self.radius,
                self.angle1,
                self.angle2,
                self.color,
                self.layer,
            )
        )

    def store_text(self) -> None:
        """Store text read from DXF file."""
        if self.text:
            self.text = self.text.replace("\\U+00B2", "\u00B2")
        self.entities.append(Text(self.x1, -self.y1, self.text, self.color, self.layer))


if __name__ == "__main__":
    from exporters.drawing_exporter import DrawingExporter

    importer = DxfImporter("Branna_3np.dxf")
    entities = importer.import_dxf()
    exporter = DrawingExporter("Branna_3np.drawing", entities)
    exporter.export()
