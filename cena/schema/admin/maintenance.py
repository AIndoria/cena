from cena.schema._cena import CenaModel


class MaintenanceSummary(CenaModel):
    data_dir_size: str
    log_file_size: str
    cleanable_images: int
    cleanable_dirs: int


class MaintenanceStorageDetails(CenaModel):
    temp_dir_size: str
    backups_dir_size: str
    groups_dir_size: str
    recipes_dir_size: str
    user_dir_size: str


class MaintenanceLogs(CenaModel):
    logs: list[str]
