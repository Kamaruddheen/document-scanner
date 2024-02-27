# build_files.sh
pip install -r requirements.txt

# List all the packages
pip list

# make migrations
python3.9 manage.py migrate 
python3.9 manage.py collectstatic
