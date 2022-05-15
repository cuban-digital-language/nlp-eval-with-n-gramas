import progressbar


def get_progressbar(N, name=""):
    return progressbar.ProgressBar(
        maxval=N,
        widgets=[progressbar.Bar('#', '[', ']'),
                 name,
                 progressbar.Percentage()])
