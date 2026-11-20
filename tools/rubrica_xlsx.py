#!/usr/bin/env python3
"""Genera la hoja de cálculo de la rúbrica de la segunda prueba a partir de data/rubrica.yaml.
Uso: python3 tools/rubrica_xlsx.py  (requiere pyyaml y openpyxl)"""
import pathlib, yaml
from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill, Border, Side
from openpyxl.worksheet.datavalidation import DataValidation

RAIZ = pathlib.Path(__file__).resolve().parent.parent
R = yaml.safe_load(open(RAIZ / 'data/rubrica.yaml', encoding='utf-8'))
SALIDA = RAIZ / 'static/recursos/t09-defensa/rubrica-segunda-prueba-254.xlsx'
TXT = {
    'es': dict(hoja='Castellano', tit='Rúbrica de la segunda prueba · Especialidad 254 Informática',
               sub='Basada en los criterios de la comisión de selección (Orden 1/2025). Escribe el nivel (1-4) en la columna «Nivel».',
               alumno='Persona evaluada:', ev='Evaluador/a:', ind='Indicador', niv='Nivel (1-4)', pts='Puntos',
               blo='Media del bloque', peso='Peso', nota='NOTA DE LA SEGUNDA PRUEBA (sobre 10)'),
    'val': dict(hoja='Valencià', tit='Rúbrica de la segona prova · Especialitat 254 Informàtica',
                sub="Basada en els criteris de la comissió de selecció (Ordre 1/2025). Escriu el nivell (1-4) en la columna «Nivell».",
                alumno='Persona avaluada:', ev='Avaluador/a:', ind='Indicador', niv='Nivell (1-4)', pts='Punts',
                blo='Mitjana del bloc', peso='Pes', nota='NOTA DE LA SEGONA PROVA (sobre 10)'),
}
fino = Side(style='thin', color='BBBBBB')
caja = Border(left=fino, right=fino, top=fino, bottom=fino)
wb = Workbook(); wb.remove(wb.active)
for lang, t in TXT.items():
    ws = wb.create_sheet(t['hoja'])
    ws.column_dimensions['A'].width = 6
    ws.column_dimensions['B'].width = 60
    for c, w in zip('CDEFGHI', (22, 22, 22, 22, 9, 8, 10)):
        ws.column_dimensions[c].width = w
    ws['A1'] = t['tit']; ws['A1'].font = Font(bold=True, size=14)
    ws['A2'] = t['sub']; ws['A2'].font = Font(italic=True, color='555555')
    ws['A3'] = t['alumno']; ws['A3'].font = Font(bold=True)
    ws['E3'] = t['ev']; ws['E3'].font = Font(bold=True)
    dv = DataValidation(type='whole', operator='between', formula1='1', formula2='4', allow_blank=True)
    ws.add_data_validation(dv)
    fila = 5
    medias = []
    niveles = R['niveles'][lang]
    for b in R['bloques']:
        ws.cell(fila, 1, f"{b['id']}. {b[lang]} · {t['peso']} {b['peso']} %").font = Font(bold=True, color='FFFFFF')
        for c in range(1, 10):
            ws.cell(fila, c).fill = PatternFill('solid', fgColor='5B3FBF')
        fila += 1
        cab = ['', t['ind']] + [f'{i+1} · {n}' for i, n in enumerate(niveles)] + [t['niv'], t['pts']]
        for c, v in enumerate(cab, 1):
            x = ws.cell(fila, c, v); x.font = Font(bold=True); x.fill = PatternFill('solid', fgColor='E8E4F7'); x.border = caja
        fila += 1
        ini = fila
        for k, it in enumerate(b['items']):
            ws.cell(fila, 1, f"{b['id']}{k+1}")
            ws.cell(fila, 2, it[lang])
            for i, d in enumerate(it['n']):
                ws.cell(fila, 3 + i, d[0 if lang == 'es' else 1])
            ws.cell(fila, 7).fill = PatternFill('solid', fgColor='FFF7D6')
            dv.add(ws.cell(fila, 7))
            ws.cell(fila, 8, f'=IF(G{fila}="","",G{fila}*2.5)')
            for c in range(1, 9):
                ws.cell(fila, c).alignment = Alignment(wrap_text=True, vertical='top'); ws.cell(fila, c).border = caja
            fila += 1
        ws.cell(fila, 6, t['blo']).font = Font(bold=True)
        ws.cell(fila, 8, f'=IFERROR(AVERAGE(H{ini}:H{fila-1}),0)').font = Font(bold=True)
        ws.cell(fila, 9, b['peso'] / 100)
        ws.cell(fila, 9).number_format = '0%'
        medias.append(f'H{fila}*I{fila}')
        fila += 2
    ws.cell(fila, 2, t['nota']).font = Font(bold=True, size=13)
    x = ws.cell(fila, 8, '=ROUND(' + '+'.join(medias) + ',2)'); x.font = Font(bold=True, size=13)
    x.fill = PatternFill('solid', fgColor='FFE08A')
    ws.freeze_panes = 'A5'
    ws.page_setup.orientation = 'landscape'; ws.page_setup.fitToWidth = 1
SALIDA.parent.mkdir(parents=True, exist_ok=True)
wb.save(SALIDA)
print('Generado', SALIDA)
