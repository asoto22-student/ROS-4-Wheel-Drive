#!/usr/bin/env bash

# Directory names
# Also linux doesn't care if you double slash for some reason

INSTALL_DIR=/home/user/etc
PROJECT_NAME=sotopellotAngel
INSTALL_BIN=/home/user/bin
BIN_NAME=sotopellotAngel
export PATH="$PATH:$INSTALL_BIN"

Install()
{
    # Makes a folder for install
    # -p makes every folder inbetween, so it creates all the subfolders for you
    mkdir -p $INSTALL_DIR/$PROJECT_NAME

    # put all the install files in /etc
    cp -r sotopellotAngel $INSTALL_DIR/

    export PATH="$PATH:$INSTALL_BIN"
    exit 0
}

Uninstall()
{
    rm -r $INSTALL_DIR/$PROJECT_NAME
    exit 0
}

Start()
{
    cat "1" > /tmp/$PROJECT_NAME
    cd $INSTALL_DIR/$PROJECT_NAME/

    ./loadRobot.sh
    sleep 5s

    echo "======== Robot Loaded ========"
    cd $INSTALL_DIR/$PROJECT_NAME/src

    python robot_control.py &
    echo "==== Robot Control Loaded ===="

    python keyboard_control.py
    echo "===== Keyboard Unloaded ======"

    exit 0
}

Stop()
{
    ./rmRobot.sh
    rosnode kill /fw_control
    exit 0
}

Status()
{
    echo $(cat /tmp/$PROJECT_NAME)
}

Help()
{
    echo ' '
    echo ' '
    echo '----------------------------------------------------------------'
    echo '---------------- 4 Wheel Drive Robot Control -------------------'
    echo '----------------------------------------------------------------'
    echo 'install                   : Install the progam'
    echo 'uninstall                 : Uninstall the progam'
    echo 'start                     : Starts the program'
    echo 'stop                      : Stops the program'
    echo 'status                    : Checks if there are locks are made'
    echo 'help                      : Shows this dialog'
    echo ' '
    echo ' '
    exit 0
}

case $1 in
'install')
    Install
    ;;
'uninstall')
    Uninstall
    ;;
'start')
    Start $@
    ;;
'stop')
    Stop
    ;;
'status')
    Stop
    ;;
'help')
    Help
    ;;
*)
    Help
    ;;
    esac
exit 0