#!/usr/bin/env python3
"""Genera los listados de material de cada tema a partir de la copia de seguridad de Moodle.

Uso:  python3 tools/material.py <carpeta_mbz_descomprimida>

- Copia los archivos de cada recurso a static/recursos/<tema>/.
- Sustituye en content.es y content.val el bloque comprendido entre
  <!-- MATERIAL:inicio --> y <!-- MATERIAL:fin --> de la página de cada tema.
El reparto de recursos por tema está en la tabla TEMAS. Los identificadores son los
del módulo (cmid) en la copia de Moodle.
"""
import html, json, os, pathlib, re, shutil, sys, unicodedata
import xml.etree.ElementTree as ET

RAIZ = pathlib.Path(__file__).resolve().parent.parent
MAX_MB = 15  # los archivos mayores no se copian (se enlaza la fuente oficial)
EXCLUIR_NOMBRES = ('McGrawHill', 'Getting_Started', '.mhtml', 'panfleto')

# tema -> lista de (clave de grupo, [ids])
TEMAS = {
    'guia': [('doc', [72228])],
    't01-sistema-educativo': [
        ('ley', [72263, 72230, 72264, 72267, 72268, 72229]),
        ('fp', [72317, 72212, 72213, 72243, 72244, 72314, 72215, 72214]),
        ('gestion', [72245, 72246, 72247, 72248]),
    ],
    't02-ensenanzas-informatica': [
        ('titulos', [72274, 72275, 72276, 72277]),
        ('curcv', [72293, 72294, 72295, 72296, 72232, 72233]),
        ('fpcv', [72265, 72315, 72313, 72316]),
        ('eso', [72286, 72302, 72303, 72311, 72312, 72300, 72285, 72217, 72279, 72255]),
        ('lectura', [72299, 72452]),
    ],
    't03-programacion-didactica': [
        ('guia', [72260, 72289, 72430, 72431, 72288, 72411]),
        ('centro', [72282, 72262]),
        ('ejfp', [72310, 72368, 72343, 72344]),
        ('ejeso', [72284, 72261]),
        ('videos', [72412, 72413]),
    ],
    't04-metodologia': [
        ('met', [72341, 72361]),
        ('sa', [72304, 72305, 72218, 72219, 72278, 72256, 72220, 72221, 72222, 72301]),
        ('retos', [72458, 72460, 72459, 72461]),
        ('gamif', [72363, 72364, 72366, 72365, 72367]),
        ('equipos', [72209, 85140]),
    ],
    't05-evaluacion': [
        ('norma', [72352, 72357, 72353, 72354, 72358, 72362]),
        ('plan', [72355, 72356, 72386, 72385, 72360]),
        ('instr', [72370, 72389, 72371, 72372, 72390]),
        ('rubr', [72373, 72374, 72375, 72376, 72377, 72378]),
    ],
    't06-inclusion': [
        ('norma', [72400, 72401, 72402, 72403]),
        ('neae', [72392, 72393, 72394, 72395, 72477]),
        ('gva', [72404, 72405, 72406, 72408]),
    ],
    't07-unidad-programacion': [
        ('guia', [72435, 72436, 72440, 72441]),
        ('ej', [72437, 72438, 72439, 72455]),
    ],
    't08-oposiciones': [
        ('conv', [72253, 72339, 72252, 72251, 72254]),
        ('crit', [72225, 72337, 72338, 72387]),
        ('temario', [72332, 72333, 72334]),
        ('acceso', [72335, 72336, 72318, 72235, 72231, 88685]),
    ],
    't09-defensa': [
        ('pd', [72470, 72471, 72472]),
        ('ut', [72474, 72475, 72476]),
        ('encerrona', [72480]),
        ('rubr', [72490, 72489, 108034]),
    ],
}

GRUPOS = {
    'doc': ('Documentos', 'Documents'),
    'ley': ('Leyes orgánicas de educación', "Lleis orgàniques d'educació"),
    'fp': ('Formación Profesional: ley y desarrollo', 'Formació Professional: llei i desplegament'),
    'gestion': ('Gestión de la FP en la Comunitat Valenciana', 'Gestió de la FP a la Comunitat Valenciana'),
    'titulos': ('Reales decretos de título', 'Reials decrets de títol'),
    'curcv': ('Currículos de la Comunitat Valenciana y oferta', 'Currículums de la Comunitat Valenciana i oferta'),
    'fpcv': ('Ordenación de la FP', 'Ordenació de la FP'),
    'eso': ('ESO y Bachillerato', 'ESO i Batxillerat'),
    'lectura': ('Para leer y reflexionar', 'Per a llegir i reflexionar'),
    'guia': ('Guías y plantillas', 'Guies i plantilles'),
    'centro': ('Documentos de centro', 'Documents de centre'),
    'ejfp': ('Ejemplos de programaciones de FP', 'Exemples de programacions de FP'),
    'ejeso': ('Ejemplos de programaciones de ESO', "Exemples de programacions d'ESO"),
    'videos': ('Vídeos', 'Vídeos'),
    'met': ('Metodologías', 'Metodologies'),
    'sa': ("Situaciones de aprendizaje", "Situacions d'aprenentatge"),
    'retos': ('Aprendizaje basado en retos', 'Aprenentatge basat en reptes'),
    'gamif': ('Gamificación y herramientas de aula', "Gamificació i eines d'aula"),
    'equipos': ('Dinámicas y creación de equipos', "Dinàmiques i creació d'equips"),
    'norma': ('Normativa', 'Normativa'),
    'plan': ('Planificar la evaluación', "Planificar l'avaluació"),
    'instr': ('Técnicas e instrumentos', 'Tècniques i instruments'),
    'rubr': ('Rúbricas', 'Rúbriques'),
    'neae': ('Alumnado con necesidades específicas de apoyo educativo', "Alumnat amb necessitats específiques de suport educatiu"),
    'gva': ('Modelos y recursos de la Conselleria', 'Models i recursos de la Conselleria'),
    'ej': ('Ejemplos de unidades', "Exemples d'unitats"),
    'conv': ('Convocatorias', 'Convocatòries'),
    'crit': ('Criterios de evaluación de los tribunales', 'Criteris d\'avaluació dels tribunals'),
    'temario': ('Temario de la especialidad', "Temari de l'especialitat"),
    'acceso': ('Acceso a la función docente', 'Accés a la funció docent'),
    'pd': ('Defensa de la programación', 'Defensa de la programació'),
    'ut': ('Exposición de la unidad', 'Exposició de la unitat'),
    'encerrona': ('La «encerrona»', "L'«encerrona»"),
}
NOMBRES = {  # títulos más claros que los de Moodle (es, val)
    72430: ('Resumen de la programación didáctica (presentación)', 'Resum de la programació didàctica (presentació)'),
    72431: ('Orientaciones, verbos y ejemplos de UT', "Orientacions, verbs i exemples d'UT"),
}
CABECERA = ('Material de la asignatura', "Material de l'assignatura")
NOTA_GRANDE = ('(archivo muy grande: consúltalo en la web oficial)', "(fitxer molt gran: consulta'l en la web oficial)")


def t(e, tag):
    x = e.find(tag)
    return (x.text or '') if x is not None and x.text not in (None, '$@NULL@$') else ''


def limpia(h, lang='es'):
    # Moodle multilang: <span lang="es" class="multilang">..</span><span lang="ca_valencia" ...>
    spans = re.findall(r'<span lang="([^"]+)" class="multilang">(.*?)</span>', h, re.S)
    if spans:
        want = 'es' if lang == 'es' else 'ca'
        for l, txt in spans:
            if l.startswith(want):
                h = txt
                break
        else:
            h = spans[0][1]
    h = re.sub(r'<[^>]+>', ' ', h)
    h = html.unescape(h).replace('`', "'")
    return re.sub(r'\s+', ' ', h).strip()


def slug(nombre):
    base, ext = os.path.splitext(nombre)
    base = unicodedata.normalize('NFKD', base).encode('ascii', 'ignore').decode()
    base = re.sub(r'[^A-Za-z0-9]+', '-', base).strip('-').lower()[:70]
    return f'{base}{ext.lower()}'


def bonito(nombre):
    base = os.path.splitext(nombre)[0].replace('_', ' ')
    return re.sub(r'\s+', ' ', base).strip()


def carga(mbz):
    files = {}
    for f in ET.parse(mbz / 'files.xml').getroot():
        if t(f, 'filename') == '.':
            continue
        files.setdefault(f.get('id'), {k: t(f, k) for k in ('contenthash', 'filearea', 'filename', 'filesize', 'component')})
    items = {}
    for a in ET.parse(mbz / 'moodle_backup.xml').getroot().iter('activity'):
        d = t(a, 'directory')
        if not d:
            continue
        mod = t(a, 'modulename')
        ax = ET.parse(mbz / d / f'{mod}.xml').getroot()[0]
        refs = []
        inf = mbz / d / 'inforef.xml'
        if inf.exists():
            refs = [files[i.find('id').text] for i in ET.parse(inf).getroot().iter('file') if i.find('id').text in files]
        refs = [r for r in refs if r['filearea'] == 'content']
        items[int(t(a, 'moduleid'))] = dict(mod=mod, name=t(ax, 'name'), intro=t(ax, 'intro'),
                                            url=t(ax, 'externalurl'), files=refs)
    return items


def main():
    mbz = pathlib.Path(sys.argv[1])
    items = carga(mbz)
    copiados = 0
    bloques = {}
    for tema, grupos in TEMAS.items():
        dest = RAIZ / 'static' / 'recursos' / tema
        dest.mkdir(parents=True, exist_ok=True)
        out = {'es': [], 'val': []}
        for g, ids in grupos:
            filas = {'es': [], 'val': []}
            for cid in ids:
                it = items[cid]
                for lang in ('es', 'val'):
                    nom = NOMBRES[cid][lang == 'val'] if cid in NOMBRES else limpia(it['name'], lang)
                    intro = limpia(it['intro'], lang)
                    desc = intro if intro and intro.lower() != nom.lower() and len(intro) < 320 and not intro.startswith('http') else ''
                    if it['mod'] == 'url':
                        linea = f'- [{nom}]({it["url"]})'
                        filas[lang].append(linea + (f' — {desc}' if desc else ''))
                        continue
                    fs = [f for f in it['files'] if not any(x in f['filename'] for x in EXCLUIR_NOMBRES)]
                    if not fs:
                        continue
                    if it['mod'] == 'folder' or len(fs) > 1:
                        filas[lang].append(f'- **{nom}**' + (f' — {desc}' if desc else ''))
                        pref = '  - '
                    else:
                        pref = '- '
                    for f in sorted(fs, key=lambda f: f['filename'].lower()):
                        etiqueta = nom if pref == '- ' else bonito(f['filename'])
                        if int(f['filesize']) > MAX_MB * 1024 * 1024:
                            filas[lang].append(f'{pref}{etiqueta} {NOTA_GRANDE[lang == "val"]}')
                            continue
                        nombre = slug(f['filename'])
                        src = mbz / 'files' / f['contenthash'][:2] / f['contenthash']
                        if not (dest / nombre).exists():
                            shutil.copyfile(src, dest / nombre)
                            copiados += 1
                        filas[lang].append(f'{pref}{{{{< doc `{tema}/{nombre}` `{etiqueta}` >}}}}'
                                           + (f' — {desc}' if desc and pref == '- ' else ''))
            for lang in ('es', 'val'):
                if filas[lang]:
                    out[lang].append(f'### {GRUPOS[g][lang == "val"]}\n\n' + '\n'.join(filas[lang]))
        bloques[tema] = out

    for lang in ('es', 'val'):
        for tema, out in bloques.items():
            pag = RAIZ / f'content.{lang}' / tema / '_index.md'
            if not pag.exists():
                print('Falta', pag)
                continue
            s = pag.read_text(encoding='utf-8')
            cuerpo = f'## {CABECERA[lang == "val"]}\n\n' + '\n\n'.join(out[lang]) if tema != 'guia' else '\n\n'.join(out[lang])
            nuevo = re.sub(r'<!-- MATERIAL:inicio -->.*?<!-- MATERIAL:fin -->',
                           lambda m: f'<!-- MATERIAL:inicio -->\n{cuerpo}\n<!-- MATERIAL:fin -->', s, flags=re.S)
            if nuevo == s and '<!-- MATERIAL:inicio -->' not in s:
                print('Sin marcador', pag)
            pag.write_text(nuevo, encoding='utf-8')
    print('Archivos copiados:', copiados)


if __name__ == '__main__':
    main()
