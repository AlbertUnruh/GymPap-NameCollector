# just to sort ./GymPapNameCollector/.not_a_name.txt alphabetically and remove duplicates


from pathlib import Path


not_a_name_txt: Path = Path(__file__).parent.joinpath("GymPapNameCollector/.not_a_name.txt")

content: set[str] = set(map(str.strip, not_a_name_txt.read_text("utf-8", "ignore").splitlines(False)))

not_a_name_txt.write_text("\n".join(sorted(content)) + "\n", "utf-8")
