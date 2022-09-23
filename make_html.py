from pathlib import Path


results = dict()
for study in Path("studies").iterdir():
    if study.is_dir():
        slugs = set()
        notations = []
        ext = dict()
        for notation in study.iterdir():
            if notation.is_dir():
                notations.append(notation.stem)
                for spec in notation.iterdir():
                    if spec.is_file():
                        slugs.add(spec.stem)
                        ext[notation.stem] = spec.suffix
        results[study.stem] = dict(slugs=slugs, notations=notations, ext=ext)

for study in results:
    slugs = results[study]["slugs"]
    notations = results[study]["notations"]
    ext = results[study]["ext"]
    rows = []
    for slug in sorted(slugs):
        row = f"<tr><th align=right>{slug}</th>"
        for notation in notations:
            slug_path = Path(f"studies/{study}/{notation}/{slug}{ext[notation]}")
            if not slug_path.exists():
                slug_path.write_text("")
            row += f"""
      <td>
        <a href="vscode://file/{str(slug_path.resolve())}">
          <img src='{notation}/img/{slug}.svg' />
        </a>
      </td>
      """
        row += "</tr>"
        rows.append(row)
    Path(f"results/{study}/summary.html").write_text(
        f"""
    <html>
      <head><title>{study}</title></head>
      <body>
      <h1>{study}</h1>
      <table>
        <tr><th></th>{"".join(f'<th>{n}</th>' for n in notations)}</tr>
        {"".join(rows)}
      </table>
      </body>
    </html>
    """
    )
