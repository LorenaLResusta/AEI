# AEI · Aprendizaje y Enseñanza de la Informática

Web del **Bloque II · La programación didáctica** (Máster de Profesorado de Secundaria, Universidad de Alicante, curso 2026/27), en castellano y valenciano.

Publicada en GitHub Pages: <https://lorenalresusta.github.io/AEI/>.

## Estructura

| Carpeta | Contenido |
|---|---|
| `content.es/`, `content.val/` | Páginas en castellano y valenciano (mismas rutas en los dos idiomas) |
| `data/sesiones.yaml` | Planificación sesión a sesión. Alimenta el calendario de la portada y la tabla de la guía |
| `static/recursos/<tema>/` | Documentos de la asignatura (procedentes de la copia de Moodle) |
| `layouts/_shortcodes/` | `calendario`, `sesiones`, `doc`, `quiz`, `tarjetas`, `curiosidad` |
| `tools/material.py` | Regenera los listados «Material de la asignatura» a partir de una copia `.mbz` descomprimida |

## Cambiar el calendario

Edita `data/sesiones.yaml`: cada sesión tiene fecha, horas, tipo (`clase`, `taller`, `expo`, `festivo`), tema enlazado y texto en `es` y `val`.

## Volver a generar el material desde Moodle

```bash
mkdir mbz && tar -xzf AEI.mbz -C mbz
python3 tools/material.py mbz
```

El reparto de recursos por tema está en la tabla `TEMAS` de `tools/material.py`.

## Publicación

El flujo `.github/workflows/hugo.yaml` compila con Hugo 0.166 y publica en GitHub Pages en cada push a `main` (en *Settings → Pages*, la fuente debe ser **GitHub Actions**).

Para probar en local: `hugo server` y abrir <http://localhost:1313/AEI/>.
