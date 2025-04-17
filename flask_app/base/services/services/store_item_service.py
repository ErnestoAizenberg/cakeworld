class StoreItemService:
    def __init__(self, repository):
        self.repository = repository

    def save(self, item):
        return self.repository.save(item)

    def get(self, item_id):
        return self.repository.get(item_id)

    def get_all(self):
        return self.repository.get_all()

    def update(self, item):
        return self.repository.update(item)

    def delete(self, item):
        return self.repository.delete(item)
