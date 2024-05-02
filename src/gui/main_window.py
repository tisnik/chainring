"""Main window shown on screen."""

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

import tkinter
from tkinter import messagebox

from draw_service import DrawServiceInterface
from exporters.drawing_exporter import DrawingExporter
from exporters.room_exporter import RoomExporter
from geometry.utils import GeometryUtils
from geometry.bounds import Bounds
from geometry.rescaler import Rescaler
from gui.canvas import Canvas
from gui.canvas_mode import CanvasMode
from gui.dialogs.error_dialogs import *
from gui.dialogs.load_dialogs import LoadDialogs
from gui.dialogs.room_error_dialog import *
from gui.dialogs.save_dialogs import SaveDialogs
from gui.dialogs.yes_no_dialogs import *
from gui.icons import *
from gui.menubar import *
from gui.palette import *
from gui.room import Room
from gui.status_bar import *
from gui.toolbar import *
from importers.drawing_importer import DrawingImporter
from importers.dxf_importer import DxfImporter
from importers.room_importer import RoomImporter


class MainWindow:
    """Main window shown on screen."""

    SCALE_UP_FACTOR = 1.1
    SCALE_DOWN_FACTOR = 0.9

    def __init__(self, configuration):
        """Initialize main window."""
        self._drawing = None
        self.root = tkinter.Tk()
        self.root.title("Integrace CAD výkresů do SAP, (c) eLevel system")

        self.icons = Icons()
        self.canvas_mode = CanvasMode.VIEW

        self.configuration = configuration
        self.rooms_export_filename = None

        window_width = configuration.window_width
        window_height = configuration.window_height

        self.canvas = Canvas(self.root, window_width, window_height, self)
        self.palette = Palette(self.root, self)
        self.toolbar = Toolbar(self.root, self, self.canvas)
        self.statusbar = StatusBar(self.root)

        self.menubar = Menubar(self.root, self, self.canvas)

        self.root.config(menu=self.menubar)

        self.configure_grid()

        self.toolbar.grid(column=1, row=1, columnspan=2, sticky="WE")
        self.palette.grid(column=1, row=2, sticky="NWSE")
        self.canvas.grid(column=2, row=2, sticky="NWSE")
        self.statusbar.grid(column=1, row=3, columnspan=2, sticky="WE")

        self.canvas.bind("<ButtonPress-1>", self.on_left_button_pressed)
        self.canvas.bind("<B1-Motion>", self.on_left_button_drag)
        self.canvas.bind("<ButtonPress-3>", self.on_right_button_pressed)

        # scroll on Linux
        self.canvas.bind("<Button-4>", self.zoom_plus)
        self.canvas.bind("<Button-5>", self.zoom_minus)

        # scroll on windows
        self.canvas.bind("<MouseWheel>", self.zoom)

        self.room = Room()
        self.edited_room_id = None

    def send_drawing_to_server(self):
        """Send the drawing to server."""
        if self.drawing is None:
            messagebox.showerror("Nastala chyba", "Výkres není aktivní")
            return
        if self.drawing.drawing_id is None:
            messagebox.showerror(
                "Nastala chyba", "Výkres nemá přiřazen jednoznačný identifikátor (ID)"
            )
            return
        address = self.configuration.server_address
        port = self.configuration.server_port
        if not address:
            messagebox.showerror("Nastala chyba", "Není nastavená adresa serveru")
            return
        if not port:
            messagebox.showerror("Nastala chyba", "Není nastaven port serveru")
            return
        url = DrawServiceInterface.get_url(address, port)
        drawServiceInterface = DrawServiceInterface(service_url=url)
        status, message = drawServiceInterface.send_drawing(self.drawing)
        if status:
            messagebox.showinfo("Výsledek operace", message)
        else:
            messagebox.showerror(
                "Nastala chyba", f"Nastala chyba: {message}"
            )

    def disable_ui_items_for_no_drawing_mode(self):
        """Disable all related UI items when the application is set to no drawing mode."""
        self.toolbar.disable_ui_items_for_no_drawing_mode()
        self.menubar.disable_ui_items_for_no_drawing_mode()

    def enable_ui_items_for_drawing_mode(self):
        """Enable all related UI items when the application is set to drawing mode."""
        self.toolbar.enable_ui_items_for_drawing_mode()
        self.menubar.enable_ui_items_for_drawing_mode()

    def set_ui_items_for_actual_mode(self):
        """Enable or disable all related UI items according to current application mode."""
        if self.drawing is None:
            self.disable_ui_items_for_no_drawing_mode()
        else:
            self.enable_ui_items_for_drawing_mode()

    def configure_grid(self):
        """Configure grid on canvas."""
        tkinter.Grid.rowconfigure(self.root, 2, weight=1)
        tkinter.Grid.columnconfigure(self.root, 2, weight=1)

    def draw_new_room_command(self, event=None):
        """Change the application state to draw new room."""
        self.canvas_mode = CanvasMode.DRAW_ROOM

    def get_rooms_from_sap(self, rooms_from_sap):
        """Handle rooms read from SAP."""
        rooms = []
        for r in rooms_from_sap:
            polygon = []
            rooms.append({"room_id": r["AOID"], "polygon": polygon})
        return rooms

    def import_rooms_from_sap(self, event=None):
        """Import rooms from SAP."""
        if (
            self.drawing.rooms is None
            or len(self.drawing.rooms) == 0
            or dialog_load_rooms_from_sap()
        ):
            rooms_from_sap, drawing_id = LoadDialogs.load_rooms_from_sap(
                self.root, self.configuration
            )
            if rooms_from_sap is not None:
                # process drawing_id
                if drawing_id is not None:
                    self.drawing.drawing_id = drawing_id
                else:
                    messagebox.showerror(
                        "Nastala chyba",
                        "Nelze zjistit jednoznačný identifikátor výkresu",
                    )
                # delete rooms from canvas
                if self.drawing.rooms is not None:
                    for room in self.drawing.rooms:
                        if "canvas_id" in room:
                            self.canvas.delete_object_with_id(room["canvas_id"])
                self.drawing.rooms = None
                self.drawing.room_counter = 0
                self.palette.remove_all_rooms()
                self.drawing.rooms = self.get_rooms_from_sap(rooms_from_sap)
                self.drawing.room_counter = len(self.drawing.rooms) + 1
                self.redraw()
                self.add_all_rooms_from_drawing()

    def synchronize_rooms_with_sap(self, event=None):
        """Synchronize rooms with SAP."""
        if (
            self.drawing.rooms is None
            or len(self.drawing.rooms) == 0
            or dialog_synchronize_rooms_with_sap()
        ):
            rooms_from_sap, drawing_id = LoadDialogs.load_rooms_from_sap(
                self.root, self.configuration
            )
            if rooms_from_sap is not None:
                deleted = 0
                inserted = 0
                # process drawing_id
                if drawing_id is not None:
                    self.drawing.drawing_id = drawing_id
                else:
                    messagebox.showerror(
                        "Nastala chyba",
                        "Nelze zjistit jednoznačný identifikátor výkresu",
                    )
                if self.drawing.rooms is not None:
                    # if some room is missing in SAP, remove it from drawing as well
                    for room in list(self.drawing.rooms):
                        room_id = room["room_id"]
                        found = False
                        for q in rooms_from_sap:
                            if q["AOID"] == room_id:
                                found = True
                                break
                        if not found:
                            print("Deleting " + room_id)
                            deleted += 1
                            if "canvas_id" in room:
                                self.canvas.delete_object_with_id(room["canvas_id"])
                            self.drawing.rooms.remove(room)
                    # now check for new rooms added into SAP
                    for q in rooms_from_sap:
                        sap_id = q["AOID"]
                        found = False
                        for room in list(self.drawing.rooms):
                            if room["room_id"] == sap_id:
                                found = True
                                break
                        if not found:
                            print("Adding " + sap_id)
                            inserted += 1
                            self.drawing.rooms.append(
                                {"room_id": sap_id, "polygon": []}
                            )

                self.palette.remove_all_rooms()
                self.drawing.room_counter = len(self.drawing.rooms) + 1
                self.redraw()
                self.add_all_rooms_from_drawing()
                message = (
                    "Přidaných místností: {i}\n" + "Vymazaných místností: {d}"
                ).format(i=inserted, d=deleted)
                messagebox.showinfo("Výsledek synchronizace", message)

    def import_drawing_command(self, filename):
        """Import drawing (empty in this version)."""

    def import_rooms_command(self, event=None):
        """Handle the command to import rooms."""
        if (
            self.drawing.rooms is None
            or len(self.drawing.rooms) == 0
            or dialog_load_rooms()
        ):
            room_file_name = LoadDialogs.load_rooms(None)
            if (
                room_file_name is not None
                and room_file_name != ""
                and room_file_name != ()
            ):
                # delete rooms from canvas
                if self.drawing.rooms is not None:
                    for room in self.drawing.rooms:
                        if "canvas_id" in room:
                            self.canvas.delete_object_with_id(room["canvas_id"])
                self.drawing.rooms = None
                self.drawing.room_counter = 0
                self.palette.remove_all_rooms()
                room_importer = RoomImporter(room_file_name)
                self.drawing.rooms = room_importer.import_rooms()
                self.drawing.room_counter = len(self.drawing.rooms) + 1
                self.redraw()
                self.add_all_rooms_from_drawing()

    def export_rooms_command(self, event=None):
        """Handle the command to export rooms."""
        filename = self.rooms_export_filename
        if filename is None:
            self.export_rooms_as_command(self)
        else:
            exporter = RoomExporter(filename, self.drawing)
            exporter.export()

    def export_rooms_as_command(self, event=None):
        """Handle the command to export rooms under different name."""
        filename = SaveDialogs.save_rooms(self.root)
        if filename == "":
            filename = None
        if filename is not None:
            if not filename.endswith(".rooms"):
                filename += ".rooms"

            self.rooms_export_filename = filename
            exporter = RoomExporter(filename, self.drawing)
            exporter.export()

    def export_drawing(self, filename):
        """Export drawing into DRW or JSON format."""
        if filename:
            # set the new filename
            self.drawing.filename = filename
            exporter = DrawingExporter(filename, self.drawing)
            exporter.export()
            # filename2 = filename.replace(".drw", ".json")
            # json_exporter = JSONExporter(filename2, self.drawing)
            # json_exporter.export()

    def export_drawing_command(self, event=None):
        """Handle the command to export drawing."""
        filename = self.drawing.filename
        if filename is None:
            filename = SaveDialogs.save_drawing(self.root)
            if not filename.endswith(".drw"):
                filename += ".drw"

        self.export_drawing(filename)

    def export_drawing_as_command(self, event=None):
        """Handle the command to export drawing under different name."""
        filename = SaveDialogs.save_drawing(self.root)
        self.export_drawing(filename)

    def open_drawing_command(self, event=None):
        """Handle the command to open drawing."""
        if self.drawing is not None:
            if not dialog_load_new_drawing():
                return
        drawing_file_name = LoadDialogs.load_drawing(None)
        if (
            drawing_file_name is not None
            and drawing_file_name != ""
            and drawing_file_name != ()
        ):
            if drawing_file_name.endswith(".drw"):
                importer = DrawingImporter(drawing_file_name)
                drawing = importer.import_drawing()
            else:
                importer = DxfImporter(drawing_file_name)
                drawing = importer.import_dxf()
            if drawing is None:
                error_dialog_drawing_load()
            else:
                bounds = Bounds.compute_bounds(drawing.entities)
                xoffset, yoffset, scale = Rescaler.compute_scale_for_canvas(
                    bounds, self.canvas
                )
                drawing.rescale(xoffset, yoffset, scale)
                self.drawing = drawing
                self.redraw()
                self.add_all_rooms_from_drawing()
                self.set_ui_items_for_actual_mode()

    def save_drawing_command(self, event=None):
        """Handle the command to save drawing."""
        self.export_drawing_command()

    def delete_room_command(self, index, value):
        """Handle the command to delete room from drawing."""
        # print(index, value)
        if dialog_delete_whole_room(value):
            room = self.drawing.find_room_by_room_id(value)
            if room is not None:
                self.canvas.delete_object_with_id(room["canvas_id"])
            # must be deleted after the room is removed from canvas!
            self.drawing.delete_room(value)
            self.palette.delete_room_from_list(index)

    def delete_room_polygon_command(self, index, value):
        """Handle the command to delete room polygon from drawing."""
        if dialog_delete_room_polygon(value):
            room = self.drawing.find_room_by_room_id(value)
            if room is not None:
                self.canvas.delete_object_with_id(room["canvas_id"])
            self.drawing.delete_room_polygon(value)
            self.palette.fill_in_room_info(room)

    def redraw_room_polygon_command(self, index, value):
        """Redraw specified room polygon."""
        room = self.drawing.find_room_by_room_id(value)
        if room is not None:
            self.canvas.delete_object_with_id(room["canvas_id"])
            self.drawing.delete_room_polygon(value)
        self.canvas_mode = CanvasMode.DRAW_ROOM
        self.edited_room_id = value

    def select_polygon_for_room(self, index, value):
        """Select the specified room."""
        room = self.drawing.find_room_by_room_id(value)
        if room is not None:
            self.canvas.delete_object_with_id(room["canvas_id"])
            self.drawing.delete_room_polygon(value)
        self.canvas_mode = CanvasMode.SELECT_POLYGON_FOR_ROOM
        self.edited_room_id = value

    def scroll_start(self, event):
        """Handle scrolling event (start)."""
        self.canvas.scan_mark(event.x, event.y)

    def scroll_move(self, event):
        """Handle scrolling event (finish)."""
        self.canvas.scan_dragto(event.x, event.y, gain=1)
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def get_nearest_entity(self, x, y):
        """Find nearest entity to specified coordinates [x, y]."""
        return self.canvas.find_closest(x, y)[0]

    def finish_new_room(self):
        """Finish drawing of new room."""
        canvas_id = self.canvas.draw_new_room(self.room)
        room_id = None
        if self.edited_room_id is None:
            room_id = self._drawing.add_new_room(canvas_id, self.room.polygon_world)
            self.palette.add_new_room(room_id)
        else:
            room_id = self.edited_room_id
            self._drawing.update_room_polygon(
                room_id, canvas_id, self.room.polygon_world, "L"
            )
        self.edited_room_id = None
        self.canvas.delete_temporary_entities()

        # update left palette
        r = {"room_id": room_id, "polygon": self.room.polygon_world}
        self.palette.fill_in_room_info(r)

        # cleanup
        self.room.cleanup()
        self.canvas_mode = CanvasMode.VIEW
        self.room.polygon_world = []
        self.room.polygon_canvas = []

    def on_right_button_pressed(self, event):
        """Handle the right mouse button press event."""
        if self.canvas_mode == CanvasMode.DRAW_ROOM:
            vertexes = self.room.vertexes()
            if vertexes == 0:
                error_dialog_no_points()
                return
            elif vertexes < 3:
                error_dialog_not_enough_points()
                return
            elif vertexes == 3:
                if dialog_store_vertex_with_three_vertexes():
                    self.finish_new_room()
            else:
                self.finish_new_room()

    def entity_with_endpoints(self, item):
        """Return the drawing entity for the given canvas item."""
        # sanity check
        if item is None:
            return None

        # first check canvas entity type
        entity_type = self.canvas.type(item)
        if entity_type != "line":
            return None

        # then check the tags associated with the canvas entity
        tags = self.canvas.gettags(item)
        if "drawing" not in tags:
            return None

        # third check if canvas entity relates to drawing entity
        entity = self.drawing.find_entity_by_id(item)
        if entity is None:
            return None

        # fourth check drawing entity type
        # (not needed ATM)
        return entity

    def on_room_click_listbox(self, room_id):
        """Handle the left mouse button press on listbox with list of rooms."""
        room = self.drawing.find_room_by_room_id(room_id)
        if room:
            self.palette.enable_all()
            self.palette.fill_in_room_info(room)
            self.canvas.highlight_room(room)

    def on_room_click_canvas(self, canvas_object_id):
        """Handle the left mouse button click onto the canvas."""
        room = self.drawing.find_room_by_canvas_id(canvas_object_id)
        if room:
            self.palette.enable_all()
            self.palette.fill_in_room_info(room)
            self.palette.select_room_in_list(room)
            self.canvas.highlight_room(room)

    def on_polygon_for_room_click_canvas(self, canvas_object_id):
        """Handle the left mouse button click onto the polygon on canvas."""
        if self.canvas_mode == CanvasMode.SELECT_POLYGON_FOR_ROOM:
            entity = self.drawing.find_entity_by_id(canvas_object_id)
            if entity is not None:
                room_id = self.edited_room_id

                self.room.polygon_canvas = self.canvas.coords(canvas_object_id)

                xpoints = entity.points_x
                ypoints = entity.points_y
                self.room.polygon_world = []
                for i in range(len(xpoints)):
                    self.room.polygon_world.append((xpoints[i], ypoints[i]))
                canvas_id = self.canvas.draw_new_room(self.room)

                self._drawing.update_room_polygon(
                    room_id, canvas_id, self.room.polygon_world, "P"
                )
                print(entity)
                print(canvas_object_id)
                print(canvas_id)
                print(xpoints)
                print(ypoints)
                r = {"room_id": room_id, "polygon": self.room.polygon_world}
                self.palette.fill_in_room_info(r)
                self.room.polygon_world = []
                self.room.polygon_canvas = []

            self.edited_room_id = None
            # update left palette

            self.canvas_mode = CanvasMode.VIEW

    def draw_new_room_line(self, canvas_x, canvas_y):
        """Draw new line for room that's being drawn."""
        if self.room.last_point_exist():
            self.canvas.draw_new_room_temporary_line(
                self.room.last_x, self.room.last_y, canvas_x, canvas_y
            )
        self.room.last_x = canvas_x
        self.room.last_y = canvas_y

    def nearest_endpoint(self, x, y, item, entity):
        """Find nearest endpoint for given entity and coordinates [x,y]."""
        x1, y1, x2, y2 = self.canvas.coords(item)
        if GeometryUtils.square_length(x1, y1, x, y) < GeometryUtils.square_length(
            x2, y2, x, y
        ):
            return x1, y1, entity.x1, entity.y1
        else:
            return x2, y2, entity.x2, entity.y2

    def add_vertex(self, canvas_x, canvas_y, world_x, world_y):
        """Add new vertex to polygon."""
        self.canvas.draw_cross(canvas_x, canvas_y)
        self.draw_new_room_line(canvas_x, canvas_y)
        self.room.polygon_canvas.append((canvas_x, canvas_y))
        self.room.polygon_world.append((world_x, world_y))
        # self.canvas.itemconfig(item, fill='cyan')

    def add_vertex_to_room(self, event):
        """Add new vertex to room polygon."""
        # get the coordinates before canvas scroll
        x = self.canvas.canvasx(event.x)
        y = self.canvas.canvasy(event.y)
        item = self.get_nearest_entity(x, y)

        entity = self.entity_with_endpoints(item)
        if entity is not None:
            canvas_x, canvas_y, world_x, world_y = self.nearest_endpoint(
                x, y, item, entity
            )
            self.add_vertex(canvas_x, canvas_y, world_x, world_y)

    def get_scale(self):
        """Compute scale from the special entity scale-line."""
        scale_line = self.canvas.find_withtag("scale")[0]
        x1, y1, x2, y2 = self.canvas.coords(scale_line)
        len1 = self.canvas.width
        len2 = x2 - x1
        return 1.0 * len2 / len1, x1, y1

    def add_current_vertex_to_room(self, event):
        """Add current vertex to room."""
        canvas_x = self.canvas.canvasx(event.x)
        canvas_y = self.canvas.canvasy(event.y)
        current_scale, xd, yd = self.get_scale()
        world_x = (canvas_x - xd) / current_scale
        world_y = (canvas_y - yd) / current_scale
        self.add_vertex(canvas_x, canvas_y, world_x, world_y)

    def on_left_button_pressed(self, event):
        """Handle the left mouse button press event."""
        if self.canvas_mode == CanvasMode.DRAW_ROOM:
            # shift key
            shift = (event.state & 0x1) != 0
            if shift:
                self.add_current_vertex_to_room(event)
            else:
                self.add_vertex_to_room(event)
        elif self.canvas_mode == CanvasMode.SELECT_POLYGON_FOR_ROOM:
            pass
        else:
            self.scroll_start(event)

    def on_left_button_drag(self, event):
        """Handle the left mouse button drag event."""
        if (
            self.canvas_mode == CanvasMode.DRAW_ROOM
            or self.canvas_mode == CanvasMode.SELECT_POLYGON_FOR_ROOM
        ):
            pass
        else:
            self.scroll_move(event)

    # zoom on Windows
    def zoom(self, event):
        """Handle zoom event on Windows."""
        if self.canvas_mode == CanvasMode.DRAW_ROOM:
            return
        if event.delta > 0:
            self.canvas.scale("all", event.x, event.y, 1.1, 1.1)
        elif event.delta < 0:
            self.canvas.scale("all", event.x, event.y, 0.9, 0.9)
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    # zoom on Linux
    def zoom_plus(self, event=None):
        """Handle zoom plus event on Linux."""
        if self.canvas_mode == CanvasMode.DRAW_ROOM:
            return
        if event:
            self.canvas.scale(
                "all",
                event.x,
                event.y,
                MainWindow.SCALE_UP_FACTOR,
                MainWindow.SCALE_UP_FACTOR,
            )
        else:
            self.canvas.scale(
                "all",
                self.canvas.width / 2,
                self.canvas.height / 2,
                MainWindow.SCALE_UP_FACTOR,
                MainWindow.SCALE_UP_FACTOR,
            )
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    # zoom on Linux
    def zoom_minus(self, event=None):
        """Handle zoom minus event on Linux."""
        if self.canvas_mode == CanvasMode.DRAW_ROOM:
            return
        if event:
            self.canvas.scale(
                "all",
                event.x,
                event.y,
                MainWindow.SCALE_DOWN_FACTOR,
                MainWindow.SCALE_DOWN_FACTOR,
            )
        else:
            self.canvas.scale(
                "all",
                self.canvas.width / 2,
                self.canvas.height / 2,
                MainWindow.SCALE_DOWN_FACTOR,
                MainWindow.SCALE_DOWN_FACTOR,
            )
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def quit(self):
        """Display message box whether to quit the application."""
        answer = messagebox.askyesno(
            "Skutečně ukončit program?", "Skutečně ukončit program?"
        )
        if answer:
            self.root.quit()

    def show(self):
        """Display the main window on screen."""
        self.root.mainloop()

    @property
    def drawing(self):
        """Return the current drawing attribute."""
        return self._drawing

    @drawing.setter
    def drawing(self, drawing):
        """Set the current drawing attribute."""
        self._drawing = drawing

    def redraw_drawing(self):
        """Redraw the whole drawing."""
        self.canvas.draw_grid()
        self.canvas.draw_boundary()
        self.canvas.draw_scale_line()
        self.canvas.draw_entities(self.drawing.entities, 0, 0, 1)
        self.canvas.draw_rooms(self.drawing.rooms, 0, 0, 1)

    def redraw(self):
        """Redraw the whole drawing or display message when drawing does not exist."""
        self.canvas.delete("all")
        if self.drawing is not None:
            self.redraw_drawing()
        else:
            self.canvas.draw_empty_drawing_message()

    def add_all_rooms_from_drawing(self):
        """Add all rooms from drawing onto the palette (listbox)."""
        self.palette.remove_all_rooms()
        if self.drawing is not None:
            for room in self.drawing.rooms:
                self.palette.add_new_room(room["room_id"])
