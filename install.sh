sudo apt update && sudo apt install bazel-bootstrap
sudo apt update && sudo apt full-upgrade

sudo cp record_noise.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl restart record_noise
