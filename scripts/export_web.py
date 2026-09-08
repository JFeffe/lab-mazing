"""Rebuild with Godot 4.5.1 and its official export templates installed."""
from pathlib import Path
import subprocess,sys
root=Path(__file__).resolve().parents[1]
(root/'web').mkdir(exist_ok=True)
subprocess.run([sys.argv[1] if len(sys.argv)>1 else 'godot','--headless','--path',str(root/'game'),'--export-release','Web',str(root/'web/index.html')],check=True)
p=root/'web/index.html'
s=p.read_text().replace('</style>','canvas { touch-action: none; }\nhtml, body { overscroll-behavior: none; }\n</style>')
s=s.replace('</body>', '<script>document.getElementById("canvas").addEventListener("contextmenu", function(event) { event.preventDefault(); });</script>\n</body>')
p.write_text(s)
(root/'web/.nojekyll').touch()

# Bound the full WebGL drawing buffer on touch devices, including 2D and
# intermediate buffers. Viewport.scaling_3d_scale alone does not bound these.
js=root/'web/index.js'
source=js.read_text()
original='GodotDisplayScreen.hidpi?window.devicePixelRatio||1:1'
replacement='GodotDisplayScreen.hidpi?(window.matchMedia("(pointer: coarse)").matches?Math.min(window.devicePixelRatio||1,1.5):(window.devicePixelRatio||1)):1'
if source.count(original)!=1:
    raise RuntimeError('Godot display adapter changed; review mobile pixel ratio cap')
js.write_text(source.replace(original,replacement))
