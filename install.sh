sudo apt update && sudo apt install bazel
sudo apt update && sudo apt full-upgrade

sudo systemctl stop record_noise
sudo cp record_noise.service /etc/systemd/system/
sudo systemctl restart record_noise