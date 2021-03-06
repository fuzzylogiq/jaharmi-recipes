#!/usr/bin/env python

import urllib2

from autopkglib import Processor, ProcessorError


__all__ = ["XRGURLProvider"]

# URL to consult for current version of XRG
# http://download.gauchosoft.com/xrg/latest_version.txt

update_url = "http://download.gauchosoft.com/xrg/latest_version.txt"

# Sample URL to download a specific version of XRG
# http://download.gauchosoft.com/xrg/XRG-release-1.7.3.zip


class XRGURLProvider(Processor):
    description = "Provides URL to the latest XRG download."
    input_variables = {
    }
    output_variables = {
        "version": {
            "description": "Version of the XRG download.",
        },
        "filename": {
            "description": "Filename of the latest XRG release download.",
        },
        "url": {
            "description": "URL to the latest XRG release download.",
        },
    }

    __doc__ = description

    def get_xrg_version(self, update_url):
        """Find the latest version of XRG and output as a string."""
        try:
            f = urllib2.urlopen(update_url)
            html = f.read()
            # The version is currently the only string in the text file at the
            # update URL, so capture that string
            # If this should change in the future or more error checking is desired,
            # perform more processing here
            download_version_string = html.strip()
            f.close()
        except BaseException as e:
            raise ProcessorError("Can't download %s: %s" % (update_url, e))
        return download_version_string

    def get_xrg_archive_file(self, download_version):
        """Construct the name of the XRG archive file used in
        the download URL."""
        dmg_filename = "XRG-release-{0}.zip".format(download_version)
        return dmg_filename

    def get_xrg_dmg_url(self, download_filename):
        """Construct the URL for the XRG file download."""
        # Return URL
        dmg_url = "http://download.gauchosoft.com/xrg/{0}".format(download_filename)
        return dmg_url

    def main(self):
        """Find and return a download URL."""

        # Get the string representing the requested XRG version
        download_version = self.get_xrg_version(update_url)
        self.env["version"] = download_version
        self.output("Found version %s" % self.env["version"])

        # Get the filename of the XRG disk image download using the version
        download_filename = self.get_xrg_archive_file(download_version)
        self.env["filename"] = download_filename
        self.output("Found download filename %s" % self.env["filename"])

        # Get the URL of the XRG disk image download using the filename
        download_url = self.get_xrg_dmg_url(download_filename)

        self.env["url"] = download_url
        self.output("Found URL %s" % self.env["url"])


if __name__ == "__main__":
    processor = XRGURLProvider()
    processor.execute_shell()
