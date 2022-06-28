systemctl stop myportfolio
cd project-elegant-elephant
git fetch && git reset origin/main --hard
source python3-virtualenv/bin/activate
pip3 install -r requirements.txt
systemctl start myportfolio

