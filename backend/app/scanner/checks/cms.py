from bs4 import BeautifulSoup


class CMSDetector:
    """
    Performs passive technology and CMS detection.
    """

    CMS_SIGNATURES = {
        "WordPress": [
            "wordpress",
            "wp-content",
            "wp-includes",
        ],
        "Drupal": [
            "drupal",
        ],
        "Joomla": [
            "joomla",
        ],
    }

    def analyze(self, context: dict) -> dict:
        """
        Analyze response headers and HTML content.

        Args:
            context:
                {
                    "url": "...",
                    "response": requests.Response
                }

        Returns:
            Detected technologies and CMS information.
        """

        response = context["response"]

        technologies = []
        cms = []

        headers = response.headers

        server = headers.get("Server")

        if server:
            technologies.append(
                {
                    "name": "Server",
                    "value": server,
                }
            )

        powered_by = headers.get("X-Powered-By")

        if powered_by:
            technologies.append(
                {
                    "name": "X-Powered-By",
                    "value": powered_by,
                }
            )

        html = response.text.lower()

        soup = BeautifulSoup(
            response.text,
            "html.parser",
        )

        generator = soup.find(
            "meta",
            attrs={
                "name": "generator"
            },
        )

        if generator and generator.get("content"):

            cms.append(
                {
                    "name": generator.get("content"),
                    "source": "meta generator",
                }
            )

        for cms_name, signatures in self.CMS_SIGNATURES.items():

            for signature in signatures:

                if signature in html:

                    cms.append(
                        {
                            "name": cms_name,
                            "source": "html signature",
                        }
                    )

                    break

        return {
            "technologies": technologies,
            "cms": cms,
        }