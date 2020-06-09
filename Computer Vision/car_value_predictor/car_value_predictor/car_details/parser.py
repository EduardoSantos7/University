from bs4 import BeautifulSoup
from dateutil.parser import parse


class Parser():
    def __init__(self, html):
        self.soup = BeautifulSoup(html, features="lxml")
        self.data = {}
        self.IDS = {
            'result_container': 'response-detail',
            'ocra': 'tab-ocra',
            'pgj': 'tab-avisoRobo'
        }

    def _verify(self):
        """Check for important divs to verify the HTML
        """
        containers = []

        containers.extend(
            [self.soup.find('div', {'id': id_}) for id_ in self.IDS.values()])

        return all(containers)

    def process(self):
        if not self._verify:
            return Exception("The HTML is not valid")
        result_container, ocra, pgj = [self.soup.find(
            'div', {'id': id_}) for id_ in self.IDS.values()]

        tbody = result_container.find('tbody')
        data = {}

        for row in tbody.find_all('tr'):
            field, value = row.find_all('td')

            if field:
                field = field.text.replace(':', '').strip()

            if value:
                value = value.text.replace('\n', ' ').strip()

            data[field] = value

        self.data = self.standarize_data(data)
        self.data['ocra_msg'] = ocra.text
        self.data['pgj_msg'] = pgj.text
        self.data['status'] = self.soup.find(
            'td', {'class': 'alert alert-success'}).text

    def standarize_data(self, data_dict):
        enrolled_date = f'{data_dict.get("Fecha de inscripción", "")} {data_dict.get("Hora de inscripción", "")}'
        enrolled_date = self.date_from_string(enrolled_date)
        license_plate_date = self.date_from_string(
            data_dict.get("Fecha de emplacado", ""))
        last_update = self.date_from_string(
            data_dict.get("Fecha de última actualización", ""))

        data = {
            'brand': data_dict.get("Marca", ""),
            'model': data_dict.get("Modelo", ""),
            'model_year': data_dict.get("Año Modelo", 0),
            'class': data_dict.get("Clase", ""),
            'type': data_dict.get("Tipo", ""),
            'niv': data_dict.get("Número de Identificación Vehicular (NIV)", 0),
            'nci': data_dict.get("Número de Identificación Vehicular (NIV)", 0),
            'license_plate': data_dict.get("Placa", ""),
            'number_of_doors': data_dict.get("Número de puertas", 0),
            'origin': data_dict.get("País de origen", ""),
            'version': data_dict.get("Versión", ""),
            'displacement': data_dict.get("Desplazamiento (cc/L)", 0),
            'number_of_cilinders': data_dict.get("Número de cilindros", 0),
            'number_of_axes': data_dict.get("Número de ejes", 0),
            'assembly_plant': data_dict.get("Planta de ensamble", ""),
            'complement_data': data_dict.get("Datos complementarios", ""),
            'enrolled_by': data_dict.get("Institución que lo inscribió", ""),
            'enrolled_date': enrolled_date,
            'license_plate_state': data_dict.get("Entidad que emplacó", ""),
            'license_plate_date': license_plate_date,
            'last_update': last_update,
            'registration_certificate_folio': data_dict.get("Folio de Constancia de Inscripción", ""),
            'observations': data_dict.get("Observaciones", ""),
        }
        return data

    def date_from_string(self, raw_date, append_tz=False):
        """ Parse string containing date into a tz-aware datetime object.
        :param raw_date: string containing date in a parsable format
        :param append_to_raw: string that gets added to raw_date to help parse
        :returns: tz-aware datetime object or None in case of parsing error
        """
        date = None
        try:
            if append_tz:
                tz_extended_date = raw_date + " 08:00:00 -0800"
                date = parse(tz_extended_date)
            else:
                date = parse(raw_date)
        except (ValueError, TypeError):
            pass
        return date
