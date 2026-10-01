# Практическое занятие №2. Менеджеры пакетов

## Задача 1. Служебная информация о пакете matplotlib

### Команда

```bash
py -3.10 -m pip show matplotlib
```

### Вывод команды (ключевые строки)

```
Name: matplotlib
Version: 3.10.8
Summary: Python plotting package
Home-page:
Author: John D. Hunter, Michael Droettboom
Author-email: Unknown <matplotlib-users@python.org>
License: License agreement for matplotlib versions 1.3.0 and later
Location: c:\users\girlg\appdata\local\programs\python\python310\lib\site-packages
Requires: contourpy, cycler, fonttools, kiwisolver, numpy, packaging, pillow, pyparsing, python-dateutil
Required-by:
```

(Полный вывод включает длинный текст лицензии — опущен для краткости.)

### Разбор основных элементов

| Поле | Значение | Что означает |
|------|----------|--------------|
| Name | matplotlib | Имя пакета |
| Version | 3.10.8 | Версия по SemVer: MAJOR.MINOR.PATCH |
| Summary | Python plotting package | Краткое описание |
| Home-page | (пусто) | Официальный сайт не указан |
| Author | John D. Hunter, Michael Droettboom | Авторы пакета |
| Author-email | matplotlib-users@python.org | Email авторов |
| License | License agreement for matplotlib... | Лицензия |
| Location | c:\users\girlg\...\site-packages | Где лежат файлы пакета |
| Requires | contourpy, cycler, fonttools, kiwisolver, numpy, packaging, pillow, pyparsing, python-dateutil | Зависимости — другие пакеты |
| Required-by | (пусто) | Кто зависит от этого пакета |

### Что такое SemVer

SemVer (Semantic Versioning) — стандарт нумерации версий. Формат: `MAJOR.MINOR.PATCH`.

- MAJOR (3) — несовместимые изменения.
- MINOR (10) — новые функции, обратно совместимые.
- PATCH (8) — исправления ошибок.

Примеры интервалов:
- `^1.2.3` — совместимо с `>=1.2.3` и `<2.0.0`.
- `~1.2.3` — совместимо с `>=1.2.3` и `<1.3.0`.

### Зависимости matplotlib

Поле `Requires` — это список пакетов, от которых зависит `matplotlib`:
- `contourpy` — для контурных графиков.
- `cycler` — для циклических цветов.
- `fonttools` — для работы со шрифтами.
- `kiwisolver` — для решения уравнений раскладки.
- `numpy` — для математических операций.
- `packaging` — для работы с версиями.
- `pillow` — для работы с изображениями.
- `pyparsing` — для парсинга.
- `python-dateutil` — для работы с датами.

Когда устанавливаешь `matplotlib`, `pip` автоматически ставит все эти зависимости.

### Как получить пакет без менеджера пакетов

Менеджер пакетов (`pip`) автоматизирует скачивание и установку. Но можно сделать это вручную:

1. Открыть официальный репозиторий **PyPI**: [pypi.org/project/matplotlib](https://pypi.org/project/matplotlib/)
2. Перейти в раздел **Download files**.
3. Скачать файл `.whl` (wheel) или `.tar.gz` (source) для своей версии Python и ОС.
4. Распаковать архив:
   ```bash
   tar -xzf matplotlib-3.10.8.tar.gz
   cd matplotlib-3.10.8
   ```
5. Установить:
   ```bash
   python setup.py install
   ```
6. Или установить wheel-файл:
   ```bash
   pip install matplotlib-3.10.8-py3-none-any.whl
   ```

**Вывод**: `pip` просто автоматизирует эти шаги. Без него всё делается вручную.
