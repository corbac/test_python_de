from os import listdir


def rejections_alert(rejection_dir) -> None:
    items = listdir(rejection_dir)

    if len(items) > 0:
        #Rise Alert
        ...