
class ActivityName:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name


CREATE = ActivityName('create')
UPDATE = ActivityName('update')
DELETE = ActivityName('delete')
