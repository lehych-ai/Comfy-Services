#!/bin/bash
set -uo pipefail

source /venv/main/bin/activate

WORKSPACE=${WORKSPACE:-/workspace}
COMFYUI_DIR="${WORKSPACE}/ComfyUI"
HF_TOKEN="${HF_TOKEN:-}"

echo "=== ComfyUI запуск ==="

APT_PACKAGES=(
    git-lfs
    wget
)

PIP_PACKAGES=()

NODES=(
   "https://github.com/ltdrdata/ComfyUI-Manager"
    "https://github.com/ltdrdata/ComfyUI-Impact-Pack"
    "https://github.com/pythongosssss/ComfyUI-Custom-Scripts"
    "https://github.com/chflame163/ComfyUI_LayerStyle"
    "https://github.com/PGCRT/CRT-Nodes CRT-Nodes-PGCRT"
    "https://github.com/MONKEYFOREVER2/comfyui-quantum-spectral-nodes"
    "https://github.com/rgthree/rgthree-comfy"
    "https://github.com/yolain/ComfyUI-Easy-Use"
    "https://github.com/facok/comfyui-meancache-z"
    "https://github.com/teskor-hub/comfyui-teskors-utils"
    "https://github.com/ClownsharkBatwing/RES4LYF"
    "https://github.com/chrisgoringe/cg-use-everywhere"
    "https://github.com/ltdrdata/ComfyUI-Impact-Subpack"
    "https://github.com/Smirnov75/ComfyUI-mxToolkit"
    "https://github.com/ZhiHui6/zhihui_nodes_comfyui"
    "https://github.com/kijai/ComfyUI-KJNodes"
    "https://github.com/crystian/ComfyUI-Crystools"
    "https://github.com/plugcrypt/CRT-Nodes CRT-Nodes-plugcrypt"
    "https://github.com/EllangoK/ComfyUI-post-processing-nodes"
    "https://github.com/Fannovel16/comfyui_controlnet_aux"
    "https://github.com/GACLove/ComfyUI-VFI"
    "https://github.com/yoyodontsnitch777/node"
    "https://github.com/cubiq/ComfyUI_essentials"
    "https://github.com/ClownsharkBatwing/RES4LYF"
    "https://github.com/jnxmx/ComfyUI_HuggingFace_Downloader"
    "https://github.com/chrisgoringe/cg-use-everywhere"
    "https://github.com/ltdrdata/ComfyUI-Impact-Subpack"
    "https://github.com/Smirnov75/ComfyUI-mxToolkit"
    "https://github.com/TheLustriVA/ComfyUI-Image-Size-Tools"
    "https://github.com/jnxmx/ComfyUI_HuggingFace_Downloader"
    "https://github.com/kijai/ComfyUI-WanVideoWrapper"
)

DIFFUSION_MODELS=(
    "https://huggingface.co/lehychh/Z-image-Turbo/resolve/main/z-image-turbo.safetensors"
)

VAE_MODELS=(
    "https://huggingface.co/lehychh/Z-image-Turbo/resolve/main/vae.safetensors"
)

SAM_MODELS=(
    "https://huggingface.co/lehychh/Z-image-Turbo/resolve/main/sam_vit_b_01ec64.pth"
)

TEXT_ENCODER_MODELS=(
    "https://huggingface.co/lehychh/Z-image-Turbo/resolve/main/qwen.safetensors"
)

UPSCALE_MODELS=(
    "https://huggingface.co/lehychh/Z-image-Turbo/resolve/main/2x_PureVision.pth"
)

ULTRALYTICS_BBOX_MODELS=(
    "https://huggingface.co/lehychh/Z-image-Turbo/resolve/main/face_yolov9c.pt"
    "https://huggingface.co/lehychh/Z-image-Turbo/resolve/main/Eyes.pt"
    "https://huggingface.co/lehychh/Z-image-Turbo/resolve/main/nipple.pt"
    "https://huggingface.co/lehychh/Z-image-Turbo/resolve/main/vagina-v4.2.pt"
    "https://huggingface.co/lehychh/Z-image-Turbo/resolve/main/hand_yolov8s.pt"
    "https://huggingface.co/lehychh/Z-image-Turbo/resolve/main/assdetailer-seg.pt"
)

ULTRALYTICS_SEGM_MODELS=(
    "https://huggingface.co/lehychh/Z-image-Turbo/resolve/main/person_yolov8m-seg.pt"
)

MODEL_PATCHES=(
    "https://huggingface.co/lehychh/Z-image-Turbo/resolve/main/Z-Image-Turbo-Fun-Controlnet-Union-2.1-2602-8steps.safetensors"
)

LORA_MODELS=(
    "https://huggingface.co/lehychh/Z-image-Turbo/resolve/main/pussy_lily_v5_XL.safetensors"
)

CHECKPOINT_MODELS=(
    "https://huggingface.co/lehychh/Z-image-Turbo/resolve/main/lustifySDXLNSFW_V7.safetensors"
)

WORKFLOW_FILES=(
    "https://huggingface.co/lehychh/closer-ai-workflows/resolve/main/photo_heaven_v2.json"
    "https://huggingface.co/lehychh/closer-ai-workflows/resolve/main/ZIT%20by%20CloserAI%20t2i%20SFW.json"
    "https://huggingface.co/lehychh/closer-ai-workflows/resolve/main/ZIT%20by%20CloserAI%20t2i%20NSFW.json"
)

function provisioning_start() {
    provisioning_get_apt_packages
    provisioning_clone_comfyui
    provisioning_install_base_reqs
    provisioning_get_nodes
    provisioning_get_models
    provisioning_get_workflows
    provisioning_get_pip_packages
}

function provisioning_get_apt_packages() {
    if [[ ${#APT_PACKAGES[@]} -gt 0 ]]; then
        local SUDO=()
        if [[ "$(id -u)" -ne 0 ]]; then
            SUDO=(sudo)
        fi

        "${SUDO[@]}" apt-get update
        "${SUDO[@]}" apt-get install -y "${APT_PACKAGES[@]}"

        git lfs install || true
    fi
}

function provisioning_clone_comfyui() {
    if [[ ! -d "${COMFYUI_DIR}/.git" ]]; then
        rm -rf "${COMFYUI_DIR}"
        git clone https://github.com/comfyanonymous/ComfyUI.git "${COMFYUI_DIR}"
    fi

    cd "${COMFYUI_DIR}"
    git fetch origin
    git reset --hard origin/master
}

function provisioning_install_base_reqs() {
    cd "${COMFYUI_DIR}"

    if [[ -f requirements.txt ]]; then
        pip install --no-cache-dir -r requirements.txt
    fi
}

function provisioning_get_nodes() {
    echo "=== Устанавливаем custom nodes ==="

    mkdir -p "${COMFYUI_DIR}/custom_nodes"
    cd "${COMFYUI_DIR}/custom_nodes"

    for entry in "${NODES[@]}"; do
        repo="${entry%% *}"
        custom_dir="${entry#* }"

        if [[ "${custom_dir}" == "${repo}" ]]; then
            custom_dir="${repo##*/}"
        fi

        path="./${custom_dir}"

        echo "=== Node: ${custom_dir} ==="

        if [[ -d "${path}/.git" ]]; then
            (cd "${path}" && git pull --ff-only) || echo "WARN: не удалось обновить ${custom_dir}, пропускаю"
        else
            git clone --recursive "${repo}" "${path}" || echo "WARN: не удалось клонировать ${repo}, продолжаю"
        fi

        if [[ -f "${path}/requirements.txt" ]]; then
            pip install --no-cache-dir -r "${path}/requirements.txt" || echo "WARN: requirements failed for ${custom_dir}, продолжаю"
        fi
    done
}

function provisioning_get_pip_packages() {
    if [[ ${#PIP_PACKAGES[@]} -gt 0 ]]; then
        pip install --no-cache-dir "${PIP_PACKAGES[@]}"
    fi
}

function download_files() {
    local dir="$1"
    shift

    mkdir -p "$dir"

    for url in "$@"; do
        echo "=== Downloading to ${dir}: ${url} ==="

        if [[ -n "${HF_TOKEN:-}" && "$url" == *"huggingface.co"* ]]; then
            wget \
                --header="Authorization: Bearer ${HF_TOKEN}" \
                --tries=5 \
                --timeout=60 \
                -c \
                --content-disposition \
                -P "$dir" \
                "$url" || echo "WARN: не удалось скачать ${url}, продолжаю"
        else
            wget \
                --tries=5 \
                --timeout=60 \
                -c \
                --content-disposition \
                -P "$dir" \
                "$url" || echo "WARN: не удалось скачать ${url}, продолжаю"
        fi
    done
}

function provisioning_get_models() {
    echo "=== Загружаем модели ==="

    mkdir -p \
        "${COMFYUI_DIR}/models/diffusion_models" \
        "${COMFYUI_DIR}/models/vae" \
        "${COMFYUI_DIR}/models/sams" \
        "${COMFYUI_DIR}/models/text_encoders" \
        "${COMFYUI_DIR}/models/upscale_models" \
        "${COMFYUI_DIR}/models/ultralytics/bbox" \
        "${COMFYUI_DIR}/models/ultralytics/segm" \
        "${COMFYUI_DIR}/models/model_patches" \
        "${COMFYUI_DIR}/models/loras" \
        "${COMFYUI_DIR}/models/checkpoints"

    download_files "${COMFYUI_DIR}/models/diffusion_models" "${DIFFUSION_MODELS[@]}"
    download_files "${COMFYUI_DIR}/models/vae"              "${VAE_MODELS[@]}"
    download_files "${COMFYUI_DIR}/models/sams"             "${SAM_MODELS[@]}"
    download_files "${COMFYUI_DIR}/models/text_encoders"    "${TEXT_ENCODER_MODELS[@]}"
    download_files "${COMFYUI_DIR}/models/upscale_models"   "${UPSCALE_MODELS[@]}"
    download_files "${COMFYUI_DIR}/models/ultralytics/bbox" "${ULTRALYTICS_BBOX_MODELS[@]}"
    download_files "${COMFYUI_DIR}/models/ultralytics/segm" "${ULTRALYTICS_SEGM_MODELS[@]}"
    download_files "${COMFYUI_DIR}/models/model_patches"    "${MODEL_PATCHES[@]}"
    download_files "${COMFYUI_DIR}/models/loras"            "${LORA_MODELS[@]}"
    download_files "${COMFYUI_DIR}/models/checkpoints"      "${CHECKPOINT_MODELS[@]}"

    echo "=== Загрузка моделей завершена ==="
}

function provisioning_get_workflows() {
    echo "=== Загружаем workflow / рабочие процессы ==="

    local workflows_dir="${COMFYUI_DIR}/user/default/workflows"
    mkdir -p "${workflows_dir}"

    download_files "${workflows_dir}" "${WORKFLOW_FILES[@]}"

    echo "=== Workflow загружены в ${workflows_dir} ==="
}

if [[ ! -f /.noprovisioning ]]; then
    provisioning_start
fi

if [[ ! -f "${COMFYUI_DIR}/main.py" ]]; then
    echo "ERROR: ComfyUI не установлен: ${COMFYUI_DIR}/main.py не найден"
    exit 1
fi

echo "=== Запускаем ComfyUI (порт 8188) ==="
cd "${COMFYUI_DIR}"
nohup /venv/main/bin/python main.py --listen 0.0.0.0 --port 8188 --enable-cors-header > /var/log/comfyui.log 2>&1 &
disown

# === ФИКС: надёжное удаление /.provisioning ===
echo "=== Снимаем блокировку provisioning для ComfyUI ==="
PROVISIONING_REMOVED=false
for attempt in 1 2 3; do
    if [[ ! -f /.provisioning ]]; then
        echo "/.provisioning уже не существует"
        PROVISIONING_REMOVED=true
        break
    fi
    if rm -f /.provisioning 2>/dev/null; then
        echo "/.provisioning удалён (без sudo)"
        PROVISIONING_REMOVED=true
        break
    fi
    if sudo rm -f /.provisioning 2>/dev/null; then
        echo "/.provisioning удалён (sudo)"
        PROVISIONING_REMOVED=true
        break
    fi
    echo "WARN: попытка ${attempt} не удалась, жду 2 секунды..."
    sleep 2
done

if [[ "${PROVISIONING_REMOVED}" == "false" ]]; then
    echo "ERROR: не удалось удалить /.provisioning после 3 попыток!"
    echo "Попробуй вручную: sudo rm -f /.provisioning"
fi

echo "=== Provisioning завершён, ComfyUI запущен ==="
