import unittest
from typing import ClassVar

from mediafile import MediaFile

class ReplayGainCliTest:
    FNAME: str

    def _add_album(self, *args, **kwargs):
        # Use a file with non-zero volume (most test assets are total silence)
        album = self.add_album_fixture(*args, fname=self.FNAME, **kwargs)
        for item in album.items():
            reset_replaygain(item)

        return album

    def test_cli_saves_track_gain(self):
        self._add_album(2)

        for item in self.lib.items():
            assert item.rg_track_peak is None
            assert item.rg_track_gain is None
            mediafile = MediaFile(item.path)
            assert mediafile.rg_track_peak is None
            assert mediafile.rg_track_gain is None

        self.run_command("replaygain")

        # Skip the test if rg_track_peak and rg_track gain is None, assuming
        # that it could only happen if the decoder plugins are missing.
        if all(
            i.rg_track_peak is None and i.rg_track_gain is None
            for i in self.lib.items()
        ):
            self.skipTest("decoder plugins could not be loaded.")

        for item in self.lib.items():
            assert item.rg_track_peak is not None
            assert item.rg_track_gain is not None
            mediafile = MediaFile(item.path)
            self.assertAlmostEqual(
                mediafile.rg_track_peak, item.rg_track_peak, places=6
            )
            self.assertAlmostEqual(
                mediafile.rg_track_gain, item.rg_track_gain, places=2
            )
