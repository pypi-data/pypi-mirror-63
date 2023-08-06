import requests

import pynando.data


def default_download_dir():
    return pynando.data.path


class Downloader(object):
    def __init__(self, download_dir=None):
        self._download_dir = download_dir
        if self._download_dir is None:
            self._download_dir = default_download_dir()

    def download(self):
        print('download nando data')
        url_list = [
            'https://raw.githubusercontent.com/aidrd/nando/master/data/nanbyo.json',
            'https://raw.githubusercontent.com/aidrd/nando/master/data/nanbyo_class.json',
            'https://raw.githubusercontent.com/aidrd/nando/master/data/shoman.json',
            'https://raw.githubusercontent.com/aidrd/nando/master/data/shoman_class.json',
        ]
        for url in url_list:
            fname = url.split('/')[-1]
            fp = self._download_dir / fname
            if fp.exists():
                continue

            print('downloading {}'.format(fname))
            res = requests.get(url)
            with fp.open(mode='wb') as f:
                f.write(res.content)
