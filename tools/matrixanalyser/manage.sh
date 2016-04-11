#!/bin/bash

case "$1" in
    setup)
        mkdir data 2>/dev/null
        mkdir figures 2>/dev/null
        touch data/coordinates.data
        ;;
    clean)
        rm -r data/
        rm -r figures/
        ;;
    usage|*)
        echo 'Usage: [setup|clean]'
        exit 1
        ;;
esac

