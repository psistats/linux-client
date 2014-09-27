echo "---- LAYING AN EGG ----"

cd $PROJECT_DIR
python setup.py sdist
RETCODE=$?

if [[ $RETCODE != 0 ]]; then
    echo "[ERROR] python setup.py sdist failed."
    exit $RETCODE
fi

echo "---- EGG READY FOR HATCING ---"
