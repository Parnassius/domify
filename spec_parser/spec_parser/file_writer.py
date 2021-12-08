from textwrap import wrap
from typing import Dict, List, Tuple, Union


class FileWriter:
    def __init__(self, file_path: str) -> None:
        self._file_path = file_path
        self._marker_comment = "# begin automatic"
        self._classes: List[str] = []

    @staticmethod
    def _format_data_dict(data: Dict[str, str], *, sort: bool) -> str:
        items = list(data.items())
        if sort:
            items.sort()
        parts = [f"'{k}': {v}" for k, v in items]
        return "{" + ",".join(parts) + "}"

    def add_class(
        self,
        class_name: str,
        docstring: str,
        **kwargs: Union[Tuple[bool, bool], Tuple[Dict[str, str], str, bool]],
    ) -> None:
        super_class = "BaseElement" if class_name == "HtmlElement" else "HtmlElement"
        docstring = "\n".join(
            wrap(docstring, width=88, initial_indent="    ", subsequent_indent="    ")
        )
        data = [
            f"class {class_name}({super_class}):",
            '    """',
            f"{docstring}",
            '    """',
        ]

        for key, val in kwargs.items():
            if isinstance(val[0], bool):
                attrib_value, default_value = val
                if attrib_value is not default_value:
                    data.append(f"    {key} = {attrib_value}")
            elif isinstance(val[0], dict):
                attrib_raw_data, annotation_str, sort = val
                if attrib_raw_data:
                    annotation = ""
                    if any(
                        x for x in attrib_raw_data.values() if x.startswith("lambda ")
                    ):
                        annotation = f": {annotation_str}"
                    attrib_data = self._format_data_dict(attrib_raw_data, sort=sort)
                    data.append(f"    {key}{annotation} = {attrib_data}")

        self._classes.append("\n".join(data))

    def write(self) -> None:
        with open(self._file_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
        with open(self._file_path, "w", encoding="utf-8") as f:
            for line in lines:
                f.write(line)
                if line.strip() == self._marker_comment:
                    break
            f.write("\n")
            f.write("\n".join(self._classes))
