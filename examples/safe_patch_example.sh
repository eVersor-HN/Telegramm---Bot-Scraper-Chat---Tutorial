cd ~/telegram-bot
sudo systemctl stop telegram-bot
cp bot.py bot.py.bak-$(date +%Y%m%d-%H%M%S)
cat > bot.py <<'BOTPY'
# paste the complete new bot.py here
BOTPY
./venv/bin/python -m py_compile bot.py
sudo systemctl start telegram-bot
systemctl status telegram-bot --no-pager -l
