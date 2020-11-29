Generates certificates for course.

Requires Figma svg-templates in `templates/` directory. 

Requires people lists in `lists/` directory: one name per line.

### Patch original exported files

Patch sed commands Written for Mac OS only.

```bash
./patch_templates.sh
```

### Run generator

```bash
./generate.py
```

Result is generated in `_generated`.

Look at `generate_certs` in `generate.py` for hardcoded templates and people list values.
