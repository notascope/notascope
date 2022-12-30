from pathlib import Path
import sys

gallery = sys.argv[1]

slugs = set()
notations = []
ext = dict()
for notation in Path("galleries", gallery).iterdir():
    if notation.is_dir():
        notations.append(notation.stem)
        for spec in notation.iterdir():
            if spec.is_file():
                slugs.add(spec.stem)
                ext[notation.stem] = spec.suffix

rows = []
for slug in sorted(slugs):
    row = f"<tr><th align=right>{slug}</th>"
    for notation in notations:
        slug_path = Path(f"galleries/{gallery}/{notation}/{slug}{ext[notation]}")
        if not slug_path.exists():
            slug_path.write_text("")
        row += f"""
          <td>
            <a href="vscode://file/{str(slug_path.resolve())}">
              <img src='{notation}/img/{slug}.svg' style="max-height:300px; max-width: 300px" />
            </a>
          </td>
          """
    row += "</tr>"
    rows.append(row)

Path(f"results/{gallery}/summary.html").write_text(
    f"""
    <html>
      <head><title>{gallery}</title></head>
      <body>
      <h1>{gallery}</h1>
      <table>
        <tr><th></th>{"".join(f'<th>{n}</th>' for n in notations)}</tr>
        {"".join(rows)}
      </table>
      </body>
    </html>
    """
)
