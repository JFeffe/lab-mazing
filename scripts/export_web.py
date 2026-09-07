"""Rebuild with Godot 4.5.1 and its official export templates installed."""
from pathlib import Path
import subprocess,sys
root=Path(__file__).resolve().parents[1]
(root/'web').mkdir(exist_ok=True)
subprocess.run([sys.argv[1] if len(sys.argv)>1 else 'godot','--headless','--path',str(root/'game'),'--export-release','Web',str(root/'web/index.html')],check=True)
p=root/'web/index.html'
s=p.read_text().replace('</style>','canvas { touch-action: none; }\nhtml, body { overscroll-behavior: none; }\n</style>')
p.write_text(s)
(root/'web/.nojekyll').touch()
