#!/bin/sh
# Задача 8: архивировать все файлы с указанным расширением

# $1 — каталог, $2 — расширение
dir="$1"
ext="$2"
archive="archive_${ext}.tar"

# ищем файлы по расширению и архивируем
find "$dir" -maxdepth 1 -name "*.$ext" -print0 | tar --null -cvf "$archive" --files-from=-
echo "Создан архив $archive"
