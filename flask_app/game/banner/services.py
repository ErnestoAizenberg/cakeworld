from typing import List, Optional

from .dtos import BannerDTO


class BannerService:
    def __init__(self, repository):
        self.repository = repository

    def create_banner(self, banner_data: dict) -> BannerDTO:
        banner_dto = BannerDTO(**banner_data)
        return self.repository.save(banner_dto)

    def get_banner(self, banner_id: int) -> Optional[BannerDTO]:
        return self.repository.get(banner_id)

    def get_all_banners(self) -> List[BannerDTO]:
        return self.repository.get_all()

    def update_banner(self, banner_id: int, banner_data: dict) -> Optional[BannerDTO]:
        banner_data["id"] = banner_id
        banner_dto = BannerDTO(**banner_data)
        return self.repository.update(banner_dto)

    def delete_banner(self, banner_id: int) -> bool:
        return self.repository.delete(banner_id)
