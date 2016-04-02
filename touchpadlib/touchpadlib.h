#ifndef TOUCHPADLIB_H
#define TOUCHPADLIB_H

#include <sys/time.h>
#include <linux/input.h>

struct touchpad_event {
    int32_t x;
    int32_t y;
    int32_t pressure;
    time_t seconds;
    suseconds_t useconds;
};

int has_root_privileges(void); // @TODO
int initalize_touchpadlib_usage();
int fetch_touchpad_event(int fd, struct touchpad_event *touchpad_event);
void print_event(const struct touchpad_event *event);

#endif /* TOUCHPADLIB_H */
