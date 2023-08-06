from os.path import dirname

from html5tagger import E
from niceback.trace import extract_exc

stylefile = f"{dirname(__file__)}/style.css"

with open(stylefile) as f:
    style = f.read()

detail_show = "{display: inherit}"

symbols = dict(call="➤", warning="⚠️", error="💣")

niceback_show = """\
function niceback_show(id) {
    document.getElementById(id).scrollIntoView(
        {behavior: 'smooth', block: 'nearest', inline: 'start'}
    )
}
"""


def html_traceback():
    chain = extract_exc()[-3:]
    with E.div(class_="niceback") as doc:
        doc.script(niceback_show)
        doc.style(style)
        for e in chain:
            if e is not chain[0]:
                doc.p("The above exception occurred after catching")
            _exception(doc, e)
        with doc.script:
            for e in reversed(chain):
                for info in e["frames"]:
                    if info["relevance"] != "call":
                        doc(f"niceback_show('{info['id']}')\n")
                        break
    return doc


def _exception(doc, info):
    """Format single exception message and traceback"""
    summary, message = info["summary"], info["message"]
    doc.h3(E.span(f"{info['type']}:", class_="exctype")(f" {summary}"))
    if summary != message:
        if message.startswith(summary):
            message = message[len(summary):]
        doc.pre(message, class_="excmessage")
    # Traceback available?
    frames = info["frames"]
    if not frames:
        return
    # Format call chain
    limitedframes = frames[:16]
    with doc.div(class_="traceback-tabs"):
        if len(limitedframes) > 1:
            with doc.div(class_="traceback-labels"):
                for info in limitedframes:
                    doc.button(
                        E.strong(info["location"]).br.small(
                            info["function"] or "－"),
                        onclick=f"niceback_show('{info['id']}')"
                    )
        with doc.div(class_="content"):
            for info in limitedframes:
                with doc.div(class_="traceback-details", id=info['id']):
                    doc.span(
                        style="font-size: 2em",
                    )
                    if info['filename']:
                        doc.p.b(f"{info['filename']}")(f":{info['lineno']}")
                        urls = info["urls"]
                        if urls:
                            for name, href in urls.items():
                                doc(" ").a(name, href=href)
                    else:
                        doc.p.b(info["location"] + ":")
                    # Code printout
                    lines = info["lines"].splitlines(keepends=True)
                    if not lines:
                        doc.p("Code not available")
                    else:
                        with doc.pre, doc.code:
                            start = info["linenostart"]
                            lineno = info["lineno"]
                            for i, line in enumerate(lines, start=start):
                                with doc.span(class_="codeline", data_lineno=i):
                                    doc(
                                        marked(line, symbols.get(info["relevance"]))
                                        if i == lineno else
                                        line
                                    )
                    # Variable inspector
                    if info["variables"]:
                        with doc.table(class_="inspector"):
                            doc.thead.tr.th("Variable").th("Type").th("Value").tbody
                            for n, t, v in info["variables"]:
                                doc.tr.td(n).td(t).td(v)


def marked(line, symbol=None):
    indent, code, trailing = split3(line)
    return E(indent).mark(E.span(code), data_symbol=symbol)(trailing)


def split3(s):
    """Split s into indent, code and trailing whitespace"""
    a, b, c = s.rstrip(), s.strip(), s.lstrip()
    codelen = len(b)
    return a[:-codelen], b, c[codelen:]
