import program


class Definder:
    def __init__(self, name: str):
        self.data = name.split(' ')

    def __dict__(self):
        return {}

    def set_type(self):
        data = program.Settings('devices').settings_object.get('devices')
        for x in self.data:
            if x.lower() in data:
                return x.lower(), 100
        else:
            return False, 0

    """def __set_device(self):
        device_data = {'class': '', 'number': ''}
        for x in self.name:
            print(x)
            if x in self.device_type:
                device_data.update({"type": x})
            if x in self.device_class:
                device_data.update({'class': x})
            if isinstance(x, int):
                device_data.update({'number': x})
            if x[-2:-1] == 'gb':
                device_data.update({'memory': x})
        return device_data
"""


print(Definder("Смартфон Apple iPhone 13 128Gb Green").set_type())
