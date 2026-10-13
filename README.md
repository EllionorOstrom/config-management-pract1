# Эмулятор оболочки UNIX (вариант 17)

## Общее описание

Консольный эмулятор командной строки UNIX-подобной ОС на Python 3
(только стандартная библиотека). Практическая работа по дисциплине
«Конфигурационное управление».

Реализовано: этап 1 (REPL), этап 2 (конфигурация), этап 3 (VFS).

## Функции и настройки

- Приглашение: `имя_пользователя@имя_хоста:~$` (данные реальной ОС).
- Парсер с поддержкой кавычек: `ls "my dir"`.
- Команды: `ls`, `cd` (заглушки), `exit`, `vfs-info` (служебная).
  Ошибки: неизвестная команда, лишние аргументы, незакрытая кавычка.
- Параметры командной строки:
  - `--vfs PATH` — ZIP-архив, из которого загружается VFS;
  - `--script PATH` — стартовый скрипт.
- При запуске выводится отладочная информация о параметрах.
- Стартовый скрипт: одна команда в строке, `#` — комментарий. Ввод и
  вывод отображаются как диалог. Ошибки в строках скрипт не прерывают.
  Если нет `exit`, эмулятор переходит в интерактивный режим.
- VFS:
  - источник — ZIP-архив, все данные хранятся только в памяти, архив
    не распаковывается на диск и не изменяется;
  - текстовые файлы (UTF-8) хранятся как текст, двоичные — в base64;
  - ошибки загрузки (файл не найден, неверный формат ZIP) выводятся
    в stderr, код возврата 1;
  - `vfs-info` показывает дерево загруженной VFS.

## Сборка, запуск и тесты

Нужен Python 3.8+. Сборка не требуется.

```
python scripts\make_vfs.py
run.bat --vfs vfs\deep.zip
python -m unittest discover -v
scripts\test_stage2.bat
scripts\test_vfs.bat
```

ZIP-файлы в репозитории не хранятся: `scripts\make_vfs.py` создаёт
тестовые архивы (`minimal`, `several`, `deep`, `broken`) в папке `vfs`.

## Пример

```
> run.bat --vfs vfs\several.zip
[debug] start-up parameters:
[debug]   vfs    = vfs\several.zip
[debug]   script = (not set)
user@host:~$ vfs-info
VFS source: vfs\several.zip
directories: 0, files: 4
data.bin [binary, 8 bytes]
empty.txt [text, 0 bytes]
hello.txt [text, 14 bytes]
notes.txt [text, 29 bytes]
user@host:~$ exit

> run.bat --vfs vfs\missing.zip
vfs error: file not found: vfs\missing.zip
```
