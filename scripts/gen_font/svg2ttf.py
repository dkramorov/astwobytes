import sys
import os
import json
import fontforge

# brew install fontforge
# virtualenv --system-site-packages env либо без env - я предпочитаю без

IMPORT_OPTIONS = ('removeoverlap', 'correctdir')


def loadConfig():
    """Создание специального маппинга под шрифт
>>> 0x30
48
>>> hex(48)
'0x30'
    """
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
    indexes = [i + 370 for i in range(len(icons_folder))]

    for i, item in enumerate(icons_folder):
        index = indexes[i]
        if item.endswith('.svg'):
            config['glyphs']['0x%s' % index] = item

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
        font.appendSFNTName(str(t[0]), str(t[1]), str(t[2]))


def addGlyphs(font, config):
    """Создание глифов
Without the 0x prefix, you need to specify the base explicitly, otherwise there's no way to tell:

x = int("deadbeef", 16)

With the 0x prefix, Python can distinguish hex and decimal automatically.

>>> print(int("0xdeadbeef", 0))
3735928559
>>> print(int("10", 0))
10

    """
    css_styles = []
    html_icons = []
    data_icons = []

    for k, v in config['glyphs'].items():

        icon_key = k.split('x')[-1]
        icon_name = v.split('.svg')[0].replace('-', '_')
        # Для приложения
        data_icons.append([icon_name, icon_key])

        g = font.createMappedChar(int(k, 0))
        print(g)

        css_styles.append('.fu-%s:before{content:"\%s"} ' % (icon_name, icon_key))
        html_icons.append(
            '<div class="icon"><span class="fu fu-%s"></span> %s <em>%s</em></div>' % (icon_name, icon_name, k))

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

    with open('funtya.css', 'w+', encoding='utf-8') as f:
        f.write("""
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
}
i.fu {
  font-size: 28px !important;
}""")
        f.write('\n'.join(css_styles))

    with open('demo.html', 'w+', encoding='utf-8') as f:
        f.write("""<html>
<head>
<link href="funtya.css" rel="stylesheet"/>
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
</style>
</head>
<body>""")
        f.write('\n'.join(html_icons))
        f.write("""</body>
</html>""")
    with open('font-funtya.json', 'w+', encoding='utf-8') as f:
        mapping = {
            'results': [{
                'id': v.split('.svg')[0].replace('-', '_'), 'text': v.split('.svg')[0] + ' ' + k
            } for k, v in config['glyphs'].items()]
        }
        f.write(json.dumps(mapping))

    with open('app_class.txt', 'w+', encoding='utf-8') as f:
        conditions = []
        for name, code in data_icons:
            f.write('\nstatic const IconData %s = IconData(0x%s, fontFamily: _kFontFam, fontPackage: _kFontPkg);' % (name, code))

            conditions.append("""
            '%s': %s,""" % (name, name))

        f.write("""
static const Map<String, IconData> icons = {
%s
};
        """ % ''.join(conditions))


def main():
    config = loadConfig()
    font = fontforge.font()
    setProperties(font, config)
    addGlyphs(font, config)
    for outfile in config['output']:
        sys.stderr.write('Generating %s...\n' % outfile)
        print(font.generate(outfile))


if __name__ == '__main__':
    # if len(sys.argv) > 1:
    #    main(sys.argv[1])
    # else:
    #    sys.stderr.write("\nUsage: %s something.json\n" % sys.argv[0] )
    main()
