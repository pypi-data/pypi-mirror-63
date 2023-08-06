import dataclasses


@dataclasses.dataclass
class ImagePath:
    # ex: /xxx/xxx/xxx.jpg
    value: str

    def __hash__(self):
        return hash(self.value)

    def get_path(self, project_root_path: str = "") -> str:
        """
        :param project_root_path: Set project root path if the image file path is from the project root.
        :return: Absolute path of the image.
        """
        return project_root_path + self.value
