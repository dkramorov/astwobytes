import sys
import os
import json
import fontforge

# brew install fontforge
# virtualenv --system-site-packages env либо без env - я предпочитаю без

IMPORT_OPTIONS = ('removeoverlap', 'correctdir')

try:
    unicode
except NameError:
    unicode = str

def loadConfig():
    folder = 'icons'

    config = {
        'props': {
            'ascent': 800,
            'descent': 200,
            'em': 1000,
            'family': 'Funtya',
        },
        'input': folder,
        'output': ['funtya.ttf'],
        'glyphs': {
            #'0x41': '24-hours.svg',
            #'0x42': '360-degree.svg',
        },
    }
    icons_folder = os.listdir(folder)
    for i, item in enumerate(icons_folder):
        if item.endswith('.svg'):
            name = item.split('.svg')[0]
            config['glyphs']['0x%s' % i] = item

    return config

def setProperties(font, config):
    props = config['props']
    lang = props.pop('lang', 'English (US)')
    family = props.pop('family', None)
    style = props.pop('style', 'Regular')
    props['encoding'] = props.get('encoding', 'UnicodeFull')
    if family is not None:
        font.familyname = family
        font.fontname = family + '-' + style
        font.fullname = family + ' ' + style
    for k, v in config['props'].items():
        if hasattr(font, k):
            if isinstance(v, list):
                v = tuple(v)
            setattr(font, k, v)
        else:
            font.appendSFNTName(lang, k, v)
    for t in config.get('sfnt_names', []):
        font.appendSFNTName(str(t[0]), str(t[1]), unicode(t[2]))

def addGlyphs(font, config):
    css_styles = []
    html_icons = []
    for k, v in config['glyphs'].items():
        #print(k, v)
        icon_name = v.split('.svg')[0]
        icon_code = k.split('x')[-1]
        css_styles.append('.fu-%s:before{content:"\%s"} ' % (icon_name, icon_code))
        html_icons.append('<div class="icon"><span class="fu fu-%s"></span> %s <em>%s</em></div>' % (icon_name, icon_name, k))

        g = font.createMappedChar(int(k, 0))
        # Get outlines
        src = '%s.svg' % k
        if not isinstance(v, dict):
            v = {'src': v or src}
        src = '%s%s%s' % (config.get('input', '.'), os.path.sep, v.pop('src', src))
        g.importOutlines(src, IMPORT_OPTIONS)
        g.removeOverlap()
        # Copy attributes
        for k2, v2 in v.items():
            if hasattr(g, k2):
                if isinstance(v2, list):
                    v2 = tuple(v2)
                setattr(g, k2, v2)

    with open('demo.html', 'w+', encoding='utf-8') as f:
        f.write("""<html>
<head>
<style type="text/css">
body {
  padding-left: 50px;
}
.icon {
  border: 1px solid #ccc;
  padding: 5px;
  font-size: 30px !important;
}
.icon .fu {
  font-size: 60px !important;
  display: inline-block;
  width: 90px;
}
.icon em {
  float: right;
}
@font-face{
  font-family:'Funtya';
  src:url('funtya.ttf');
  font-weight:normal;
  font-style:normal
}
.fu{
  display:inline-block;
  font:normal normal normal 14px/1 Funtya;
  font-size:inherit;
  text-rendering:auto;
  -webkit-font-smoothing:antialiased;
  -moz-osx-font-smoothing:grayscale
}""")
        f.write('\n'.join(css_styles))
        f.write("""</style>
</head>
<body>""")
        f.write('\n'.join(html_icons))
        f.write("""<body>
</html>""")
    with open('font-funtya.json', 'w+', encoding='utf-8') as f:
        mapping = {
            'results': [{
                'id': v.split('.svg')[0], 'text': v.split('.svg')[0] + ' ' + k
            } for k, v in config['glyphs'].items()]
        }
        f.write(json.dumps(mapping))

def main():
    config = loadConfig()
    font = fontforge.font()
    setProperties(font, config)
    addGlyphs(font, config)
    for outfile in config['output']:
        sys.stderr.write('Generating %s...\n' % outfile)
        font.generate(outfile)

if __name__ == '__main__':
    #if len(sys.argv) > 1:
    #    main(sys.argv[1])
    #else:
    #    sys.stderr.write("\nUsage: %s something.json\n" % sys.argv[0] )
    main()

