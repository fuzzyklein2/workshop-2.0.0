# pkg-config --cflags --libs gtkmm-4.0 gtest > data/pkg-config.out
pkg-config --cflags --libs $($WORKSHOP_SCRIPTS_DIRECTORY/get_packages.py) > $WORKSHOP_TEMP_DIRECTORY/pkg-config.out