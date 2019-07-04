
WD='{job_path}'
cd $WD

INCLUDE_PATHS=({include_paths})

{{
    set -e
    while [ -f .env.tmp ]
    do
        sleep 1
    done

    CONDA_DIR=$(which conda | xargs dirname | xargs dirname)

    if [ ! -d "$WD/.venv" ]; then
        cd $WD && touch .env.tmp
        . $CONDA_DIR/etc/profile.d/conda.sh
        conda create -p .venv -y python="{python}"
        conda activate "$WD/.venv"
        echo "Using python path $(which python)"
        pip install -r requirements.txt

        for i in "${{INCLUDE_PATHS[@]}}"; do
            if [ -f "$i/requirements.txt" ]; then
                pip install -r "$i/requirements.txt"
            fi
        done

        if [ -f "$WD/addons.sh" ]; then
            bash addons.sh
        fi

        rm -f .env.tmp
    else
        exit 0
    fi
}} || {{
    cd $WD && rm -rf .env.tmp && rm -rf .venv*
}}


