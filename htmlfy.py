#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import os

dirs = ['.','cv','publications','student']
i = 'index'
sfx = 'lm'

def dirs_name(dl):
    if dl == '.':
        return 'home'
    else:
        return dl

def html_head(title="LM Home Pages",root=""):
  ret = """
<html>
  <head>
    <meta http-equiv=Content-Type content="text/html; charset=utf-8">
    <title>%s</title>
    <link href="%slm.css" rel="stylesheet" type="text/css">
    <script language="javascript" type="text/javascript">
      function emailCloak() {
	if (document.getElementById) {
	  var alltags = document.all? document.all :
	    document.getElementsByTagName("*");
	  for (i=0; i < alltags.length; i++) {
	    if (alltags[i].className == "emailCloak") {
	      var oldText = alltags[i].firstChild;
	      var emailAddress = alltags[i].firstChild.nodeValue;
	      var usr = emailAddress.substring(0, emailAddress.indexOf("("));
	      var wb = emailAddress.substring(emailAddress.indexOf(")")+1,
		  emailAddress.length);
	      var newText = usr+"@"+wb;
	      var a = document.createElement("a");
	      a.href = "mailto:"+newText;
	      var address = document.createTextNode(newText);
	      a.appendChild(address);
	      alltags[i].replaceChild(a,oldText);
	    }
	  }
	}
      }
window.onload = emailCloak;
</script>

<script type="text/javascript">
  function unhide(divID) {
   var item = document.getElementById(divID);
   if (item) {
    item.className=(item.className=='hidden')?'abstract-body':'hidden';
   }
  }
</script>

<body>
<div id="container">
<div id="top">dr hab. prof UŚ Łukasz Machura</div>
"""%(title,"" if root == '.' else '../')
  ret += html_navi(dirs,root)
  ret += """
<div id="main">"""
  return ret

def html_foot():
    ret = """
</div>
</div>
<div id="footer">
&copy; 2014, <a href="mailto:lukasz.machura@us.edu.pl">Łukasz Machura</a>,
Institute of Physics, SMCEBI,
University of Silesia,
ul. 75 Pułku Piechoty 1A, 41-500 Chorzów
</div></body></html>"""
    return ret

def html_navi(d,thisdir):
    ret = '<div class="navid">'
    for _d in d:
        if _d == thisdir:
            ret += """
            <div class="here">%s</div>"""%dirs_name(_d).title()
        else:
            link = "" if thisdir == '.' else "../"
            link += _d
            link += "/index.html"
            ret += """
            <div class="nav"><a href="%s">%s</a></div>"""%(link,dirs_name(_d).title())
    return ret + "\n</div>"

def parse_content(sourcefile,title,root):
    ret = html_head(title,root)
    with open(sourcefile) as f:
        ret += f.read()
    ret += html_foot()
    return ret

def write_index_file(title,d):
    f = os.path.join(d,i+'.'+sfx)
    content = parse_content(f,title,d)
    f = os.path.join(d,i+'.html')
    with open(f,'w') as outf:
        outf.write(content)

def create_publication_list(root):
  content = "<h2>List of publications</h2>"
  _base, _dirs, _files = iter(os.walk(root)).next()
  ld = sorted(_dirs, reverse=True)
  lld = len(ld)
  for _dir in ld:
    pubdict = {'title':None,
	'author':None,
	'abstract':None,
	'ref':None,
	'arxiv':None,
	'pdf':None,
	'source':None,
	}
    f = os.path.join(root,_dir,'info.pub')
    with open(f) as inf:
        for line in inf:
            line = line.split('::')
            if len(line) > 1:
                if len(line[1].rstrip()) > 0:
                    pubdict[line[0]] = line[1]#.rstrip()
    #print _dir, pubdict
    content += """<div style="padding-top: 10px;">%i. "%s","""%(lld,pubdict['title'].rstrip())
    content += """<br>%s"""%pubdict['author']
    if pubdict['ref'] != None:
      content += """<br>ref: <b>%s</b>, """ % pubdict['ref'].split(',')[0]
      content += """%s""" % " ".join(pubdict['ref'].split(',')[1:])
    else:
      content += """<br>submitted"""
    content += """<br><a href="javascript:unhide('pub%d');">Abstract and paper</a>"""%lld
    content += """<div id="pub%d" class="hidden">%s<br>"""%(lld,pubdict['abstract'].rstrip())
    if pubdict['pdf'] != None:
      content += """<br>pdf: <a href="%s/%s" download target="_blank">%s</a>, """%(_dir,pubdict['pdf'],pubdict['pdf'])
    if pubdict['arxiv'] != None:
      content += """arXiv: <a href="http://arxiv.org/abs/%s" target="_blank">%s</a>, """%(pubdict['arxiv'],pubdict['arxiv'])
    if pubdict['source'] != None:
      content += """source: <a href="%s/%s">%s</a>"""%(_dir,pubdict['source'],pubdict['source'])
    content += "</div></div>\n\n"
    lld -= 1

  f = os.path.join(root,i+'.'+sfx)
  with open(f,'w') as outf:
    outf.write(content)


def create_publication_list_for_ZFT(root):
  content = ""
  _base, _dirs, _files = iter(os.walk(root)).next()
  ld = sorted(_dirs, reverse=True)
  lld = len(ld)
  for _dir in ld:
    pubdict = {'title':None,
	'author':None,
	'abstract':None,
	'ref':None,
	'arxiv':None,
	'pdf':None,
	'source':None,
	}

    f = os.path.join(root,_dir,'info.pub')
    with open(f) as inf:
        for line in inf:
            line = line.split('::')
            if len(line) > 1:
                if len(line[1].rstrip()) > 0:
                    pubdict[line[0]] = line[1]#.rstrip()

    #print _dir, pubdict
    content += """<div style="padding-top: 10px;">%i. "%s","""%(lld,pubdict['title'].rstrip())
    content += """<br>%s"""%pubdict['author']
    if pubdict['ref'] != None:
      content += """<br>ref: <b>%s</b>, """ % pubdict['ref'].split(',')[0]
      content += """%s""" % " ".join(pubdict['ref'].split(',')[1:])
    else:
      content += """<br>submitted"""
    if pubdict['arxiv'] != None:
      content += """<br />\narXiv: <a href="http://arxiv.org/abs/%s" target="_blank">%s</a>, """%(pubdict['arxiv'],pubdict['arxiv'])
    content += "</div></div>\n\n"
    lld -= 1

  f = os.path.join(root,i+'_ZFT.'+sfx)
  with open(f,'w') as outf:
    outf.write(content)

def latex_publication_list(root):
  content = """\section{List of publications}
  """
  content += r"""\begin{etaremune}  %add \usepackage{etaremune}
  """
  _base, _dirs, _files = iter(os.walk(root)).next()
  ld = sorted(_dirs, reverse=True)
  lld = len(ld)
  for _dir in ld:
    pubdict = {'title':None,
	'author':None,
	'abstract':None,
	'ref':None,
	'arxiv':None,
	'pdf':None,
	'source':None,
	}
    f = os.path.join(root, _dir, 'info.pub')
    with open(f) as inf:
        for line in inf:
            line = line.split('::')
            if len(line) > 1:
                if len(line[1].rstrip()) > 0:
                    pubdict[line[0]] = line[1]#.rstrip()
    #print _dir, pubdict
    content += """\item %s, """ % (pubdict['title'].rstrip())
    content += """%s""" % pubdict['author'].rstrip()
    if pubdict['ref'] != None:
      content += """, %s, """ % pubdict['ref'].split(',')[0]
      content += """%s""" % " ".join(pubdict['ref'].split(',')[1:])
    else:
      content += """, submitted"""
    content += "\n"
    lld -= 1
  content += r"""\end{etaremune}"""

  f = os.path.join(root, i + '.tex')
  with open(f, 'w') as outf:
    outf.write(content)


if __name__ == "__main__":
    #index
    root = '.'
    title = "LM's home page"
    write_index_file(title,root)
    print title, "written"

    #cv
    root = 'cv'
    title = "LM's CV"
    write_index_file(title,root)
    print title, "written"

    #publications
    root = 'publications'
    title = "LM's publications"
    create_publication_list(root)
    latex_publication_list(root)
    write_index_file(title,root)
    print title, "written"

    #ZFT
    root = 'publications'
    title = "LM's publications for ZFT"
    create_publication_list_for_ZFT(root)
    print title, "written"

    #student
    root = 'student'
    title = "Informacje dla studenta"
    write_index_file(title,root)
    print title, "written"

    #tech
    root = 'tech'
    title = 'Technikalia'
    write_index_file(title, root)
    print title, "written"
