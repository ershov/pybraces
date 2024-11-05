#!/bin/bash
twine check dist/* && twine upload `ls -1 dist/pybraces-* | LC_ALL=C sort -r`
