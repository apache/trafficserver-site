#!/usr/bin/python3

import markdown, codecs, os, sys, re, time, io, shutil

"""
Script to process the markdown files:
- converts text enclosed in ~~~ to <pre>
- adds anchor links to <h1-6>
- fixes references to UPPERCASE.md files
- applies markdown processing
- writes the files as lower-case .html to content/ tree

Note: only .md files will be copied to content/
Static files such as css and images are assumed to be already present under content/
"""

template = ""
MD = markdown.Markdown(extensions = ['meta', 'toc'])
with open("template.html", "r") as tmpl:
    template = tmpl.read()
    tmpl.close()
    
def runDir(path):
    files = os.listdir(path)
    for f in files:
        if os.path.isdir('%s/%s' % (path, f)):
            runDir('%s/%s/' % (path, f))
        elif f.endswith(".md") or f.endswith(".mdtext"):
            print("Processing %s" % f)
            input_file = codecs.open("%s/%s" % (path, f), mode="r", encoding="utf-8")
            outfile = re.sub(r".md(text)*$", ".html", f).lower().replace("//", "/")
            outfile = path.replace("markdown", "", 1) + outfile
            text = input_file.read()
            # convert sections enclosed in ~~~ to <pre> blocks
            text = re.sub(r"~~~([\s\S]+?)~~~", "<pre>\\1</pre>", text, flags=re.MULTILINE)
            # convert references to UPPERCASE.md files to lower-case.html
            # e.g. Refer to the [General installation documentation](INSTALLING.md)
            # =>   Refer to the [General installation documentation](installing.html)
            text = re.sub(r"([A-Z/]+)\.md(text)*", lambda x: x.group(1).lower() + ".html", text, flags =re.MULTILINE)
            html = MD.convert(text)
            title = MD.Meta.get('title', [''])[0]
            # Convert h1-h6 into anchors with paragraph mark hover links
            html = re.sub(r"<h([1-6]) id=\"([^\"]+)\">(.+?)</h[1-6]>", lambda x:
                "<h%s id='%s'>%s<a href='#%s' title='Permanent link to this' class='headerlink'>&para;</a></h%s>" % (
                x.group(1),
                x.group(2),
                re.sub(r"#\s*\{#.+?\}", "", x.group(3)),
                x.group(2),
                x.group(1)
                       )
                          , html)
            # merge the transformed file with the template
            
            html = template.replace("%TITLE%", title).replace("%CONTENT%", html, 1)
            print("Writing %s..." % outfile)
            bpath = os.path.dirname(outfile)
            if not os.path.isdir("../content/" + bpath):
                print("Making dir %s" % bpath)
                os.mkdir("../content/%s" % bpath)
            with io.open('../content/%s' % outfile, "w", encoding='utf8') as out:
                out.write(html)
                out.close()
        elif f.endswith(".html"):
            print("Processing %s" % f)
            shutil.copyfile("%s/%s" % (path, f), '../content/%s' % f)
            
runDir('markdown')
print("All done!")