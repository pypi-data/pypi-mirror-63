class MarkdownFileService:
    def __init__(self, markdown_file_path: str):
        self.markdown_file_path = markdown_file_path

    def open_markdown(self) -> str:
        with open(self.markdown_file_path, "r", encoding="utf-8") as file:
            return file.read()

    def save_markdown(self, markdown_string: str) -> None:
        with open(self.markdown_file_path, "w", encoding="utf-8") as file:
            file.write(markdown_string)
