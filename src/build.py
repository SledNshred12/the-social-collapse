"""Build public/index.html from the pieces in src/.  Run:  python3 src/build.py"""
import base64, pathlib
S = pathlib.Path(__file__).parent
R = S.parent
b64 = lambda p: base64.b64encode((S / p).read_bytes()).decode()
t = (S / "template.html").read_text()
t = t.replace("__MAP__", (S / "map.json").read_text())
t = t.replace("__LOGO__", "data:image/png;base64," + b64("logo256.png"))
t = t.replace("__AXVID__", "data:video/mp4;base64," + b64("axiom_intro.mp4"))
t = t.replace("<title>The Social Collapse</title>", (S / "head.html").read_text(), 1)
w = 'showModal(`<h2>Welcome, Mr. President</h2>'
assert w in t
t = t.replace(w, 'showModal(`<img src="logo.png" alt="" style="width:120px;height:120px;display:block;margin:0 auto 6px"><h2>Welcome, Mr. President</h2>', 1)
(R / "public" / "index.html").write_text(t)
print("built public/index.html", len(t), "bytes")
