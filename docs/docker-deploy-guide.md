# Arknights Mower Docker 部署

## 运行环境准备

Docker >= 24.0、Linux。安卓设备开启USB调试。

## 克隆仓库

```bash
git clone https://github.com/ArkMowers/arknights-mower.git
cd arknights-mower
```

国内 `git clone` 慢的话，下载 zip 解压：
`https://codeload.github.com/ArkMowers/arknights-mower/zip/refs/heads/main`

## 准备 MAA

从 [MAA 发布页](https://github.com/MaaAssistantArknights/MaaAssistantArknights/releases/latest) 下载 Linux tar.gz 包，解压到 `docker/maa/`：

```bash
cd arknights-mower/docker
mkdir -p maa
curl -fL -o /tmp/maa.tar.gz "https://github.com/.../MAA-linux-x86_64.tar.gz"
tar -xzf /tmp/maa.tar.gz -C maa
```

## docker-compose.yml

在 `docker/` 目录下创建：

```yaml
name: arknights-mower

services:
  mower:
    build:
      context: ..
      dockerfile: docker/Dockerfile
      # args:
      #   HTTP_PROXY: http://proxy:port
      #   HTTPS_PROXY: http://proxy:port
      #   http_proxy: http://proxy:port
      #   https_proxy: http://proxy:port
    image: arknights-mower:latest
    container_name: arknights-mower
    restart: unless-stopped
    network_mode: host
    privileged: true
    environment:
      MOWER_TOKEN: mower
      MOWER_PORT: "58000"
      TZ: Asia/Shanghai
      # HTTP_PROXY: http://proxy:port
      # HTTPS_PROXY: http://proxy:port
      # NO_PROXY: 127.0.0.1,localhost,::1
      # no_proxy: 127.0.0.1,localhost,::1
    volumes:
      - /dev/bus/usb:/dev/bus/usb
      - ~/.android:/root/.android
      - ./mower-data:/mower-data
      - ./maa:/MAA
```

需要代理时取消注释。不用USB连手机时删掉 `privileged` 和 `/dev/bus/usb` 卷。

## 镜像构建并启动

```bash
cd arknights-mower/docker
docker compose build mower
docker compose up -d mower
```

启动后浏览器访问 `http://127.0.0.1:58000?token=mower` 或 `http://局域网IP:58000?token=mower`。仅需在 WebUI 中配置 ADB 连接地址。

## 升级

```bash
cd arknights-mower/docker
docker compose down
cd .. && git pull origin main && cd docker
docker compose build --pull=false mower
docker compose up -d mower
```

`mower-data`（含 `conf.yml`、`plan.json`）通过 volume 挂载，升级不会丢失。

```bash
# 不放心先备份
cp -a mower-data mower-data.bak-$(date +%Y%m%d)
```

## 排错

**不认 USB 设备**：`lsusb` 看到手机 → `adb devices` 显示 `device`（不能是 `unauthorized`）→ 手机弹出"允许USB调试"并确认 → `.android/adbkey` 存在。

**容器反复重启**：`docker logs arknights-mower --tail 50`，一般是 MAA 没放或代理不通。

**配置了代理但容器 unhealthy**：健康检查 curl 走代理访问 127.0.0.1 可能失败，加上 `NO_PROXY: 127.0.0.1,localhost,::1`。
