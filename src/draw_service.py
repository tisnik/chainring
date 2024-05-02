"""Interface to web service that provide list of rooms and drawing storage."""

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

import requests
from exporters.json_exporter import JSONExporter


class DrawServiceInterface:
    """Interface to web service that provide list of rooms and drawing storage."""

    API_PREFIX = "api/v1"

    @staticmethod
    def get_url(address, port):
        """Get URL prefix to the service."""
        return f"http://{address}:{port}"

    def __init__(self, service_url="http://localhost:3000"):
        """Initialize the interface."""
        self._service_url = service_url

    def get(self, endpoint):
        """Get full URL to selected endpoint."""
        url = f"{self._service_url}/{DrawServiceInterface.API_PREFIX}/{endpoint}"
        response = requests.get(url, timeout=10)
        return response.status_code, response.json()

    def check_liveness(self):
        """Check service liveness."""
        try:
            code, data = self.get("liveness")
            if code != 200:
                return False, f"Návratový kód {code}"
            if "status" in data and data["status"] == "ok":
                return True, None
            return False, "Neplatná data vrácená serverem"
        except Exception as e:
            return False, repr(e)

    def read_version(self):
        """Read service API version."""
        try:
            code, data = self.get("info")
            if code != 200:
                return False, f"Návratový kód {code}"
            if "service-version" in data:
                return True, data["service-version"], "Success"
            return False, None, "Neplatná data vrácená serverem"
        except Exception as e:
            return False, None, repr(e)

    def read_aoid(self, url, selector, error_message):
        """Read AOID from the web service."""
        try:
            code, data = self.get(url)
            if code != 200:
                return None, f"Návratový kód {code}"
            if "status" in data and data["status"] == "ok":
                if selector in data:
                    return data[selector], "Ok"
                else:
                    return None, error_message
            return None, "Neplatná data vrácená serverem"
        except Exception as e:
            return None, repr(e)

    def read_areals(self, valid_from):
        """Read list of areals from the web service."""
        url = f"areals?valid-from={valid_from}"
        return self.read_aoid(url, "areals", "Seznam areálů je prázdný")

    def read_buildings(self, valid_from, aoid):
        """Read list of buildings from the web service."""
        url = f"buildings?valid-from={valid_from}&areal-id={aoid}"
        return self.read_aoid(url, "buildings", "Seznam budov je prázdný")

    def read_floors(self, valid_from, aoid):
        """Read list of floors from the web service."""
        url = f"floors?valid-from={valid_from}&building-id={aoid}"
        return self.read_aoid(url, "floors", "Seznam podlaží je prázdný")

    def read_rooms(self, valid_from, aoid):
        """Read list of rooms from the web service."""
        url = f"rooms?valid-from={valid_from}&floor-id={aoid}"
        return self.read_aoid(url, "rooms", "Seznam místností je prázdný")

    def check_input_data(self, data):
        """Check the basic structure of data read from web service."""
        return (
            "projects" in data
            and "buildings" in data
            and "floors" in data
            and "drawings" in data
        )

    def send_drawing(self, drawing):
        """Send drawing onto the web service."""
        endpoint = f"drawing-data?drawing={drawing.drawing_id}&format=json"
        url = f"{self._service_url}/{DrawServiceInterface.API_PREFIX}/{endpoint}"
        json_exporter = JSONExporter("output.json", drawing)
        payload = json_exporter.as_string()
        try:
            response = requests.post(url, data=payload, timeout=30)
            code, data = self.get("info")
            print(code, data)
            if code != 200:
                return False, f"Návratový kód {code}"
            else:
                message = f"Výkres byl uložen pod ID {drawing.drawing_id} ({len(payload)} bajtů)"
                return True, message
        except Exception as e:
            return False, e

    def read_all_drawings(self):
        """Read list of all drawings from the web service."""
        try:
            code, data = self.get("all-drawings")
            if code != 200:
                return False, f"Návratový kód {code}"
            if self.check_input_data(data):
                return True, data, "Success"
            return False, None, "Neplatná data"
        except Exception as e:
            return False, None, repr(e)
