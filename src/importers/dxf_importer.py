#
#  (C) Copyright 2017  Pavel Tisnovsky
#
#  All rights reserved. This program and the accompanying materials
#  are made available under the terms of the Eclipse Public License v1.0
#  which accompanies this distribution, and is available at
#  http://www.eclipse.org/legal/epl-v10.html
#
#  Contributors:
#      Pavel Tisnovsky
#

from dxf_reader_state import *
from dxf_entity_type import *


class DxfImporter():

    def __init__(self, filename):
        self.filename = filename
        self.state_switcher = {
            DxfReaderState.BEGINNING: DxfImporter.process_beginning,
            DxfReaderState.BEGINNING_SECTION: DxfImporter.process_beginning_section,
            DxfReaderState.SECTION_HEADER: DxfImporter.process_section_header,
            DxfReaderState.SECTION_TABLES: DxfImporter.process_section_tables,
            DxfReaderState.SECTION_BLOCKS: DxfImporter.process_section_blocks,
            DxfReaderState.SECTION_ENTITIES: DxfImporter.process_section_entities,
            DxfReaderState.SECTION_OBJECTS: DxfImporter.process_section_objects,
        }

    def dxf_entry(self, fin):
        """Generate pair dxf_code + dxf_data for each iteration."""
        while True:
            line1 = fin.readline()
            line2 = fin.readline()
            if not line1 or not line2:
                break
            code = int(line1.strip())
            data = line2.strip()
            yield code, data

    def import_dxf(self):
        self.state = DxfReaderState.BEGINNING
        self.entity_type = DxfEntityType.UNKNOWN
        codeStr = None
        dataStr = None
        blockName = None

        with open(self.filename) as fin:
            lines = 0
            for code, data in self.dxf_entry(fin):
                function = self.state_switcher.get(self.state, lambda self, code, data: "nothing")
                function(self, code, data)
                lines += 1
        print(lines)



if __name__ == "__main__":
    importer = DxfImporter("Branna_3np.dxf")
    importer.import_dxf()
