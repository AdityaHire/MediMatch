#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Compile .po files to .mo files using polib
"""
import polib
import os

def compile_po_to_mo(po_file, mo_file):
    """Compile .po file to .mo file using polib"""
    try:
        po = polib.pofile(po_file, encoding='utf-8')
        po.save_as_mofile(mo_file)
        print(f'✓ Compiled {po_file} -> {mo_file}')
        print(f'  Total entries: {len(po)}')
        print(f'  Translated: {len(po.translated_entries())}')
        print(f'  Untranslated: {len(po.untranslated_entries())}')
        return True
    except Exception as e:
        print(f'✗ Error compiling {po_file}: {e}')
        return False

if __name__ == '__main__':
    po_file = 'locale/hi/LC_MESSAGES/django.po'
    mo_file = 'locale/hi/LC_MESSAGES/django.mo'
    
    if os.path.exists(po_file):
        if compile_po_to_mo(po_file, mo_file):
            print('\n✓ Translation compilation successful!')
        else:
            print('\n✗ Translation compilation failed!')
    else:
        print(f'✗ Error: {po_file} not found')
