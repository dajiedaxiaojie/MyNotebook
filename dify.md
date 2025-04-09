podman machine list
podman machine stop --log-level debug
https://github.com/containers/podman/issues/25121#issuecomment-2653583685
podman machine reset
podman ps -a 
podman compose version
docker-compose version
vi ~/.zshrc
source ~/.zshrc 
docker ps -a
cd /Users/athenazhang/Documents/code/remote/dify-main/docker
docker compose ps


git clone https://github.com/langgenius/dify.git
cd dify/docker

cp .env.example .env
Modify .env file (optional)
Docker Compose Service Expose Host Port Configurations
EXPOSE_NGINX_PORT=80
EXPOSE_NGINX_SSL_PORT=443
Generally, you have to change expose port in your development environment.

問題：restarting 原因：docker版本過低
解決：修改 dify/docker/docker-compose.yaml
在對應項目下添加：privileged: true


docker compose up -d
http://localhost/install
http://ip:port/install

https://jhtnaee.atlassian.net/wiki/spaces/AWT/pages/4742971498/Get+Started
https://jhtnaee.atlassian.net/wiki/spaces/AWT/pages/4924211204/K8S+in+localhost
模型比較說明
token：在自然語言處理中，token 是指一個詞或一個子詞。
多模態：指能夠處理多種形式的數據，例如文本、圖片、音頻等。
選擇哪個模型，主要取決於您的需求和預算。
GPT-40 mini 適合預算有限，但需要快速回應的使用者。
Claude 3.5 Sonnet 擅長處理文字，並能生成視覺內容，但無法生成圖片。
Gemini 1.5 Pro 處理能力強大，適合處理大量複雜數據，但費用較高。
https://x.com/SuguruKun_ai/status/1814517513260310869
