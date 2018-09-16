# Attribution: https://stackoverflow.com/questions/1527049/join-elements-of-an-array
function join_by { local IFS="$1"; shift; echo "$*"; }

EXCLUDED_FILES=(
    "yget/__init__.py"
    "yget/__main__.py"
    "yget/downloader_factory.py"
    "yget/file_reader.py"
    "yget/input_provider.py"
    "yget/logger.py"
    "yget/path_validator.py"
)

OMIT=$(join_by , "${EXCLUDED_FILES[@]}")

coverage3 run \
    --source=yget \
    --omit=$OMIT \
    -m unittest discover;
coverage3 report -m;
coverage3 html;
