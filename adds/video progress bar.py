import sys
import ssl

from pytube import YouTube

ssl._create_default_https_context = ssl._create_unverified_context


def progress_func(stream, chunk, bytes_remaining):
    current = stream.filesize - bytes_remaining
    done = int(50 * current / stream.filesize)

    sys.stdout.write(
        "\r[{}{}] {} MB / {} MB".format('=' * done, ' ' * (50 - done), "{:.2f}".format(bytes_to_megabytes(current)),
                                        "{:.2f}".format(bytes_to_megabytes(stream.filesize))))
    sys.stdout.flush()


def bytes_to_megabytes(bytes_size):
    megabytes_size = bytes_size / (1024 ** 2)
    return megabytes_size


yt = YouTube("http://youtube.com/watch?v=2lAe1cqCOXo", on_progress_callback=progress_func)

yt.streams.get_highest_resolution().download()