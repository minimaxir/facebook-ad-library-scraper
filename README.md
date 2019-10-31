# facebook-ad-library-scraper

A Python scraper for the Facebook Ad Library, using the official [Facebook Ad Library API](https://www.facebook.com/ads/library/api/). This tool will **ONLY** work for users who have been approved for access to the API via Facebook. This scraper also performs cleaning to make the data easier to analyze and work around very strange data encoding decisions.

The intent of this tool is to help surface adversarial political advertisements on Facebook in light of Facebook's current stances on political ads. It should *only* be used for research and analysis, not for monetary gain. This tool follows the Terms of Use outlined on the API page and does not attempt to circumvent API limitations.

Analysis of the retrieved data is up to the user.

## Usage

In order to use the API, you need to gain access to the Facebook Ads Library API at https://www.facebook.com/ID and confirm your identity for `Running Ads About Social Issues, Elections or Politics`, which involves receiving a letter w/ a code at your US address and sending picture identification to Facebook.

If you have done so, install the Python package requirements via `pip`:

```sh
pip3 install requests tqdm
```

You configure the rest of the script via `config.yaml`. Go to https://developers.facebook.com/tools/explorer/ to get a User Access Token, and fill it in with your token (it expires after a few hours). Change other parameters as necessary.

You can run the scraper script via:

```sh
python3 fb_ad_lib_scraper.py
```

## Outputs

This script outputs three CSV files in an ideal format to be analyzed with Excel/Python/R:

* `fb_ads.csv`: The raw ads and their metadata.
* `fb_ads_demos.csv`: The unnested demographic distributions of people reached by ads, which can be mapped to `fb_ads.csv` via the `ad_id` field.
* `fb_ads_regions.csv`: The unnested region distributions of people reached by ads, which can be mapped to `fb_ads.csv` via the `ad_id` field.

You can view an example of 100 ads from querying `aoc` in the `/examples` folder.
  
## Helpful Notes

## Maintainer/Creator

Max Woolf ([@minimaxir](https://minimaxir.com))

*Max's open-source projects are supported by his [Patreon](https://www.patreon.com/minimaxir) and GitHub Sponsors. If you found this project helpful, any monetary contributions to the Patreon are appreciated and will be put to good creative use.*

## License

MIT
